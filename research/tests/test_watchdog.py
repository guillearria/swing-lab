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
