"""Conservative calendar-day cleanup for the sample collection database."""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from backend.database.collection_store import utc


def cleanup_buffer(store, ticker, now, settings, *, apply=False):
    # Only sample-tested calendar-day mode is enabled at this stage.
    if settings.get("day_mode") != "calendar":
        raise ValueError("Trading-day mode needs an exchange calendar in Step 5.")
    before = settings["before_days"]
    after = settings["after_days"]
    grace = settings["grace_days"]
    if any(type(n) is not int or n < 0 for n in (before, after, grace)):
        raise ValueError("Retention days must be non-negative integers.")
    sources = settings["required_news_sources"]
    if not isinstance(sources, list) or not sources or not all(
        isinstance(source, str) and source.strip() for source in sources
    ):
        raise ValueError("At least one required news source is necessary.")
    ticker = ticker.upper()
    zone = ZoneInfo(settings["exchange_timezone"])
    today = datetime.fromisoformat(utc(now)).astimezone(zone).date()
    cutoff_date = today - timedelta(days=before + grace)

    def midnight(day):
        return utc(datetime.combine(day, time.min, tzinfo=zone).isoformat())

    # Hold the write lock while checking protections and applying deletions.
    with store.transaction():
        coverage = []
        for source in set(sources):
            row = store.db.execute("""
                SELECT * FROM news_coverage WHERE ticker=? AND source=?
            """, (ticker, source)).fetchone()
            if row is None or not row["healthy"]:
                return {"eligible": [], "deleted": 0,
                        "blocked": f"News coverage unavailable: {source}"}
            coverage.append(row)

        rows = store.db.execute("""
            SELECT o.id, o.timestamp FROM observations AS o
            WHERE o.ticker=? AND o.timestamp < ?
              AND NOT EXISTS (
                SELECT 1 FROM retention_holds AS h
                WHERE h.ticker=o.ticker
                  AND h.start_at<=o.timestamp AND o.timestamp<h.end_at
              )
            ORDER BY o.timestamp
        """, (ticker, midnight(cutoff_date))).fetchall()

        eligible = []
        for row in rows:
            day = datetime.fromisoformat(row["timestamp"]).astimezone(zone).date()
            # All event dates that could protect this bar must have been scanned.
            required_start = midnight(day - timedelta(days=after))
            required_end = midnight(day + timedelta(days=before + 1))
            if all(c["start_at"] <= required_start
                   and c["through_at"] >= required_end for c in coverage):
                eligible.append(dict(row))

        if apply:
            store.db.executemany(
                "DELETE FROM observations WHERE id=?",
                [(row["id"],) for row in eligible],
            )
        return {"eligible": eligible, "deleted": len(eligible) if apply else 0,
                "blocked": None}
