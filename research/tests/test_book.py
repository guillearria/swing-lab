"""Guard the paper live book: cash conservation + direction-aware realized P&L."""
from research import book as BK


def _fresh(cash: float):
    rows = []
    BK._set_cash(rows, cash)
    return rows


def test_long_roundtrip_cash_and_pnl():
    rows = _fresh(1000.0)
    BK.open_(rows, "AAA", "long", 10, 50, 45, 60, 5, "t")
    assert BK._cash(rows) == 500.0                      # debited 10*50
    BK.close_(rows, "AAA", 60)
    assert BK._cash(rows) == 1100.0                     # credited 10*60
    closed = [r for r in rows if r["status"] == "closed"][0]
    assert float(closed["realized_pnl"]) == 100.0       # 10*(60-50); == net cash change


def test_short_pnl_sign():
    rows = _fresh(1000.0)
    BK.open_(rows, "BBB", "short", 10, 50, 55, 40, 5, "t")
    assert BK._cash(rows) == 1500.0                     # short credits proceeds
    BK.close_(rows, "BBB", 40)                          # covered lower = win
    assert float([r for r in rows if r["status"] == "closed"][0]["realized_pnl"]) == 100.0
    assert BK._cash(rows) == 1100.0                     # 1500 - 10*40


def test_short_loss_when_price_rises():
    rows = _fresh(1000.0)
    BK.open_(rows, "CCC", "short", 10, 50, 55, 40, 5, "t")
    BK.close_(rows, "CCC", 60)                          # covered higher = loss
    assert float([r for r in rows if r["status"] == "closed"][0]["realized_pnl"]) == -100.0


def test_partial_close_splits_position():
    rows = _fresh(1000.0)
    BK.open_(rows, "EEE", "long", 10, 50, 45, 60, 5, "t")   # cash -> 500
    BK.close_(rows, "EEE", 60, 4)                            # sell 4 of 10
    openp = [r for r in rows if r["status"] == "open" and r["ticker"] == "EEE"][0]
    closed = [r for r in rows if r["status"] == "closed" and r["ticker"] == "EEE"][0]
    assert float(openp["shares"]) == 6                       # 6 still held
    assert float(closed["shares"]) == 4
    assert float(closed["realized_pnl"]) == 40.0             # 4*(60-50)
    assert BK._cash(rows) == 740.0                           # 500 + 4*60


def test_long_blocked_when_cash_short():
    rows = _fresh(100.0)
    BK.open_(rows, "DDD", "long", 10, 50, 45, 60, 5, "t")   # needs 500, have 100
    assert not [r for r in rows if r["status"] == "open"]   # no position opened
    assert BK._cash(rows) == 100.0                          # cash untouched


def test_stop_sets_latest_open_and_appends_note():
    rows = _fresh(1000.0)
    BK.open_(rows, "AAA", "long", 10, 50, 0, 0, 5, "thesis")
    BK.stop_(rows, "AAA", 47.5, "below base")
    r = [r for r in rows if r["status"] == "open" and r["ticker"] == "AAA"][0]
    assert float(r["stop"]) == 47.5                          # stop written
    assert r["thesis"].endswith("below base")               # note appended, not clobbered


def test_stop_noop_when_no_open_position():
    rows = _fresh(1000.0)
    BK.stop_(rows, "ZZZ", 10)                                # nothing to stop
    assert not [r for r in rows if r["ticker"] == "ZZZ"]     # no row created


def test_through_target_is_direction_aware_with_zero_guards():
    """through_stop's mirror [2026-08-04]: a long exits INTO strength (spot >= target),
    a short covers into weakness (spot <= target). 0/blank target = no target."""
    assert BK.through_target("long", 4.94, 4.85)             # NIO's actual touch
    assert not BK.through_target("long", 4.78, 4.85)
    assert BK.through_target("short", 90.0, 95.0)
    assert not BK.through_target("short", 96.0, 95.0)
    assert not BK.through_target("long", None, 4.85)         # no spot → no claim
    assert not BK.through_target("long", 4.94, 0.0)          # no target set


def test_target_sets_latest_open_lot_and_zero_clears():
    rows = _fresh(1000.0)
    BK.open_(rows, "AAA", "long", 10, 50, 45, 0, 5, "thesis")
    BK.target_(rows, "AAA", 60, "sell into strength")
    r = [x for x in rows if x["status"] == "open" and x["ticker"] == "AAA"][0]
    assert float(r["target"]) == 60.0
    assert r["thesis"].endswith("sell into strength")
    BK.target_(rows, "AAA", 0)                               # 0 clears (retired-stop convention)
    assert r["target"] == ""


def test_target_noop_when_no_open_position():
    rows = _fresh(1000.0)
    BK.target_(rows, "ZZZ", 10)
    assert not [r for r in rows if r["ticker"] == "ZZZ"]


# ---------------------------------------------------------------- mark_delta (the honesty guard)
# Driven by the REAL committed curve rows, so the guard is tested against the event that
# motivated it rather than a fixture invented to pass.
_R0802 = {"date": "2026-08-02", "equity": "5460.11", "cash": "427.81",
          "unrealized": "-326.33", "realized": "-525.31", "spy_equiv": "6696.40"}
_R0803 = {"date": "2026-08-03", "equity": "3510.10", "cash": "427.81",
          "unrealized": "-356.34", "realized": "-525.31", "spy_equiv": "4810.78"}
_R0804 = {"date": "2026-08-04", "equity": "3509.45", "cash": "427.81",
          "unrealized": "-356.99", "realized": "-525.31", "spy_equiv": "4743.25"}


def _as_mark(row: dict) -> dict:
    return {k: float(row[k]) for k in ("equity", "cash", "unrealized", "realized", "spy_equiv")}


def test_a_periods_pl_is_unrealized_plus_realized_not_the_equity_change():
    """The definition the whole band rests on. On a clean day the two agree exactly."""
    d = BK.mark_delta(_R0803, _as_mark(_R0804))
    assert d["clean"] and abs(d["unexplained"]) < 0.01
    assert round(d["d_equity"], 2) == -0.65 and round(d["d_perf"], 2) == -0.65
    assert round(d["d_gap"], 2) == 66.88          # ground GAINED on SPY even on a down day


def test_a_scope_removal_reports_the_real_pl_and_names_the_rest():
    """2026-08-02→08-03 took a long-realm holding out of scope: -$1,950 of EQUITY, but the market only
    did -$30.01 that day. The old residual test refused to print any % here; that threw away a
    real number. Now the P&L is right AND the fiat move is named."""
    d = BK.mark_delta(_R0802, _as_mark(_R0803))
    assert not d["clean"]
    assert round(d["d_equity"], 2) == -1950.01     # what equity did
    assert round(d["d_perf"], 2) == -30.01         # what the MARKET did — the honest number
    assert round(d["unexplained"], 2) == -1920.00  # what left the book by fiat
    assert d["d_gap"] is None                      # spy_equiv moved with the seed — no race result
    assert round(d["pct"], 2) == round(-30.01 / 5460.11 * 100, 2)


def test_a_deposit_is_never_reported_as_a_gain():
    """THE bug this rewrite exists for. A deposit raises cash AND equity by the same amount, so
    it satisfies the old `d_equity == d_cash + d_unrealized` test exactly and printed as a +28%
    day. The book takes real deposits, so it would have lied the first time it was funded."""
    after = {**_as_mark(_R0803), "equity": float(_R0803["equity"]) + 1000,
             "cash": float(_R0803["cash"]) + 1000}
    d = BK.mark_delta(_R0803, after)
    assert round(d["d_equity"], 2) == 1000.00
    assert round(d["d_perf"], 2) == 0.00 and round(d["pct"], 2) == 0.00   # earned NOTHING
    assert round(d["unexplained"], 2) == 1000.00 and not d["clean"]
    assert d["flat"]


def test_a_deposit_on_a_moving_day_still_reports_only_the_market():
    after = {**_as_mark(_R0803), "equity": float(_R0803["equity"]) + 950,
             "cash": float(_R0803["cash"]) + 1000,
             "unrealized": float(_R0803["unrealized"]) - 50}
    d = BK.mark_delta(_R0803, after)
    assert round(d["d_perf"], 2) == -50.00 and round(d["unexplained"], 2) == 1000.00


def test_an_ordinary_trade_day_is_still_reported_as_performance():
    """The mirror-image bug: `book open` moves cash against basis, which broke the old identity,
    so a NORMAL trading day rendered as "not P&L". Opening a position is equity-neutral — the
    day's real move must survive it. This is the next thing that happens when DXCM fills."""
    after = {**_as_mark(_R0803), "equity": float(_R0803["equity"]) + 50,
             "cash": float(_R0803["cash"]) - 421.40,          # 5 DXCM @ 84.28 bought
             "unrealized": float(_R0803["unrealized"]) + 50}
    d = BK.mark_delta(_R0803, after)
    assert d["clean"] and round(d["d_perf"], 2) == 50.00
    assert d["pct"] is not None and d["d_gap"] is not None


def test_mark_delta_calls_a_weekend_duplicate_flat():
    """Weekend rows are byte-identical copies of Friday — that is 'nothing moved', not a $0 day."""
    d = BK.mark_delta(_R0803, _as_mark(_R0803))
    assert d["flat"] and d["clean"] and d["d_perf"] == 0.0


def test_mark_delta_survives_a_missing_yardstick():
    """spy_equiv is blank in the curve until a seed row exists — never raise on it."""
    d = BK.mark_delta({"equity": "100", "cash": "100", "unrealized": "0", "realized": "0",
                       "spy_equiv": ""},
                      {"equity": 110.0, "cash": 100.0, "unrealized": 10.0, "realized": 0.0})
    assert d["clean"] and d["gap"] is None and d["d_gap"] is None
    assert round(d["pct"], 1) == 10.0


def test_pool_floor_is_one_definition():
    assert BK.pool_floor(4662.74) == (1 - BK.POOL_STOP) * 4662.74
    assert round(BK.pool_floor(4662.74), 2) == 2797.64


# ---------------------------------------------------- terminal CLOSED state [ARC 5 #12 / #12a]

def _retired_rows(cash=0.0):
    rows = _fresh(cash)
    BK.retire(rows)
    return rows


def test_retire_refuses_while_positions_are_open():
    rows = _fresh(1000.0)
    BK.open_(rows, "AAA", "long", 10, 50, 45, 60, 5, "t")
    assert BK.retire(rows) is False
    assert not BK.is_retired(rows)


def test_retire_sweeps_cash_and_stamps_the_meta_row():
    rows = _fresh(1495.0)
    assert BK.retire(rows) is True
    assert BK.is_retired(rows) and BK._cash(rows) == 0.0
    meta = BK._retired_row(rows)
    assert meta["entry"] == "1495.00"                   # the swept amount is evidence
    assert meta["status"] == "meta" and set(meta) == set(BK.FIELDS)
    assert BK.retire(rows) is False                     # terminal means once


def test_retired_book_never_marks_or_snapshots(monkeypatch, capsys):
    """The one-liner paths must fetch NOTHING (no spots/SPY/dual-mom — the perpetual
    POOL-STOP print is unreachable) and must write NOTHING (frozen means frozen)."""
    def boom(*a, **k):
        raise AssertionError("a retired book must not fetch prices")
    monkeypatch.setattr(BK, "_spot", boom)
    monkeypatch.setattr(BK, "equity_marks", boom)
    rows = _retired_rows()
    BK.mark(rows)
    BK.show(rows)
    assert BK.snapshot(rows, path="/nonexistent/dir/never-written.csv") is None
    out = capsys.readouterr().out
    assert out.count("BOOK CLOSED") == 3 and "[ARC 5 #12]" in out


def test_retired_book_refuses_mutations(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(BK, "BOOK", str(tmp_path / "book.csv"))
    rows = _retired_rows(0.0)
    BK._save(rows)
    before = open(BK.BOOK).read()
    for argv in (["open", "AAA", "long", "1", "50", "45", "60", "5", "t"],
                 ["close", "AAA", "60"], ["stop", "AAA", "44"], ["seed"]):
        BK.run(argv)
    assert open(BK.BOOK).read() == before               # nothing written by any of them
    assert "BOOK CLOSED" in capsys.readouterr().out
