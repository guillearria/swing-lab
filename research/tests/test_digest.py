"""Guard the digest assembly: DO-NOW list, the quiet 'nothing' path, and fail-soft."""
import pytest

from research import digest as D

# Captured before the autouse fixture below can stub them out, so the two sections that
# read the real repo/filesystem can still be tested directly.
_REAL_GIT, _REAL_FEED = D._git_section, D._feed_section
_REAL_STRANDED, _REAL_ORDERS = D._stranded_section, D._orders_section
_REAL_BOARD = D._pool_scoreboard
_REAL_PUSHLOG = D._pushlog_section


def _mk(**kw) -> dict:
    """A synthetic `book.equity_marks` result — the ONE seam the digest reads the book through.

    Tests used to stub three or four `book` privates each (_cash, _open_positions, _seed_row,
    _spot); since the digest stopped re-deriving equity itself there is a single thing to fake.
    """
    return {"cash": 0.0, "equity": 0.0, "unrealized": 0.0, "realized": 0.0, "lines": [],
            "spots": {}, "seed": None, "spy_equiv": None, "dualmom_equiv": None,
            "dualmom_hold": None, **kw}


@pytest.fixture(autouse=True)
def _neutralize_environment_sections(monkeypatch):
    """These inspect the actual repo, remote, data dir and equity log, so they would make
    every compose test depend on this checkout's state (and _stranded_section / _delta_band
    would hit the NETWORK and git). Stub them by default; each has its own dedicated test."""
    monkeypatch.setattr(D, "_git_section", lambda: ([], [], []))
    monkeypatch.setattr(D, "_stranded_section", lambda: ([], [], []))
    monkeypatch.setattr(D, "_feed_section", lambda: ([], [], []))
    monkeypatch.setattr(D, "_orders_section", lambda *a, **k: ([], [], []))   # reads orders.csv
    monkeypatch.setattr(D, "_pool_scoreboard", lambda: ([], [], []))  # shells out to git
    # _pushlog_section reads the LIVE research/data/push_log.csv — a real stranded-settle
    # alarm (e.g. the 2026-08-07 night) injected a DO-NOW into every compose test and broke
    # 4 of them. Same rule as the sections above: stub by default, dedicated test uses
    # _REAL_PUSHLOG against a tmp_path file.
    monkeypatch.setattr(D, "_pushlog_section", lambda: ([], [], []))
    # _marks is lru_cached for the life of the PROCESS, which in a test run is the whole
    # session — without this a mark faked by one test leaks into every later one.
    D._marks.cache_clear()
    # _book_section also consults the orders ledger (a working order silences the idle-cash
    # nag), so an un-stubbed load makes every cash test depend on what is really pending.
    from research import orders, prices
    monkeypatch.setattr(orders, "_load", lambda: [])
    # The order countdown fetches bars per pending order. Left live it puts a real yfinance call
    # in four existing tests (the suite went 1.6s -> 6.9s the moment it landed) and makes them
    # depend on the network. Empty bars = a full, unburned window, which is the neutral default.
    monkeypatch.setattr(prices, "bars_after", lambda *a, **k: [])


def test_compose_lists_actions_and_fyi(monkeypatch):
    monkeypatch.setattr(D, "_book_section", lambda *a, **k: (["X has NO stop"], [], ["book: eq"]))
    monkeypatch.setattr(D, "_bets_section", lambda: ([], ["Y maturing"], ["bets: 1 open"]))
    monkeypatch.setattr(D, "_movers_section", lambda: ([], [], ["movers: 0/0"]))
    out = D.compose()
    assert "DO NOW (1)" in out and "1. X has NO stop" in out
    assert "heads-up" in out and "Y maturing" in out
    assert "book: eq" in out and "movers: 0/0" in out          # state block carries every silo


def test_broken_silo_escalates_to_do_now(monkeypatch):
    """A dead silo must be an ACTION, not a quiet trailing line — the insider ledger was the
    intended 2nd verdict silo and could previously stop accruing evidence unnoticed."""
    def boom():
        raise ModuleNotFoundError("pandas")
    actions, _, lines = D._safe(boom, "movers")
    assert actions and "silo DOWN" in actions[0] and "ModuleNotFoundError" in actions[0]
    assert lines and "unavailable" in lines[0]      # still shown in the state block


def test_idle_cash_never_nags_in_the_paper_regime(monkeypatch):
    """The idle-cash bridge retired with the broker leg [ARC 5 #12a] — cash sitting in the
    (soon-frozen) book is reported as state, never as a DO-NOW."""
    from research import book
    monkeypatch.setattr(book, "_load", lambda: [{"__": "nonempty"}])
    monkeypatch.setattr(book, "_open_positions", lambda rows: [])
    monkeypatch.setattr(D, "_marks", lambda: _mk(cash=427.81, equity=427.81))
    actions, _, lines = D._book_section()
    assert not any("idle" in a for a in actions)
    assert "cash $428" in lines                     # the state line still reports it


def test_git_section_flags_uncommitted_ledgers(monkeypatch):
    """The 2026-07-27 bug: an alert claiming to be 'scored either way' while no row was
    committed. The digest now says so in the same message."""
    import subprocess
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: type(
        "R", (), {"stdout": " M research/bets_catalogue.csv\n"})())
    actions, _, _ = _REAL_GIT()
    assert actions and "uncommitted" in actions[0] and "NOT scored" in actions[0]


def test_stranded_section_flags_a_parked_backup_ref(monkeypatch):
    """A $FAILS heartbeat fires once, on the day of the strand. 1b014cc proved that is not
    enough — the alarm was seen, nothing was done, and master ran two days without the work.
    This nags every run until a human recovers the ref and deletes it."""
    import subprocess
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: type("R", (), {
        "stdout": "1b014ccf915596594d293b823a50a05f2c017ca6\trefs/heads/settle-backup/20260731-1b014cc\n"})())
    actions, _, _ = _REAL_STRANDED()
    assert len(actions) == 1
    assert "STRANDED" in actions[0] and "settle-backup/20260731-1b014cc" in actions[0]
    assert "cherry-pick" in actions[0] and "--delete" in actions[0]   # paste-ready cure


def test_stranded_section_silent_when_nothing_is_parked(monkeypatch):
    """The healthy case must add ZERO noise, or the DO-NOW list trains the human to skim it."""
    import subprocess
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: type("R", (), {"stdout": "\n"})())
    assert _REAL_STRANDED() == ([], [], [])


def test_stranded_section_silent_without_network(monkeypatch):
    """ls-remote is the only NETWORK call in the digest. Offline must degrade to silence, not
    take the whole push down — the digest is the daily proof-of-life."""
    import subprocess

    def boom(*a, **k):
        raise subprocess.TimeoutExpired("git", 20)
    monkeypatch.setattr(subprocess, "run", boom)
    assert _REAL_STRANDED() == ([], [], [])


def test_git_section_silent_without_git(monkeypatch):
    """Fail-soft: no git / no upstream must never add noise or break the push."""
    import subprocess

    def boom(*a, **k):
        raise FileNotFoundError("git")
    monkeypatch.setattr(subprocess, "run", boom)
    assert _REAL_GIT() == ([], [], [])


def test_feed_section_escalates_a_stale_source(tmp_path, monkeypatch):
    """A dead feed returns nothing rather than raising, so only a recorded last_ok can
    distinguish 'quiet day' from 'openinsider has been down for a week'."""
    import json
    from datetime import date, timedelta
    p = tmp_path / "feed.json"
    old = (date.today() - timedelta(days=21)).isoformat()
    p.write_text(json.dumps({"openinsider": {"last_ok": old, "last_error": "HTTP 503"}}))
    monkeypatch.setattr(D, "FEED_STATUS", str(p))
    actions, _, _ = _REAL_FEED()
    assert actions and "openinsider" in actions[0] and "HTTP 503" in actions[0]


def test_feed_section_never_invents_a_duration(tmp_path, monkeypatch):
    """A source with no last_ok has never succeeded — say THAT. The untested else-branch used
    a `99` sentinel, so the live alarm read "has not succeeded in 99 weekdays" when the real
    gap was 27. A fabricated number inside an alarm is how a DO-NOW list loses its authority."""
    import json
    p = tmp_path / "feed.json"
    p.write_text(json.dumps({"openinsider": {"last_error": "URLError: [Errno 111] refused"}}))
    monkeypatch.setattr(D, "FEED_STATUS", str(p))
    actions, _, _ = _REAL_FEED()
    assert actions and "NEVER reported a successful fetch" in actions[0]
    assert "99" not in actions[0]
    assert "Errno 111" in actions[0]        # the REAL cause, not "fetch returned no clusters"


def test_feed_section_quiet_when_fresh(tmp_path, monkeypatch):
    import json
    from datetime import date
    p = tmp_path / "feed.json"
    p.write_text(json.dumps({"openinsider": {"last_ok": date.today().isoformat()}}))
    monkeypatch.setattr(D, "FEED_STATUS", str(p))
    assert _REAL_FEED() == ([], [], [])
    monkeypatch.setattr(D, "FEED_STATUS", str(tmp_path / "missing.json"))
    assert _REAL_FEED() == ([], [], [])        # never written yet → claim nothing


def _feed_json(tmp_path, monkeypatch, st):
    import json
    p = tmp_path / "feed.json"
    p.write_text(json.dumps({"sp500-movers": st}))
    monkeypatch.setattr(D, "FEED_STATUS", str(p))


def test_feed_section_escalates_stale_bars_even_when_last_ok_is_fresh(tmp_path, monkeypatch):
    """The 2026-08-04 shape: the fetch succeeded TODAY but bars sat at 07-31 — the old check
    read only last_ok, so the run logged 0 movers with no alarm [FINDINGS 2026-08-04 ops]."""
    from datetime import date, timedelta
    d = date.today()
    old_bar = d - timedelta(days=7)                       # far past any FEED_BAR_STALE_D
    _feed_json(tmp_path, monkeypatch,
               {"last_ok": d.isoformat(), "last_bar": old_bar.isoformat(),
                "n_ok": 500, "n_total": 503})
    actions, _, _ = _REAL_FEED()
    assert actions and "bars last advanced" in actions[0]
    assert "denominator did not advance" in actions[0]


def test_feed_section_escalates_thin_coverage(tmp_path, monkeypatch):
    from datetime import date
    _feed_json(tmp_path, monkeypatch,
               {"last_ok": date.today().isoformat(), "n_ok": 250, "n_total": 503})
    actions, _, _ = _REAL_FEED()
    assert actions and "250/503" in actions[0] and "denominator is short" in actions[0]


def test_feed_section_fresh_bar_and_full_coverage_silent(tmp_path, monkeypatch):
    """A healthy pre-market shape — yesterday's completed bar, near-full coverage — is quiet.
    Uses a 1-weekday lag computed backwards so the test passes on any weekday."""
    from datetime import date, timedelta
    d = date.today()
    prev = d - timedelta(days=1)
    while prev.weekday() >= 5:
        prev -= timedelta(days=1)
    _feed_json(tmp_path, monkeypatch,
               {"last_ok": d.isoformat(), "last_bar": prev.isoformat(),
                "n_ok": 498, "n_total": 503})
    assert _REAL_FEED() == ([], [], [])


def test_feed_section_legacy_key_without_new_fields_silent(tmp_path, monkeypatch):
    from datetime import date
    _feed_json(tmp_path, monkeypatch, {"last_ok": date.today().isoformat()})
    assert _REAL_FEED() == ([], [], [])


def test_feed_section_weekend_gap_is_not_stale(tmp_path, monkeypatch):
    """Sat/Sun after a Friday scan: the newest possible bar is Thursday's, so a today-based
    lag reads 2 and false-alarmed BOTH cohorts all weekend 2026-08-08/09 (the first weekend
    the last_bar field was live). Lag is measured against the last SUCCESSFUL scan instead,
    which makes the healthy weekend shape = 1."""
    from datetime import date

    class _Sunday(date):
        @classmethod
        def today(cls):
            return cls(2026, 8, 9)                # the live false-positive Sunday

    monkeypatch.setattr(D, "date", _Sunday)
    _feed_json(tmp_path, monkeypatch,
               {"last_ok": "2026-08-07", "last_bar": "2026-08-06",
                "n_ok": 503, "n_total": 503})
    assert _REAL_FEED() == ([], [], [])


def test_feed_section_frozen_bars_with_live_scan_fires_at_the_threshold(tmp_path, monkeypatch):
    """The 2026-08-04 failure shape must survive the weekend fix at its minimal size: the
    fetch succeeds today while bars sit 2 weekdays behind the scan — still an alarm."""
    from datetime import date, timedelta
    d = date.today()
    prev = d - timedelta(days=1)
    while prev.weekday() >= 5:
        prev -= timedelta(days=1)
    prev2 = prev - timedelta(days=1)
    while prev2.weekday() >= 5:
        prev2 -= timedelta(days=1)                # 2 weekdays behind last_ok on ANY run day
    _feed_json(tmp_path, monkeypatch,
               {"last_ok": d.isoformat(), "last_bar": prev2.isoformat(),
                "n_ok": 503, "n_total": 503})
    actions, _, _ = _REAL_FEED()
    assert actions and "behind the last scan" in actions[0]


def test_feed_section_dead_scan_flags_on_the_second_missed_weekday(tmp_path, monkeypatch):
    """The 08-09 lag fix measures bars against the LAST scan, so a dead read routine freezes
    last_ok and last_bar together and the bar alarm can never fire — last_ok staleness is the
    only detector left, and nothing else watches the read leg (push_log alarms are
    settle-only, the watchdog watches settle's commits). At the old FEED_STALE_D=3 a dead
    scan rode THREE weekdays behind an all-clear DO-NOW; this pins escalation at the second
    missed weekday [2026-08-09 control review]."""
    from datetime import date, timedelta
    d = date.today()
    prev = d - timedelta(days=1)
    while prev.weekday() >= 5:
        prev -= timedelta(days=1)
    prev2 = prev - timedelta(days=1)
    while prev2.weekday() >= 5:
        prev2 -= timedelta(days=1)          # last scan 2 weekdays back = 2nd missed run
    _feed_json(tmp_path, monkeypatch,
               {"last_ok": prev2.isoformat(), "last_bar": prev2.isoformat(),
                "n_ok": 503, "n_total": 503})
    actions, _, _ = _REAL_FEED()
    assert actions and "has not succeeded" in actions[0]


# The liveness tests died with _liveness_section [ARC 5 #12a]: the frozen equity curve made
# the clock unclearable; _pushlog_section + the watchdog carry the "run stopped" alarm now.


def test_overdue_bet_escalates_but_holiday_drift_does_not(monkeypatch):
    """A bet a day or two "overdue" is holiday drift (July 4 is why MU showed -1d while
    maturing on time). Genuinely stuck ones must leave the passive list and become an action."""
    from datetime import date, timedelta
    from research import bets

    def row(ticker, busdays_elapsed, horizon=21):
        d = date.today()
        back = 0
        while busdays_elapsed > 0:               # walk back that many weekdays
            back += 1
            if (d - timedelta(days=back)).weekday() < 5:
                busdays_elapsed -= 1
        return {"logged_at": (d - timedelta(days=back)).isoformat(), "ticker": ticker,
                "horizon_d": str(horizon), "status": "open", "benchmark": "SPY",
                "direction": "long", "excess_pct": "", "pattern_tag": ""}

    monkeypatch.setattr(bets, "_load", lambda: [row("DRIFT", 22), row("STUCK", 40)])
    actions, _, lines = D._bets_section()
    assert actions and "settlement STUCK" in actions[0] and "STUCK overdue" in actions[0]
    assert "DRIFT" not in actions[0]             # -1d is normal, not an alarm
    assert any("DRIFT(-1d)" in l for l in lines)   # still shown passively (mix line rides too)


def test_compose_none_path(monkeypatch):
    for name in ("_book_section", "_bets_section", "_movers_section"):
        monkeypatch.setattr(D, name, lambda *a, **k: ([], [], ["s"]))
    assert "DO NOW: nothing" in D.compose()


def test_multiline_action_keeps_code_line_whole(monkeypatch):
    """Paste-ready <code> lines ride under their numbered item, tags intact on one line."""
    monkeypatch.setattr(D, "_book_section",
                        lambda *a, **k: (["X THROUGH stop — exit:\n<code>book close X</code>"],
                                         [], ["b"]))
    monkeypatch.setattr(D, "_bets_section", lambda: ([], [], ["t"]))
    monkeypatch.setattr(D, "_movers_section", lambda: ([], [], ["m"]))
    lines = D.compose().split("\n")
    assert "1. X THROUGH stop — exit:" in lines
    assert "<code>book close X</code>" in lines                 # own line, tag not split


def test_tags_never_span_lines(monkeypatch):
    """The notify truncation cuts at a newline — every tag must open+close on one line."""
    monkeypatch.setattr(D, "_book_section",
                        lambda: (["a:\n<code>cmd</code>"], [], ["<b>BOOK</b> $1", "T 1 @ 2→3"]))
    monkeypatch.setattr(D, "_bets_section", lambda: ([], [], ["<b>BETS</b> 0"]))
    monkeypatch.setattr(D, "_movers_section", lambda: ([], [], ["<b>MOVERS</b> 0"]))
    for line in D.compose().split("\n"):
        assert line.count("<b>") == line.count("</b>")
        assert line.count("<code>") == line.count("</code>")


def test_no_blank_gap_from_alarm_only_sections(monkeypatch):
    """Regression [2026-08-04, user-reported]: git/stranded/feed/liveness only ever return
    DO-NOW *actions* and never display lines, but compose() emitted a separator per section
    unconditionally — so EVERY message ended in five blank lines, a wall of dead space right
    where the eye stops reading. A section with nothing to show gets no separator."""
    for name in ("_book_section", "_bets_section", "_movers_section"):
        monkeypatch.setattr(D, name, lambda *a, **k: ([], [], ["s"]))
    out = D.compose()
    assert "\n\n\n" not in out                      # never two blank lines in a row
    assert out.rstrip("\n") == out                  # and no trailing blanks at all


def test_run_note_splits_headline_from_body(monkeypatch):
    """The read run's note is a headline plus multi-line 5a/5b alert blocks. Prepending it WHOLE
    pushed the DO-NOW list ~15 lines down and duplicated the ORDERS section above it. Line 1 is
    the headline (the Telegram preview); the body goes to a RUN NOTE block at the bottom."""
    monkeypatch.setattr(D, "_book_section", lambda *a, **k: (["X has NO stop"], [], ["book: eq"]))
    for name in ("_bets_section", "_movers_section"):
        monkeypatch.setattr(D, name, lambda *a, **k: ([], [], ["s"]))
    lines = D.compose("📖 read run: 2 bets\n🟢 ORDER — BUY 5 DXCM\nref 83.45").split("\n")
    assert lines[0] == "<b>📖 read run: 2 bets</b>"          # headline on top, bolded
    assert lines.index("1. X has NO stop") < lines.index("🟢 ORDER — BUY 5 DXCM")
    assert "📖 <b>RUN NOTE</b>" in lines                     # body demoted to its own block
    assert "ref 83.45" in lines


def test_run_note_body_is_escaped_and_never_splits_a_tag(monkeypatch):
    """The note is free text from the read agent — it must not be able to inject markup or
    hand notify a half-tag to truncate on."""
    for name in ("_book_section", "_bets_section", "_movers_section"):
        monkeypatch.setattr(D, name, lambda *a, **k: ([], [], ["s"]))
    out = D.compose("head <b>x</b> & co\nbody <i>y</i> & <code>z")
    assert "head &lt;b&gt;x&lt;/b&gt; &amp; co" in out
    assert "body &lt;i&gt;y&lt;/i&gt; &amp; &lt;code&gt;z" in out
    for line in out.split("\n"):
        assert line.count("<b>") == line.count("</b>")
        assert line.count("<code>") == line.count("</code>")


def test_empty_note_adds_nothing(monkeypatch):
    """settle passes no note; its message must be byte-identical to the plain compose()."""
    for name in ("_book_section", "_bets_section", "_movers_section"):
        monkeypatch.setattr(D, name, lambda *a, **k: ([], [], ["s"]))
    assert D.compose("") == D.compose() and D.compose().startswith("📋 <b>DIGEST")


# ------------------------- the 🎯 POOL scoreboard [ARC 5 #12a digest v2] — replaces the band
# The band's book half (equity delta, mark_delta, blind-price guard) retired with the book; its
# ledger-diff half survives verbatim as the Δ-since-HEAD line and keeps its regression tests.

_L = {"logged_at": "2026-06-01T00:00:00+00:00", "direction": "long", "horizon_d": "21",
      "benchmark": "SPY", "thesis": "t", "pattern_tag": "", "notified": "x",
      "entry_date": "2026-06-02", "entry": "10.00"}


def _closed_bet(ticker, excess, direction="long"):
    return {**_L, "ticker": ticker, "direction": direction, "status": "closed",
            "excess_pct": excess}


def _open_bet(ticker, direction="long"):
    return {**_L, "ticker": ticker, "direction": direction, "status": "open",
            "excess_pct": "", "entry_date": "", "entry": ""}


# The lock-time live vector [ARC 5 #12a]: long-only n=5 median −7.99% beat 20% p=29/32,
# plus the ILLR short that the long-only rule strips from the verdict.
_LIVE_POOL = [_closed_bet("MU", "-7.99"), _closed_bet("ON", "+15.28"),
              _closed_bet("AYI", "-6.17"), _closed_bet("BB", "-33.30"),
              _closed_bet("CIEN", "-19.09"), _closed_bet("ILLR", "+69.74", "short")]


def _board(monkeypatch, rows, head_rows=None):
    """Drive the real _pool_scoreboard with a faked catalogue + faked HEAD copy."""
    from research import bets, movers, orders
    monkeypatch.setattr(bets, "_load", lambda: list(rows))
    monkeypatch.setattr(movers, "_load", lambda: [])
    monkeypatch.setattr(orders, "_load", lambda: [])
    monkeypatch.setattr(D, "_committed", lambda p: {
        bets.CATALOGUE: list(head_rows if head_rows is not None else rows),
        movers.LEDGER: [], orders.LEDGER: []}[p])
    return _REAL_BOARD()


def test_scoreboard_headline_carries_the_verdict_numbers(monkeypatch):
    """The owner's one ask: performance-vs-bar leads the message. Long-only n/median/beat,
    Σ equal-weight vs OWN benchmarks, the computed Wilcoxon p, and the distance to the bar."""
    actions, _, lines = _board(monkeypatch, _LIVE_POOL)
    assert actions == []                        # the scoreboard never asks for anything
    pool = next(l for l in lines if "POOL" in l)
    assert "n=5 settled (long-only)" in pool
    assert "median -7.99%" in pool and "beat 20%" in pool
    assert "Σ -51.3pp (equal-wt, own benchmarks)" in pool
    assert "p=0.91" in pool                     # 29/32 — the exact DP, not a decoration
    assert "25 to go" in pool and "N≥30" in pool


def test_scoreboard_shows_the_short_contrast_below_bar(monkeypatch):
    _, _, lines = _board(monkeypatch, _LIVE_POOL)
    sh = next(l for l in lines if "shorts" in l)
    assert "diagnostic, below-bar" in sh and "n=1" in sh and "+69.74%" in sh


def test_scoreboard_zero_settled_prints_the_bar_and_no_p(monkeypatch):
    _, _, lines = _board(monkeypatch, [_open_bet("NOW")])
    pool = next(l for l in lines if "POOL" in l)
    assert "0 settled (long-only)" in pool and "N≥30" in pool
    assert "p=" not in pool


def test_pass_candidate_appears_from_n10_and_is_labeled_below_bar(monkeypatch):
    """The early-shape flag can never be quoted as a pass — the label travels with it."""
    ten = [_closed_bet(f"T{i}", "+3.00") for i in range(10)]
    _, _, lines = _board(monkeypatch, ten)
    pc = next(l for l in lines if "PASS-CANDIDATE" in l)
    assert "below-bar" in pc and "N≥30" in pc

    nine = ten[:9]
    _, _, lines2 = _board(monkeypatch, nine)
    assert not any("PASS-CANDIDATE" in l for l in lines2)   # n=9: no flag, however pretty


def test_milestone_fires_only_on_a_crossing(monkeypatch):
    """Stateless: HEAD had 9 settled longs, the tree has 10 → banner. HEAD already at 10 →
    quiet. Depends on daily.sh running the digest BEFORE push_ledgers commits."""
    ten = [_closed_bet(f"T{i}", "+1.00") for i in range(10)]
    _, _, lines = _board(monkeypatch, ten, head_rows=ten[:9])
    assert any("MILESTONE" in l and "n=10" in l for l in lines)

    _, _, lines2 = _board(monkeypatch, ten + [_closed_bet("T11", "+1.00")], head_rows=ten)
    assert not any("MILESTONE" in l for l in lines2)        # 10→11 is not a crossing


def test_scoreboard_never_reads_the_book(monkeypatch):
    """The band's book coupling is dead: no marks, no equity, no curve — a retired OR live
    book changes nothing here."""
    from research import book
    def boom(*a, **k):
        raise AssertionError("the scoreboard must not touch the book")
    monkeypatch.setattr(book, "_load", boom)
    monkeypatch.setattr(book, "equity_marks", boom)
    monkeypatch.setattr(D, "_marks", boom)
    _, _, lines = _board(monkeypatch, _LIVE_POOL)
    assert any("POOL" in l for l in lines)


def test_delta_line_counts_what_the_ledgers_gained_since_the_commit(monkeypatch):
    """Row-level against HEAD — so it needs no settled_at/scored_at column in any silo, which is
    exactly the cost the 2026-07-10 'fold the 🚨s in' rejection refused to pay."""
    was_bet = {"logged_at": "2026-07-01T00:00:00+00:00", "ticker": "SMCI", "status": "open",
               "excess_pct": ""}
    now_bet = {**was_bet, "status": "closed", "excess_pct": "+4.20"}
    fresh = {"logged_at": "2026-08-04T00:00:00+00:00", "ticker": "NEW", "status": "open",
             "excess_pct": ""}
    from research import bets, movers, orders
    monkeypatch.setattr(D, "_committed", lambda p: {
        bets.CATALOGUE: [was_bet], movers.LEDGER: [], orders.LEDGER: [_order()]}[p])
    monkeypatch.setattr(bets, "_load", lambda: [now_bet, fresh])
    monkeypatch.setattr(movers, "_load", lambda: [])
    monkeypatch.setattr(orders, "_load", lambda: [_order(status="filled")])
    line = _REAL_BOARD()[2][-1]                 # Δ since HEAD is the scoreboard's last line
    assert line.startswith("Δ since HEAD")
    assert "1 scored (SMCI +4.20%)" in line
    assert "+1 bets" in line
    assert "DXCM pending→filled" in line


def test_delta_line_counts_scored_movers(monkeypatch):
    """daily.sh settles MOVERS too. Omitting them made the old band print "nothing scored" on a
    run that had just scored 25 rows — in the line whose whole job is to say what changed."""
    from research import bets, movers, orders
    was = [{"seen_at": "2026-07-01T00:00:00+00:00", "ticker": "AAA", "x21_pct": "", "x63_pct": ""},
           {"seen_at": "2026-07-01T00:00:00+00:00", "ticker": "BBB", "x21_pct": "", "x63_pct": ""}]
    now = [{**was[0], "x63_pct": "+1.10"}, dict(was[1])]
    monkeypatch.setattr(D, "_committed", lambda p: {
        bets.CATALOGUE: [], movers.LEDGER: was, orders.LEDGER: []}[p])
    monkeypatch.setattr(movers, "_load", lambda: now)
    for mod in (bets, orders):
        monkeypatch.setattr(mod, "_load", lambda: [])
    line = _REAL_BOARD()[2][-1]
    assert "1 movers scored" in line and "nothing scored" not in line


def test_a_batch_write_is_not_reported_as_a_settlement(monkeypatch):
    """Regression [2026-08-04, caught on the band's FIRST live render, inherited by the
    scoreboard's Δ line]: rows were keyed by logged_at alone, but a batch write stamps every
    row in it with the same second — 11 timestamps in the live catalogue are shared by two
    bets each. The pairs collapsed, the survivor was compared against the wrong row, and a bet
    was announced as newly SCORED on a day nothing settled. Identity is (logged_at, ticker)."""
    ts = "2026-06-26T22:13:56+00:00"                       # the real BB/OXM collision
    pair = [{"logged_at": ts, "ticker": "BB", "status": "closed", "excess_pct": "-33.30",
             "direction": "long"},
            {"logged_at": ts, "ticker": "OXM", "status": "open", "excess_pct": "",
             "direction": "short"}]
    from research import bets, movers, orders
    monkeypatch.setattr(D, "_committed", lambda p: {
        bets.CATALOGUE: list(pair), movers.LEDGER: [], orders.LEDGER: []}[p])
    monkeypatch.setattr(bets, "_load", lambda: list(pair))   # NOTHING changed since HEAD
    monkeypatch.setattr(movers, "_load", lambda: [])
    monkeypatch.setattr(orders, "_load", lambda: [])
    line = _REAL_BOARD()[2][-1]
    assert "nothing scored" in line
    assert not any("MILESTONE" in l for l in _REAL_BOARD()[2])


def test_scoreboard_degrades_loud_not_silent_without_git(monkeypatch):
    """No git / no HEAD copy must not quietly revert the message to a shape that looks normal —
    the whole scoreboard goes DOWN through _safe (the band's proven contract; a half-degraded
    scoreboard that silently drops milestones would look completely healthy)."""
    def boom(*a, **k):
        raise RuntimeError("not a git repository")
    monkeypatch.setattr(D, "_committed", boom)
    for name in ("_book_section", "_bets_section", "_movers_section"):
        monkeypatch.setattr(D, name, lambda *a, **k: ([], [], ["s"]))
    monkeypatch.setattr(D, "_pool_scoreboard", _REAL_BOARD)
    out = D.compose()
    assert "scoreboard silo DOWN" in out and "DO NOW (1)" in out


def test_scoreboard_block_keeps_the_do_now_list_near_the_top(monkeypatch):
    """v2 trades the band's one-line rule for the scoreboard block (the owner's headline ask),
    but the DO-NOW list must stay within eyeshot — bounded mechanically, not by intent."""
    monkeypatch.setattr(D, "_book_section", lambda *a, **k: (["X has NO stop"], [], ["book: eq"]))
    for name in ("_bets_section", "_movers_section"):
        monkeypatch.setattr(D, name, lambda *a, **k: ([], [], ["s"]))
    monkeypatch.setattr(D, "_pool_scoreboard", lambda: ([], [], [
        "🎯 <b>POOL</b> n=5 settled (long-only)", "shorts (diagnostic)", "Δ since HEAD: x"]))
    lines = D.compose().split("\n")
    assert lines.index("⚠️ <b>DO NOW (1)</b>") <= 8
    # ...and with a read-run headline on top, which is the case that actually ships weekdays
    with_note = D.compose("📖 read run: 2 bets\n🟢 system take").split("\n")
    assert with_note.index("⚠️ <b>DO NOW (1)</b>") <= 10


# ---------------------------------------------------------------- pool stop + next evidence

def test_pool_stop_level_rides_on_the_book_line(monkeypatch):
    """The project's ONE circuit breaker [ARC5#4] could previously only fire into cron.log."""
    from research import book
    monkeypatch.setattr(book, "_load", lambda: [{"__": "nonempty"}])
    monkeypatch.setattr(book, "_open_positions", lambda r: [])
    monkeypatch.setattr(D, "_marks", lambda: _mk(equity=3598.0, seed=4662.74))
    actions, _, lines = D._book_section()
    assert "pool stop -40% ($2,798)" in lines[0]        # 0.6 x 4662.74 = 2797.64
    assert not any("POOL STOP HIT" in a for a in actions)


def test_pool_stop_breach_becomes_a_do_now(monkeypatch):
    from research import book
    monkeypatch.setattr(book, "_load", lambda: [{"__": "nonempty"}])
    monkeypatch.setattr(book, "_open_positions",
                        lambda r: [{"ticker": "NIO", "side": "long", "shares": "28",
                                    "entry": "8.50", "stop": "2.90"}])
    monkeypatch.setattr(D, "_marks", lambda: _mk(equity=2700.0, seed=4662.74,
                                                 spots={"NIO": 4.78}))
    actions, _, _ = D._book_section()
    assert any("POOL STOP HIT" in a and "HALT" in a for a in actions), actions

    # ...and it goes quiet once the instruction has been FOLLOWED (flat = risk off). A breach is
    # permanent — equity never climbs back over the floor after a halt — so an unconditional
    # alarm could never be cleared, which this project forbids [FINDINGS 2026-08-02].
    monkeypatch.setattr(book, "_open_positions", lambda r: [])
    monkeypatch.setattr(D, "_marks", lambda: _mk(equity=2700.0, seed=4662.74))
    actions2, _, lines2 = D._book_section()
    assert not any("POOL STOP HIT" in a for a in actions2)
    assert "pool stop -40%" in lines2[0]          # the LEVEL still shows; only the ASK is gated


def test_exit_target_renders_and_touched_band_is_a_do_now(monkeypatch):
    """NIO's exit band lived in thesis prose; the market touched it (high 4.94 vs 4.85-5.15)
    and nothing noticed [FINDINGS 2026-08-04]. Structured target → visible line + DO-NOW."""
    from research import book
    monkeypatch.setattr(book, "_load", lambda: [{"__": "nonempty"}])
    monkeypatch.setattr(book, "_open_positions",
                        lambda r: [{"ticker": "NIO", "side": "long", "shares": "28",
                                    "entry": "8.50", "stop": "2.90", "target": "4.8500"}])
    monkeypatch.setattr(D, "_marks", lambda: _mk(equity=4000.0, seed=4662.74,
                                                 spots={"NIO": 4.94}))
    actions, _, lines = D._book_section()
    assert any("exit ≥4.85" in ln for ln in lines)
    assert any("exit band TOUCHED" in a and "book close NIO" in a for a in actions), actions

    # Below the band: the line still shows the level, no DO-NOW.
    monkeypatch.setattr(D, "_marks", lambda: _mk(equity=4000.0, seed=4662.74,
                                                 spots={"NIO": 4.78}))
    actions2, _, lines2 = D._book_section()
    assert any("exit ≥4.85" in ln for ln in lines2)
    assert not any("exit band TOUCHED" in a for a in actions2)


def test_exit_target_blank_or_legacy_row_is_silent(monkeypatch):
    """Rows without a target (today's live book, and any pre-column row) change nothing."""
    from research import book
    monkeypatch.setattr(book, "_load", lambda: [{"__": "nonempty"}])
    monkeypatch.setattr(book, "_open_positions",
                        lambda r: [{"ticker": "CMPS", "side": "long", "shares": "193",
                                    "entry": "12.72", "stop": "10.80"}])   # no target key at all
    monkeypatch.setattr(D, "_marks", lambda: _mk(equity=4000.0, seed=4662.74,
                                                 spots={"CMPS": 11.77}))
    actions, _, lines = D._book_section()
    assert not any("exit" in a for a in actions)
    assert not any("exit ≥" in ln for ln in lines)


def test_bets_line_carries_the_next_evidence_date(monkeypatch):
    """Under a LOW-edge prior 'nothing to do' is the honest message most days — so it must come
    with the date on which the scoreboard can next move on its own."""
    from research import bets
    monkeypatch.setattr(bets, "_load", lambda: [
        {"logged_at": "2026-08-04T00:00:00+00:00", "ticker": "SMCI", "horizon_d": "21",
         "status": "open", "excess_pct": "", "benchmark": "SPY", "direction": "long",
         "pattern_tag": ""}])
    _, _, lines = D._bets_section()
    assert "next score ≥2026-09-02 (SMCI)" in lines[0]


def test_one_equity_number_per_message(monkeypatch):
    """equity_marks is fetched at most ONCE per message. Under v2 only the book section reads
    it (the scoreboard has no book coupling at all) — a second caller would mean two copies of
    the arithmetic drifting apart again, the 2026-08-04 bug shape."""
    from research import bets, book, movers, orders
    calls = []
    monkeypatch.setattr(book, "equity_marks", lambda rows: (calls.append(1), _mk())[1])
    monkeypatch.setattr(book, "_load", lambda: [{"__": "nonempty"}])
    monkeypatch.setattr(book, "_open_positions", lambda r: [])
    monkeypatch.setattr(D, "_committed", lambda p: [])
    monkeypatch.setattr(D, "_pool_scoreboard", _REAL_BOARD)
    for mod in (bets, movers, orders):
        monkeypatch.setattr(mod, "_load", lambda: [])
    for name in ("_bets_section", "_movers_section"):
        monkeypatch.setattr(D, name, lambda *a, **k: ([], [], ["s"]))
    D.compose()
    assert len(calls) == 1, f"equity_marks called {len(calls)}x — the mark must be shared"


def test_plain_strips_markup():
    assert D._plain("<b>BOOK</b> &lt;fill&gt;") == "BOOK <fill>"


def test_safe_degrades_on_error():
    """Fail-soft, but LOUD since 2026-07-27: the run survives a dead silo and now SAYS so
    in the DO-NOW list instead of degrading to a line nobody reads."""
    a, f, lines = D._safe(lambda: (_ for _ in ()).throw(RuntimeError("boom")), "book")
    assert f == [] and lines[0].startswith("book: unavailable")
    assert a and "book silo DOWN" in a[0]


def test_no_stop_nag_is_not_silenced_by_the_word_lock_in_a_thesis(monkeypatch):
    """Regression [2026-08-02]: the 🔒 flag was keyed on thesis PROSE, so a position's alarm
    state depended on its wording — SPCX rendered locked because its thesis contained "lock"
    inside sentences saying the OPPOSITE ("NO lockup"). A stopless non-cash-equivalent must
    always raise the NO-STOP DO-NOW, whatever its prose says."""
    from research import book
    rows = [{"opened_at": "2026-08-01", "ticker": "ACME", "side": "long", "shares": "10",
             "entry": "10.00", "stop": "0.0000", "target": "", "horizon_d": "",
             "thesis": "locked lockup parked — prose that used to suppress the nag",
             "status": "open", "closed_at": "", "exit": "", "realized_pnl": ""}]
    monkeypatch.setattr(book, "_load", lambda: rows)
    monkeypatch.setattr(D, "_marks", lambda: _mk(spots={"ACME": 10.0}))
    actions, _, _ = D._book_section()
    assert any("NO stop" in a for a in actions), actions

    # ...and a real cash park still IS silenced, by TICKER not by prose
    park = next(iter(D.CASH_EQUIV))
    rows[0]["ticker"] = park
    rows[0]["thesis"] = "no mention of the l-word at all"
    monkeypatch.setattr(D, "_marks", lambda: _mk(spots={park: 10.0}))
    actions2, _, _ = D._book_section()
    assert not any("NO stop" in a for a in actions2), actions2


def _order(**kw):
    base = {"logged_at": "2026-08-03T11:43:00+00:00", "ticker": "DXCM", "direction": "long",
            "shares": "5", "ref": "83.45", "ref_date": "2026-07-31", "scan_from": "2026-07-31",
            "limit_px": "84.28", "stop_px": "76.80", "horizon_d": "21", "benchmark": "XLV",
            "status": "pending", "resolved_on": "", "fill_px": "", "x21_pct": "", "note": ""}
    return {**base, **kw}


# ------------- the orders section is counterfactual since [ARC 5 #12a]: display, NEVER a DO-NOW

def test_pending_order_is_a_display_line_not_an_action(monkeypatch):
    """The daily re-push survives (a LIMIT is age-invariant) but as INFORMATION: a 🟢 system
    take with the live spot beside it — zero instructions, zero DO-NOWs."""
    from research import book, orders
    monkeypatch.setattr(orders, "_load", lambda: [_order()])
    monkeypatch.setattr(book, "_spot", lambda t: 86.54)
    actions, fyi, lines = _REAL_ORDERS()
    assert actions == [] and fyi == []
    joined = " ".join(lines)
    assert "system take (counterfactual)" in joined
    assert "≤ 84.28" in joined and "last 86.54" in joined and "+2.7% above" in joined
    assert "no fill yet" in joined and "resolves on its own" in joined


def test_an_in_range_order_says_so(monkeypatch):
    from research import book, orders
    monkeypatch.setattr(orders, "_load", lambda: [_order()])
    monkeypatch.setattr(book, "_spot", lambda t: 83.90)      # below the buy limit
    _, _, lines = _REAL_ORDERS()
    assert "IN RANGE" in " ".join(lines)


def test_orders_section_never_speaks_broker(monkeypatch):
    """No row shape may produce an instruction: pending, filled+placed (historical real-money),
    expired+placed+unpulled (the old stale-GTC alarm), cancelled+placed — all display-only now.
    The broker-reconciliation verbs are gone; an ask would name a command that no longer exists."""
    from research import book, orders
    rows = [_order(),
            _order(ticker="DVA", status="filled", resolved_on="2026-08-07", fill_px="178.00",
                   placed_at="2026-08-07"),
            _order(ticker="CACI", status="expired", resolved_on="2026-08-06",
                   placed_at="2026-08-03"),
            _order(ticker="TPR", status="cancelled", resolved_on="2026-08-06",
                   placed_at="2026-08-03")]
    monkeypatch.setattr(orders, "_load", lambda: rows)
    monkeypatch.setattr(book, "_spot", lambda t: 86.54)
    actions, fyi, lines = _REAL_ORDERS()
    assert actions == [] and fyi == []
    joined = " ".join(lines)
    for verb in ("orders placed", "orders pulled", "book open", "Place at the broker",
                 "confirm the REAL fill", "may STILL be live"):
        assert verb not in joined
    # historical placed fills tell no daily story — the frozen book's closing verdict owns them
    assert "DVA" not in joined


def test_a_recent_unplaced_fill_shows_as_counterfactual_then_ages_out(monkeypatch):
    """The regime's data point gets one informational line while fresh; the ledger, not the
    daily photo, is where counterfactual fills accumulate (orders show)."""
    from datetime import date, timedelta
    from research import book, orders
    fresh = _order(status="filled", fill_px="84.28",
                   resolved_on=(date.today() - timedelta(days=1)).isoformat())
    monkeypatch.setattr(orders, "_load", lambda: [fresh])
    monkeypatch.setattr(book, "_spot", lambda t: 86.54)
    actions, _, lines = _REAL_ORDERS()
    assert actions == []
    assert any("would have filled @ 84.28" in l and "counterfactual" in l for l in lines)

    stale = dict(fresh, resolved_on=(date.today() - timedelta(days=9)).isoformat())
    monkeypatch.setattr(orders, "_load", lambda: [stale])
    _, _, lines2 = _REAL_ORDERS()
    assert not any("would have filled" in l for l in lines2)


def test_countdown_survives_and_degrades_without_the_feed(monkeypatch):
    """The expiry countdown stays useful information; a dead price feed costs the countdown,
    never the whole order line."""
    from research import book, config, orders, prices
    monkeypatch.setattr(orders, "_load", lambda: [_order()])
    monkeypatch.setattr(book, "_spot", lambda t: 86.54)
    monkeypatch.setattr(prices, "bars_after",
                        lambda *a, **k: [{"date": "2026-08-04"}, {"date": "2026-08-05"}])
    monkeypatch.setattr(orders, "_complete", lambda bars, today=None: bars)
    _, _, lines = _REAL_ORDERS()
    assert f"{config.ORDER_EXPIRY_D - 2} of {config.ORDER_EXPIRY_D} sessions left" in " ".join(lines)

    def boom(*a, **k):
        raise RuntimeError("feed down")
    monkeypatch.setattr(prices, "bars_after", boom)
    _, _, lines2 = _REAL_ORDERS()
    joined = " ".join(lines2)
    assert "sessions left" not in joined and "≤ 84.28" in joined


# ---- slim mode [2026-08-05, reshaped 2026-08-06, v2 2026-08-14] — the read push's shape ------
# v2 [ARC 5 #12a]: slim KEEPS the 🎯 POOL scoreboard (the verdict headline leads BOTH legs —
# the owner's ask) + the book + the 🟢 system-take lines; it DROPS the bets/movers state lines
# and the 📋 banner. Slim touches DISPLAY LINES ONLY — every DO-NOW action must survive.

def test_book_positions_carry_dollars_and_distances(monkeypatch):
    """[2026-08-06] A position line answers 'where do I stand?' by itself: $ P&L beside the %,
    and the live distance to stop and target — the % alone sent the reader to book mark."""
    from research import book
    monkeypatch.setattr(book, "_load", lambda: [{"__": "nonempty"}])
    monkeypatch.setattr(book, "_open_positions",
                        lambda r: [{"ticker": "DXCM", "side": "long", "shares": "5",
                                    "entry": "84.28", "stop": "76.80", "target": "95.00"}])
    monkeypatch.setattr(D, "_marks", lambda: _mk(equity=3948.0, seed=4662.74, cash=6.0,
                                                 spots={"DXCM": 82.66}))
    actions, _, lines = D._book_section()
    assert "pool stop -40%" in lines[0]                 # circuit breaker stays visible daily
    row = next(l for l in lines if l.startswith("DXCM"))
    assert "-$8 (-2%)" in row                           # 5 × (82.66−84.28) = −$8.10
    assert "stop 76.80 (-7.1% away)" in row
    assert "exit ≥95.00 (+14.9% away)" in row
    assert lines[-1].startswith("cash $")               # 5b prices its order against this


def test_slim_compose_keeps_scoreboard_and_positions_drops_state_lines(monkeypatch):
    """The 📖 is the morning brief: the 🎯 POOL scoreboard leads it, the book stays, the
    bets/movers state lines go — display only, their actions always ride."""
    monkeypatch.setattr(D, "_book_section",
                        lambda: ([], [], ["💼 BOOK $3,948", "DXCM 5 @ 84.28→82.66", "cash $6"]))
    monkeypatch.setattr(D, "_orders_section", lambda slim=False: ([], [], []))
    monkeypatch.setattr(D, "_bets_section", lambda: (["bets action"], [], ["BETS 51 open"]))
    monkeypatch.setattr(D, "_movers_section", lambda: ([], [], ["📡 MOVERS 45 take"]))
    monkeypatch.setattr(D, "_pool_scoreboard",
                        lambda: ([], [], ["🎯 <b>POOL</b> n=5 settled (long-only)"]))
    slimmed = D.compose("📖 read run", slim=True)
    assert "DXCM 5 @ 84.28→82.66" in slimmed            # positions in the message he reads
    assert "🎯 <b>POOL</b>" in slimmed                  # the verdict headline leads BOTH legs
    assert "BETS 51 open" not in slimmed and "📡" not in slimmed
    assert "bets action" in slimmed                     # actions never slimmed
    full = D.compose("note")
    assert all(s in full for s in ("🎯 <b>POOL</b>", "📡", "BETS 51 open"))


def test_slim_orders_carries_the_system_take_lines_only(monkeypatch):
    """v2: the 🟢 system-take line(s) ride the morning 📖 (they replaced the old DO-NOW copy
    of the pending order); counts, counterfactual-fill history and diagnostics stay settle's."""
    from research import book, orders
    monkeypatch.setattr(orders, "_load", lambda: [_order()])
    monkeypatch.setattr(book, "_spot", lambda t: 86.54)
    actions, fyi, lines = _REAL_ORDERS(slim=True)
    assert actions == [] and fyi == []
    assert len(lines) == 1 and "system take (counterfactual)" in lines[0]

    filled = _order(status="filled", resolved_on="2026-08-04", fill_px="84.28")
    monkeypatch.setattr(orders, "_load", lambda: [filled])
    actions2, _, lines2 = _REAL_ORDERS(slim=True)
    assert not actions2 and lines2 == []                # no pending → nothing rides slim


def test_slim_with_headline_drops_the_digest_banner(monkeypatch):
    """📋 marks THE full photo (settle); the slim read push is the 📖 report. Same banner on
    both was half of why the two daily messages read as duplicates."""
    monkeypatch.setattr(D, "_book_section", lambda *a, **k: ([], [], ["b"]))
    monkeypatch.setattr(D, "_bets_section", lambda *a, **k: ([], [], []))
    monkeypatch.setattr(D, "_movers_section", lambda *a, **k: ([], [], []))
    assert "📋" not in D.compose("📖 read run: 1 bet", slim=True)
    assert "📋" in D.compose("📖 read run: 1 bet")          # the full photo keeps it
    assert "📋" in D.compose("", slim=True)                 # headline-less slim is never anonymous


def test_run_parses_the_slim_flag(monkeypatch, capsys):
    calls = []
    monkeypatch.setattr(D, "compose", lambda note, slim=False: calls.append((note, slim)) or "x")
    D.run(["--slim", "note"])
    D.run(["note"])
    assert calls == [("note", True), ("note", False)]   # flag reaches compose, never the note


def test_run_prints_the_delivery_verdict(monkeypatch, capsys, tmp_path):
    """The verdict line is the ONLY truth about delivery [2026-08-06]: exit 1 covers both
    non-delivered states (daily.sh accounting unchanged), but only REJECTED licenses a
    re-send — an agent that re-sent on UNCONFIRMED double-posted (the 'delivery check' copy)."""
    from research import notify
    monkeypatch.setattr(D, "PUSH_LOG", str(tmp_path / "push_log.csv"))
    monkeypatch.setattr(D, "compose", lambda note, slim=False: "x")
    for verdict, marker, code in [(True, "PUSH DELIVERED", 0),
                                  (None, "PUSH UNCONFIRMED", 1),
                                  (False, "PUSH REJECTED", 1)]:
        monkeypatch.setattr(notify, "send", lambda t, html=False, v=verdict: v)
        assert D.run(["--notify", "note"]) == code
        assert marker in capsys.readouterr().out


def test_run_stamps_the_push_log(monkeypatch, tmp_path):
    """Every --notify push leaves one committed delivery row — the record a later run reads
    to detect a message that died in transport while the commits landed."""
    import csv
    from research import notify
    p = tmp_path / "push_log.csv"
    monkeypatch.setattr(D, "PUSH_LOG", str(p))
    monkeypatch.setattr(D, "compose", lambda note, slim=False: "x")
    monkeypatch.setattr(notify, "send", lambda t, html=False: True)
    D.run(["--notify", "--slim", "n"])
    monkeypatch.setattr(notify, "send", lambda t, html=False: None)
    D.run(["--notify", "n"])
    with open(p, newline="") as f:
        rows = list(csv.DictReader(f))
    assert [(r["kind"], r["verdict"]) for r in rows] == [("read", "DELIVERED"),
                                                         ("settle", "UNCONFIRMED")]


def test_run_survives_a_notify_death_and_still_stamps(monkeypatch, capsys, tmp_path):
    """The 2026-08-07 strand: a cold container without python-dotenv killed the notify import
    AND the heartbeat's — no stamp, no verdict, no alarm. A death anywhere in the notify block
    must now still leave a stamp and print a verdict line (FINDINGS 2026-08-08). A raising
    send() is treated as AMBIGUOUS (may be post-request) → UNCONFIRMED, never re-send."""
    import csv
    from research import notify
    p = tmp_path / "push_log.csv"
    monkeypatch.setattr(D, "PUSH_LOG", str(p))
    monkeypatch.setattr(D, "compose", lambda note, slim=False: "x")

    def boom(t, html=False):
        raise RuntimeError("ImportError-by-proxy: dotenv missing")
    monkeypatch.setattr(notify, "send", boom)
    assert D.run(["--notify", "n"]) == 1
    assert "PUSH UNCONFIRMED" in capsys.readouterr().out
    with open(p, newline="") as f:
        rows = list(csv.DictReader(f))
    assert [(r["kind"], r["verdict"]) for r in rows] == [("settle", "UNCONFIRMED")]


def test_a_stranded_settle_push_becomes_a_do_now(monkeypatch, tmp_path):
    """Settle commits its ledgers even when its 📋 dies in transport (08-05 + 08-06, two
    consecutive nights) — the watchdog watches commits, so only the push log can surface it.
    The next delivered message carries the alarm."""
    from datetime import datetime, timezone
    p = tmp_path / "push_log.csv"
    monkeypatch.setattr(D, "PUSH_LOG", str(p))
    # settle fires 22:30 UTC (moved 2026-08-07); today's push becomes due at 23:00
    monkeypatch.setattr(D, "_utcnow", lambda: datetime(2026, 8, 7, 23, 42, tzinfo=timezone.utc))
    assert _REAL_PUSHLOG() == ([], [], [])          # no file (pre-rollout) → silent
    p.write_text("date_utc,kind,verdict\n2026-08-07,read,DELIVERED\n")
    assert _REAL_PUSHLOG() == ([], [], [])          # no settle rows yet → silent
    p.write_text("date_utc,kind,verdict\n2026-08-07,settle,UNCONFIRMED\n")
    actions, _, _ = _REAL_PUSHLOG()
    assert actions and "never confirmed delivered" in actions[0]
    p.write_text("date_utc,kind,verdict\n2026-08-06,settle,DELIVERED\n")
    actions2, _, _ = _REAL_PUSHLOG()
    assert actions2                                      # today's due settle never stamped
    p.write_text("date_utc,kind,verdict\n2026-08-07,settle,DELIVERED\n")
    assert _REAL_PUSHLOG() == ([], [], [])          # healthy
    # before 23:00 UTC today's settle is not yet due — yesterday's DELIVERED row satisfies
    # (this is also the next-morning read composing at 11:42)
    monkeypatch.setattr(D, "_utcnow", lambda: datetime(2026, 8, 7, 11, 42, tzinfo=timezone.utc))
    p.write_text("date_utc,kind,verdict\n2026-08-06,settle,DELIVERED\n")
    assert _REAL_PUSHLOG() == ([], [], [])


# ------------------------------------------- the 2026-08-10 delivery incident (FINDINGS 08-11)

def _pushlog(monkeypatch, tmp_path, rows: str, when):
    from datetime import datetime, timezone
    p = tmp_path / "push_log.csv"
    p.write_text("date_utc,kind,verdict\n" + rows)
    monkeypatch.setattr(D, "PUSH_LOG", str(p))
    monkeypatch.setattr(D, "_utcnow", lambda: datetime(*when, tzinfo=timezone.utc))
    return _REAL_PUSHLOG()[0]


_LOG_0810 = ("2026-08-07,read,DELIVERED\n"
             "2026-08-09,settle,DELIVERED\n"
             "2026-08-10,read,UNCONFIRMED\n"
             "2026-08-10,settle,REJECTED\n")


def test_a_stranded_read_brief_becomes_a_do_now(monkeypatch, tmp_path):
    """2026-08-10: the read ran, committed a bet (TTD) and died in transport (UNCONFIRMED).
    NOTHING alarmed — this check filtered to kind == 'settle' and the read leg has no watcher
    of its own — so the next morning's brief still opened with 'DO NOW: nothing'. The read leg
    is the one that carries the TRADE ALERTS. FEED_STALE_D=1 cannot cover it: the run was alive
    and the feed was healthy, only the push died."""
    actions = _pushlog(monkeypatch, tmp_path, _LOG_0810, (2026, 8, 10, 22, 48))
    assert len(actions) == 1
    assert "read brief for 2026-08-10" in actions[0] and "UNCONFIRMED" in actions[0]


def test_a_retry_does_not_alarm_about_its_own_superseded_attempt(monkeypatch, tmp_path):
    """The delivered 08-10 message accused 2026-08-09 of never arriving while the log showed
    08-09 DELIVERED: the old test held the LAST row (today's REJECTED first attempt) and then
    printed `due` instead of that row's own date, sending the human to debug a failure that had
    self-healed one line above. A due day with a DELIVERED stamp is healthy whatever follows."""
    actions = _pushlog(monkeypatch, tmp_path, _LOG_0810, (2026, 8, 10, 22, 48))
    assert not any("settle digest" in a for a in actions)


def test_a_delivered_read_clears_the_alarm(monkeypatch, tmp_path):
    """Self-clearing, so a one-off transport failure cannot become a permanent nag."""
    actions = _pushlog(monkeypatch, tmp_path,
                       _LOG_0810 + "2026-08-10,settle,DELIVERED\n2026-08-11,read,DELIVERED\n",
                       (2026, 8, 11, 12, 0))
    assert actions == []


def test_no_read_is_due_on_a_weekend(monkeypatch, tmp_path):
    """Saturday's settle must not nag for a brief nobody schedules — the read due date rolls
    back to Friday. The weekend false alarm is the mistake FEED_BAR_STALE_D already made once."""
    actions = _pushlog(monkeypatch, tmp_path,
                       "2026-08-07,read,DELIVERED\n2026-08-08,settle,DELIVERED\n",
                       (2026, 8, 8, 22, 30))          # Saturday
    assert actions == []


# (The band's re-run-baseline test [2026-08-11] died with the band's book half — the Δ line
# diffs LEDGERS vs HEAD, where a re-run's own committed copy simply reads as "nothing scored",
# the safe direction. The MU-shape lesson lives on in test_a_batch_write_... above.)


# ------------------------------------------- the terminal CLOSED book [ARC 5 #12 / #12a, P1a]

def _retired_book(monkeypatch):
    from research import book
    rows = [{**{k: "" for k in book.FIELDS}, "ticker": book.CASH_T, "status": "cash",
             "entry": "0.00"},
            {**{k: "" for k in book.FIELDS}, "ticker": book.RETIRED_T, "status": "meta",
             "opened_at": "2026-08-17", "entry": "3984.00"}]
    monkeypatch.setattr(book, "_load", lambda: rows)
    return rows


def test_closed_book_is_one_line_and_never_marks(monkeypatch):
    """The retired guard sits BEFORE _marks(): no spots, no SPY, no dual-mom, no stop/target/
    pool-stop/idle-cash asks — one display line pointing at the closing verdict."""
    _retired_book(monkeypatch)
    def boom():
        raise AssertionError("a closed book must not call _marks()")
    monkeypatch.setattr(D, "_marks", boom)
    actions, fyi, lines = D._book_section()
    assert actions == [] and fyi == []
    assert len(lines) == 1 and "BOOK</b> CLOSED" in lines[0] and "[ARC 5 #12]" in lines[0]


# (The band's retired-guard test died with the band itself — the scoreboard has no book
# coupling at all; test_scoreboard_never_reads_the_book above is the stronger replacement.)
