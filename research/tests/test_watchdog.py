"""Guard the external dead-man's switch: the staleness decision is pure and conservative."""
import time

from research import watchdog as W


def test_fresh_commit_is_not_stale():
    stale, msg = W.verdict(int(time.time()) - 3600, time.time())
    assert stale is False and msg.startswith("✅") and "1h ago" in msg


def test_stale_commit_fires():
    stale, msg = W.verdict(int(time.time()) - 72 * 3600, time.time())
    assert stale is True and msg.startswith("🚨")
    assert "72h" in msg and "NOT" in msg


def test_boundary_is_exclusive():
    """Exactly at the threshold is still healthy — a routine that lands on the hour must not
    flap between alive and dead."""
    now = float(int(time.time()))                # exact seconds: the boundary is what's under test
    assert W.verdict(int(now - W.STALE_H * 3600), now)[0] is False
    assert W.verdict(int(now - (W.STALE_H + 1) * 3600), now)[0] is True


def test_unreadable_history_is_treated_as_broken():
    """No git / no history = we cannot prove the pipeline is alive, so we must not claim it
    is. Fail LOUD, never silently pass."""
    stale, msg = W.verdict(None, time.time())
    assert stale is True and "cannot read" in msg


def test_watched_set_holds_a_file_written_every_day_including_weekends():
    """The dead-man's switch is only as live as the most frequently written file it watches.

    `book_equity.csv` was that file until `book retire` (2026-08-18) made `snapshot` a no-op and
    froze it. The other two ledgers are written only when a trading-day window matures, so the
    watched set aged across every weekend (~44h against STALE_H=36) and this switch would have
    fired a FALSE 🚨 each Sunday while both routines ran normally — alarm fatigue on the one
    alarm that cannot be emitted by the run it watches. push_log.csv is appended by
    digest._log_push on EVERY delivered push and committed by daily.sh, weekends included.
    """
    assert "research/data/push_log.csv" in W.WATCHED
    assert "research/book_equity.csv" not in W.WATCHED     # frozen evidence, never written again


def test_compose_folds_undelivered_pushes_into_the_verdict():
    """[2026-09-13] the push-log check joins the commit check: a settle that committed on time
    but never delivered (09-11) is an alarm, and any failure is one 🚨 text."""
    from research import watchdog as W
    ok = "✅ watchdog: last ledger commit 3h ago (threshold 36h)"
    assert W.compose(False, ok, []) == (False, ok)
    alarm, text = W.compose(False, ok, ["the settle digest for 2026-09-11 was never confirmed delivered (x)"])
    assert alarm and text.startswith("🚨 WATCHDOG: the settle digest for 2026-09-11")
    alarm, text = W.compose(True, "🚨 WATCHDOG: no ledger commit for 40h", ["a"])
    assert alarm and text.count("🚨") == 2


def test_run_exits_red_on_an_undelivered_push_and_never_sends_when_healthy(monkeypatch):
    from research import watchdog as W
    import research.notify as N
    sent = []
    monkeypatch.setattr(N, "send", lambda text, **k: sent.append(text) or True)
    monkeypatch.setattr(W, "last_commit_epoch", lambda paths=W.WATCHED: W.time.time() - 3600)
    monkeypatch.setattr(W, "pushlog_actions", lambda: [])
    assert W.run(["--notify"]) == 0 and sent == []          # healthy: silent, green
    monkeypatch.setattr(W, "pushlog_actions", lambda: ["the settle digest for 2026-09-14 was never confirmed delivered"])
    assert W.run(["--notify"]) == 1 and len(sent) == 1 and "settle digest" in sent[0]


def test_watchdog_imports_on_a_bare_runner(monkeypatch):
    """The Action installs nothing: watchdog → digest → notify → config must import with
    every third-party module absent (requests/yfinance/pandas/dotenv)."""
    import importlib, sys
    for m in ("requests", "yfinance", "pandas", "dotenv"):
        monkeypatch.setitem(sys.modules, m, None)
    for m in ("research.config", "research.notify", "research.digest", "research.watchdog"):
        monkeypatch.delitem(sys.modules, m, raising=False)
    W = importlib.import_module("research.watchdog")
    assert isinstance(W.pushlog_actions(), list)         # runs end-to-end on the real push log


# ------------------------------------------------- 📬 outside-activity watch (2026-10-16)

def _item(n, who, comments=0, pr=False, state="open"):
    it = {"number": n, "user": {"login": who}, "comments": comments, "state": state,
          "title": f"title {n}", "html_url": f"https://github.com/x/y/issues/{n}",
          "created_at": "2026-09-03T15:33:47Z"}
    if pr:
        it["pull_request"] = {"url": "u"}
    return it


def test_waiting_flags_only_unanswered_third_party_items():
    """The 09-03 issue sat unseen for six weeks. Flag: open + not the owner's + no owner
    comment. Skip: the owner's own items, anything the owner already answered, closed items."""
    from research import watchdog as W
    owner_said = [{"user": {"login": W.OWNER}}]
    others_said = [{"user": {"login": "someone"}}]
    by_n = {3: owner_said, 4: others_said}
    items = [_item(1, W.OWNER), _item(2, "stranger"), _item(3, "stranger", comments=1),
             _item(4, "bot", comments=1, pr=True), _item(5, "stranger", state="closed")]
    lines = W.waiting(items, lambda it: by_n[it["number"]])
    assert len(lines) == 2
    assert lines[0].startswith("📬 issue #2 by @stranger (opened 2026-09-03), no reply from you")
    assert lines[1].startswith("📬 PR #4 by @bot")
    assert all("🚨" not in l for l in lines)


def test_waiting_never_fetches_comments_for_an_uncommented_item():
    from research import watchdog as W
    def boom(it):
        raise AssertionError("no comments to fetch")
    assert len(W.waiting([_item(9, "stranger")], boom)) == 1


def test_issue_api_failure_is_one_line_not_an_exception(monkeypatch):
    from research import watchdog as W
    def down(path):
        raise OSError("HTTP Error 403: Forbidden")
    monkeypatch.setattr(W, "_gh", down)
    lines = W.issue_lines()
    assert lines == ["📬 issue watch could not run (OSError) — check watchdog.yml permissions "
                     "and the GitHub API"]


def test_issue_watch_never_masks_or_reddens_the_alarm(monkeypatch):
    """The 🚨 decides and sends FIRST; the 📬 rides after it and never changes the exit code."""
    from research import watchdog as W
    import research.notify as N
    sent = []
    monkeypatch.setattr(N, "send", lambda text, **k: sent.append(text) or True)
    monkeypatch.setattr(W, "pushlog_actions", lambda: [])
    monkeypatch.setattr(W, "issue_lines", lambda: ["📬 issue #2 by @stranger"])
    monkeypatch.setattr(W, "last_commit_epoch", lambda paths=W.WATCHED: W.time.time() - 72 * 3600)
    assert W.run(["--notify", "--issues"]) == 1                      # stale → still red
    assert sent[0].startswith("🚨") and sent[1] == "📬 issue #2 by @stranger"
    sent.clear()
    monkeypatch.setattr(W, "last_commit_epoch", lambda paths=W.WATCHED: W.time.time() - 3600)
    assert W.run(["--notify", "--issues"]) == 0                      # healthy → green
    assert sent == ["📬 issue #2 by @stranger"]                      # and the 📬 still lands


def test_issues_fetched_only_with_the_flag(monkeypatch):
    from research import watchdog as W
    def boom():
        raise AssertionError("issue watch must not run without --issues")
    monkeypatch.setattr(W, "issue_lines", boom)
    monkeypatch.setattr(W, "pushlog_actions", lambda: [])
    monkeypatch.setattr(W, "last_commit_epoch", lambda paths=W.WATCHED: W.time.time() - 3600)
    assert W.run([]) == 0


def test_workflow_grants_issue_read_and_runs_the_watch_at_1230_only():
    import os
    yml = open(os.path.join(os.path.dirname(__file__), "..", "..", ".github", "workflows",
                            "watchdog.yml")).read()
    assert "issues: read" in yml and "pull-requests: read" in yml and "contents: read" in yml
    assert "GITHUB_TOKEN: ${{ github.token }}" in yml
    run = next(l for l in yml.splitlines() if l.strip().startswith("run:"))
    assert "github.event.schedule == '30 12 * * *'" in run and "'--issues'" in run
    assert "write" not in yml.split("permissions:")[1].split("jobs:")[0]
