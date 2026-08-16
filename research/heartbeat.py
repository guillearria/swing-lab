"""FALLBACK alive-signal — since 2026-07-10 daily.sh fires this ONLY when a step or the
📋 digest push failed (the digest is the clean day's one message; SILENCE = BROKEN holds).
The read leg gained the same parity 2026-08-11 (READ_LOOP step 7: `digest-read` on a
non-DELIVERED verdict) — before that a read whose push died produced total silence (08-10).

Settlements push their own 🚨 message from the settle paths; this is the proof-of-life
under them: ✅ ran clean (with ledger tallies, manual use), 🚨 a step failed (step names
arrive as argv from scripts/daily.sh). Fail-soft like all notify traffic — a lost
heartbeat never breaks the settle run.

  python3 -m research.heartbeat            # send ✅ alive + tallies
  python3 -m research.heartbeat bets push  # send 🚨 naming the failed steps
"""
import sys
from datetime import datetime, timezone

from research import bets, notify


def msg(day: str, bet_rows: list[dict], fails: list[str]) -> str:
    """One-line daily status. PURE (testable)."""
    gc = sum(1 for r in bet_rows if r["status"] == "closed")
    go = sum(1 for r in bet_rows if r["status"] == "open")
    body = f"general {gc} closed / {go} open"
    if fails:
        # "RUN", not "SETTLE" [2026-08-11]: the read leg fires this too now, and a 🚨 that
        # names the wrong routine sends the human to the wrong cron.log.
        return f"🚨 RUN FAILURE {day} — failed: {', '.join(fails)} — check cron.log | {body}"
    return f"✅ settle ran clean {day} | {body}"


def run(argv: list[str]) -> None:
    day = datetime.now(timezone.utc).date().isoformat()
    text = msg(day, bets._load(), argv)
    print(text)
    print("sent" if notify.send(text) else "NOT sent (see log)")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    run(sys.argv[1:])
