"""Guard the forward-track diagnostic display: every split must show closed AND open counts.

Until 2026-08-04 a group with ≥1 closed row rendered only "Ncl med X%" and silently dropped
its open count — post-earnings-drift showed "1cl" while hiding ~20 open bets, so the surface
built to make concentration visible understated exactly the biggest tag.
"""
from research import engine as E


def _bet(status, tag="", ticker="AAA", horizon="63", excess=""):
    return {"logged_at": "2026-07-01T00:00:00+00:00", "ticker": ticker, "direction": "long",
            "horizon_d": horizon, "benchmark": "SPY", "thesis": "t", "status": status,
            "entry_date": "2026-07-02", "entry": "100", "excess_pct": excess,
            "pattern_tag": tag, "notified": ""}


def _wire(monkeypatch, bet_rows, mover_rows=()):
    from research import bets, movers, universe
    monkeypatch.setattr(bets, "_load", lambda: list(bet_rows))
    monkeypatch.setattr(movers, "_load", lambda: list(mover_rows))
    monkeypatch.setattr(universe, "sp500_cached", lambda: ["AAA"])
    monkeypatch.setattr(universe, "tail", lambda: ["TTT"])


def test_split_with_closed_rows_still_shows_open_count(monkeypatch, capsys):
    rows = [_bet("closed", tag="post-earnings-drift", excess="-19.09")] + \
           [_bet("open", tag="post-earnings-drift") for _ in range(20)]
    _wire(monkeypatch, rows)
    E.forward_track()
    out = capsys.readouterr().out
    assert "post-earnings-drift 1cl med -19.1% 20op" in out    # both counts, both labels


def test_split_with_no_closed_rows_labels_the_open_count(monkeypatch, capsys):
    _wire(monkeypatch, [_bet("open", tag="analyst-rerating") for _ in range(3)])
    E.forward_track()
    out = capsys.readouterr().out
    assert "analyst-rerating 0cl 3op" in out                   # unit label, not a bare number


def test_universe_diagnostic_classifies_by_current_caches(monkeypatch, capsys):
    rows = [_bet("open", ticker="AAA"),          # in the sp500 cache
            _bet("open", ticker="TTT"),          # in the tail caches
            _bet("open", ticker="ZZZ")]          # in neither → other
    _wire(monkeypatch, rows)
    E.forward_track()
    out = capsys.readouterr().out
    assert "by universe (diagnostic, not a goalpost) [ARC 5 #11]" in out
    assert "sp500 0cl 1op" in out and "tail 0cl 1op" in out and "other 0cl 1op" in out


def test_pooled_headline_is_long_only_but_tag_split_keeps_shorts(monkeypatch, capsys):
    """[ARC 5 #12a]: a settled short is OUT of the pooled verdict headline but must stay
    visible in its diagnostic tag split (via bets._agg) — else the diagnostics go blind."""
    short = dict(_bet("closed", tag="spike-fade", excess="+69.74"), direction="short")
    rows = [short, _bet("closed", excess="-5.00")]
    _wire(monkeypatch, rows)
    E.forward_track()
    out = capsys.readouterr().out
    assert "pooled long-only): 1 settled" in out            # short excluded from the verdict
    assert "median -5.00%" in out
    assert "spike-fade 1cl med +69.7%" in out               # ...but present in its tag split


def test_denominator_line_decomposes_by_universe(monkeypatch, capsys):
    movers_rows = [{"status": "taken", "universe": "sp500"},
                   {"status": "skip", "universe": "sp500"},
                   {"status": "skip", "universe": "tail"}]
    _wire(monkeypatch, [_bet("open")], movers_rows)
    E.forward_track()
    out = capsys.readouterr().out
    assert "sp500 2 / tail 1" in out
    assert "1 taken / 2 skipped / 0 unread" in out
