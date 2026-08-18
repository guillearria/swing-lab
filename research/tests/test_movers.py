"""Guard the mover-scan denominator: rank() is pure (no I/O), so test it directly —
it must filter sub-threshold names, keep BOTH directions, sort by |move|, and respect top_n."""
from datetime import date, timedelta

from research import movers as M


def _bars(n: int, step: float, vol: float = 1.0):
    d0 = date(2026, 1, 1)
    out, px = [], 100.0
    for i in range(n):
        out.append({"date": (d0 + timedelta(days=i)).isoformat(), "close": px, "volume": vol})
        px *= (1 + step)
    return out


def test_rank_filters_and_keeps_both_directions():
    ranked = M.rank({"BIG": _bars(30, 0.02),      # ~+10% over 5d
                     "SMALL": _bars(30, 0.002),   # ~+1% over 5d → below PCT_STRONG (3%)
                     "DOWN": _bars(30, -0.02)},   # big DOWN mover
                    top_n=10)
    tickers = [c["ticker"] for c in ranked]
    assert "SMALL" not in tickers                 # sub-threshold, filtered out
    assert "BIG" in tickers and "DOWN" in tickers  # bidirectional (we read longs AND shorts)
    assert tickers[0] in ("BIG", "DOWN")          # sorted by |move| desc


def test_rank_respects_top_n():
    bars = {f"T{i}": _bars(30, 0.05 + i * 0.001) for i in range(5)}
    assert len(M.rank(bars, top_n=2)) == 2


def test_rank_skips_short_history():
    assert M.rank({"X": _bars(10, 0.05)}) == []   # < 26 bars → momentum.compute None → skipped


def test_outcome_stats_ignores_unscored_and_wrong_status():
    rows = [{"status": "skip", "x21_pct": "+2.00"},
            {"status": "skip", "x21_pct": "-1.00"},
            {"status": "skip", "x21_pct": ""},        # unscored → ignored
            {"status": "taken", "x21_pct": "+5.00"}]  # wrong status → ignored
    n, med, beat = M.outcome_stats(rows, "skip", "x21_pct")
    assert (n, med, beat) == (2, 0.5, 50.0)           # median(+2,-1)=0.5; 1/2 positive
    assert M.outcome_stats(rows, "skip", "x63_pct") is None


def test_settle_scores_decisions_only(monkeypatch):
    from research import prices
    def fake_bars_after(sym, day, n):                 # stock +10% flat vs flat bench
        closes = [100.0] * 70 if sym == M.BENCH else [100.0] + [110.0] * 69
        return [{"date": f"2026-02-{(i % 27) + 1:02d}", "close": closes[i]} for i in range(n)]
    monkeypatch.setattr(prices, "bars_after", fake_bars_after)
    rows = [{"status": "skip", "direction_hint": "long", "ticker": "AAA",
             "logged_at": "2026-01-31T00:00:00+00:00", "seen_at": "", "x21_pct": "", "x63_pct": ""},
            {"status": "seen", "direction_hint": "long", "ticker": "BBB",   # undecided
             "logged_at": "", "seen_at": "2026-01-31T00:00:00+00:00", "x21_pct": "", "x63_pct": ""}]
    assert M.settle(rows) == 1                         # only the decided row scores
    assert rows[0]["x21_pct"] == "+10.00" and rows[0]["x63_pct"] == "+10.00"
    assert rows[1]["x21_pct"] == "" and rows[1]["x63_pct"] == ""   # SEEN untouched


def test_bare_and_unknown_commands_never_write(tmp_path, monkeypatch):
    """2026-08-02: a bare `python3 -m research.movers` — the form README and the dashboard list
    as an INSPECTION command — defaulted to `scan` and appended 25 re-scanned rows to the
    ledger, inflating the multiple-testing denominator. Any typo did the same, because every
    unrecognised command fell through to the write path. A read-only-looking command must be
    read-only, and an unknown one must fail loudly rather than write."""
    from research import movers as M
    led = tmp_path / "movers.csv"
    led.write_text("seen_at,date,ticker,pct_change,rel_volume,direction_hint,action,"
                   "logged_at,rationale,status,pattern_tag,x21_pct,x63_pct,universe\n")
    before = led.read_bytes()
    monkeypatch.setattr(M, "LEDGER", str(led))

    def boom(*a, **k):
        raise AssertionError("must not scan")
    monkeypatch.setattr(M, "scan", boom)
    for argv in ([], ["sho"], ["SCAN"], ["--help"]):
        M.run(argv)
        assert led.read_bytes() == before, f"{argv!r} wrote to the ledger"


def test_load_backfills_pre_universe_rows(tmp_path, monkeypatch):
    """The 425-row live ledger predates the universe column [ARC 5 #11]; _load must backfill
    it (orders.py pattern) so no code path KeyErrors, and label those rows sp500 — which is a
    fact, not a guess: the scan was S&P-500-only when they were written."""
    led = tmp_path / "movers.csv"
    led.write_text("seen_at,date,ticker,pct_change,rel_volume,direction_hint,action,"
                   "logged_at,rationale,status,pattern_tag,x21_pct,x63_pct\n"
                   "2026-07-01T00:00:00+00:00,2026-06-30,AAA,+5.0,1.2,long,take,"
                   "2026-07-01T01:00:00+00:00,why,taken,,,\n")
    monkeypatch.setattr(M, "LEDGER", str(led))
    rows = M._load()
    assert rows[0]["universe"] == "sp500"
    assert rows[0]["ticker"] == "AAA"


def _cohort_setup(monkeypatch, sp500_bars, tail_bars, statuses):
    """Wire scan() to synthetic universes/bars; capture feedstatus records."""
    from research import universe as U
    monkeypatch.setattr(U, "sp500", lambda: list(sp500_bars))
    monkeypatch.setattr(U, "tail", lambda: list(tail_bars))
    all_bars = {**{t: _bars(30, 0.04) for t in sp500_bars},
                **{t: _bars(30, 0.05) for t in tail_bars}}
    monkeypatch.setattr(M, "_fetch", lambda syms: {t: all_bars[t] for t in syms})
    from research import feedstatus as F
    monkeypatch.setattr(F, "record",
                        lambda source, ok, error="", path=None, **kw: statuses.append(
                            {"source": source, "ok": ok, "error": error, **kw}))


def test_scan_two_cohorts_stamp_universe_and_feed_keys(monkeypatch):
    statuses = []
    _cohort_setup(monkeypatch, ["SPA", "SPB"], ["TLA"], statuses)
    rows = []
    n = M.scan(rows, today="2026-03-01")     # all synthetic bars are Jan/Feb → complete
    assert n == 3
    assert {r["ticker"]: r["universe"] for r in rows} == \
        {"SPA": "sp500", "SPB": "sp500", "TLA": "tail"}
    assert [s["source"] for s in statuses] == ["sp500-movers", "tail-movers"]
    for s in statuses:
        assert s["ok"] and s["last_bar"] and s["n_ok"] == s["n_total"]


def test_scan_dead_tail_cohort_does_not_abort_sp500(monkeypatch):
    """A missing tail cache records its OWN failure and the sp500 cohort still logs."""
    statuses = []
    _cohort_setup(monkeypatch, ["SPA"], [], statuses)
    rows = []
    assert M.scan(rows, today="2026-03-01") == 1
    assert rows[0]["universe"] == "sp500"
    tail = next(s for s in statuses if s["source"] == "tail-movers")
    assert not tail["ok"] and "empty" in tail["error"]


def test_scan_partial_bar_guard_defers_to_completed_session(monkeypatch):
    """A mid-session scan must rank yesterday's COMPLETED close, not the still-moving bar —
    and a rescan after the close must then be able to record the real bar (the old behavior
    logged the intraday date and the dedup blocked the real close forever, BACKLOG item)."""
    statuses = []
    _cohort_setup(monkeypatch, ["SPA"], [], statuses)
    rows = []
    # _bars(30, ...) ends 2026-01-30; pretend that last bar is TODAY (still moving).
    M.scan(rows, today="2026-01-30")
    assert rows and rows[0]["date"] == "2026-01-29"          # ranked on the completed session
    assert statuses[0]["last_bar"] == "2026-01-29"
    # Next day the 01-30 close is complete: the same name logs its REAL close.
    n2 = M.scan(rows, today="2026-01-31")
    assert n2 == 1 and rows[-1]["date"] == "2026-01-30"


def test_scan_quiet_day_is_ok_not_outage(monkeypatch):
    """Bars returned but nothing clears PCT_STRONG → ok=True (the old ok=bool(ranked)
    conflated a quiet day with a dead feed)."""
    statuses = []
    from research import universe as U
    monkeypatch.setattr(U, "sp500", lambda: ["FLAT"])
    monkeypatch.setattr(U, "tail", lambda: [])
    monkeypatch.setattr(M, "_fetch", lambda syms: {"FLAT": _bars(30, 0.0001)})
    from research import feedstatus as F
    monkeypatch.setattr(F, "record",
                        lambda source, ok, error="", path=None, **kw: statuses.append(
                            {"source": source, "ok": ok, **kw}))
    rows = []
    assert M.scan(rows, today="2026-03-01") == 0
    sp = next(s for s in statuses if s["source"] == "sp500-movers")
    assert sp["ok"] and sp["n_ok"] == 1


def test_ledger_survives_a_save_crash_and_malformed_rows_are_named(tmp_path, monkeypatch):
    """The 2026-08-18 orders incident, guarded here too: a hand-edit's unquoted comma must be
    refused BY NAME at load, and a writer crash must leave the file untouched (write-then-
    replace), never truncated mid-save."""
    import pytest
    led = tmp_path / "movers.csv"
    led.write_text("date,ticker\n2026-08-03,PNR,OVERFLOW\n")
    monkeypatch.setattr(M, "LEDGER", str(led))
    with pytest.raises(ValueError, match="PNR"):
        M._load()
    original = led.read_text()
    with pytest.raises(ValueError):
        M._save([{None: ["overflow"]}])
    assert led.read_text() == original
