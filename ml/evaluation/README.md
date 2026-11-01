# Model evaluation and comparison

Status: **TODO — this folder contains instructions only.**

## Code or content to add

Add reusable evaluation code and result exports when you extract them from the forecasting script. Start with its walk_forward(), confidence_table(), and backtest() functions. Keep date-based splits and the existing horizon gap when refactoring.

Example files: walk_forward.py, metrics.py, backtesting.py. Compare forecast models on the same data and dates; evaluate FinBERT sentiment separately using labeled headlines.

## First useful milestone

The same fixed inputs produce a documented, comparable metrics report. Existing evaluation still lives in ../forecasting/marketmind_model.py.
