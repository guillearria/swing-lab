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
    monkeypatch.setattr(W, "pushlog_actions", lambda: ["the read brief for 2026-09-14 was never confirmed delivered"])
    assert W.run(["--notify"]) == 1 and len(sent) == 1 and "read brief" in sent[0]


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
