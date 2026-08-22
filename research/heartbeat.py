"""FALLBACK alive-signal — since 2026-07-10 daily.sh fires this ONLY when a step or the
📋 digest push failed (the digest is the clean day's one message; SILENCE = BROKEN holds).
The read leg gained the same parity 2026-08-11 (READ_LOOP step 7: `digest-read` on a
non-DELIVERED verdict) — before that a read whose push died produced total silence (08-10).

Settlements push their own 🚨 message from the settle paths; this is the proof-of-life
under them: ✅ ran clean (with ledger tallies, manual use), 🚨 a step failed (step names
arrive as argv from scripts/daily.sh). Fail-soft like all notify traffic — a lost
heartbeat never breaks the settle run.

  python3 -m research.heartbeat            # DRY RUN — prints the ✅ line, sends nothing
  python3 -m research.heartbeat --notify   # actually send the ✅ (manual use only)
  python3 -m research.heartbeat bets push  # send 🚨 naming the failed steps — ALWAYS sends
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
    """A 🚨 always sends; a ✅ needs --notify [2026-08-21].

    The asymmetry IS the contract: 🚨 means FAILURE ONLY and a ✅ success ping is a violation
    this repo has now logged twice (2026-08-05, and again 2026-08-21 when a session ran the
    bare command to LOOK at it and pushed "✅ settle ran clean" to the owner's phone). Bare
    invocation was a send while this module sat in the live command index next to `digest`,
    which needs --notify — same index, opposite behaviour, and the footgun fired.

    Gating the ✅ rather than every path is deliberate: an alarm that needs a flag is an alarm
    someone forgets to pass. Every automated caller is the 🚨 path and none of them change —
    daily.sh only runs this when $FAILS is non-empty, READ_LOOP step 7 passes `digest-read`.
    """
    day = datetime.now(timezone.utc).date().isoformat()
    # Flags are never step names: $FAILS arrives unquoted as argv, so an unfiltered "--notify"
    # would render as a failed step inside the 🚨 itself. Same idiom as digest.run.
    fails = [a for a in argv if not a.startswith("--")]
    text = msg(day, bets._load(), fails)
    print(text)
    if not fails and "--notify" not in argv:
        print("DRY RUN — no failed step named; pass --notify to send the ✅")
        return
    print("sent" if notify.send(text) else "NOT sent (see log)")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    run(sys.argv[1:])
