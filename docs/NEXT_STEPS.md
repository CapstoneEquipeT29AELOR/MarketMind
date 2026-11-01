# Suggested development order

The supplied project notes prioritize a dashboard, financial/news data,
source-backed AI summaries, a database, basic analysis, and an end-to-end demo.
The following is a proposed order, not a claim that these features exist.

| Order | Work to add | Folder | First useful result |
| --- | --- | --- | --- |
| 1 | Agree on response formats and choose frontend/backend/database tooling | docs/architecture/ | Small documented prices/news/summary contract |
| 2 | Build dashboard with fixture data | frontend/src/ | A selected ticker updates chart and news panels |
| 3 | Create API entrypoint and routes | backend/api/ | Health, stocks, prices, and news endpoints return JSON |
| 4 | Add financial/news provider clients | backend/integrations/ | Normalize prices/news with timestamps and source references |
| 5 | Add schema, migrations, and repositories | backend/database/ | Save/retrieve data without duplicate news records |
| 6 | Connect service workflows and frontend API client | backend/services/ + frontend/src/services/ | Dashboard shows retrieved provider data |
| 7 | Implement source-backed news summaries | ml/summarization/ | Summary links back to the articles used |
| 8 | Integrate existing sentiment scoring where useful | ml/sentiment/ + backend/services/ | Headline sentiment is available to the dashboard |
| 9 | Add repeatable imports, configuration, and startup commands | scripts/ + config/ | Teammates can repeat the demo setup |
| 10 | Document deployment and complete smoke checks | docs/architecture/ + tests/smoke/ | A reproducible end-to-end demonstration |

Add unit and integration tests alongside the corresponding implementation,
starting with normalized provider records and service behavior. Do not wait
until the last step to test the data pipeline.

## Existing forecasting research

Continue experiments in ml/forecasting/, ml/evaluation/, experiments/, and
notebooks/ without making them a prerequisite for the dashboard MVP.
Compare forecast models on identical dates and features. The bundled news
sample covers only NVDA in 2022–2023; other tickers and live summaries need
additional data with source references.

## Immediate environment follow-up

Create a clean local environment, install the ML dependencies, and record
tested Python/package versions. The supplied long environment snapshot and
short unpinned list have both been preserved so the team can reconcile them.
