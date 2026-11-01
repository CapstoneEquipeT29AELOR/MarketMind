# MarketMind

**Start here.** This package organizes the supplied FinBERT / XGBoost research
code and reserves clearly labeled folders for the rest of the application.
Folders marked **TODO** contain READMEs only: their suggested filenames are
examples to implement, not working features.

## Where to put your work

| Folder | What belongs here | Current state |
| --- | --- | --- |
| [frontend/](frontend/README.md) | Dashboard pages, components, API client, styles | TODO |
| [backend/](backend/README.md) | HTTP API, application services, provider adapters, database | TODO |
| [ml/](ml/README.md) | Sentiment, experimental forecasting, future summaries and evaluation | Existing scripts + TODOs |
| [data/](data/README.md) | Raw inputs and processed datasets | NVDA news sample included |
| [notebooks/](notebooks/README.md) | Interactive research | Existing trading notebook |
| [experiments/](experiments/README.md) | Standalone prototypes | Existing SMA signal script |
| [tests/](tests/README.md) | Unit, integration, and smoke tests | TODO |
| [config/](config/README.md) | Shared configuration examples | TODO |
| [scripts/](scripts/README.md) | Repeatable import, scoring, and demo commands | TODO |
| [requirements/](requirements/README.md) | Python dependency lists | Original lists retained |
| [artifacts/](artifacts/README.md) | Generated trained models and prediction JSON | Output folders prepared |
| [logs/](logs/README.md) | Generated runtime logs | Output folder prepared |
| [docs/](docs/README.md) | Project proposal, meetings, architecture, development order | Existing notes + new guides |

See [the complete file map](docs/FILE_MAP.md) for every original file's new
location and [NEXT_STEPS.md](docs/NEXT_STEPS.md) for what to implement first.
The original team roster and project description are preserved in
[project-proposal.md](docs/project-proposal.md).

## Existing code

- `ml/sentiment/finbert_sentiment.py` scores news headlines using FinBERT.
- `ml/forecasting/marketmind_model.py` trains a pooled XGBoost forecaster and
  evaluates it alongside logistic regression and random forest.
- `experiments/generate_signals.py` plots an SMA crossover prototype.
- `notebooks/trading.ipynb` explores SMA, RSI, and news sentiment.

FinBERT classifies headline sentiment; XGBoost forecasts a price-related
target using engineered features. They serve different steps in the pipeline.
The notebook's existing outputs are retained and have not been regenerated.

The frontend, API, database, and news summaries have **not** been implemented
in this archive. The supplied notes prioritize a market-information dashboard
and source-backed news summaries; forecasting and trading research remain
separate from that MVP.

## Run the existing scripts

Extract the ZIP, open the `MarketMind` folder in your editor, and run these
commands from that folder. Create and activate a virtual environment first:

```bash
python -m venv .venv
```

Windows PowerShell: `.\.venv\Scripts\Activate.ps1`

macOS / Linux: `source .venv/bin/activate`

```bash
python -m pip install -r requirements.txt
python ml/sentiment/finbert_sentiment.py --help
python ml/forecasting/marketmind_model.py --help
python ml/forecasting/marketmind_model.py NVDA --news data/processed/news_scored_all.csv
```

To compare the existing feature-group experiments:

```bash
python ml/forecasting/marketmind_model.py NVDA --news data/processed/news_scored_all.csv --experiments
```

To score your own raw news CSV (you must supply this input):

```bash
python ml/sentiment/finbert_sentiment.py data/raw/news.csv --tickers NVDA --out data/processed/news_scored.csv
```

The raw CSV must have `Date`, `Article_title`, and `Stock_symbol` columns,
or you must pass the script's column-name options. The bundled processed CSV
already contains scores and does not need FinBERT run on it again.

To run the original plotting prototype or notebook:

```bash
python -m pip install -r requirements/research.txt
python experiments/generate_signals.py
jupyter notebook notebooks/trading.ipynb
```

These are local setup commands, not a claim that the full pipeline was run.
Price retrieval requires network access; initial FinBERT use downloads its
model. Dependency compatibility still needs validation in your environment.

## Inputs and outputs

| Item | Location |
| --- | --- |
| Bundled scored news | `data/processed/news_scored_all.csv` |
| New raw data | `data/raw/` |
| Default newly scored news | `data/processed/news_scored.csv` |
| Trained model | `artifacts/models/marketmind_model.joblib` |
| Forecast JSON | `artifacts/predictions/marketmind_signals.json` |
| Model log | `logs/marketmind.log` |

The bundled CSV contains **2,951 NVDA headlines, January 1, 2022 through
December 16, 2023**. It is historical sample data, not a live news feed.
Model output paths are based on the script location, so files stay in these
folders regardless of your terminal's working directory. Explicit relative
input paths and a custom `--out` path remain relative to your terminal.

## What changed in this organization

Files were moved by responsibility. Script examples, the notebook's CSV
lookup, model outputs, and default FinBERT output now use the new layout.
Training, sentiment scoring, features, and evaluation algorithms were kept.
Both original dependency lists are retained; the root `requirements.txt`
now forwards to the shorter existing ML list. No new dependencies were pinned.
Future code folders contain instructions only, with no dummy application code.

See [VERIFICATION.md](docs/VERIFICATION.md) for the checks and limitations.
