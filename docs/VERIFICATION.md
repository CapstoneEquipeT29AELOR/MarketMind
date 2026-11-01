# Organization checks

Checked on November 1, 2026. These checks validate the reorganization, not the
forecasting accuracy or readiness of the future application.

## Checked

- All 11 original files are accounted for in FILE_MAP.md.
- Seven relocated files remain byte-for-byte identical: the proposal, meeting
  notes, trading concept, SMA script, sample CSV, and both dependency lists.
- All original .gitignore rules are retained; only additional rules were appended.
- All three Python scripts and all nine notebook code cells compile.
- Existing computation functions are unchanged; predict_signals() differs only
  in output paths and creation of the corresponding directories.
- The notebook retains its original metadata and stored outputs. Only its CSV
  lookup cell source was adjusted, and that lookup resolves from both the project
  root and the notebooks folder.
- Model, prediction, log, and default FinBERT output paths resolve under the
  organized project root.
- The FinBERT --help command executes successfully from outside the project.
- New documentation's local links and dependency include paths resolve.
- The sample CSV remains unchanged: 2,951 NVDA rows, dated 2022-01-01 through
  2023-12-16.
- Every leaf folder contains a README, including folders reserved for future code.
- The final ZIP passes its integrity check and includes all project files and
  README-only folders.

## Not run

The complete dependency installation, live price retrieval, FinBERT inference,
forecast training, plotting, and full notebook execution were not run. This
environment lacks yfinance, xgboost, torch, and transformers. No packages or
model weights were downloaded for this file-organization task.

No frontend, API server, database, summarizer, or application test suite exists
yet in this package. Their folders are intentionally README-only placeholders.
There is no end-to-end application validation to report.
