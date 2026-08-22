"""EXTERNAL dead-man's switch — is the daily pipeline still alive?

Every other alarm in this system is emitted BY the daily run, so none of them can fire when
the daily run is what died. "SILENCE = BROKEN" pushed that detection onto a human noticing an
absence, which people reliably do not do (a missing message looks exactly like a quiet day).

This checks the one artifact a live pipeline cannot fake: the timestamp of the last commit
touching the ledgers / equity log. Run it from a SEPARATE cloud routine, on its own schedule,
in a fresh session — the whole point is that it fails independently of what it watches.

HONEST LIMIT: this narrows the blind spot, it does not close it. The watchdog only reports
while the watchdog itself runs; if the scheduling platform dies, both go with it and nothing
here says so. Only an off-platform monitor would cover that, and we have not bought one.

  python3 -m research.watchdog             # print the verdict
  python3 -m research.watchdog --notify    # print + 🚨 Telegram push when stale
"""
import logging
import subprocess
import sys
import time

log = logging.getLogger(__name__)
# push_log.csv, NOT book_equity.csv [2026-08-21]: the equity curve was the only watched file
# written EVERY day including weekends, and `book retire` (2026-08-18) froze it — snapshot is a
# no-op on a retired book. The other two are written only when a trading-day window matures, so
# the watched set went stale across every weekend (~44h vs the 36h bar) and this switch would
# have cried wolf each Sunday while both routines ran normally. push_log.csv is appended by
# digest._log_push on EVERY delivered push and committed by daily.sh — the daily heartbeat the
# retirement removed without replacing.
WATCHED = ("research/bets_catalogue.csv", "research/movers_ledger.csv",
           "research/data/push_log.csv")
STALE_H = 36    # settle runs daily; 36h tolerates one missed run + a weekend edge, not two


def last_commit_epoch(paths=WATCHED) -> int | None:
    """UTC epoch of the newest commit touching any watched ledger, or None if unknown."""
    try:
        out = subprocess.run(("git", "log", "-1", "--format=%ct", "--", *paths),
                             capture_output=True, text=True, timeout=15, check=True).stdout.strip()
        return int(out) if out else None
    except Exception as e:
        log.debug("watchdog: git log failed (%s)", e)
        return None


def verdict(last_epoch: int | None, now_epoch: float, stale_h: int = STALE_H) -> tuple[bool, str]:
    """(is_stale, message). PURE (testable) — all clock/git I/O stays in the caller."""
    if last_epoch is None:
        return True, ("🚨 WATCHDOG: cannot read the ledger history at all — "
                      "the checkout or git itself is broken")
    hours = (now_epoch - last_epoch) / 3600
    if hours > stale_h:
        return True, (f"🚨 WATCHDOG: no ledger commit for {hours:.0f}h "
                      f"(threshold {stale_h}h) — the daily settle/read routines are NOT "
                      f"running. Check the cloud schedule + cron.log.")
    return False, f"✅ watchdog: last ledger commit {hours:.0f}h ago (threshold {stale_h}h)"


def run(argv: list[str]) -> int:
    stale, msg = verdict(last_commit_epoch(), time.time())
    print(msg)
    # Push ONLY when stale: a healthy watchdog stays silent so it never competes with the
    # digest for attention. The digest is the daily proof-of-life; this is the exception.
    if stale and "--notify" in argv:
        from research import notify
        if not notify.send(msg):
            return 1
    return 1 if stale else 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(run(sys.argv[1:]))
