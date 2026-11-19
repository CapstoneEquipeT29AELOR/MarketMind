# MarketMind

## Where to put your work

| Folder | What belongs here | Current state |
| --- | --- | --- |
| [frontend/](frontend/) | React + Vite app: landing page, dashboard pages, components, API client, translations, styles | Implemented |
| [backend/](backend/README.md) | FastAPI service: stock search, charts, news and FinBERT analysis endpoints | Implemented |
| [ml/](ml/README.md) | Sentiment, forecasting, prototypes, data, notebooks, scripts and logs | Existing scripts + TODOs |
| [docs/](docs/README.md) | Project proposal, meetings, architecture, development order | Existing notes + guides |

Inside the frontend, put new pages in `frontend/src/pages/`, reusable UI in
`frontend/src/components/`, backend calls in `frontend/src/api/`, and every
user-facing string in both languages in `frontend/src/i18n/translations.js`.
Backend routes go in `backend/main.py`, request schemas in `backend/models.py`
and data/model logic in `backend/utils.py`; keep both `openapi.yaml` files in
sync when the API changes. Docker setup lives in each service's `Dockerfile`
and in the root `docker-compose.yml` (production) and `docker-compose.dev.yml`
(development).

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

## Installation (Docker)

The app (React frontend + FastAPI backend) runs entirely in Docker. You only
need [Docker](https://docs.docker.com/get-docker/) with Docker Compose v2.

```bash
git clone git@github.com:ErikSkjenna/MarketMind.git
cd MarketMind
cp backend/.env.example backend/.env   # then fill in FINNHUB_API_KEY
```

### Development (no SSL)

Runs the Vite dev server and uvicorn with hot reload; source folders are
mounted, so edits apply immediately.

```bash
docker compose -f docker-compose.dev.yml up --build
```

- Frontend: <http://localhost:5173>
- Backend API docs: <http://localhost:8080/docs>

### Production (HTTPS)

Serves the built frontend through nginx on ports 80/443 (HTTP redirects to
HTTPS) and proxies `/api` to the backend. Put your certificate in `./certs`
as `fullchain.pem` and `privkey.pem`. For a local test, a self-signed one works:

```bash
mkdir -p certs
openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
  -keyout certs/privkey.pem -out certs/fullchain.pem -subj "/CN=localhost"
docker compose up -d --build
```

Then open <https://localhost>.

### Useful commands

```bash
docker compose logs -f backend                    # follow backend logs
docker compose down                               # stop production stack
docker compose -f docker-compose.dev.yml down     # stop dev stack
```

The first AI analysis request downloads the FinBERT model (a few hundred MB);
it is cached in a Docker volume, so later starts are fast.

## Run the existing scripts

The ML research scripts are not containerized; run them with a local Python
environment. From the `MarketMind` folder, create and activate a virtual
environment first:

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
