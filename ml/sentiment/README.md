# News sentiment

Existing: finbert_sentiment.py. It filters a raw news CSV by ticker/date,
scores headlines, and writes date, ticker, score, positive, negative,
neutral, and headline columns. Score is positive minus negative probability.

Add preprocessing or a reusable sentiment service here when needed, for
example preprocessing.py and sentiment_service.py. Keep a loaded model
reusable in a future service rather than loading it for each article.

Run commands and expected raw columns are documented in ../../README.md.
Default output is data/processed/news_scored.csv under the project root.
A custom --out path is honored and its parent folders are created.
