import copy
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from backend.database.collection_store import CollectionStore
from backend.services.buffer_service import cleanup_buffer


ROOT = Path(__file__).resolve().parents[2]
PRICES = {"open": 100, "high": 102, "low": 99, "close": 101, "volume": 500}
NOW = "2026-10-20T16:00:00Z"


class BufferTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "sample.sqlite3"
        self.store = CollectionStore(self.path)
        self.settings = json.loads((ROOT / "config/collection.json").read_text())

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def add(self, day=5, ticker="NVDA", **kwargs):
        return self.store.add_bar(ticker, f"2026-10-{day:02d}T14:30:00Z", PRICES, **kwargs)

    def covered(self, ticker="NVDA", source="sample-news", start="2026-10-01T00:00:00Z", end=NOW):
        self.store.record_news_scan(ticker, source, start, end)

    def clean(self, apply=False, now=NOW):
        return cleanup_buffer(self.store, "NVDA", now, self.settings, apply=apply)

    def test_identical_ingestion_is_idempotent(self):
        self.assertTrue(self.add())
        self.assertFalse(self.add())
        self.assertEqual(self.store.count(), 1)

    def test_equivalent_timezone_timestamps_are_one_observation(self):
        self.add()
        inserted = self.store.add_bar("nvda", "2026-10-05T10:30:00-04:00", PRICES)
        self.assertFalse(inserted)
        self.assertEqual(self.store.count(), 1)

    def test_first_discovery_time_survives_replay(self):
        self.add(received_at="2026-10-05T14:31:00Z")
        self.add(received_at=NOW)
        received = self.store.db.execute("SELECT received_at FROM observations").fetchone()[0]
        self.assertTrue(received.startswith("2026-10-05T14:31:00"))

    def test_conflicting_price_does_not_replace_history(self):
        self.add()
        changed = {**PRICES, "close": 102}
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            self.store.add_bar("NVDA", "2026-10-05T14:30:00Z", changed)
        payload = self.store.db.execute("SELECT ohlcv FROM observations").fetchone()[0]
        self.assertEqual(json.loads(payload)["close"], 101)
        self.assertEqual(self.store.count(), 1)

    def test_provider_conflict_does_not_mix_feeds(self):
        self.add()
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            self.add(provider="another-feed")

    def test_price_bases_are_separate_observations(self):
        self.add()
        self.add(price_basis="adjusted")
        self.assertEqual(self.store.count(), 2)

    def test_rejects_naive_timestamps_and_bad_prices(self):
        with self.assertRaises(ValueError):
            self.store.add_bar("NVDA", "2026-10-05T14:30:00", PRICES)
        for bad in [float("nan"), float("inf"), -1, 999]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.store.add_bar("NVDA", "2026-10-05T14:30:00Z", {**PRICES, "close": bad})
        self.assertEqual(self.store.count(), 0)

    def test_rejects_unsupported_interval_and_non_aligned_bars(self):
        with self.assertRaises(ValueError):
            self.add(interval="5m")
        with self.assertRaises(ValueError):
            self.store.add_bar("NVDA", "2026-10-05T14:30:01Z", PRICES)

    def test_missing_coverage_blocks_cleanup(self):
        self.add()
        result = self.clean(apply=True)
        self.assertIsNotNone(result["blocked"])
        self.assertEqual(self.store.count(), 1)

    def test_failure_blocks_deletion_without_advancing_coverage(self):
        self.add()
        self.covered()
        previous = self.store.db.execute("SELECT through_at FROM news_coverage").fetchone()[0]
        self.store.record_news_failure("NVDA", "sample-news")
        result = self.clean(apply=True)
        self.assertIsNotNone(result["blocked"])
        self.assertEqual(self.store.count(), 1)
        self.assertEqual(previous, self.store.db.execute("SELECT through_at FROM news_coverage").fetchone()[0])

    def test_incomplete_recovery_does_not_clear_outage(self):
        self.add()
        self.covered()
        self.store.record_news_failure("NVDA", "sample-news")
        with self.assertRaises(ValueError):
            self.covered(end="2026-10-10T00:00:00Z")
        self.assertIsNotNone(self.clean(apply=True)["blocked"])
        self.assertEqual(self.store.count(), 1)

    def test_full_successful_rescan_unblocks_cleanup(self):
        self.add()
        self.covered()
        self.store.record_news_failure("NVDA", "sample-news")
        self.covered()
        self.assertEqual(self.clean(apply=True)["deleted"], 1)

    def test_every_configured_source_must_be_covered(self):
        self.add()
        self.covered()
        self.settings["required_news_sources"].append("second-source")
        self.assertIsNotNone(self.clean(apply=True)["blocked"])
        self.covered(source="second-source")
        self.assertEqual(self.clean(apply=True)["deleted"], 1)

    def test_scan_cannot_skip_a_gap(self):
        self.covered(end="2026-10-06T00:00:00Z")
        with self.assertRaisesRegex(ValueError, "gap"):
            self.covered(start="2026-10-07T00:00:00Z")
        end = self.store.db.execute("SELECT through_at FROM news_coverage").fetchone()[0]
        self.assertTrue(end.startswith("2026-10-06"))

    def test_insufficient_history_and_future_news_coverage_prevent_deletion(self):
        self.add()
        self.covered(start="2026-10-04T00:00:00Z", end="2026-10-08T00:00:00Z")
        self.assertEqual(self.clean(apply=True)["deleted"], 0)
        # Complete the past, but still miss the last possible event day's end.
        self.covered(start="2026-10-01T00:00:00Z", end="2026-10-09T03:59:00Z")
        self.assertEqual(self.clean(apply=True)["deleted"], 0)
        self.covered(start="2026-10-09T03:59:00Z", end="2026-10-09T04:00:00Z")
        self.assertEqual(self.clean(apply=True)["deleted"], 1)

    def test_buffer_preserves_five_full_days_and_today(self):
        for day in (14, 15, 19, 20):
            self.add(day)
        self.covered()
        result = self.clean(apply=True)
        self.assertEqual([r["timestamp"][:10] for r in result["eligible"]], ["2026-10-14"])
        self.assertEqual(self.store.count(), 3)

    def test_dry_run_does_not_delete(self):
        self.add()
        self.covered()
        result = self.clean()
        self.assertEqual(len(result["eligible"]), 1)
        self.assertEqual(result["deleted"], 0)
        self.assertEqual(self.store.count(), 1)

    def test_overlapping_holds_share_one_bar(self):
        self.add()
        self.covered()
        self.store.protect_range("a", "NVDA", "2026-10-04T00:00:00Z", "2026-10-06T00:00:00Z")
        self.store.protect_range("b", "NVDA", "2026-10-05T00:00:00Z", "2026-10-07T00:00:00Z")
        self.store.protect_range("a", "NVDA", "2026-10-04T00:00:00Z", "2026-10-06T00:00:00Z")
        self.assertEqual(self.clean(apply=True)["deleted"], 0)
        self.assertEqual(self.store.count(), 1)
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM retention_holds").fetchone()[0], 2)

    def test_hold_created_before_bar_arrives_protects_it(self):
        self.store.protect_range("future", "NVDA", "2026-10-05T00:00:00Z", "2026-10-06T00:00:00Z")
        self.add()
        self.covered()
        self.assertEqual(self.clean(apply=True)["deleted"], 0)

    def test_hold_cannot_shrink_or_change_ticker(self):
        self.add()
        self.covered()
        self.store.protect_range("a", "NVDA", "2026-10-04T00:00:00Z", "2026-10-07T00:00:00Z")
        self.store.protect_range("a", "NVDA", "2026-10-06T00:00:00Z", "2026-10-07T00:00:00Z")
        self.assertEqual(self.clean(apply=True)["deleted"], 0)
        with self.assertRaises(ValueError):
            self.store.protect_range("a", "AAPL", "2026-10-04T00:00:00Z", "2026-10-07T00:00:00Z")

    def test_other_tickers_are_not_deleted(self):
        self.add(ticker="AAPL")
        self.add(ticker="NVDA")
        self.covered()
        self.assertEqual(self.clean(apply=True)["deleted"], 1)
        self.assertEqual(self.store.db.execute("SELECT ticker FROM observations").fetchone()[0], "AAPL")

    def test_transaction_rolls_back_partial_cleanup(self):
        self.add(5)
        self.add(6)
        self.covered()
        self.store.db.execute("""
            CREATE TEMP TRIGGER fail_second BEFORE DELETE ON observations
            WHEN OLD.timestamp LIKE '2026-10-06%'
            BEGIN SELECT RAISE(ABORT, 'simulated interruption'); END
        """)
        with self.assertRaises(sqlite3.IntegrityError):
            self.clean(apply=True)
        self.assertEqual(self.store.count(), 2)

    def test_reopen_preserves_data_holds_and_coverage(self):
        self.add()
        self.covered()
        self.store.protect_range("a", "NVDA", "2026-10-04T00:00:00Z", "2026-10-06T00:00:00Z")
        self.store.close()
        self.store = CollectionStore(self.path)
        self.assertEqual(self.store.count(), 1)
        self.assertFalse(self.add())
        self.assertEqual(self.clean(apply=True)["deleted"], 0)

    def test_calendar_cutoff_uses_exchange_timezone_across_dst(self):
        self.store.add_bar("NVDA", "2026-10-29T03:59:00Z", PRICES)
        self.store.add_bar("NVDA", "2026-10-29T04:00:00Z", PRICES)
        self.covered(end="2026-11-03T16:00:00Z")
        result = self.clean(apply=True, now="2026-11-03T16:00:00Z")
        self.assertEqual(len(result["eligible"]), 1)
        self.assertTrue(result["eligible"][0]["timestamp"].startswith("2026-10-29T03:59"))
        self.assertEqual(self.store.count(), 1)

    def test_bad_config_cannot_delete_data(self):
        self.add()
        self.covered()
        for key, value in [("before_days", -1), ("grace_days", 1.5), ("day_mode", "trading"),
                           ("required_news_sources", []), ("required_news_sources", "sample-news")]:
            settings = copy.deepcopy(self.settings)
            settings[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                cleanup_buffer(self.store, "NVDA", NOW, settings, apply=True)
        self.assertEqual(self.store.count(), 1)

    def test_demo_runs_twice_in_preview_and_apply_modes(self):
        env = {**os.environ, "LOCALAPPDATA": self.temp.name}
        for flags in [[], [], ["--apply-cleanup"], ["--apply-cleanup"]]:
            result = subprocess.run([sys.executable, str(ROOT / "scripts/demo_collection.py"), *flags],
                                    env=env, cwd=self.temp.name, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("After replay: 3 bars (before replay: 3)", result.stdout)
            self.assertIn("NVDA eligible dates: ['2026-10-05']", result.stdout)
            self.assertIn("Remaining bars: " + ("2" if flags else "3"), result.stdout)


if __name__ == "__main__":
    unittest.main()
