#!/usr/bin/env bash
# Land the settled ledgers on origin/master — or PARK them somewhere that outlives this
# container. Called by scripts/daily.sh; usage: push_ledgers.sh <path> [path...]
#
# WHY THIS IS ITS OWN FILE: on 2026-07-31 the settle run committed 1b014cc (six Telegram
# delivery stamps + a day of the equity curve + 25 scored movers rows), the push failed, and
# the ephemeral cloud checkout was destroyed. The work survived only by accident, on the
# harness's own session branch, and master ran two days without it while nothing said so.
# The old code reacted to a failed push by appending a word to $FAILS and letting the
# container die on top of the commit. "Commit incrementally" is worthless if the commit dies
# with the container. This logic lives here, not inline in daily.sh, because inline it was
# untestable — and untestable is how it shipped (see research/tests/test_daily_push.py).
#
# Contract: exit 0 == the commit is provably reachable from origin/master. On any other
# outcome, exit 1 and print ONE word on stdout for daily.sh's $FAILS:
#   add            staging failed (e.g. a LEDGERS path does not exist) — nothing staged
#   commit         the commit itself failed — nothing was created
#   push-stranded  work is SAFE on origin at settle-backup/<date>-<sha>, needs a human merge
#   push-LOST      the remote is unreachable; the work exists ONLY in this container
set -uo pipefail
LEDGERS="$*"

# stdout is a STATUS CHANNEL, not a log. daily.sh does `OUT=$(push_ledgers.sh …)` and then
# `FAILS="$FAILS $OUT"`, and $FAILS is passed to heartbeat.py as ARGV — so a stray line of
# `git commit` chatter would become fake step names in a 🚨 alert. Send every command's stdout
# to stderr (daily.sh routes that to cron.log, where it belongs) and reserve fd 3 for the one
# word this script is allowed to say.
exec 3>&1 1>&2
say() { echo "$1" >&3; }

# Stage BEFORE testing for changes. `git diff --quiet` only sees TRACKED files, so a
# brand-new ledger (a first-of-its-kind cache/day file) looked like "nothing to do" and was
# never committed at all. Staging first and diffing --cached counts new files too.
git add -A -- $LEDGERS || { say add; exit 1; }
git diff --cached --quiet -- $LEDGERS && exit 0        # genuinely nothing to persist

git commit -m "chore: settle forward bets ($(date -u +%Y-%m-%d))" || { say commit; exit 1; }

# Two attempts. A non-fast-forward here is usually a real race (the read routine commits on
# its own schedule) and a fresh fetch+rebase clears it. NEVER force: a ledger is evidence.
# A rebase CONFLICT will not self-heal, so break out and let the backup path take it — an
# unattended auto-merge of an append-only evidence file is worse than a stranded commit.
for _ in 1 2; do
  git fetch origin || continue
  git rebase origin/master || { git rebase --abort; break; }
  git push origin HEAD:master && break
done

# VERIFY rather than trust the exit code. The only question that matters is whether this
# commit is reachable from the remote — not whether some command returned 0.
git fetch origin
git merge-base --is-ancestor HEAD origin/master && exit 0

# Park it. Dated AND sha-suffixed so a re-run reuses the same ref instead of littering, while
# two genuinely different commits still get two refs. Never one shared force-pushed ref —
# that would clobber an earlier strand nobody has recovered yet.
BACKUP="settle-backup/$(date -u +%Y%m%d)-$(git rev-parse --short HEAD)"
if git push origin "HEAD:refs/heads/$BACKUP"; then say push-stranded; else say push-LOST; fi
exit 1
