"""EXTERNAL dead-man's switch — is the daily pipeline still alive?

Every other alarm in this system is emitted BY the daily run, so none of them can fire when
the daily run is what died. "SILENCE = BROKEN" pushed that detection onto a human noticing an
absence, which people reliably do not do (a missing message looks exactly like a quiet day).

This checks the one artifact a live pipeline cannot fake: the timestamp of the last commit
touching the ledgers / equity log. Run it from a SEPARATE cloud routine, on its own schedule,
in a fresh session — the whole point is that it fails independently of what it watches.

OFF-PLATFORM since 2026-09-13: this runs as a GitHub Action (`.github/workflows/watchdog.yml`,
twice daily, stdlib only, no pip) — a different platform from the cloud routines it watches, so
a dead routine platform no longer kills the alarm with the pipeline. It also inherited the
push-log check the daily digest already runs (`digest._pushlog_section`): a due settle or read
push with no DELIVERED stamp is the failure a commit-watcher cannot see — the 09-11 settle
committed on time and pushed nothing, and nothing alarmed for 24 h. A red run emails the
owner by itself; the 🚨 Telegram push rides on the repo's TELEGRAM_* secrets. Silent when
healthy, by contract (🚨 means failure only).

OUTSIDE-ACTIVITY WATCH since 2026-10-16 (`--issues`, the 12:30 UTC run only): a third-party
issue opened 2026-09-03 sat unseen for six weeks, because nothing in this system read GitHub.
Any OPEN issue or PR authored by someone other than the owner, with no comment from the owner,
becomes one 📬 line, sent as its own message once a day until it is answered or closed. It is
not a failure, so it never uses 🚨 and never changes the exit code; the 🚨 check runs and sends
FIRST, so a slow or dead GitHub API can never mask or delay the alarm of record.

  python3 -m research.watchdog                      # print the verdict
  python3 -m research.watchdog --notify             # print + 🚨 Telegram push when anything is wrong
  python3 -m research.watchdog --notify --issues    # ... + 📬 for third-party items awaiting a reply
"""
import json
import logging
import os
import subprocess
import sys
import time
import urllib.request

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
OWNER = "guillearria"
API = "https://api.github.com"


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
                      f"(threshold {stale_h}h) — the daily settle routine is NOT "
                      f"running. Check the cloud schedule + cron.log.")
    return False, f"✅ watchdog: last ledger commit {hours:.0f}h ago (threshold {stale_h}h)"


def pushlog_actions() -> list[str]:
    """The digest's own delivery check, judged on the full calendar (no composing leg here) —
    the settle leg only since the read leg retired [ARC 5 #19]. A broken check is itself an
    alarm, never a silent pass."""
    try:
        from research import digest
        actions, _ = digest._pushlog_section("")
        return list(actions)
    except Exception as e:                      # import/parse death → say so, loudly
        return [f"push-log check could not run ({type(e).__name__}: {e})"]


def _gh(path: str):
    """GET one GitHub API path → parsed JSON. Uses the Action's GITHUB_TOKEN when present (the
    repo is public, so it also works unauthenticated at a lower rate limit). Raises on failure;
    issue_lines() is the one caller and turns any failure into a single line."""
    req = urllib.request.Request(f"{API}/{path}", headers={
        "Accept": "application/vnd.github+json", "User-Agent": "swing-lab-watchdog"})
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def waiting(items: list[dict], comments_of) -> list[str]:
    """📬 lines for OPEN items by someone else that the owner has not answered. PURE (testable):
    `comments_of(item)` is injected and only called when the item has comments at all."""
    out = []
    for it in items:
        who = (it.get("user") or {}).get("login", "")
        if who == OWNER or it.get("state", "open") != "open":
            continue
        if it.get("comments") and any((c.get("user") or {}).get("login") == OWNER
                                      for c in comments_of(it)):
            continue
        kind = "PR" if it.get("pull_request") else "issue"
        out.append(f"📬 {kind} #{it.get('number')} by @{who} (opened "
                   f"{str(it.get('created_at', ''))[:10]}), no reply from you: "
                   f"{str(it.get('title', ''))[:80]} {it.get('html_url', '')}")
    return out


def issue_lines() -> list[str]:
    """The outside-activity watch. Never raises: an API failure is ONE 📬 line naming it."""
    repo = os.getenv("GITHUB_REPOSITORY", f"{OWNER}/swing-lab")
    try:
        items = _gh(f"repos/{repo}/issues?state=open&per_page=50")
        return waiting(items, lambda it: _gh(f"repos/{repo}/issues/{it['number']}/comments"
                                             f"?per_page=100"))
    except Exception as e:
        return [f"📬 issue watch could not run ({type(e).__name__}) — check watchdog.yml "
                f"permissions and the GitHub API"]


def compose(stale: bool, msg: str, actions: list[str]) -> tuple[bool, str]:
    """(alarm, text). PURE. Commit staleness and undelivered pushes are ONE verdict: any
    failure is a 🚨; a healthy day is the single ✅ line."""
    lines = ([msg] if stale else []) + [f"🚨 WATCHDOG: {a}" for a in actions]
    return (True, "\n".join(lines)) if lines else (False, msg)


def run(argv: list[str]) -> int:
    stale, msg = verdict(last_commit_epoch(), time.time())
    alarm, text = compose(stale, msg, pushlog_actions())
    print(text)
    # Push ONLY on alarm: a healthy watchdog stays silent so it never competes with the
    # digest for attention. The digest is the daily proof-of-life; this is the exception.
    if alarm and "--notify" in argv:
        from research import notify
        notify.send(text)                       # fail-soft; the red exit is the alarm of record
    # The 📬 watch runs only AFTER the 🚨 above has been decided and sent, and never touches
    # the exit code: outside activity is news for the owner, not a failure of the pipeline.
    if "--issues" in argv:
        lines = issue_lines()
        if lines:
            print("\n".join(lines))
            if "--notify" in argv:
                from research import notify
                notify.send("\n".join(lines))
        else:
            print("📬 issue watch: nothing waiting")
    return 1 if alarm else 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(run(sys.argv[1:]))
