"""Guard the forward-track diagnostic display: every split must show closed AND open counts.

Until 2026-08-04 a group with ≥1 closed row rendered only "Ncl med X%" and silently dropped
its open count — post-earnings-drift showed "1cl" while hiding ~20 open bets, so the surface
built to make concentration visible understated exactly the biggest tag.
"""
from research import engine as E


def _bet(status, tag="", ticker="AAA", horizon="63", excess="", conviction=""):
    return {"logged_at": "2026-07-01T00:00:00+00:00", "ticker": ticker, "direction": "long",
            "horizon_d": horizon, "benchmark": "SPY", "thesis": "t", "status": status,
            "entry_date": "2026-07-02", "entry": "100", "excess_pct": excess,
            "pattern_tag": tag, "notified": "", "conviction": conviction}


def _wire(monkeypatch, bet_rows, mover_rows=(), cases=()):
    """Every input to forward_track() is a FIXTURE — including which tags have a case file.

    `cases` was ambient repo state until 2026-08-21: tags_with_cases() globs research/cases/*.md,
    so the read routine adding EL.md/MRK.md on 08-20 (declaring post-earnings-drift and
    analyst-rerating) un-starred two tags these tests had hardcoded as unbacked, and the suite
    went red for a LIVE-DATA change with no code change behind it. The star is incidental to
    what these tests guard — the DISPLAY invariant: both counts, both unit labels, every branch."""
    from research import bets, movers, universe
    monkeypatch.setattr(bets, "_load", lambda: list(bet_rows))
    monkeypatch.setattr(movers, "_load", lambda: list(mover_rows))
    monkeypatch.setattr(bets, "tags_with_cases", lambda: set(cases))
    monkeypatch.setattr(universe, "sp500_cached", lambda: ["AAA"])
    monkeypatch.setattr(universe, "tail", lambda: ["TTT"])


def test_split_with_closed_rows_still_shows_open_count(monkeypatch, capsys):
    rows = [_bet("closed", tag="post-earnings-drift", excess="-19.09")] + \
           [_bet("open", tag="post-earnings-drift") for _ in range(20)]
    _wire(monkeypatch, rows)
    E.forward_track()
    out = capsys.readouterr().out
    assert "post-earnings-drift* 1cl med -19.1% 20op" in out   # both counts, both labels
    assert "* = no case file (1 of 1)" in out                  # unbacked tag, flagged


def test_split_with_no_closed_rows_labels_the_open_count(monkeypatch, capsys):
    _wire(monkeypatch, [_bet("open", tag="analyst-rerating") for _ in range(3)])
    E.forward_track()
    out = capsys.readouterr().out
    assert "analyst-rerating* 0cl 3op" in out                  # unit label, not a bare number


def test_a_tag_with_a_case_file_is_not_starred(monkeypatch, capsys):
    """[ARC 5 #14b] The star is the accountability: it says this scenario names a phrase, not a
    documented mechanism. A tag the case layer actually declares must come back clean, and the
    legend must not fire when nothing is loose."""
    _wire(monkeypatch, [_bet("open", tag="unlock-relief") for _ in range(2)],
          cases={"unlock-relief"})
    E.forward_track()
    out = capsys.readouterr().out
    assert "unlock-relief 0cl 2op" in out and "unlock-relief*" not in out
    assert "no case file" not in out


def test_untagged_rows_are_never_starred(monkeypatch, capsys):
    """'untagged' is the absence of a claim, not an undocumented one — starring it would invent
    a defect. The 14 pre-#14b untagged rows stay as they are; backfilling 5 SETTLED ones would
    be retroactive labelling with the outcome already known."""
    _wire(monkeypatch, [_bet("open") for _ in range(2)])
    E.forward_track()
    out = capsys.readouterr().out
    assert "untagged 0cl 2op" in out and "untagged*" not in out


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
    assert "spike-fade* 1cl med +69.7%" in out              # ...but present in its tag split


def test_denominator_line_decomposes_by_universe(monkeypatch, capsys):
    movers_rows = [{"status": "taken", "universe": "sp500"},
                   {"status": "skip", "universe": "sp500"},
                   {"status": "skip", "universe": "tail"}]
    _wire(monkeypatch, [_bet("open")], movers_rows)
    E.forward_track()
    out = capsys.readouterr().out
    assert "sp500 2 / tail 1" in out
    assert "1 taken / 2 skipped / 0 unread" in out


def test_conviction_split_is_diagnostic_and_groups_unstated(monkeypatch, capsys):
    """[ARC 5 #15] The by-conviction lens rides _grp: both counts, both unit labels, tiers
    PRESENT only — and a row with no conviction KEY at all (any pre-#15 row surviving in a
    fixture or an old CSV read) groups as `unstated`, never a KeyError."""
    legacy = _bet("open")
    del legacy["conviction"]                       # pre-#15 row shape: key absent entirely
    _wire(monkeypatch, [_bet("closed", excess="+2.00", conviction="high"),
                        _bet("open", conviction="high"), legacy])
    E.forward_track()
    out = capsys.readouterr().out
    assert "by conviction (diagnostic, not a goalpost) [ARC 5 #15]" in out
    assert "high 1cl med +2.0% 1op" in out         # both counts, both labels
    assert "unstated 0cl 1op" in out
    assert "medium" not in out                     # absent tier renders nothing
