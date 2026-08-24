"""Guard the path diagnostic [PATHS #1]: pure math pinned, read-only contract pinned.

The module is DESCRIPTIVE by pre-registration — these tests pin (1) the walk reproduces
bets._score's settled number on the same bars (position-indexed, the stated alignment),
(2) the peak/give-back arithmetic, (3) the noise reference formula, (4) that nothing ever
writes or fetches on a bad command, and (5) the named-caveat fail-soft rows."""
from datetime import date, timedelta

from research import bets as B
from research import paths as P


def _bars(closes, start="2026-01-01"):
    d0 = date.fromisoformat(start)
    return [{"date": (d0 + timedelta(days=i)).isoformat(), "close": float(c)}
            for i, c in enumerate(closes)]


def test_walk_rise_then_fade_pins_peak_and_give_back():
    """The user-story path: thesis plays out by day 2, fades by the horizon — the walk must
    show exactly that shape, because this diagnostic exists to measure it."""
    stock = _bars([100, 110, 120, 110, 105])      # peaks day 2 at +20%, ends +5%
    bench = _bars([100, 100, 100, 100, 100])      # flat benchmark → excess = raw return
    ex = P.walk(stock, bench, "long", 5)
    st = P.path_stats(ex)
    assert st["peak_t"] == 2
    assert abs(st["mfe"] - 0.20) < 1e-9
    assert abs(st["final"] - 0.05) < 1e-9
    assert abs(st["give_back"] - 0.15) < 1e-9


def test_walk_short_direction_sign_flips():
    stock = _bars([100, 90, 80])                  # falling stock
    bench = _bars([100, 100, 100])
    ex = P.walk(stock, bench, "short", 3)
    assert ex[0] == 0 and ex[-1] > 0              # a short profits from the fall


def test_walk_final_reproduces_the_settled_number():
    """Position-indexed like _score — the stated [PATHS #1] alignment choice. On identical
    bars the walk's last point must equal what settle wrote to the ledger."""
    stock = _bars([100, 104, 103, 108], start="2026-01-02")
    bench = _bars([100, 101, 101, 102], start="2026-01-02")
    scored = B._score(stock, bench, "long", 4, "2026-01-01", today="2026-02-01")
    ex = P.walk(stock, bench, "long", 4)
    assert scored is not None
    assert abs(ex[-1] - scored[2]) < 1e-12


def test_walk_none_when_either_leg_short():
    assert P.walk(_bars([100, 101]), _bars([100, 101, 102]), "long", 3) is None
    assert P.walk(_bars([100, 101, 102]), _bars([100, 101]), "long", 3) is None


def test_noise_ref_hand_check_and_minimum_points():
    """σ·√(2T/π) with σ from the increments — pinned against a hand computation."""
    import math
    import statistics
    ex = [0.0, 0.01, -0.01, 0.02]                 # increments: +.01, -.02, +.03
    want = statistics.stdev([0.01, -0.02, 0.03]) * math.sqrt(2 * 4 / math.pi)
    assert abs(P.noise_ref(ex) - want) < 1e-12
    assert P.noise_ref([0.0, 0.01]) is None       # below 3 points: no stdev, no reference


def test_report_fail_soft_caveats_and_drift(monkeypatch, capsys):
    """A short-history row is named and skipped; a ledger-drift row is named and still shown;
    the run survives both (the bets.settle per-row-isolation lesson)."""
    good = _bars([100, 110, 105], start="2026-01-02")
    flat = _bars([100, 100, 100], start="2026-01-02")
    def bars(sym, day, n):
        if sym == "DEAD":
            return []                             # feed flake → CAVEAT + skip
        return good if sym in ("OK", "DRIFTY") else flat
    monkeypatch.setattr(P.prices, "bars_after", bars)
    rows = [{"ticker": "DEAD", "benchmark": "SPY", "direction": "long", "horizon_d": "3",
             "logged_at": "2026-01-01T00:00:00+00:00", "status": "closed",
             "entry_date": "2026-01-02", "excess_pct": "+5.00"},
            {"ticker": "OK", "benchmark": "SPY", "direction": "long", "horizon_d": "3",
             "logged_at": "2026-01-01T00:00:00+00:00", "status": "closed",
             "entry_date": "2026-01-02", "excess_pct": "+5.00"},   # matches walk final
            {"ticker": "DRIFTY", "benchmark": "SPY", "direction": "long", "horizon_d": "3",
             "logged_at": "2026-01-01T00:00:00+00:00", "status": "closed",
             "entry_date": "2026-01-02", "excess_pct": "+9.99"},   # ledger disagrees
            {"ticker": "OPEN", "benchmark": "SPY", "direction": "long", "horizon_d": "3",
             "logged_at": "2026-01-01T00:00:00+00:00", "status": "open",
             "entry_date": "", "excess_pct": ""}]                  # settled only: excluded
    shown = P.report(rows)
    out = capsys.readouterr().out
    assert shown == 2
    assert "CAVEAT DEAD" in out and "skipped" in out
    assert "DRIFT" in out and "DRIFTY" in out
    assert "OPEN" not in out                      # open rows never walked [PATHS #1]
    assert "DESCRIPTIVE" in out and "verdict" in out.lower()


def test_bare_is_show_and_unknown_command_is_an_error(monkeypatch, capsys):
    """Read-only contract (movers.run guard): bare = show, typo = error, and an unknown
    command touches NEITHER the ledger NOR the network."""
    monkeypatch.setattr(P.bets, "_load", lambda: [])
    def boom(*a, **k):
        raise AssertionError("unknown command must not fetch")
    monkeypatch.setattr(P.prices, "bars_after", boom)
    assert P.run(["scan"]) == 1                   # error, nothing fetched (boom not raised)
    assert P.run([]) == 0                         # bare = show; empty catalogue = clean exit
    assert "no settled rows yet" in capsys.readouterr().out
