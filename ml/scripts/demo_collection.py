"""Offline Step 2 demo. Writes only a dedicated sample database."""

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.database.collection_store import CollectionStore
from backend.services.buffer_service import cleanup_buffer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-cleanup", action="store_true")
    args = parser.parse_args()
    settings = json.loads((ROOT / "config/collection.json").read_text(encoding="utf-8-sig"))
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / ".local/share")))
    path = base / "MarketMind" / "step2_sample.sqlite3"
    print(f"SAMPLE database: {path}")
    store = CollectionStore(path)
    try:
        # Fictional prices and a fixed clock make the example repeatable.
        prices = {"open": 100, "high": 102, "low": 99, "close": 101, "volume": 500}
        for ticker in settings["tickers"]:
            for day in (5, 12, 19):
                store.add_bar(ticker, f"2026-10-{day:02d}T14:30:00Z", prices,
                              interval=settings["interval"],
                              received_at="2026-10-20T16:00:00Z")
        before = store.count()
        for ticker in settings["tickers"]:
            for day in (5, 12, 19):
                store.add_bar(ticker, f"2026-10-{day:02d}T14:30:00Z", prices,
                              interval=settings["interval"])
        print(f"After replay: {store.count()} bars (before replay: {before})")

        now = "2026-10-20T16:00:00Z"
        for ticker in settings["tickers"]:
            store.protect_range(f"sample-event-{ticker}", ticker,
                                "2026-10-09T00:00:00-04:00",
                                "2026-10-16T00:00:00-04:00")
            # An explicit synthetic success record; no API request is made.
            store.record_news_scan(ticker, "sample-news",
                                   "2026-10-01T00:00:00Z", now)
            store.record_news_failure(ticker, "sample-news")
            blocked = cleanup_buffer(store, ticker, now, settings)
            print(f"{ticker} simulated outage: {blocked['blocked']}")
            store.record_news_scan(ticker, "sample-news",
                                   "2026-10-01T00:00:00Z",
                                   "2026-10-20T16:01:00Z")
            result = cleanup_buffer(store, ticker, "2026-10-20T16:01:00Z",
                                    settings, apply=args.apply_cleanup)
            print(f"{ticker} eligible dates: {[r['timestamp'][:10] for r in result['eligible']]}")
            print(f"{ticker} deleted: {result['deleted']}")
        print(f"Remaining bars: {store.count()}")
        print("October 12 is protected; October 19 is still in the temporary buffer.")
    finally:
        store.close()


if __name__ == "__main__":
    main()
