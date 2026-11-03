"""Step 2: local sample storage. No provider requests or story classification."""

import json
import math
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def utc(value):
    moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise ValueError("Timestamps must include a timezone, e.g. ...Z.")
    return moment.astimezone(timezone.utc).isoformat(timespec="microseconds")


class CollectionStore:
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, isolation_level=None, timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY,
                ticker TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                interval TEXT NOT NULL,
                price_basis TEXT NOT NULL,
                provider TEXT NOT NULL,
                ohlcv TEXT NOT NULL,
                received_at TEXT NOT NULL,
                UNIQUE(ticker, timestamp, interval, price_basis)
            );
            CREATE TABLE IF NOT EXISTS retention_holds (
                hold_id TEXT PRIMARY KEY,
                ticker TEXT NOT NULL,
                start_at TEXT NOT NULL,
                end_at TEXT NOT NULL,
                CHECK(start_at < end_at)
            );
            CREATE INDEX IF NOT EXISTS holds_by_ticker
                ON retention_holds(ticker, start_at, end_at);
            CREATE TABLE IF NOT EXISTS news_coverage (
                ticker TEXT NOT NULL,
                source TEXT NOT NULL,
                start_at TEXT NOT NULL,
                through_at TEXT NOT NULL,
                healthy INTEGER NOT NULL CHECK(healthy IN (0, 1)),
                CHECK(start_at < through_at),
                PRIMARY KEY(ticker, source)
            );
        """)

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise

    def add_bar(self, ticker, timestamp, values, *, provider="sample",
                interval="1m", price_basis="unadjusted", received_at=None):
        # This first version accepts finalized one-minute bars only.
        if interval != "1m":
            raise ValueError("Step 2 supports finalized 1m sample bars only.")
        ticker = ticker.strip().upper()
        if not ticker or not provider or price_basis not in {"unadjusted", "adjusted"}:
            raise ValueError("Invalid ticker, provider, or price basis.")
        timestamp = utc(timestamp)
        moment = datetime.fromisoformat(timestamp)
        if moment.second or moment.microsecond:
            raise ValueError("Bar timestamps must be aligned to a minute.")
        names = ("open", "high", "low", "close", "volume")
        prices = {name: float(values[name]) for name in names}
        if not all(math.isfinite(value) for value in prices.values()):
            raise ValueError("OHLCV values must be finite.")
        if not (0 < prices["low"] <= min(prices["open"], prices["close"])
                <= max(prices["open"], prices["close"]) <= prices["high"]
                and prices["volume"] >= 0):
            raise ValueError("Invalid OHLCV values.")
        payload = json.dumps(prices, sort_keys=True, allow_nan=False)
        key = (ticker, timestamp, interval, price_basis)
        received = utc(received_at or datetime.now(timezone.utc).isoformat())
        with self.transaction():
            previous = self.db.execute("""
                SELECT provider, ohlcv FROM observations
                WHERE ticker=? AND timestamp=? AND interval=? AND price_basis=?
            """, key).fetchone()
            if previous:
                if previous["provider"] != provider or previous["ohlcv"] != payload:
                    raise ValueError("Conflicting bar; revision handling comes later.")
                return False
            self.db.execute("""
                INSERT INTO observations
                (ticker,timestamp,interval,price_basis,provider,ohlcv,received_at)
                VALUES (?,?,?,?,?,?,?)
            """, (*key, provider, payload, received))
        return True

    def protect_range(self, hold_id, ticker, start, end):
        # Manual sample holds; automatic story windows come in Step 5.
        ticker, start, end = ticker.upper(), utc(start), utc(end)
        if not hold_id or start >= end:
            raise ValueError("A hold needs an ID and a valid time range.")
        with self.transaction():
            previous = self.db.execute(
                "SELECT ticker FROM retention_holds WHERE hold_id=?", (hold_id,)
            ).fetchone()
            if previous and previous["ticker"] != ticker:
                raise ValueError("A hold ID cannot change its ticker.")
            self.db.execute("""
                INSERT INTO retention_holds VALUES (?,?,?,?)
                ON CONFLICT(hold_id) DO UPDATE SET
                    start_at=MIN(start_at, excluded.start_at),
                    end_at=MAX(end_at, excluded.end_at)
            """, (hold_id, ticker, start, end))

    def record_news_scan(self, ticker, source, start, through):
        # Call only after ALL pages are collected AND classified for this range.
        ticker, start, through = ticker.upper(), utc(start), utc(through)
        if not source or start >= through:
            raise ValueError("Invalid completed news scan.")
        with self.transaction():
            previous = self.db.execute("""
                SELECT * FROM news_coverage WHERE ticker=? AND source=?
            """, (ticker, source)).fetchone()
            if previous:
                if start > previous["through_at"] or through < previous["start_at"]:
                    raise ValueError("Coverage has a gap; recover it before advancing.")
                if not previous["healthy"] and (
                    start > previous["through_at"] or through < previous["through_at"]
                ):
                    raise ValueError("Recovery must scan through the old checkpoint.")
                start = min(start, previous["start_at"])
                through = max(through, previous["through_at"])
            self.db.execute("""
                INSERT INTO news_coverage VALUES (?,?,?,?,1)
                ON CONFLICT(ticker,source) DO UPDATE SET
                    start_at=excluded.start_at,
                    through_at=excluded.through_at, healthy=1
            """, (ticker, source, start, through))

    def record_news_failure(self, ticker, source):
        # A missing source row also blocks cleanup, so no row needs inventing.
        with self.transaction():
            self.db.execute("""
                UPDATE news_coverage SET healthy=0 WHERE ticker=? AND source=?
            """, (ticker.upper(), source))

    def count(self):
        return self.db.execute("SELECT COUNT(*) FROM observations").fetchone()[0]

    def close(self):
        self.db.close()
