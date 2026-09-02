#!/usr/bin/env bash
# Daily SETTLE for swing_lab. The cloud /schedule "settle" routine is the PRIMARY path
# (laptop is often off); this same script runs there and locally. It scores matured forward
# bets + movers, then commits the updated ledgers so unattended runs land in the audit
# trail. Generation (new bets) is the separate "read" routine — see research/READ_LOOP.md.
set -uo pipefail
# Repo root resolved from THIS script's location — the cloud checkout path is not the laptop's
# (a hardcoded /home/... path exited 1 on every cloud run, so the PRIMARY settle path was silently
# dead and the routine improvised its own messages; fixed 2026-07-24).
cd "$(dirname "$(readlink -f "$0")")/.." || exit 1

# Single-flight guard [2026-09-01]: two copies of this script ran CONCURRENTLY on 08-26 and
# 09-01 — a cloud agent re-launched it while the first copy sat in the tool's background
# after the 120s timeout (this script takes 15–20 min and prints nothing to stdout) — two 📋
# digests, two commits, two writers on the same CSVs. The kernel releases the lock when the
# holder exits, so a crashed run can never wedge tomorrow's. Exit 0 on purpose: a refused
# duplicate is not a failure and must not raise a 🚨. Fails OPEN (guard skipped, run proceeds)
# if flock is missing or the lock path is unwritable — a guard that could fail closed would
# be a silent kill switch on the primary settle path.
if command -v flock >/dev/null 2>&1 && exec 9>>"${TMPDIR:-/tmp}/swing-lab-settle.lock" 2>/dev/null; then
  if ! flock -n 9; then
    echo "settle already running — another daily.sh holds the lock; this copy exits. Wait for the first one (pgrep -f scripts/daily.sh), then read cron.log."
    exit 0
  fi
fi

# Dependency guard [2026-08-08]: a COLD cloud container without python-dotenv kills the digest
# push AND the heartbeat on the same import (notify → config → dotenv) — no message, no alarm,
# no stamp (the 08-07 strand; FINDINGS 2026-08-08). The watchdog prompt already installs deps;
# the routine that matters most did not. Quiet no-op on a warm container.
python3 -c "import dotenv, requests, yfinance, pandas" 2>/dev/null \
  || pip install -q -r requirements.txt >> cron.log 2>&1

# Telegram (research/notify.py, fail-soft — needs TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID in
# the env): settlements push their own 🚨 message from the settle paths; the 📋 digest below
# is the ONE per-run message (and the proof-of-life — it exits nonzero on a failed send);
# the heartbeat fires ONLY as the 🚨 fallback when a step or the digest push failed.
# Contract unchanged: a scheduled day with ZERO messages = the system is down, never "no news".
FAILS=""
python3 -m research.bets settle           >> cron.log 2>&1 || FAILS="$FAILS bets"
python3 -m research.movers settle         >> cron.log 2>&1 || FAILS="$FAILS movers"  # score take+skip fwd vs SPY [W3]
# Resolve working orders against real bars BEFORE the digest composes — otherwise a limit that
# filled this morning is still advertised as "no fill yet" in the very push that reports it.
python3 -m research.orders check          >> cron.log 2>&1 || FAILS="$FAILS orders"
python3 -m research.book mark             >> cron.log 2>&1 || FAILS="$FAILS book"  # display only, writes nothing
# One row per day on the equity curve — the book was judged point-in-time forever (no path,
# no drawdown). It doubles as the liveness clock the digest reads: a stale newest date means
# THIS script stopped running.
python3 -m research.book snapshot         >> cron.log 2>&1 || FAILS="$FAILS snapshot"
# The ONE actionable push (📋 what CHANGED since the last push + DO-NOW + state) — the
# "when to come back" surface [W4].
# Exits nonzero when the Telegram send fails, so a lost push lands in $FAILS.
python3 -m research.digest --notify       >> cron.log 2>&1 || FAILS="$FAILS digest"
# Regenerate the public dashboard page from the just-settled ledgers [P7a] — a GENERATED,
# committed surface (docs/index.html); uncommitted it would drift from the ledgers it renders.
# Stdlib + no network, so a failure here is a code bug, not a feed outage.
python3 -m research.site                  >> cron.log 2>&1 || FAILS="$FAILS site"
# The X pulse [P7b] — DETERMINISTIC AUTOPOST BY POLICY (BACKLOG P7b, 2026-08-15): fires only
# when this run scored a verdict row vs git HEAD, so it MUST run BEFORE push_ledgers commits
# (same ordering contract as the digest's 🏁 milestone check — reorder and the gate goes
# silent). Quiet no-op until the X_* env keys exist; ≤1 POSTED/UTC-day cap inside.
python3 -m research.pulse --post          >> cron.log 2>&1 || FAILS="$FAILS pulse"

# Persist any newly-scored rows (no-op commit is skipped). Forward verdicts are the audit trail.
# Pushes to master so the cloud routine's work survives the ephemeral checkout (laptop-off-safe).
# book.csv is tracked in git (private repo) but mark doesn't write it — nothing to commit here.
# book_equity.csv IS written (by snapshot above) and committed, so the curve survives the
# ephemeral checkout and every run leaves a dated trace for the watchdog to read.
# _feed_status.json MUST be committed too: cloud checkouts are ephemeral, so an uncommitted
# last_ok resets every run and the stale-feed alarm could never fire.
# orders.csv carries the working-order state (pending/filled/expired). Uncommitted, an ephemeral
# cloud checkout would resurrect every order it just resolved and re-nag the human forever.
# push_log.csv is the delivery stamp the digest writes on every --notify: committed, it lets
# the NEXT delivered message flag a settle 📋 that died in transport (invisible to the
# commit-watching watchdog — observed two consecutive nights, 08-05 + 08-06).
LEDGERS="research/bets_catalogue.csv research/movers_ledger.csv research/book_equity.csv research/orders.csv research/data/_feed_status.json research/data/push_log.csv research/data/pulse_log.csv docs/index.html"
# The commit/rebase/push logic moved to its own script so it could be TESTED — inline here it
# never was, and on 2026-07-31 a failed push silently destroyed a whole settle run with the
# container. push_ledgers.sh verifies the commit actually reached origin/master and, when it
# did not, parks it on a settle-backup/* ref that outlives this checkout.
# ${OUT:-push} — never let a FAILED push contribute an EMPTY word [2026-08-21]. FAILS then
# held only a space: `[ -n " " ]` passes, but unquoted $FAILS word-splits to NO argv, and
# argless heartbeat.py sends "✅ settle ran clean" — a broken run reporting success, the
# exact contract violation logged on 2026-08-05 (🚨 means FAILURE ONLY).
OUT=$(scripts/push_ledgers.sh $LEDGERS 2>>cron.log) || FAILS="$FAILS ${OUT:-push}"

# 🚨 fallback proof-of-life — fires ONLY when a step or the digest push failed
# ($FAILS unquoted on purpose: step names become argv). Clean day = digest is the message.
if [ -n "$FAILS" ]; then
  python3 -m research.heartbeat $FAILS >> cron.log 2>&1
fi
