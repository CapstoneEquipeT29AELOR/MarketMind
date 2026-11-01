# Experimental forecasting

Existing: marketmind_model.py. It includes price/market retrieval, feature
engineering, pooled training, date-based validation, model comparisons,
backtesting, and prediction export.

Run from the project root:

```bash
python ml/forecasting/marketmind_model.py NVDA --news data/processed/news_scored_all.csv
```

Add future forecasting code here, for example features.py, train.py, and
predict.py when you deliberately split the current script. Move reusable
evaluation to ../evaluation/ only after adding regression coverage.

Outputs go to artifacts/models/, artifacts/predictions/, and logs/ under
the project root. Each normal run overwrites the current model and signal
JSON filenames. Model parameters and evaluation logic were not changed by
this folder organization.
