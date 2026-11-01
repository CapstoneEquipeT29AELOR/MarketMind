# Processed data

Existing: news_scored_all.csv, copied without changes from the upload.
It has 2,951 NVDA headlines dated 2022-01-01 through 2023-12-16.

Columns: date, ticker, score, positive, negative, neutral, headline.
The score is P(positive) - P(negative). Dates are historical; the file does
not provide live news, article URLs, publisher fields, or full article text.

Put newly cleaned/scored datasets here. The scorer defaults to
news_scored.csv so the supplied sample is retained. The sample CSV is
allowed by .gitignore; other generated CSVs are ignored by default.
Keep transformation code under ml/ or backend/, not in this folder.
