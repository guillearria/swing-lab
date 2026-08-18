"""Guard the forward-bet catalogue: no-lookahead gate + direction-aware scoring."""
from datetime import date, timedelta

import pytest

from research import bets as B


def _bars(start: str, n: int, step: float):
    d0 = date.fromisoformat(start)
    out, px = [], 100.0
    for i in range(n):
        out.append({"date": (d0 + timedelta(days=i)).isoformat(), "close": px})
        px *= (1 + step)
    return out


def test_none_until_matured():
    assert B._score(_bars("2025-02-01", 9, 0.0), _bars("2025-02-01", 9, 0.0),
                    "long", 10, "2025-01-15") is None


def test_rejects_lookahead():
    with pytest.raises(ValueError):
        B._score(_bars("2025-01-01", 70, 0.0), _bars("2025-01-01", 70, 0.0),
                 "long", 63, "2025-01-15")


def test_refuses_a_still_open_final_bar():
    """PARTIAL-BAR GUARD: yfinance reports the in-progress session as the latest close, so a
    mid-session settle scores against a price that is still moving — and the row then closes
    forever with that artifact. It happened on 2026-07-27 (MU booked -8.65% off an intraday
    SOXX print; the true figure vs the final close is -7.99%)."""
    bars = _bars("2025-02-01", 63, 0.001)
    last = bars[62]["date"]                       # the bar the score would land on
    assert B._score(bars, bars, "long", 63, "2025-01-15", today=last) is None
    # one day later that same bar is a completed session → scores normally
    later = (date.fromisoformat(last) + timedelta(days=1)).isoformat()
    assert B._score(bars, bars, "long", 63, "2025-01-15", today=later) is not None


def test_guard_is_on_by_default():
    """Omitting `today` must NOT bypass the gate — bars dated in the future are refused
    against the real clock, so a caller cannot silently opt out."""
    future = (date.today() + timedelta(days=5)).isoformat()
    bars = _bars(future, 63, 0.001)
    assert B._score(bars, bars, "long", 63, "2025-01-15") is None


def test_direction_sign():
    stock = _bars("2025-02-01", 70, 0.001)   # stock rises
    flat = _bars("2025-02-01", 70, 0.0)      # benchmark flat
    _, _, ex_long = B._score(stock, flat, "long", 63, "2025-01-15")
    _, _, ex_short = B._score(stock, flat, "short", 63, "2025-01-15")
    assert ex_long > 0 and ex_short < 0          # long wins, short loses on the same move
    assert abs(ex_long + ex_short) < 1e-9         # exact sign flip


def test_add_sets_pattern_tag(monkeypatch):
    monkeypatch.setattr(B, "median_dollar_vol", lambda t, today=None: 10_000_000.0)
    rows = []
    assert B.add(rows, "abc", "long", 63, "spy", "a thesis", "guidance-cut-overreaction")
    assert rows[0]["pattern_tag"] == "guidance-cut-overreaction"
    assert set(rows[0]) == set(B.FIELDS)          # row carries exactly the schema, no more/less
    assert B.add(rows, "xyz", "long", 21, "iwm", "t")   # tag omitted
    assert rows[1]["pattern_tag"] == ""           # defaults empty


# ── admission rule [ARC 5 #12a]: LONG-ONLY + the fail-closed liquidity floor ────────────────

def test_add_refuses_shorts(monkeypatch, capsys):
    """Long-only admission — a short is refused BEFORE any price fetch (re-arm path only)."""
    monkeypatch.setattr(B, "median_dollar_vol",
                        lambda t, today=None: (_ for _ in ()).throw(AssertionError("fetched")))
    rows = []
    assert B.add(rows, "TTD", "short", 21, "IGV", "t") is False
    assert rows == [] and "LONG-ONLY" in capsys.readouterr().out


def test_add_floor_refuses_thin_names(monkeypatch, capsys):
    monkeypatch.setattr(B, "median_dollar_vol", lambda t, today=None: 4_999_999.0)
    rows = []
    assert B.add(rows, "THIN", "long", 21, "IWM", "t") is False
    assert rows == [] and "floor" in capsys.readouterr().out


def test_add_floor_is_fail_closed_when_unverifiable(monkeypatch, capsys):
    """A gate that opens on a fetch failure is not a gate — None refuses."""
    monkeypatch.setattr(B, "median_dollar_vol", lambda t, today=None: None)
    rows = []
    assert B.add(rows, "DEAD", "long", 21, "SPY", "t") is False
    assert rows == [] and "UNVERIFIABLE" in capsys.readouterr().out


def _liq_bars(n, dollar=6_000_000.0, start="2026-07-01", price=100.0):
    d0 = date.fromisoformat(start)
    return [{"date": (d0 + timedelta(days=i)).isoformat(),
             "close": price, "volume": dollar / price} for i in range(n)]


def test_median_dollar_vol_uses_completed_bars_only(monkeypatch):
    """The in-progress bar is excluded (same partial-bar discipline as _score) and short
    history returns None rather than a number computed on less than the window."""
    bars = _liq_bars(20) + [{"date": "2026-08-15", "close": 100.0, "volume": 1e9}]
    monkeypatch.setattr(B.prices, "daily_bars", lambda t, n: bars)
    dv = B.median_dollar_vol("X", today="2026-08-15")   # today's 1e9-share bar must not count
    assert dv == 6_000_000.0
    monkeypatch.setattr(B.prices, "daily_bars", lambda t, n: _liq_bars(19))
    assert B.median_dollar_vol("X", today="2026-08-15") is None   # <20 completed → None
    monkeypatch.setattr(B.prices, "daily_bars",
                        lambda t, n: (_ for _ in ()).throw(OSError("egress")))
    assert B.median_dollar_vol("X", today="2026-08-15") is None   # fetch raises → None


def test_run_add_saves_nothing_on_refusal(tmp_path, monkeypatch):
    monkeypatch.setattr(B, "CATALOGUE", str(tmp_path / "bets.csv"))
    monkeypatch.setattr(B, "median_dollar_vol", lambda t, today=None: None)
    assert B.run(["add", "X", "long", "21", "SPY", "thesis"]) == 1
    assert B._load() == []                        # nothing written


# ── pooled verdict = LONG-ONLY [ARC 5 #12a]; _agg stays raw for the diagnostics ─────────────

def _closed(ticker, direction, excess):
    return {"logged_at": "2026-06-01T00:00:00+00:00", "ticker": ticker, "direction": direction,
            "horizon_d": "21", "benchmark": "SPY", "thesis": "t", "status": "closed",
            "entry_date": "2026-06-02", "entry": "10.00", "excess_pct": excess,
            "pattern_tag": "", "notified": "x"}


def test_stats_is_long_only_while_agg_keeps_shorts():
    rows = [_closed("L1", "long", "-5.00"), _closed("S1", "short", "+69.74")]
    n, _, md, beat = B.stats(rows)                # the verdict population: longs only
    assert (n, md, beat) == (1, -5.0, 0.0)
    an, _, amd, _ = B._agg(rows)                  # the raw diagnostic: both rows
    assert an == 2 and amd == pytest.approx(32.37)


def test_settle_msg_speaks_scored_results_and_the_plain_tally():
    """[MSG v3, 2026-08-18]: 📊 SCORED per result (beat ✓ / miss stated plainly), 🧪 counts
    for the tally — never the 🚨 glyph, which now means failure only. A settling short is
    announced as diagnostic and the tally stays the long-only verdict population [#12a]."""
    done = [_closed("S1", "short", "+69.74")]
    msg = B.settle_msg(done, B.stats(done))       # a settling short with 0 settled longs
    assert "📊 SCORED — S1" in msg and "short — diagnostic" in msg
    assert "🧪 0 of 30 settled (long-only)" in msg
    assert "🚨" not in msg
    win = [_closed("L1", "long", "+2.00")]
    msg2 = B.settle_msg(win, B.stats(win))
    assert "📊 SCORED — L1 21d vs SPY: +2.00%, beat ✓" in msg2
    assert "🧪 now 1 of 30 settled · 1 of 1 beat · median +2.0%" in msg2
    loss = [_closed("L2", "long", "-3.10")]
    assert ", miss" in B.settle_msg(loss, B.stats(loss))


# ── wilcoxon_p [ARC 5 #12a]: the bar's significance test, computed at last ──────────────────

def test_wilcoxon_exact_small_n():
    assert B.wilcoxon_p([1, 2, 3, 4, 5]) == pytest.approx(1 / 32)      # n=5 all positive
    assert B.wilcoxon_p([1, 2, 3, 4, 5, 6]) == pytest.approx(1 / 64)   # n=6 all positive
    assert B.wilcoxon_p([-1, -2, -3, -4, -5]) == pytest.approx(1.0)    # all negative → p=1


def test_wilcoxon_handles_ties_and_zeros():
    # |values| = [1,2,3,1] → tied ranks 1.5/1.5 → doubled-rank DP: P(W+ ≥ 8.5) = 3/16
    assert B.wilcoxon_p([1, 2, 3, -1]) == pytest.approx(3 / 16)
    assert B.wilcoxon_p([0, 1, 2, 3, -1, 0]) == pytest.approx(3 / 16)  # zeros dropped
    assert B.wilcoxon_p([0.0, 0]) is None                              # nothing left → None
    assert B.wilcoxon_p([]) is None


def test_wilcoxon_on_the_locked_live_vector():
    """The [ARC 5 #12a] lock-time long-only vector: one winner ranked 3rd of 5 → W+=3,
    P(W+ ≥ 3) = 29/32 ≈ 0.906 — nowhere near α, exactly as an adverse pool should read."""
    assert B.wilcoxon_p([-7.99, 15.28, -6.17, -33.30, -19.09]) == pytest.approx(29 / 32)


def test_wilcoxon_normal_approx_branch_behaves():
    """n>50 takes the normal-approximation branch: a uniformly positive sample must be
    overwhelmingly significant, its mirror must not be, and both must be valid p-values."""
    pos = B.wilcoxon_p([float(i) for i in range(1, 61)])          # n=60, all positive
    neg = B.wilcoxon_p([-float(i) for i in range(1, 61)])
    assert pos is not None and pos < 1e-6
    assert neg is not None and neg > 0.999
    mixed = B.wilcoxon_p([(-1.0) ** i * i for i in range(1, 61)])  # alternating signs
    assert mixed is not None and 0.0 <= mixed <= 1.0


def test_settle_isolates_a_poisoned_row(monkeypatch):
    """One unscoreable bet must NOT abort scoring for the whole catalogue.

    Before 2026-07-27 _score's lookahead ValueError propagated out of settle(), so a single
    bad row blocked every other bet and daily.sh reported only "bets failed".
    """
    good = {"logged_at": "2025-01-15T00:00:00+00:00", "ticker": "GOOD", "direction": "long",
            "horizon_d": "63", "benchmark": "SPY", "status": "open"}
    bad = dict(good, ticker="BAD")

    def bars(sym, day, n):
        # BAD's first bar predates the prereg day → _score raises lookahead
        return _bars("2025-01-01" if sym == "BAD" else "2025-02-01", 70,
                     0.001 if sym == "GOOD" else 0.0)
    monkeypatch.setattr(B.prices, "bars_after", bars)
    n, failed = B.settle([good, bad])
    assert n == 1 and failed == ["BAD"]           # good one scored, bad one NAMED
    assert good["status"] == "closed" and bad["status"] == "open"


def test_unannounced_selects_only_undelivered_settlements():
    rows = [{"status": "closed", "notified": ""},               # 🚨 never landed → retry
            {"status": "closed", "notified": "2026-07-27T00:00:00+00:00"},  # already sent
            {"status": "open", "notified": ""}]                 # not settled yet
    assert B.unannounced(rows) == [rows[0]]


def _settled_row(ticker="MU"):
    return {"logged_at": "2025-01-15T00:00:00+00:00", "ticker": ticker, "direction": "long",
            "horizon_d": "21", "benchmark": "SOXX", "thesis": "t", "status": "closed",
            "entry_date": "2025-02-01", "entry": "100.00", "excess_pct": "-8.65",
            "pattern_tag": "", "notified": ""}


def test_failed_push_keeps_settlement_unannounced_and_exits_nonzero(tmp_path, monkeypatch):
    """The MU regression: a settlement whose 🚨 is lost must stay retryable AND be
    reported as a failed step — it used to exit 0 with the message gone forever."""
    monkeypatch.setattr(B, "CATALOGUE", str(tmp_path / "bets.csv"))
    B._save([_settled_row()])
    monkeypatch.setattr(B.prices, "bars_after", lambda *a: [])
    import research.notify as N
    monkeypatch.setattr(N, "send", lambda *a, **k: False)       # telegram down

    assert B.run(["settle"]) == 1                               # daily.sh now counts it
    assert B._load()[0]["notified"] == ""                       # still owed an announcement


def test_next_run_resends_then_stamps_and_stops(tmp_path, monkeypatch):
    """Recovery: the retry set comes from the LEDGER, so the next run re-sends the lost
    message, stamps it on confirmed delivery, and never sends it twice."""
    monkeypatch.setattr(B, "CATALOGUE", str(tmp_path / "bets.csv"))
    B._save([_settled_row()])
    monkeypatch.setattr(B.prices, "bars_after", lambda *a: [])
    sent = []
    import research.notify as N
    monkeypatch.setattr(N, "send", lambda text, **k: sent.append(text) or True)

    assert B.run(["settle"]) == 0
    assert len(sent) == 1 and "MU" in sent[0]
    assert B._load()[0]["notified"]                             # stamped only after delivery

    assert B.run(["settle"]) == 0
    assert len(sent) == 1                                       # not re-announced


def test_save_backfills_old_schema_rows(tmp_path, monkeypatch):
    # [Arc 5 #8] backward-compat proof: a PRE-pattern_tag row must round-trip through _save/_load
    # as "" with no error — so an in-flight nightly settle on an old-schema CSV is safe.
    monkeypatch.setattr(B, "CATALOGUE", str(tmp_path / "bets.csv"))
    old = {k: "" for k in B.FIELDS if k != "pattern_tag"}   # row WITHOUT the new column
    old.update(logged_at="2025-01-01T00:00:00+00:00", ticker="OLD", direction="long",
               horizon_d="63", benchmark="SPY", thesis="legacy", status="open")
    B._save([old])
    back = B._load()
    assert back[0]["pattern_tag"] == "" and back[0]["ticker"] == "OLD"


def test_next_maturity_picks_the_earliest_open_bet():
    """horizon_d counts TRADING days, so the walk is weekday-only: a 21d bet logged Tue 08-04
    lands on 09-02, not 08-25."""
    rows = [{"logged_at": "2026-08-04T12:00:00+00:00", "ticker": "SMCI", "horizon_d": "21",
             "status": "open"},
            {"logged_at": "2026-08-04T12:00:00+00:00", "ticker": "SLOW", "horizon_d": "63",
             "status": "open"},
            {"logged_at": "2026-01-01T12:00:00+00:00", "ticker": "DONE", "horizon_d": "1",
             "status": "closed"}]                       # closed rows can never be "next"
    assert B.next_maturity(rows) == ("2026-09-02", "SMCI")


def test_next_maturity_is_none_with_nothing_open():
    assert B.next_maturity([]) is None
    assert B.next_maturity([{"logged_at": "2026-08-04", "ticker": "X", "horizon_d": "21",
                             "status": "closed"}]) is None


def test_next_maturity_skips_a_corrupt_row_rather_than_dying():
    """A hand-edited row must not take the whole BETS line down with it."""
    rows = [{"logged_at": "not-a-date", "ticker": "BAD", "horizon_d": "21", "status": "open"},
            {"logged_at": "2026-08-04T12:00:00+00:00", "ticker": "OK", "horizon_d": "21",
             "status": "open"}]
    assert B.next_maturity(rows) == ("2026-09-02", "OK")


def test_next_maturity_never_advertises_a_date_in_the_past():
    """A bet past its horizon and still open is settling today or STUCK (the digest has its own
    alarm for that) — it is not "next". Without this the headline sold a past date as the next
    evidence, precisely when something was already broken."""
    from datetime import date, timedelta
    old = (date.today() - timedelta(days=400)).isoformat()
    soon = date.today().isoformat()
    got = B.next_maturity([
        {"logged_at": old + "T00:00:00+00:00", "ticker": "STUCK", "horizon_d": "21",
         "status": "open"},
        {"logged_at": soon + "T00:00:00+00:00", "ticker": "REAL", "horizon_d": "21",
         "status": "open"}])
    assert got is not None and got[1] == "REAL"
    assert got[0] >= date.today().isoformat()

    # every open bet already matured -> no honest date to give
    assert B.next_maturity([{"logged_at": old + "T00:00:00+00:00", "ticker": "STUCK",
                             "horizon_d": "21", "status": "open"}]) is None


def test_catalogue_survives_a_save_crash_and_malformed_rows_are_named(tmp_path, monkeypatch):
    """The 2026-08-18 orders incident, guarded here too: a hand-edit's unquoted comma must be
    refused BY NAME at load, and a writer crash must leave the file untouched (write-then-
    replace), never truncated mid-save."""
    p = tmp_path / "bets.csv"
    p.write_text("logged_at,ticker\n2026-08-03,AAPL,OVERFLOW\n")
    monkeypatch.setattr(B, "CATALOGUE", str(p))
    with pytest.raises(ValueError, match="AAPL"):
        B._load()
    original = p.read_text()
    with pytest.raises(ValueError):
        B._save([{None: ["overflow"]}])
    assert p.read_text() == original
