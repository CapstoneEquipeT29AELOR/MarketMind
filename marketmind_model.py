"""
MarketMind - stage 1 ML module (standalone; connect to the backend/database later).

Trains ONE pooled model on one or many stocks and predicts, for each stock, whether the
close will be higher HORIZON trading days from now, with a confidence and a reliability
label based on how the model did on data it had not seen.

Feature groups (the 20/50-day SMA crossover is dashboard-only, so it is NOT a feature):
  price     returns, volatility, RSI, volume spikes, distance from 20-day high/low
  market    S&P 500 / Nasdaq returns, VIX (fear index), 10-year yield, stock vs market strength
  calendar  day of week, month
  sentiment FinBERT news scores (only when --news is given)

Install:  pip install yfinance pandas numpy scikit-learn xgboost joblib
Run:      python marketmind_model.py                        NVDA, all feature groups, signal + report
          python marketmind_model.py --experiments          which data actually helps? (start here)
          python marketmind_model.py --news news_scored_all.csv NVDA + FinBERT sentiment features
          python marketmind_model.py --target excess        predict beating the S&P 500 instead of "up"
          python marketmind_model.py --all                  all stocks in ALL_TICKERS

example: python marketmind_model.py AAPL GOOGL MSFT AMD TSLA NVDA --news news_scored_all.csv
"""
import argparse
import json
import logging

import joblib
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

logging.basicConfig(filename="marketmind.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")  # "track all events and history"
log = logging.getLogger("marketmind")
pd.set_option("display.width", 200)          # stop pandas hiding columns in the printed tables
pd.set_option("display.max_columns", 20)

DEFAULT_TICKERS = ["NVDA"]   # testing default: one stock only
# Full list, used with --all. Samsung Electronics on the Korea Exchange is 005930.KS; SONY is the US-listed ADR
ALL_TICKERS = ["AAPL", "GOOGL", "MSFT", "AMD", "TSLA", "NVDA"]
MARKET_SYMBOLS = {"spy": "SPY", "qqq": "QQQ", "vix": "^VIX", "tnx": "^TNX"}
HORIZON = 5        # predict 5 trading days ahead
THRESHOLD = 0.55   # backtest only holds a stock when P(positive) is above this
MIN_ROWS = 300     # skip tickers with too little history

GROUPS = {
    "price": ["ret_1d", "ret_5d", "ret_10d", "ret_20d", "vol_10d", "vol_20d", "range_pct",
              "dist_20d_high", "dist_20d_low", "volume_z", "rsi_14"],
    "market": ["spy_ret_1d", "spy_ret_5d", "spy_ret_20d", "qqq_ret_5d", "vix", "vix_chg_5d",
               "tnx_chg_5d", "rel_spy_5d", "rel_spy_20d", "corr_spy_60d"],
    "calendar": ["dow", "month"],
    "sentiment": ["sent_mean", "sent_count", "sent_min", "sent_mean_5d", "sent_mean_10d", "news_z"],
}


def pick(panel, groups):
    return [c for g in groups for c in GROUPS[g] if c in panel.columns]


# ---------------------------------------------------------------- data ----
def load_prices(ticker: str, start: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError("no price data returned (check the ticker symbol / internet)")
    if isinstance(df.columns, pd.MultiIndex):      # newer yfinance versions
        df.columns = df.columns.get_level_values(0)
    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


def load_market(start: str):
    """S&P 500, Nasdaq-100, VIX and 10y yield closes. Missing pieces are skipped, not fatal."""
    cols = {}
    for name, symbol in MARKET_SYMBOLS.items():
        try:
            cols[name] = load_prices(symbol, start)["Close"]
        except Exception as e:
            log.warning("market series %s unavailable: %s", symbol, e)
            print(f"  market series {symbol} unavailable: {e}")
    return pd.DataFrame(cols) if cols else None


def load_sentiment(path: str, ticker: str, trading_days: pd.DatetimeIndex):
    """
    Reads the CSV made by finbert_sentiment.py and returns one row per trading day:
    sent_mean, sent_count, sent_min. Returns None if the ticker has no news.

    No look-ahead: news published on a trading day is only used from the NEXT
    trading day (we can't know if it came before or after the close);
    weekend news goes to the next trading day.
    """
    news = pd.read_csv(path, parse_dates=["date"])
    news = news[news["ticker"] == ticker]
    if news.empty:
        return None
    d = news["date"].dt.normalize().values
    pos = trading_days.searchsorted(d)
    is_trading_day = (pos < len(trading_days)) & (trading_days.values[np.minimum(pos, len(trading_days) - 1)] == d)
    pos = pos + is_trading_day.astype(int)
    keep = pos < len(trading_days)
    news = news[keep].assign(day=trading_days[pos[keep]])
    return news.groupby("day")["score"].agg(sent_mean="mean", sent_count="count", sent_min="min")


# ------------------------------------------------------------ features ----
def make_features(prices: pd.DataFrame, sentiment=None, market=None):
    df = pd.DataFrame(index=prices.index)
    close, vol = prices["Close"], prices["Volume"]
    ret = close.pct_change()

    for n in (1, 5, 10, 20):
        df[f"ret_{n}d"] = close.pct_change(n)
    df["vol_10d"] = ret.rolling(10).std()
    df["vol_20d"] = ret.rolling(20).std()
    df["range_pct"] = (prices["High"] - prices["Low"]) / close
    df["dist_20d_high"] = close / close.rolling(20).max() - 1
    df["dist_20d_low"] = close / close.rolling(20).min() - 1
    df["volume_z"] = (vol - vol.rolling(20).mean()) / vol.rolling(20).std()
    gain = ret.clip(lower=0).rolling(14).mean()   # simple RSI(14)
    loss = (-ret.clip(upper=0)).rolling(14).mean()
    df["rsi_14"] = 100 - 100 / (1 + gain / loss)   # loss == 0 -> RSI 100

    df["dow"] = df.index.dayofweek
    df["month"] = df.index.month

    spy_future = None
    if market is not None:
        m = market.reindex(df.index, method="ffill", limit=3)   # other countries' holidays differ
        if "spy" in m:
            spy = m["spy"]
            for n in (1, 5, 20):
                df[f"spy_ret_{n}d"] = spy.pct_change(n)
            df["rel_spy_5d"] = df["ret_5d"] - df["spy_ret_5d"]      # is the stock beating the market?
            df["rel_spy_20d"] = df["ret_20d"] - df["spy_ret_20d"]
            df["corr_spy_60d"] = ret.rolling(60).corr(spy.pct_change())
            spy_future = spy.shift(-HORIZON) / spy - 1
        if "qqq" in m:
            df["qqq_ret_5d"] = m["qqq"].pct_change(5)
        if "vix" in m:
            df["vix"] = m["vix"]
            df["vix_chg_5d"] = m["vix"].pct_change(5)
        if "tnx" in m:
            df["tnx_chg_5d"] = m["tnx"].diff(5)

    if sentiment is not None:
        s = sentiment.reindex(df.index)
        df["sent_mean"] = s["sent_mean"].fillna(0)
        df["sent_count"] = s["sent_count"].fillna(0)
        df["sent_min"] = s["sent_min"].fillna(0)
        df["sent_mean_5d"] = df["sent_mean"].rolling(5, min_periods=1).mean()
        df["sent_mean_10d"] = df["sent_mean"].rolling(10, min_periods=1).mean()
        c = df["sent_count"]   # sudden jump in news volume = something is happening
        df["news_z"] = ((c - c.rolling(20).mean()) / c.rolling(20).std()).replace([np.inf, -np.inf], np.nan).fillna(0)

    future = close.shift(-HORIZON) / close - 1
    df["future_ret"] = future
    df["target"] = (future > 0).astype(int)              # 1 = higher in HORIZON days
    needed = ["future_ret"]
    if spy_future is not None:
        df["future_excess"] = future - spy_future
        df["target_excess"] = (df["future_excess"] > 0).astype(int)   # 1 = beat the S&P 500
        needed.append("future_excess")

    label_cols = ["target", "target_excess", "future_ret", "future_excess"]
    feat_cols = [c for c in df.columns if c not in label_cols]
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=feat_cols)
    return df.dropna(subset=needed).copy(), df   # (labelled rows, all rows incl. latest day)


def build_panel(tickers, start, news_csv=None):
    """Stack every stock into one table (one row per stock per day)."""
    market = load_market(start)
    frames, latest, news_end = [], [], {}
    for t in tickers:
        try:
            prices = load_prices(t, start)
            if len(prices) < MIN_ROWS:
                raise ValueError(f"only {len(prices)} rows of history")
            sent = load_sentiment(news_csv, t, prices.index) if news_csv else None
            if news_csv and sent is None:
                raise ValueError("no news for this ticker in the news file")
            data, all_rows = make_features(prices, sent, market)
            if sent is not None:                      # only train where news actually exists
                data = data.loc[sent.index.min():sent.index.max()]
                news_end[t] = sent.index.max()
            frames.append(data.assign(ticker=t))
            latest.append(all_rows.iloc[[-1]].assign(ticker=t))
            log.info("loaded %s: %d labelled rows", t, len(data))
        except Exception as e:                        # one bad ticker must not stop the rest
            log.warning("skipped %s: %s", t, e)
            print(f"  skipped {t}: {e}")
    if not frames:
        raise SystemExit("No usable tickers - check your internet connection / ticker symbols.")
    panel = pd.concat(frames).rename_axis("date").reset_index()
    latest = pd.concat(latest).rename_axis("date").reset_index()
    return panel, latest, news_end


# ------------------------------------------------------------- models -----
def get_models():
    return {
        "xgboost": XGBClassifier(   # small + regularised: stock data is noisy, big models just memorise it
            n_estimators=200, max_depth=2, learning_rate=0.03, min_child_weight=20,
            subsample=0.8, colsample_bytree=0.8, eval_metric="logloss",
        ),
        "logistic_regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "random_forest": RandomForestClassifier(n_estimators=300, min_samples_leaf=20, random_state=0),
    }


def _auc(y, p):
    return roc_auc_score(y, p) if pd.Series(y).nunique() > 1 else np.nan


def walk_forward(panel, feats, target="target", dead_zone=0.0, n_splits=5, model_names=None):
    """
    Split by DATE (not by row) so every stock's future stays out of training:
    train on the past dates, test on the next block of dates, roll forward.
    dead_zone: while TRAINING, ignore days whose move was tiny (|move| < dead_zone) - those labels
    are mostly noise. Testing always uses every day, so results stay comparable.
    """
    ret_col = "future_excess" if target == "target_excess" else "future_ret"
    X, y = panel[feats], panel[target]
    names = model_names or list(get_models())
    dates = np.sort(panel["date"].unique())
    tscv = TimeSeriesSplit(n_splits=n_splits, gap=HORIZON)   # gap: labels look HORIZON days ahead
    oof = {n: np.full(len(panel), np.nan) for n in names}

    for tr_d, te_d in tscv.split(dates):
        tr = panel["date"].isin(dates[tr_d]).values
        te = panel["date"].isin(dates[te_d]).values
        fit = tr & (panel[ret_col].abs().values >= dead_zone)
        for n in names:
            model = get_models()[n].fit(X.loc[fit], y.loc[fit])
            oof[n][te] = model.predict_proba(X.loc[te])[:, 1]

    ok = ~np.isnan(oof["xgboost"])
    overall = {n: {"accuracy": accuracy_score(y[ok], p[ok] > 0.5), "auc": _auc(y[ok], p[ok])} for n, p in oof.items()}
    base = y[ok].mean()
    overall["baseline (best constant guess)"] = {"accuracy": max(base, 1 - base), "auc": 0.5}

    per_ticker = {}

    for t, g in panel.groupby("ticker"):
        ticker_ok = ok[g.index]

        # This ticker had no out-of-sample predictions
        if ticker_ok.sum() == 0:
            per_ticker[t] = {
                "accuracy": np.nan,
                "auc": np.nan,
                "baseline": max(g[target].mean(), 1 - g[target].mean()),
            }
            continue

        valid_g = g.loc[ticker_ok]
        p = oof["xgboost"][valid_g.index]

        per_ticker[t] = {
            "accuracy": accuracy_score(valid_g[target], p > 0.5),
            "auc": _auc(valid_g[target], p),
            "baseline": max(valid_g[target].mean(), 1 - valid_g[target].mean()),
        }
    return pd.DataFrame(overall).T, pd.DataFrame(per_ticker).T, oof


def confidence_table(y, p) -> pd.DataFrame:
    """Does a higher confidence number actually mean the model is right more often?"""
    ok = ~np.isnan(p)
    y, p = np.asarray(y)[ok], p[ok]
    conf, pred = np.maximum(p, 1 - p), (p > 0.5).astype(int)
    rows = []
    for lo, hi in [(0.5, 0.55), (0.55, 0.6), (0.6, 1.01)]:
        m = (conf >= lo) & (conf < hi)
        rows.append({"confidence": f"{lo:.0%}-{min(hi, 1):.0%}", "n_predictions": int(m.sum()),
                     "accuracy": float((pred[m] == y[m]).mean()) if m.any() else np.nan})
    return pd.DataFrame(rows).set_index("confidence")


def backtest(panel: pd.DataFrame, prob: np.ndarray, cost: float = 0.001) -> pd.DataFrame:
    """Per stock: hold when P(positive) > THRESHOLD else cash, vs buy & hold (out-of-sample only)."""
    out = {}
    for t, g in panel.groupby("ticker"):
        p = pd.Series(prob[g.index], index=g.index)
        next_ret = g["ret_1d"].shift(-1)
        m = p.notna() & next_ret.notna()
        pos = (p[m] > THRESHOLD).astype(int)
        strat = pos * next_ret[m] - pos.diff().abs().fillna(0) * cost
        out[t] = {"strategy": (1 + strat).prod(), "buy_and_hold": (1 + next_ret[m]).prod()}
    return pd.DataFrame(out).T


# --------------------------------------------------------- experiments ----
def run_experiments(tickers, start, news_csv=None):
    """Try each kind of data / setting and report which ones actually improve out-of-sample AUC."""
    panel, _, _ = build_panel(tickers, start, news_csv)
    has_excess = "target_excess" in panel.columns
    plans = [("price only", ["price"], "target", 0.0),
             ("+ market context", ["price", "market"], "target", 0.0),
             ("+ calendar", ["price", "market", "calendar"], "target", 0.0)]
    all_groups = ["price", "market", "calendar"] + (["sentiment"] if news_csv else [])
    if news_csv:
        plans.append(("+ news sentiment", all_groups, "target", 0.0))
    plans.append(("all, ignore tiny moves in training (1%)", all_groups, "target", 0.01))
    if has_excess:
        plans.append(("all, target = beat the S&P 500", all_groups, "target_excess", 0.0))

    rows = []
    for label, groups, target, dz in plans:
        if any(not pick(panel, [g]) for g in groups):   # e.g. market data failed to download
            continue
        feats = pick(panel, groups)
        overall, _, _ = walk_forward(panel, feats, target, dz, model_names=["xgboost"])
        rows.append({"experiment": label, "features": len(feats),
                     "accuracy": overall.loc["xgboost", "accuracy"], "auc": overall.loc["xgboost", "auc"],
                     "baseline_acc": overall.iloc[-1]["accuracy"]})
    table = pd.DataFrame(rows).set_index("experiment")
    print(f"\nExperiments ({panel['ticker'].nunique()} stock(s), {len(panel)} stock-days, out-of-sample)\n")
    print(table.round(3))
    print("\nAUC 0.5 = coin flip. With only a few stocks, differences under ~0.03 AUC are noise, so only trust")
    print("changes bigger than that. The last row predicts a different question, so compare its AUC only.")
    return table


# ------------------------------------------------------------- signals ----
def reliability(auc: float, pooled_auc: float) -> str:
    """
    Rule of thumb from out-of-sample history: AUC 0.5 = coin flip; honest stock models rarely pass ~0.6.
    A single stock can score well by luck, so the pooled model must show some skill too.
    """
    if not auc >= 0.55 or not pooled_auc >= 0.52:
        return "LOW"
    return "MODERATE" if auc < 0.60 else "HIGH"


def predict_signals(tickers, start="2020-01-01", news_csv=None, target="target", dead_zone=0.0, verbose=True):
    excess = target == "target_excess"
    panel, latest, news_end = build_panel(tickers, start, news_csv)
    if excess and "target_excess" not in panel.columns:
        raise SystemExit("--target excess needs S&P 500 (SPY) data, which failed to download.")
    groups = ["price", "market", "calendar"] + (["sentiment"] if news_csv else [])
    feats = pick(panel, groups)
    overall, per_ticker, oof = walk_forward(panel, feats, target, dead_zone)

    ret_col = "future_excess" if excess else "future_ret"
    fit = (panel[ret_col].abs().values >= dead_zone)
    final = get_models()["xgboost"].fit(panel.loc[fit, feats], panel.loc[fit, target])
    joblib.dump({"model": final, "features": feats, "target": target}, "marketmind_model.joblib")
    p_pos = final.predict_proba(latest[feats])[:, 1]

    up, down = ("OUTPERFORM", "UNDERPERFORM") if excess else ("UP", "DOWN")
    signals = []
    for (_, row), p in zip(latest.iterrows(), p_pos):
        t = row["ticker"]
        auc = float(per_ticker.loc[t, "auc"]) if t in per_ticker.index else float("nan")
        direction = up if p >= 0.5 else down
        sig = {
            "ticker": t,
            "as_of": str(pd.Timestamp(row["date"]).date()),
            "horizon_trading_days": HORIZON,
            "question": "beats the S&P 500?" if excess else "price higher?",
            "direction": direction,
            "probability_outperform" if excess else "probability_up": round(float(p), 3),
            "confidence": round(float(p if p >= 0.5 else 1 - p), 3),  # 0.5 = coin flip
            "reliability": reliability(auc, float(overall.loc["xgboost", "auc"])),
            "walk_forward_auc": None if np.isnan(auc) else round(auc, 3),
            "walk_forward_accuracy": round(float(per_ticker.loc[t, "accuracy"]), 3),
            "baseline_accuracy": round(float(per_ticker.loc[t, "baseline"]), 3),
            "feature_groups": groups,
        }
        if t in news_end and (pd.Timestamp(row["date"]) - news_end[t]).days > 7:
            sig["note"] = f"news data ends {news_end[t].date()}; no fresh sentiment for this signal"
        signals.append(sig)

    with open("marketmind_signals.json", "w") as f:
        json.dump(signals, f, indent=2)
    log.info("wrote %d signals", len(signals))

    if verbose:
        print(f"\nPooled walk-forward results ({len(panel)} stock-days, {panel['ticker'].nunique()} stock(s), "
              f"features: {', '.join(groups)})\n")
        print(overall.round(3))
        print("\nXGBoost per stock (out-of-sample)\n")
        print(per_ticker.round(3))
        print("\nWhen the model is more confident, is it right more often?\n")
        print(confidence_table(panel[target].values, oof["xgboost"]).round(3))
        print("\nBacktest, final growth of $1 (0.1% cost per trade):\n")
        print(backtest(panel, oof["xgboost"]).round(2))
        print("\nLatest signals\n")
        show = pd.DataFrame(signals)[["ticker", "as_of", "direction", "confidence", "reliability"]]
        print(show.to_string(index=False))
        if all(s["reliability"] == "LOW" for s in signals):
            print("\nWarning: on past data this model was not better than chance for any stock. "
                  "Treat these signals as very weak.")
    return signals


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*", default=DEFAULT_TICKERS)
    ap.add_argument("--all", action="store_true", help="use every stock in ALL_TICKERS")
    ap.add_argument("--news", default=None, help="CSV from finbert_sentiment.py")
    ap.add_argument("--start", default="2020-01-01")
    ap.add_argument("--target", choices=["absolute", "excess"], default="absolute",
                    help="absolute = price up/down; excess = beats the S&P 500")
    ap.add_argument("--dead-zone", type=float, default=0.0,
                    help="ignore moves smaller than this (e.g. 0.01 = 1%%) when training")
    ap.add_argument("--experiments", action="store_true", help="compare data/settings instead of making signals")
    a = ap.parse_args()
    chosen = ALL_TICKERS if a.all else a.tickers
    if a.experiments:
        run_experiments(chosen, a.start, a.news)
    else:
        predict_signals(chosen, a.start, a.news, "target_excess" if a.target == "excess" else "target", a.dead_zone)
