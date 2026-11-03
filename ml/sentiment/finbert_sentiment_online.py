"""
MarketMind - FinBERT news scoring step (online news version).

Fetches headlines online (yfinance or Finnhub), scores each with FinBERT, and
appends new rows to a CSV that marketmind_model.py can load.

Usage:
  python ml/sentiment/finbert_sentiment_online.py --source yfinance --tickers NVDA AAPL
  python ml/sentiment/finbert_sentiment_online.py --source finnhub --tickers NVDA --since 2025-11-01

For Finnhub, set your key first (PowerShell):  $env:FINNHUB_API_KEY="your_key"

Output columns: date, ticker, score, positive, negative, neutral, headline
  score = P(positive) - P(negative), from -1 (very bad news) to +1 (very good news)

Install: pip install yfinance requests transformers torch pandas

output: news_scored.csv in data/processed/news_scored.csv
"""
import argparse
import os
import time
from pathlib import Path

import pandas as pd
import requests

DEFAULT_TICKERS = ["NVDA"]


def fetch_yfinance(tickers):
    import yfinance as yf

    rows = []
    for t in tickers:
        for item in yf.Ticker(t).news or []:
            c = item.get("content", item)  # newer yfinance nests fields under "content"
            title = c.get("title")
            ts = c.get("pubDate") or item.get("providerPublishTime")
            if not title or not ts:
                continue
            unit = "s" if isinstance(ts, (int, float)) else None
            d = pd.to_datetime(ts, unit=unit, utc=True).tz_localize(None).normalize()
            rows.append({"date": d, "ticker": t, "text": title})
    return pd.DataFrame(rows)


def fetch_finnhub(tickers, since, until):
    key = os.environ.get("FINNHUB_API_KEY")
    if not key:
        raise SystemExit("Set the FINNHUB_API_KEY environment variable first.")
    until = min(until, pd.Timestamp.today().normalize())
    rows = []
    for t in tickers:
        print(f"Fetching {t} from Finnhub...")
        for start in pd.date_range(since, until, freq="30D"):  # small windows so results aren't truncated
            end = min(start + pd.Timedelta(days=29), until)
            r = requests.get(
                "https://finnhub.io/api/v1/company-news",
                params={"symbol": t, "from": start.strftime("%Y-%m-%d"),
                        "to": end.strftime("%Y-%m-%d"), "token": key},
                timeout=30,
            )
            r.raise_for_status()
            for a in r.json():
                if a.get("headline"):
                    rows.append({"date": pd.to_datetime(a["datetime"], unit="s").normalize(),
                                 "ticker": t, "text": a["headline"]})
            time.sleep(1.1)  # stay under the free rate limit (60 calls/min)
    return pd.DataFrame(rows)


def score_texts(texts, batch_size=64):
    import torch
    from transformers import pipeline

    use_gpu = torch.cuda.is_available()
    print(f"Using {'GPU: ' + torch.cuda.get_device_name(0) if use_gpu else 'CPU (slow)'}")
    clf = pipeline("text-classification", model="ProsusAI/finbert", top_k=None,
                   device=0 if use_gpu else -1)
    rows = []
    for i in range(0, len(texts), batch_size):
        for res in clf(texts[i:i + batch_size], batch_size=batch_size, truncation=True, max_length=512):
            p = {r["label"].lower(): r["score"] for r in res}
            rows.append((p["positive"], p["negative"], p["neutral"]))
        print(f"  scored {min(i + batch_size, len(texts))}/{len(texts)}")
    return pd.DataFrame(rows, columns=["positive", "negative", "neutral"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["yfinance", "finnhub"], default="yfinance")
    ap.add_argument("--tickers", nargs="*", default=DEFAULT_TICKERS)
    ap.add_argument("--since", default=None, help="finnhub only; default = 1 year ago")
    ap.add_argument("--until", default=None, help="finnhub only; default = today")
    ap.add_argument("--per-day-cap", type=int, default=5, help="max headlines per ticker per day (0 = no cap)")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[2] / "data" / "processed" / "news_scored.csv"))
    a = ap.parse_args()

    today = pd.Timestamp.today().normalize()
    since = pd.Timestamp(a.since) if a.since else today - pd.Timedelta(days=365)
    until = pd.Timestamp(a.until) if a.until else today

    news = fetch_yfinance(a.tickers) if a.source == "yfinance" else fetch_finnhub(a.tickers, since, until)
    if news.empty:
        raise SystemExit("No headlines returned. Check the tickers / API key.")
    news = news.drop_duplicates(["date", "ticker", "text"])
    if a.per_day_cap:
        news = news.groupby(["ticker", "date"]).head(a.per_day_cap)

    # skip headlines already scored in a previous run
    output = Path(a.out).expanduser()
    old = pd.read_csv(output, parse_dates=["date"]) if output.exists() else None
    if old is not None:
        seen = set(zip(old["date"], old["ticker"], old["headline"]))
        news = news[[k not in seen for k in zip(news["date"], news["ticker"], news["text"])]]
    if news.empty:
        raise SystemExit("No new headlines since the last run.")
    news = news.reset_index(drop=True)

    print(f"Scoring {len(news)} new headlines with FinBERT...")
    scores = score_texts(news["text"].tolist())
    result = pd.concat([news, scores], axis=1).rename(columns={"text": "headline"})
    result["score"] = result["positive"] - result["negative"]
    result = result[["date", "ticker", "score", "positive", "negative", "neutral", "headline"]]
    if old is not None:
        result = pd.concat([old, result], ignore_index=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    print(f"Saved {output} ({len(result)} rows total)")