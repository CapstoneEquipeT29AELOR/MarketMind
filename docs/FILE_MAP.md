# Original-to-organized file map

Every original file is retained, with the path-only adjustments listed below.

| Original path | New path |
| --- | --- |
| `.gitignore` | `.gitignore` |
| `README.md` | `docs/project-proposal.md` |
| `MeetingMinutes.txt` | `docs/meetings/MeetingMinutes.txt` |
| `trading-bot.md` | `docs/archive/trading-bot.md` |
| `finbert_sentiment.py` | `ml/sentiment/finbert_sentiment.py` |
| `marketmind_model.py` | `ml/forecasting/marketmind_model.py` |
| `generate_signals.py` | `experiments/generate_signals.py` |
| `news_scored_all.csv` | `data/processed/news_scored_all.csv` |
| `notebooks/trading.ipynb` | `notebooks/trading.ipynb` |
| `required_libraries.txt` | `requirements/required_libraries.txt` |
| `requirements.txt` | `requirements/environment-original.txt` |

## Limited content changes

- `marketmind_model.py`: updated command examples; logs now go to `logs/`,
  trained models to `artifacts/models/`, and signals to `artifacts/predictions/`.
  Those locations are resolved from the script, and output directories are created.
- `finbert_sentiment.py`: updated command examples and default scored-CSV path;
  custom output parent directories are created. Scoring logic is retained.
- `trading.ipynb`: updated only the moved news CSV lookup in one cell. All other
  cells and stored outputs are retained.
- `.gitignore`: retained all original rules and appended project-specific output
  rules while keeping folder READMEs and the bundled sample CSV trackable.
- Root `requirements.txt`: now forwards to the original short ML list. The
  original pinned file remains unchanged at `requirements/environment-original.txt`.
- Root `README.md`: new navigation/setup guide. The full original remains
  unchanged at `docs/project-proposal.md`.

New READMEs describe planned work. Suggested source filenames inside them are
not files that already exist. No backend/frontend features or model algorithms
were added in this organization.
