"""NYSE holidays + trading-day arithmetic — the ONE place the exchange calendar lives.

Every "weekday" count in the repo silently assumed there are no holidays. Measured cost on
the week after Labor Day 2026: the feed-staleness check fired a FALSE ⚠️ on BOTH legs on
09-08 (bars "2 weekdays behind the last scan" — one of the two was the holiday), the 📈
"next scores" line ran a day early for every open bet (TWLO "Fri 09-11" for a bet whose 21st
bar was Mon 09-14), and the STUCK buffer had to absorb the drift. In a channel where the
absence of ⚠️ IS the all-clear, a false alarm nine times a year is a contract violation, not
a nuisance. Exchange holidays are a fixed, published list — they belong in code, not in an
alarm's hedge text.

Maintenance: extend HOLIDAYS before each new year (NYSE publishes 2–3 years ahead). A year
with no entries degrades to the old weekday-only behaviour — conservative, never broken.
Stdlib only: the digest and bets stay dependency-light. Early closes do not matter here (a
half session is still a completed bar).
"""
from datetime import date, datetime, timedelta, timezone

HOLIDAYS = frozenset(map(date.fromisoformat, (
    # 2026: New Year · MLK · Presidents · Good Friday · Memorial · Juneteenth · Jul 4 (obs Fri)
    #       · Labor · Thanksgiving · Christmas
    "2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25", "2026-06-19",
    "2026-07-03", "2026-09-07", "2026-11-26", "2026-12-25",
    # 2027: same set; Juneteenth obs Fri 06-18, Jul 4 obs Mon 07-05, Christmas obs Fri 12-24
    "2027-01-01", "2027-01-18", "2027-02-15", "2027-03-26", "2027-05-31", "2027-06-18",
    "2027-07-05", "2027-09-06", "2027-11-25", "2027-12-24",
)))


def is_trading_day(d: date) -> bool:
    return d.weekday() < 5 and d not in HOLIDAYS


def count(start: date, end: date) -> int:
    """Trading days in [start, end) — the weekday count minus the holidays inside. PURE."""
    n, d = 0, start
    while d < end:
        n += is_trading_day(d)
        d += timedelta(days=1)
    return n


def add(start: date, n: int) -> date:
    """The date `n` trading days after `start` — the weekday walk, holiday-aware. PURE."""
    d = start
    while n > 0:
        d += timedelta(days=1)
        if is_trading_day(d):
            n -= 1
    return d


def can_have_matured(day: str, horizon: int, today: date | None = None) -> bool:
    """Could a row pre-registered on `day` (ISO) have `horizon` COMPLETE bars strictly after it
    and strictly before `today`? Mirrors bets._score's two gates exactly (entry bar AFTER the
    pre-registration day; exit bar dated BEFORE today), so a settle loop can skip the price
    fetch for every row that cannot score yet — the [OPS 2026-09-02] proposal, built 09-13:
    both loops re-fetched EVERY unmatured row every day (4,668 chart calls, 17–20 min/run) for
    the handful that could actually mature. Conservative by construction: an unlisted closure
    makes the count LARGER, so the row is fetched and _score says None — never a missed settle.
    `today` is injected for tests; it defaults to the UTC date, the same clock _score uses."""
    today = today or datetime.now(timezone.utc).date()
    return count(date.fromisoformat(day) + timedelta(days=1), today) >= horizon
