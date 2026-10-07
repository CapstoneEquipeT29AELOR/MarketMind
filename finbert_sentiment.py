"""
MarketMind - FinBERT news scoring step.

Reads a big news CSV (e.g. FNSPID), keeps only your tickers/dates, scores each
headline with FinBERT, and writes a small CSV that marketmind_model.py can load.

Usage:
  python finbert_sentiment.py fnspid_news.csv --since 2020-01-01 --out news_scored_all.csv

example:
  python finbert_sentiment.py "C:/Users/andyj/Downloads/nasdaq_exteral_data.csv" --tickers AAPL GOOGL MSFT AMD TSLA NVDA --out news_scored_all.csv
  nasdaq_exteral_data.csv is the dataset where there is all the news regarding FNSPID: https://huggingface.co/datasets/1ceyyu/FNSPID
  You will need to download it (28gb)

Output columns: date, ticker, score, positive, negative, neutral, headline
  score = P(positive) - P(negative), so it runs from -1 (very bad news) to +1 (very good news)

Install: pip install [see requirements.txt file]
"""
import argparse

import pandas as pd

# US-listed tickers only: FNSPID covers S&P 500 companies (dataset)
DEFAULT_TICKERS = ["NVDA"]   # testing default; pass --tickers AAPL MSFT ... for more


def load_news(path, tickers, since, until, date_col, text_col, ticker_col, per_day_cap):
    parts = []
    # chunked read: the full dataset is many GB
    for chunk in pd.read_csv(path, usecols=[date_col, text_col, ticker_col], chunksize=500_000,
                            dtype={ticker_col: str}):
        chunk = chunk.dropna()
        chunk = chunk[chunk[ticker_col].isin(tickers)]
        if chunk.empty:
            continue
        d = pd.to_datetime(chunk[date_col], utc=True, errors="coerce").dt.tz_localize(None)
        out = pd.DataFrame({"date": d.dt.normalize(), "ticker": chunk[ticker_col], "text": chunk[text_col]})
        out = out.dropna(subset=["date"])
        out = out[(out["date"] >= since) & (out["date"] <= until)]
        parts.append(out)
    if not parts:
        raise SystemExit("No news rows matched those tickers/dates. Check the column names and tickers.")
    news = pd.concat(parts).drop_duplicates(["date", "ticker", "text"])
    if per_day_cap:  # keeps scoring time manageable
        news = news.groupby(["ticker", "date"]).head(per_day_cap)
    return news.reset_index(drop=True)


def score_texts(texts, batch_size=64):
    import torch
    from transformers import pipeline

    use_gpu = torch.cuda.is_available()
    print(f"Using {'GPU: ' + torch.cuda.get_device_name(0) if use_gpu else 'CPU (slow) - install the CUDA build of PyTorch from pytorch.org to use your GPU'}")
    clf = pipeline("text-classification", model="ProsusAI/finbert", top_k=None,
                   device=0 if use_gpu else -1)
    rows = []
    for i in range(0, len(texts), batch_size):
        for res in clf(texts[i:i + batch_size], batch_size=batch_size, truncation=True, max_length=512):
            p = {r["label"].lower(): r["score"] for r in res}
            rows.append((p["positive"], p["negative"], p["neutral"]))
        if (i // batch_size) % 50 == 0:
            print(f"  scored {min(i + batch_size, len(texts))}/{len(texts)}")
    return pd.DataFrame(rows, columns=["positive", "negative", "neutral"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("news_csv")
    ap.add_argument("--tickers", nargs="*", default=DEFAULT_TICKERS)
    ap.add_argument("--since", default="2020-01-01")
    ap.add_argument("--until", default="2100-01-01")
    ap.add_argument("--date-col", default="Date")
    ap.add_argument("--text-col", default="Article_title")
    ap.add_argument("--ticker-col", default="Stock_symbol")
    ap.add_argument("--per-day-cap", type=int, default=5, help="max headlines per ticker per day (0 = no cap)")
    ap.add_argument("--out", default="news_scored.csv")
    a = ap.parse_args()

    news = load_news(a.news_csv, a.tickers, pd.Timestamp(a.since), pd.Timestamp(a.until),
                     a.date_col, a.text_col, a.ticker_col, a.per_day_cap)
    print(f"Scoring {len(news)} headlines with FinBERT...")
    scores = score_texts(news["text"].tolist())
    result = pd.concat([news[["date", "ticker", "text"]], scores], axis=1).rename(columns={"text": "headline"})
    result["score"] = result["positive"] - result["negative"]
    result[["date", "ticker", "score", "positive", "negative", "neutral", "headline"]].to_csv(a.out, index=False)
    print(f"Saved {a.out}")
