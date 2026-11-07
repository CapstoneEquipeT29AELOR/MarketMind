# Raw input data

Status: **Empty except for this README.** Add original news CSVs, price
exports, or small provider fixtures here. Keep downloaded inputs unchanged.
For the existing FinBERT script, news.csv should provide Date, Article_title,
and Stock_symbol columns unless you pass different column names on the CLI.

Record provider, download date, date range, and field meanings with each
dataset. Raw files are ignored by Git by default; the full news dataset is
not bundled. Code for fetching these files belongs in backend/integrations/.
