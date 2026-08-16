"""Guard the one thing that made feedstatus dangerous to test: where it writes."""
import json

from research import feedstatus as F


def test_record_honours_a_redirected_path(tmp_path, monkeypatch):
    """PATH used to be bound as a default argument at import, so monkeypatching it did NOTHING
    and any test reaching record() wrote the LIVE evidence file — which is how a fabricated
    error string landed in the real _feed_status.json on 2026-08-01. Resolve at call time."""
    monkeypatch.setattr(F, "PATH", str(tmp_path / "feed.json"))
    F.record("some-feed", ok=False, error="boom")
    assert json.loads((tmp_path / "feed.json").read_text())["some-feed"]["last_error"] == "boom"


def test_failure_never_looks_like_a_success(tmp_path, monkeypatch):
    """A failed fetch must not touch last_ok — the staleness alarm is computed from it."""
    monkeypatch.setattr(F, "PATH", str(tmp_path / "feed.json"))
    F.record("some-feed", ok=True)
    F.record("some-feed", ok=False, error="down")
    st = json.loads((tmp_path / "feed.json").read_text())["some-feed"]
    assert st["last_error"] == "down" and st["last_ok"]      # last_ok survives, unchanged


def test_last_bar_and_coverage_persist_across_legacy_records(tmp_path, monkeypatch):
    """last_bar/n_ok/n_total are write-only-when-provided: a later legacy record (an error
    path that has no bar in hand) must not erase them — the digest's staleness math reads
    the LAST KNOWN bar, and an erased field would silence the exact alarm it feeds."""
    monkeypatch.setattr(F, "PATH", str(tmp_path / "feed.json"))
    F.record("some-feed", ok=True, last_bar="2026-08-03", n_ok=498, n_total=503)
    F.record("some-feed", ok=False, error="boom")             # legacy-shaped call
    st = json.loads((tmp_path / "feed.json").read_text())["some-feed"]
    assert st["last_bar"] == "2026-08-03"
    assert st["n_ok"] == 498 and st["n_total"] == 503
    assert st["last_error"] == "boom"
