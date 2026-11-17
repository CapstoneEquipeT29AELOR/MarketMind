import logging
import threading
import requests
import yfinance
import os
import json
import math

from datetime import datetime, timedelta, timezone
from functools import lru_cache
from collections import Counter


# ------------------------------------------------------------------ news ----
def _news_finnhub(symbol, start, end):
    res = requests.get(
        "https://finnhub.io/api/v1/company-news",
        params={"symbol": symbol, "from": start.strftime("%Y-%m-%d"),
                "to": end.strftime("%Y-%m-%d"), "token": os.getenv("FINNHUB_API_KEY")},
        timeout=15,
    )
    res.raise_for_status()
    articles = []
    for a in res.json():
        if not a.get("headline") or not a.get("datetime"):
            continue
        articles.append({
            "title": a["headline"],
            "description": a.get("summary") or None,
            "url": a.get("url"),
            "urlToImage": a.get("image") or None,
            "publishedAt": datetime.fromtimestamp(a["datetime"], tz=timezone.utc).isoformat(),
            "source": {"name": a.get("source")},
        })
    return articles


def _news_yfinance(symbol, start, end, limit):
    articles = []
    for item in yfinance.Ticker(symbol).get_news(count=max(limit, 20)) or []:
        c = item.get("content", item)  # newer yfinance nests fields under "content"
        title = c.get("title")
        ts = c.get("pubDate") or item.get("providerPublishTime")
        if not title or not ts:
            continue
        if isinstance(ts, (int, float)):
            published = datetime.fromtimestamp(ts, tz=timezone.utc)
        else:
            published = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if not (start <= published <= end):
            continue
        articles.append({
            "title": title,
            "description": c.get("summary") or None,
            "url": (c.get("canonicalUrl") or {}).get("url") or (c.get("clickThroughUrl") or {}).get("url") or item.get("link"),
            "urlToImage": (c.get("thumbnail") or {}).get("originalUrl"),
            "publishedAt": published.isoformat(),
            "source": {"name": (c.get("provider") or {}).get("displayName") or item.get("publisher")},
        })
    return articles


_finbert_lock = threading.Lock()

@lru_cache(maxsize=1)
def _finbert():
    """Loaded once, on the first request that asks for sentiment (slow the first time)."""
    import torch
    from transformers import pipeline
    return pipeline("text-classification", model="ProsusAI/finbert", top_k=None,
                    device=0 if torch.cuda.is_available() else -1)


def add_sentiment(articles):
    if not articles:
        return articles
    with _finbert_lock:  # the shared model isn't guaranteed thread-safe
        results = _finbert()([a["title"] for a in articles], batch_size=32, truncation=True, max_length=512)
    for a, res in zip(articles, results):
        p = {r["label"].lower(): r["score"] for r in res}
        a["sentiment"] = {
            "score": round(p["positive"] - p["negative"], 4),  # -1 (bad news) to +1 (good news)
            "label": max(p, key=p.get),
            "positive": round(p["positive"], 4),
            "negative": round(p["negative"], 4),
            "neutral": round(p["neutral"], 4),
        }
    return articles

log = logging.getLogger(__name__)


# ticker -> category shown on the news card (edit freely)
TRACKED = {"AAPL": "Technology", "GOOGL": "Technology", "MSFT": "Technology",
           "AMD": "Semiconductors", "TSLA": "Automotive", "NVDA": "Semiconductors"}
NEWS_DAYS = 7  # how many days of headlines the analysis looks at
MAX_ANALYSIS_HEADLINES = 50  # upper limit on headlines scored per analysis request


def _fetch_articles(symbol, start, end):
    if os.getenv("FINNHUB_API_KEY"):
        try:
            return _news_finnhub(symbol, start, end)
        except requests.RequestException as e:
            log.warning("Finnhub failed for %s (%s); falling back to yfinance", symbol, e)
    return _news_yfinance(symbol, start, end, limit=20)


def _time_ago(published_iso: str) -> str:
    secs = (datetime.now(timezone.utc) - datetime.fromisoformat(published_iso)).total_seconds()
    mins = int(secs // 60)
    if mins < 1:
        return "just now"
    if mins < 60:
        return f"{mins} min ago"
    hrs = mins // 60
    if hrs < 24:
        return f"{hrs} hr ago"
    days = hrs // 24
    return f"{days} day{'s' if days != 1 else ''} ago"


def _build_feed(symbols, limit, days):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    # with several tickers, keep each one's newest 10 so no single stock dominates the feed
    per_symbol = math.ceil(limit / len(symbols))  # each ticker's fair share of the feed
    merged = {}
    for sym in symbols:
        try:
            found = _fetch_articles(sym, start, end)
        except Exception as e:
            log.warning("news fetch failed for %s: %s", sym, e)
            continue
        found = sorted(found, key=lambda a: a["publishedAt"], reverse=True)[:per_symbol]
        for a in found:
            key = a["title"].strip().lower()
            if key in merged:
                if sym not in merged[key]["symbols"]:
                    merged[key]["symbols"].append(sym)
            else:
                merged[key] = {**a, "symbols": [sym]}
    articles = sorted(merged.values(), key=lambda a: a["publishedAt"], reverse=True)[:limit]
    try:
        add_sentiment(articles)
    except Exception as e:  # FinBERT unavailable -> tone falls back to "neutral"
        log.warning("sentiment scoring failed: %s", e)
    return articles


def _to_news_item(a):
    return {
        "source": (a.get("source") or {}).get("name") or "Unknown",
        "time": _time_ago(a["publishedAt"]),  # computed per request so it stays accurate
        "category": TRACKED.get(a["symbols"][0], "Markets"),
        "headline": a["title"],
        "summary": a.get("description") or "",
        "symbols": a["symbols"],
        "tone": (a.get("sentiment") or {}).get("label", "neutral"),
    }

def get_market_news(symbol: str | None = None, limit: int = 20, days: int = 3) -> list:
    symbols = [symbol.strip().upper()] if symbol else list(TRACKED)
    return [_to_news_item(a) for a in _build_feed(symbols, limit, days)]

# ---------------------------------------------------------------- prices ----
def _price_change_finnhub(symbol):
    """Latest price vs previous close, from Finnhub's /quote. None if there's no price."""
    res = requests.get("https://finnhub.io/api/v1/quote",
                       params={"symbol": symbol, "token": os.getenv("FINNHUB_API_KEY")}, timeout=15)
    res.raise_for_status()
    q = res.json()  # c = current price, pc = previous close
    if not q.get("c") or not q.get("pc"):  # unknown symbols come back as zeros
        return None
    return q["c"] / q["pc"] - 1


def _price_change_yfinance(symbol):
    hist = yfinance.Ticker(symbol).history(period="5d")
    if hist.empty or "Close" not in hist:
        return None
    close = hist["Close"].dropna()
    if len(close) < 2:
        return None
    return float(close.iloc[-1] / close.iloc[-2] - 1)


def _price_change(symbol):
    """Finnhub first. yfinance only if there is no Finnhub key, Finnhub errors, or has no price."""
    if os.getenv("FINNHUB_API_KEY"):
        try:
            change = _price_change_finnhub(symbol)
            if change is not None:
                return change
        except requests.RequestException as e:
            log.warning("Finnhub quote failed for %s (%s); falling back to yfinance", symbol, e)
    return _price_change_yfinance(symbol)


# -------------------------------------------------------------- analysis ----
def _impact(value, threshold):
    return "positive" if value > threshold else "negative" if value < -threshold else "caution"


def get_stock_analysis(symbol: str) -> dict | None:
    """Returns None if no price is found for the symbol (-> 404)."""
    symbol = symbol.strip().upper()
    change = _price_change(symbol)
    if change is None:
        return None

    # News: recent headlines, each already scored by FinBERT
    articles = _build_feed([symbol], MAX_ANALYSIS_HEADLINES, NEWS_DAYS)
    scored = [a for a in articles if a.get("sentiment")]
    n = len(scored)
    counts = Counter(a["sentiment"]["label"] for a in scored)

    if n:
        mean = sum(a["sentiment"]["score"] for a in scored) / n    # -1 .. +1
        score = round(50 + 50 * mean)                              # 0 .. 100
        strength = abs(counts["positive"] - counts["negative"]) / n  # 0 = no direction, 1 = all one-sided
        confidence = round(100 * strength * min(1, n / 10))        # fewer than 10 headlines -> less sure
    else:
        mean, score, confidence = 0.0, 50, 0

    sentiment = "Bullish" if score >= 60 else "Bearish" if score <= 40 else "Neutral"

    factors = []
    if n:
        factors.append({
            "label": "News sentiment",
            "detail": f"{counts['positive']} positive, {counts['negative']} negative and "
                      f"{counts['neutral']} neutral headlines in the last {NEWS_DAYS} days.",
            "impact": _impact(mean, 0.2),
        })
    factors.append({
        "label": "Latest price change",
        "detail": f"{change:+.1%} compared with the previous close.",
        "impact": _impact(change, 0.01),
    })

    if n:
        news_text = (f"{symbol} news sentiment is {sentiment.lower()}: {counts['positive']} of {n} "
                     f"recent headlines are positive and {counts['negative']} negative.")
    else:
        news_text = f"No scored news was available for {symbol} in the last {NEWS_DAYS} days."
    price_text = f"The price is {'up' if change >= 0 else 'down'} {abs(change):.1%} in the latest session."

    return {"sentiment": sentiment, "score": score, "confidence": confidence,
            "summary": f"{news_text} {price_text}", "factors": factors}

def get_stock_price_json(symbol: str, period: str) -> object:
    df = yfinance.download(symbol, period=period)
    if df.shape[0] == 0:
        return {}
    data = json.loads(df["Close"].to_json())
    parsed = {}
    kv = data[symbol].items()
    for k,v in kv:
        ts = int(k)
        dt_obj = datetime.fromtimestamp(ts//1000)
        dt_str = dt_obj.strftime("%Y-%m-%d")
        parsed[dt_str] = data[symbol][k]
    return parsed

def get_stock_lookup(query: str) -> list:
    stocks_df = yfinance.Lookup(query).get_stock(count=25)
    return stocks_df.index.tolist()
