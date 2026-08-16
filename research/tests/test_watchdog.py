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
