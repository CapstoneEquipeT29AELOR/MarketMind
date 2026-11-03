# MarketMind Step 2: sample storage and rolling buffer

This is an additive package. Copy backend/, config/, scripts/, requirements/,
and tests/ from this package into the existing MarketMind root, preserving the
folder names. Merge directories; do not replace or delete the existing folders.
These files do not replace the forecasting scripts or the root requirements.txt.
If you already created a file with the same name locally, compare it before
replacing it. The original organized project had none of these source files.

## Files and responsibilities

| File | Responsibility |
| --- | --- |
| backend/database/collection_store.py | Initial SQLite schema, validated market bars, duplicate prevention, manually protected ranges, and completed news coverage |
| backend/services/buffer_service.py | Conservative calendar-day cleanup preview and optional sample deletion |
| config/collection.json | Tracked stocks, time zone, interval, retention lengths, and required sample news sources |
| scripts/demo_collection.py | Offline demonstration using three fictional one-minute bars per stock and a fixed clock |
| requirements/collection.txt | tzdata dependency for exchange time zones on Windows |
| tests/unit/test_collection_buffer.py | 26 automated tests, including the demo rerun checks |

For easier copying, the first schema is embedded in collection_store.py. This
is an initial sample schema, not a production migration framework. It will need
versioned migrations as the later tables and provider-specific records are added.

## Install and run (Windows PowerShell, project root)

Run each command separately. These are terminal commands, not file contents.

```powershell
.\.venv312\Scripts\python.exe -m pip install -r requirements/collection.txt
```

```powershell
.\.venv312\Scripts\python.exe scripts/demo_collection.py
```

With the original NVDA configuration, the demo prints:

```text
SAMPLE database: <your local application data folder>/MarketMind/step2_sample.sqlite3
After replay: 3 bars (before replay: 3)
NVDA simulated outage: News coverage unavailable: sample-news
NVDA eligible dates: ['2026-10-05']
NVDA deleted: 0
Remaining bars: 3
October 12 is protected; October 19 is still in the temporary buffer.
```

This is a preview: no observations are removed. To test deletion in the dedicated
sample database, run:

```powershell
.\.venv312\Scripts\python.exe scripts/demo_collection.py --apply-cleanup
```

It should report one deleted observation and two remaining observations. Running
again is safe: replay does not create duplicate rows. A bar previously purged by
cleanup can be reinserted by this deliberate sample replay and cleaned again;
there are never two stored observations with the same unique key. Real provider
checkpoints and avoiding unnecessary re-fetches belong to later steps.

Run the supplied tests:

```powershell
.\.venv312\Scripts\python.exe -m unittest discover -s tests/unit -p test_collection_buffer.py -v
```

## How it works

The unique observation key is ticker + UTC bar-start timestamp + interval + price
basis. Equivalent time-zone representations normalize to the same timestamp.
Replaying identical data returns False without changing the original received_at.
Conflicting prices or providers raise an error instead of silently overwriting
history. Correction/version storage is deferred; connect only one canonical feed
per observation identity until that is implemented.

All observations live in one table. retention_holds contains protected time
ranges: start inclusive, end exclusive. Overlapping holds reference the same
underlying observations through range queries; they do not copy the prices.
Holds can expand but cannot shrink through the current API.

With before_days=3 and grace_days=2, the buffer preserves the previous five full
exchange-local calendar dates plus today. Older bars are candidates, not automatic
deletions. The cleanup checks every configured news source, any relevant holds,
and the publication dates of all possible events that could protect each bar.
For a bar on date D, that publication range is D-after_days through D+before_days,
including the final date in full. This protects the last portion of a day's news
and avoids confusing a partial day's scan with complete coverage.

Coverage ranges can expand only through overlapping or adjoining successful
scans; they cannot skip gaps. Missing coverage and marked source failures block
cleanup. Do not call record_news_scan merely because an HTTP request returned:
all pages for that range must be persisted, classified, and have any necessary
holds in place first. These checks are simulated in the demo; no providers exist
yet. A provider outage is never recorded as an empty successful news scan.

Cleanup checks protections and deletes in the same BEGIN IMMEDIATE transaction.
A failed deletion rolls back the whole cleanup operation. A retention preview
does not authorize a later blind deletion: applying cleanup recalculates the
candidates in its own transaction.

## Sample assumptions and limits

- No API calls, API keys, real news classification, or automatic collector.
- Only finalized, minute-aligned 1m bars; unsupported intervals raise an error.
- All configured sample stocks share exchange_timezone in this first version.
- Calendar-day mode only. Selecting trading-day mode raises an explicit error;
  an exchange calendar and actual market-session coverage come later.
- The fixed demo clock is October 20, 2026; dates/prices are synthetic.
- The demo hold is manually specified for October 9 through October 15 inclusive
  in New York time. It demonstrates protection, not automatic event detection.
- No prices are synthesized for missing minutes, weekends, or holidays.
- The demo always uses step2_sample.sqlite3 under LOCALAPPDATA/MarketMind (or
  ~/.local/share/MarketMind on systems without LOCALAPPDATA), outside the repo.
- Do not use this demo to write to an actual production database. A runtime
  database setting, provider credentials, coverage verification, and scheduling
  belong to the provider-integration stage.
- Story matching, source attribution, pending/complete/missing-data event
  lifecycle, automatic backfill, revision history, and training exports are not
  implemented. Manual holds provide the cleanup protection until those exist.
- The existing FinBERT/XGBoost scripts remain separate and unchanged.

## Tests completed

The supplied 26 tests passed in the execution environment. They cover duplicate
replays, conflicting data, equivalent timestamps, original receipt times, missing
and failed news coverage, recovery, all-source requirements, gaps, grace and date
boundaries, daylight-saving transitions, overlapping/pre-existing holds, other
tickers, persistence after reopening, preview-only cleanup, rollback on simulated
failure, invalid configuration, and repeated preview/apply demo runs. They do not
establish live provider behavior or semantic story-deduplication accuracy.

## Git ignore additions

Append these lines to your existing .gitignore; keep its current contents:

```gitignore
.venv312/
*.sqlite3
*.sqlite3-journal
*.sqlite3-wal
*.sqlite3-shm
```

Stop after this sample-data step. Provider integration is Step 3.
