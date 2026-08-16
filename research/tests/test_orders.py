"""Guard the counterfactual-order ledger. The band math and the resolver are PURE, so test
them directly — a wrong fill is a counterfactual that lies into the [ORDERS #1] diagnostic."""
import pytest

from research import config, orders as O


def _bar(date, o, h, l, c):
    return {"date": date, "open": o, "high": h, "low": l, "close": c, "volume": 1.0}


# ---------------------------------------------------------------- limit_price (the band)

def test_the_dxcm_case_that_prompted_this():
    """2026-08-03: ref 83.45 (Fri close), stop 76.80. The stop is 7.97% away, 20% of that is
    1.59%, so the 1.0% cap binds -> 84.28. The human was looking at 86.54."""
    assert O.limit_price(83.45, 76.80, "long") == 84.28


def test_cap_binds_on_a_wide_stop():
    # stop 20% away -> frac term is 4%, cap holds it to ENTRY_BAND_MAX
    assert O.limit_price(100.0, 80.0, "long") == round(100 * (1 + config.ENTRY_BAND_MAX), 2)


def test_stop_fraction_binds_on_a_tight_stop():
    # stop 2% away -> frac term is 0.4%, tighter than the 1% cap, so it wins
    assert O.limit_price(100.0, 98.0, "long") == 100.4


def test_short_bands_downward():
    """A short chases DOWN, never up — a sign error here buys the top instead of selling it."""
    assert O.limit_price(100.0, 120.0, "short") == round(100 * (1 - config.ENTRY_BAND_MAX), 2)


def test_no_stop_falls_back_to_the_cap():
    assert O.limit_price(100.0, 0.0, "long") == round(100 * (1 + config.ENTRY_BAND_MAX), 2)


def test_nonpositive_reference_is_refused():
    with pytest.raises(ValueError):
        O.limit_price(0.0, 90.0, "long")


# ---------------------------------------------------------------- resolve (the fill model)

def test_touch_fills_at_the_limit():
    bars = [_bar("2026-08-03", 101.0, 102.0, 99.5, 101.5)]   # low pierced 100
    assert O.resolve(bars, 100.0, "long", expiry_d=3) == ("filled", "2026-08-03", 100.0)


def test_gap_through_the_limit_fills_at_the_open():
    """Open BELOW a buy limit fills at the open — better than the limit. Modelling it at the
    limit would quietly flatter every gap-down entry in the ledger."""
    bars = [_bar("2026-08-03", 97.0, 98.0, 96.0, 97.5)]
    assert O.resolve(bars, 100.0, "long", expiry_d=3) == ("filled", "2026-08-03", 97.0)


def test_short_fills_on_a_high_and_gaps_at_the_open():
    up = [_bar("2026-08-03", 99.0, 101.0, 98.0, 100.5)]
    assert O.resolve(up, 100.0, "short", expiry_d=3) == ("filled", "2026-08-03", 100.0)
    gap = [_bar("2026-08-03", 103.0, 104.0, 102.0, 103.5)]
    assert O.resolve(gap, 100.0, "short", expiry_d=3) == ("filled", "2026-08-03", 103.0)


def test_expires_only_after_the_full_window():
    miss = [_bar(f"2026-08-0{d}", 105.0, 106.0, 104.0, 105.5) for d in (3, 4, 5)]
    assert O.resolve(miss[:2], 100.0, "long", expiry_d=3) is None      # still working
    assert O.resolve(miss, 100.0, "long", expiry_d=3) == ("expired", "2026-08-05", 0.0)


def test_a_touch_after_expiry_does_not_fill():
    """The 4th session is not ours — SMCI came back to a 1.5% limit on session 6 having already
    run +19.8% on day 1. That is a round-trip, not a bargain."""
    bars = [_bar("2026-08-03", 105.0, 106.0, 104.0, 105.0),
            _bar("2026-08-04", 105.0, 106.0, 104.0, 105.0),
            _bar("2026-08-05", 105.0, 106.0, 104.0, 105.0),
            _bar("2026-08-06", 101.0, 102.0, 99.0, 100.0)]      # would have touched
    assert O.resolve(bars, 100.0, "long", expiry_d=3) == ("expired", "2026-08-05", 0.0)


def test_first_touching_session_wins():
    bars = [_bar("2026-08-03", 105.0, 106.0, 104.0, 105.0),
            _bar("2026-08-04", 101.0, 102.0, 99.0, 100.0),
            _bar("2026-08-05", 98.0, 99.0, 95.0, 96.0)]
    assert O.resolve(bars, 100.0, "long", expiry_d=3)[1] == "2026-08-04"


# ---------------------------------------------------------------- the partial-bar guard

def test_the_in_progress_session_is_dropped():
    """Today's high/low are still being made. Resolving against them settles an order on a
    range that has not finished happening — the same artifact bets._score guards against."""
    bars = [_bar("2026-08-03", 101.0, 102.0, 99.5, 101.0),
            _bar("2026-08-04", 101.0, 102.0, 99.5, 101.0)]
    assert [b["date"] for b in O._complete(bars, today="2026-08-04")] == ["2026-08-03"]
    assert O._complete(bars, today="2026-08-03") == []


def test_countdown_reaches_zero_but_never_negative():
    assert O.sessions_left({}, []) == config.ORDER_EXPIRY_D
    assert O.sessions_left({}, [1] * (config.ORDER_EXPIRY_D + 4)) == 0


# ---------------------------------------------------------------- ledger integrity

def test_place_refuses_a_duplicate_working_order(monkeypatch):
    rows = [{"ticker": "DXCM", "status": "pending", "direction": "long",
             "shares": "5", "limit_px": "84.28"}]
    monkeypatch.setattr(O, "_load", lambda: rows)
    assert O.place(rows, "DXCM", "long", 76.80, 21, "XLV", shares=5) is False
    assert len(rows) == 1


def _wire_place(monkeypatch):
    from research import book, prices
    monkeypatch.setattr(prices, "daily_bars",
                        lambda s, n: [_bar("2026-08-03", 100.0, 101.0, 99.0, 100.0)])
    monkeypatch.setattr(O, "_complete", lambda bars, today=None: bars)

    def boom(*a, **k):
        raise AssertionError("counterfactual place must never read the book")
    for name in ("_load", "_cash", "_open_positions", "equity_marks"):
        monkeypatch.setattr(book, name, boom)


def test_place_is_unsized_and_never_reads_the_book(monkeypatch):
    """[ARC 5 #12a]: no cash, no equity, no sizing — a counterfactual order writes a blank
    shares column and must not touch book.* at all (the retired coupling)."""
    _wire_place(monkeypatch)
    rows = []
    assert O.place(rows, "AAA", "long", 80.0, 21, "SPY") is True
    assert rows[0]["shares"] == ""
    assert rows[0]["status"] == "pending" and rows[0]["limit_px"] == "101.00"


def test_place_records_explicit_shares_as_annotation(monkeypatch):
    _wire_place(monkeypatch)
    rows = []
    assert O.place(rows, "AAA", "long", 80.0, 21, "SPY", shares=7) is True
    assert rows[0]["shares"] == "7"


def test_place_speaks_counterfactual_not_broker(monkeypatch, capsys):
    """The print is the read agent's card material — it must never instruct an execution."""
    _wire_place(monkeypatch)
    assert O.place([], "AAA", "long", 80.0, 21, "SPY") is True
    out = capsys.readouterr().out
    assert "COUNTERFACTUAL" in out and "nothing to execute" in out
    assert "GTC" not in out and "broker" not in out.lower()


def test_unknown_command_writes_nothing(monkeypatch, caplog):
    written = []
    monkeypatch.setattr(O, "_load", lambda: [])
    monkeypatch.setattr(O, "_save", lambda rows: written.append(rows))
    O.run(["setle"])            # typo
    assert written == []


def test_stats_ignores_unscored_and_other_statuses():
    rows = [{"status": "expired", "x21_pct": "+4.00"},
            {"status": "expired", "x21_pct": "-2.00"},
            {"status": "expired", "x21_pct": ""},          # unscored -> ignored
            {"status": "filled", "x21_pct": "+9.00"}]      # other status -> ignored
    n, med, beat = O.stats(rows, "expired")
    assert (n, med, beat) == (2, 1.0, 50.0)
    assert O.stats(rows, "cancelled") is None


def test_retired_broker_verbs_are_unknown_and_write_nothing(monkeypatch, caplog):
    """`placed`/`pulled` retired with the broker leg [ARC 5 #12a] — they must fall through to
    the unknown-command error, and an unknown command never writes."""
    written = []
    monkeypatch.setattr(O, "_load", lambda: [{"ticker": "TPR", "status": "pending"}])
    monkeypatch.setattr(O, "_save", lambda rows: written.append(rows))
    O.run(["placed", "TPR"])
    O.run(["pulled", "TPR"])
    assert written == []
    assert not hasattr(O, "placed") and not hasattr(O, "pulled")


def test_load_backfills_columns_added_after_a_row_was_written(tmp_path, monkeypatch):
    """A schema change must not make an older row raise KeyError mid-resolve and take the
    whole pass down with it."""
    p = tmp_path / "orders.csv"
    p.write_text("logged_at,ticker,status\n2026-08-03,DXCM,pending\n")
    monkeypatch.setattr(O, "LEDGER", str(p))
    row = O._load()[0]
    assert row["ticker"] == "DXCM"
    assert row["placed_at"] == "" and row["limit_px"] == ""      # backfilled, not missing


# booked()/booked_lot() tests died with the functions in digest v2 [ARC 5 #12a].

_ORDER = {**{k: "" for k in O.FIELDS}, "ticker": "DXCM", "direction": "long",
          "status": "pending", "logged_at": "2026-08-03T18:46:15+00:00",
          "shares": "5", "ref": "83.45", "ref_date": "2026-07-31", "scan_from": "2026-08-03",
          "limit_px": "84.28", "stop_px": "76.80", "placed_at": "2026-08-03"}


def test_check_goes_loud_on_empty_bars(monkeypatch):
    """bars_after fails soft to [] — resolve() reads that as 'still working' and a feed flake
    strands the row pending forever with no alarm (DXCM 2026-08-06). Zero complete bars where
    ≥2 weekday sessions have elapsed ⇒ the ticker lands in `failed` and run() exits nonzero
    so daily.sh's FAILS → 🚨 heartbeat sees it."""
    from research import prices
    monkeypatch.setattr(prices, "bars_after", lambda *a, **k: [])
    monkeypatch.setattr(O, "_today", lambda: "2026-08-06")
    stale = {**_ORDER, "scan_from": "2026-08-01"}        # 3 weekdays elapsed, no bars
    n, failed = O.check([stale])
    assert failed == ["DXCM"] and n == 0
    monkeypatch.setattr(O, "_load", lambda: [dict(stale)])
    monkeypatch.setattr(O, "_save", lambda rows: None)
    monkeypatch.setattr(O, "score", lambda rows: 0)
    assert O.run(["check"]) == 1


def test_check_stays_quiet_on_a_day_old_order(monkeypatch):
    """An order anchored yesterday legitimately has zero complete bars — no false alarm."""
    from research import prices
    monkeypatch.setattr(prices, "bars_after", lambda *a, **k: [])
    monkeypatch.setattr(O, "_today", lambda: "2026-08-06")
    fresh = {**_ORDER, "scan_from": "2026-08-05"}        # 0 weekdays strictly between
    n, failed = O.check([fresh])
    assert failed == [] and n == 0


# --------------------------------------- check() is pure bars since [ARC 5 #12a] (no broker)

_DVA_ORDER = {**{k: "" for k in O.FIELDS}, "ticker": "DVA", "direction": "long",
              "status": "pending", "logged_at": "2026-08-07T13:53:08+00:00", "shares": "2",
              "ref": "180.67", "ref_date": "2026-08-06", "scan_from": "2026-08-07",
              "limit_px": "178.00", "stop_px": "169.00", "placed_at": "2026-08-07"}

# Real DVA sessions after the 08-07 anchor — the 178 limit is never touched again.
_DVA_BARS = [_bar("2026-08-10", 182.33, 183.95, 180.55, 183.69),
             _bar("2026-08-11", 183.70, 185.00, 183.00, 184.50),
             _bar("2026-08-12", 184.50, 186.00, 184.00, 185.00)]


def test_check_expires_an_untouched_order_from_bars_alone(monkeypatch):
    """The expired arm is the diagnostic's whole point — 'what did refusing to chase cost us?'
    is unanswerable without the no-fills."""
    from research import prices
    monkeypatch.setattr(prices, "bars_after", lambda *a, **k: _DVA_BARS)
    monkeypatch.setattr(O, "_complete", lambda bars, today=None: bars)
    row = dict(_DVA_ORDER)
    assert O.check([row]) == (1, [])
    assert row["status"] == "expired" and row["resolved_on"] == "2026-08-12"


def test_check_never_reads_the_book(monkeypatch):
    """The booked-fill precedence (the DVA 2026-08-11 fix) retired with the book [ARC 5 #12a]:
    bars are the only resolver now — a book lookup here would be dead real-money coupling."""
    from research import book, prices

    def boom(*a, **k):
        raise AssertionError("counterfactual check must never read the book")
    monkeypatch.setattr(book, "_load", boom)
    monkeypatch.setattr(prices, "bars_after", lambda *a, **k: _DVA_BARS)
    monkeypatch.setattr(O, "_complete", lambda bars, today=None: bars)
    row = dict(_DVA_ORDER)
    assert O.check([row]) == (1, [])
    assert row["status"] == "expired"


def test_retired_book_reconciliation_is_fully_gone():
    """digest v2 deleted booked()/booked_lot() — a revenant would mean broker-era coupling
    crept back in without a fresh pre-registration."""
    assert not hasattr(O, "booked") and not hasattr(O, "booked_lot")
