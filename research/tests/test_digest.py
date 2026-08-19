"""Guard the v3 digest: the pulse, ⚠️-only-when-real, and the alarm sections [MSG 2026-08-18].

The v2 book/orders/movers section tests died with their sections (the book is TERMINAL, the
diagnostics moved CLI-side); their lessons are cited where they still bind. The batch-write
row-identity test [2026-08-04] died with the Δ-since-HEAD line — the milestone check compares
COUNTS, not row identities, so the collision class cannot reach it.
"""
import pytest

from research import digest as D

# Captured before the autouse fixture below can stub them out, so the sections that read the
# real repo/filesystem can still be tested directly.
_REAL_GIT, _REAL_FEED = D._git_section, D._feed_section
_REAL_STRANDED, _REAL_BOARD = D._stranded_section, D._pool_scoreboard
_REAL_PUSHLOG, _REAL_BETS = D._pushlog_section, D._bets_section


@pytest.fixture(autouse=True)
def _neutralize_environment_sections(monkeypatch):
    """Every section inspects the actual repo, remote, ledgers or data dir — un-stubbed they
    make each compose test depend on this checkout's live state (and _stranded_section would
    hit the NETWORK). Stub them all by default; each has its own dedicated test."""
    for name in ("_bets_section", "_git_section", "_stranded_section",
                 "_feed_section", "_pushlog_section", "_pool_scoreboard"):
        monkeypatch.setattr(D, name, lambda: ([], []))


# ---------------------------------------------------------------------------- compose (v3)

def test_settle_banner_carries_the_weekday():
    from datetime import date
    today = date.today()
    assert D.compose().startswith(f"📋 <b>SETTLE {today.strftime('%a')} {today.isoformat()}</b>")


def test_empty_do_now_prints_nothing():
    """The owner skipped '✅ DO NOW: nothing' every single day — the absence of ⚠️ IS the
    all-clear. No placeholder line of any kind."""
    out = D.compose()
    assert "DO NOW" not in out and "✅" not in out


def test_actions_render_numbered_under_the_warning_header(monkeypatch):
    monkeypatch.setattr(D, "_bets_section", lambda: (["settlement STUCK: X"], ["📈 1 open"]))
    out = D.compose()
    assert "⚠️ <b>DO NOW (1)</b>" in out and "1. settlement STUCK: X" in out
    assert "📈 1 open" in out


def test_broken_silo_escalates_to_do_now():
    """A dead silo must be an ACTION, not a quiet trailing line — the insider ledger was the
    intended 2nd verdict silo and could previously stop accruing evidence unnoticed."""
    def boom():
        raise ModuleNotFoundError("pandas")
    actions, lines = D._safe(boom, "movers")
    assert actions and "silo DOWN" in actions[0] and "ModuleNotFoundError" in actions[0]
    assert lines and "unavailable" in lines[0]      # still shown in the state block


def test_multiline_action_keeps_code_line_whole(monkeypatch):
    """Paste-ready <code> lines ride under their numbered item, tags intact on one line."""
    monkeypatch.setattr(D, "_bets_section",
                        lambda: (["X STUCK — fix:\n<code>bets settle</code>"], ["📈 1 open"]))
    lines = D.compose().split("\n")
    assert "1. X STUCK — fix:" in lines
    assert "<code>bets settle</code>" in lines                  # own line, tag not split


def test_tags_never_span_lines(monkeypatch):
    """The notify truncation cuts at a newline — every tag must open+close on one line."""
    monkeypatch.setattr(D, "_bets_section", lambda: (["a:\n<code>cmd</code>"], ["📈 1 open"]))
    monkeypatch.setattr(D, "_pool_scoreboard", lambda: ([], ["<b>Scored:</b> 5 of 30 needed"]))
    for line in D.compose().split("\n"):
        assert line.count("<b>") == line.count("</b>")
        assert line.count("<code>") == line.count("</code>")


def test_blockquote_is_the_only_element_that_spans_lines():
    """The card must span lines to BE a card — so it is the one exception, it is balanced, and
    notify closes it on a truncation cut (see test_notify)."""
    out = D.compose("📖 READ\n🟢 NEW BET #1 — X long\nWhy: a\nRisk: b")
    assert out.count("<blockquote>") == out.count("</blockquote>") == 1
    for line in out.split("\n"):
        for tag in ("b", "i", "code", "pre"):
            assert line.count(f"<{tag}>") == line.count(f"</{tag}>")


def test_blocks_are_separated_by_exactly_one_blank(monkeypatch):
    """Air BETWEEN ideas, never inside one [2026-08-19 owner review]. v3 shipped "contiguous by
    design" and five unseparated blocks read on a phone as one paragraph of prose; the v2 shape
    before it ended in five blank lines [2026-08-04]. Neither, now: no double blank, no leading
    or trailing blank, exactly one between blocks."""
    monkeypatch.setattr(D, "_pool_scoreboard", lambda: ([], ["<b>Scored:</b> 5 of 30 needed"]))
    monkeypatch.setattr(D, "_bets_section", lambda: ([], ["📈 62 open"]))
    out = D.compose()
    assert "\n\n\n" not in out
    assert out.rstrip("\n") == out and not out.startswith("\n")
    # the quiet settle day is banner · scoreboard · 📈 — three blocks, two blank lines
    assert out.split("\n")[1:] == ["", "<b>Scored:</b> 5 of 30 needed", "", "📈 62 open"]


def test_an_empty_section_adds_no_blank_line(monkeypatch):
    """A silo that returns nothing must not leave its separator behind — that is how a message
    grows a blank wall one dead section at a time."""
    monkeypatch.setattr(D, "_pool_scoreboard", lambda: ([], []))
    monkeypatch.setattr(D, "_bets_section", lambda: ([], []))
    assert "\n" not in D.compose()


def test_run_note_headline_tops_and_cards_ride_above_the_bets_line(monkeypatch):
    """The note's first line is the leg's identity (Telegram preview); its body — the 🟢 NEW
    BET cards — is the morning's news and lands after the scoreboard and any ⚠️ list, ABOVE the
    📈 line. v2 demoted the cards to a bottom RUN NOTE block; v3 does not."""
    monkeypatch.setattr(D, "_pool_scoreboard", lambda: ([], ["<b>Scored:</b> 5 of 30 needed"]))
    monkeypatch.setattr(D, "_bets_section", lambda: (["X STUCK"], ["📈 63 open"]))
    lines = D.compose("📖 READ Wed 2026-08-19 pre-market: 1 bet\n"
                      "🟢 NEW BET #69 — CAVA long · 21d vs XLY\nWHY: capitulation").split("\n")
    assert lines[0] == "<b>📖 READ Wed 2026-08-19 pre-market: 1 bet</b>"
    assert "📋" not in "\n".join(lines)                     # headline replaces the banner
    i_do = lines.index("⚠️ <b>DO NOW (1)</b>")
    i_card = lines.index("<blockquote><b>🟢 NEW BET #69 — CAVA long · 21d vs XLY</b>")
    i_bets = lines.index("📈 63 open")
    assert lines.index("<b>Scored:</b> 5 of 30 needed") < i_do < i_card < i_bets


def test_run_note_body_is_escaped_and_never_splits_a_tag():
    """The note is free text from the read agent — it must not be able to inject markup or
    hand notify a half-tag to truncate on."""
    out = D.compose("head <b>x</b> & co\nbody <i>y</i> & <code>z")
    assert "head &lt;b&gt;x&lt;/b&gt; &amp; co" in out
    assert "body &lt;i&gt;y&lt;/i&gt; &amp; &lt;code&gt;z" in out
    for line in out.split("\n"):
        assert line.count("<b>") == line.count("</b>")
        assert line.count("<code>") == line.count("</code>")


def test_empty_note_is_the_settle_message():
    """settle passes no note; its message must be byte-identical to the plain compose()."""
    assert D.compose("") == D.compose() and D.compose().startswith("📋 <b>SETTLE")


def test_no_broker_terminal_blocks_survive(monkeypatch):
    """The v3 contract in one test: the fossils the owner skipped are gone from Telegram —
    BOOK tombstone, ORDERS band, MOVERS denominators, the mix mirror, Δ-since-HEAD, the
    'full:' footer — and the stats vocabulary stays CLI-side."""
    monkeypatch.setattr(D, "_pool_scoreboard", _REAL_BOARD)
    from research import bets
    monkeypatch.setattr(bets, "_load", lambda: list(_LIVE_POOL))
    monkeypatch.setattr(D, "_committed", lambda p: list(_LIVE_POOL))
    out = D.compose()
    for fossil in ("BOOK", "ORDERS", "MOVERS", "mix(", "Δ since HEAD", "full:",
                   "Σ", "p=", "α", "shorts", "POOL"):
        assert fossil not in out, fossil


# ------------------------------------------------------------------------ the 🟢 card

def test_card_is_a_blockquote_with_bold_header_and_labels():
    """The 2026-08-19 ask: a take must READ as a card, not as three more sentences. The
    <blockquote> indents it behind a left bar (so even a wrapped clause stays visibly INSIDE
    it), the header is bold, and every row label is its own bold anchor."""
    out = D.compose("📖 READ\n🟢 NEW BET #69 — HAE long · 21d vs XLV\n"
                    "Why: Q1 EPS +31%, new CSL deal\nRisk: +20% in 5d already\n"
                    "conviction: medium")
    assert "<blockquote><b>🟢 NEW BET #69 — HAE long · 21d vs XLV</b>" in out
    assert "<b>Why:</b> Q1 EPS +31%, new CSL deal" in out
    assert "<b>Conviction:</b> medium</blockquote>" in out   # label case normalized, quote closed


def test_two_takes_are_two_separate_cards():
    """At most 2 cards [READ_LOOP 5a] — and they must not fuse into one six-line block."""
    out = D.compose("📖 READ\n🟢 NEW BET #1 — A long\nWhy: a\n🟢 NEW BET #2 — B long\nWhy: b")
    assert out.count("<blockquote>") == out.count("</blockquote>") == 2
    assert "<b>Why:</b> a</blockquote>\n\n<blockquote><b>🟢 NEW BET #2 — B long</b>" in out


def test_zero_take_line_rides_plain_not_quoted():
    """A run with no take still speaks — but a sentence is not a card."""
    out = D.compose("📖 READ · no new bets\nnothing cleared the bar today")
    assert "nothing cleared the bar today" in out and "<blockquote>" not in out


def test_note_fossils_are_dropped_not_trusted():
    """The note is agent-written, so the CLI-only half of the v3 contract is ENFORCED here, not
    trusted. The FIRST live v3 read push (2026-08-19) carried both fossils: a `mix:` mirror row
    and a scan denominator in the headline."""
    out = D.compose("📖 READ Tue 2026-08-19 pre-market: 1 bet (HAE) · 1 take/39 skip\n"
                    "🟢 NEW BET #69 — HAE long\nWhy: a\n"
                    "mix: post-earnings-drift 9/15 last bets — PED-rich")
    assert out.startswith("<b>📖 READ Tue 2026-08-19 pre-market: 1 bet (HAE)</b>")
    assert "take/39 skip" not in out and "mix:" not in out and "9/15" not in out


def test_a_card_row_cannot_inject_markup():
    """Escaping survives the label split — a row is still free text from the read agent."""
    out = D.compose("📖 READ\n🟢 <b>X</b>\nWhy: <i>y</i> & <code>z")
    assert "&lt;b&gt;X&lt;/b&gt;" in out and "&lt;i&gt;y&lt;/i&gt; &amp; &lt;code&gt;z" in out
    assert out.count("<b>") == out.count("</b>")


# ------------------------------------------------------------------- the scoreboard (v3)

_L = {"logged_at": "2026-06-01T00:00:00+00:00", "direction": "long", "horizon_d": "21",
      "benchmark": "SPY", "thesis": "t", "pattern_tag": "", "notified": "x",
      "entry_date": "2026-06-02", "entry": "10.00"}


def _closed_bet(ticker, excess, direction="long"):
    return {**_L, "ticker": ticker, "direction": direction, "status": "closed",
            "excess_pct": excess}


def _open_bet(ticker, direction="long"):
    return {**_L, "ticker": ticker, "direction": direction, "status": "open",
            "excess_pct": "", "entry_date": "", "entry": ""}


# The lock-time live vector [ARC 5 #12a]: long-only n=5 median −7.99% beat 20%, plus the ILLR
# short that the long-only rule strips from the verdict (and v3 strips from Telegram entirely).
_LIVE_POOL = [_closed_bet("MU", "-7.99"), _closed_bet("ON", "+15.28"),
              _closed_bet("AYI", "-6.17"), _closed_bet("BB", "-33.30"),
              _closed_bet("CIEN", "-19.09"), _closed_bet("ILLR", "+69.74", "short")]


def _board(monkeypatch, rows, head_rows=None):
    """Drive the real _pool_scoreboard with a faked catalogue + faked HEAD copy."""
    from research import bets
    monkeypatch.setattr(bets, "_load", lambda: list(rows))
    monkeypatch.setattr(D, "_committed",
                        lambda p: list(head_rows if head_rows is not None else rows))
    return _REAL_BOARD()


def test_every_scoreboard_row_counts_the_same_bets(monkeypatch):
    """The 2026-08-19 owner report: "5 of 30 settled · 1 of 5 beat · 63 open — these all seem
    related, but they don't add up." They could not: 30 was a TARGET, 5 was the scored verdict
    pool, and 63 counted every open bet including the shorts the verdict rule strips. Every row
    now counts the SAME population — 5 scored + 53 running IS the pool, and 30 is visibly the
    finish line — and the bar is a count, so "beat" never means a rate on one row and a tally
    on the next."""
    pool = _LIVE_POOL + [_open_bet(f"O{i}") for i in range(53)] + [_open_bet("S", "short")]
    actions, lines = _board(monkeypatch, pool)
    assert actions == []                        # the scoreboard never asks for anything
    assert lines == [
        "<b>Scored:</b> 5 of 30 needed · 53 still running",
        "<b>So far:</b> 1 of 5 beat · median 8.0% behind",
        "<b>To pass:</b> 17 of 30 beating · median 1%+ ahead"]
    assert all(len(D._plain(l)) <= 50 for l in lines)   # each fits one phone line, unwrapped
    # No header, no gloss [2026-08-19, owner call]: "Scoreboard — each bet vs its benchmark"
    # explained what the rows already show. The glyph marks the block; the rows carry the news.
    assert len(lines) == 3 and not any("Scoreboard" in l or "benchmark" in l for l in lines)
    joined = " ".join(lines)
    for jargon in ("Σ", "p=", "α", "long-only", "shorts", "POOL", "n=", "-8.0%", "55%"):
        assert jargon not in joined, jargon


def test_scoreboard_zero_scored_still_shows_the_target(monkeypatch):
    """Nothing scored yet → no "So far" row to invent, but the target and the bar still stand."""
    _, lines = _board(monkeypatch, [_open_bet("NOW")])
    assert lines == ["<b>Scored:</b> 0 of 30 needed · 1 still running",
                     "<b>To pass:</b> 17 of 30 beating · median 1%+ ahead"]


def test_scoreboard_at_bar_says_verdict_time(monkeypatch):
    full = [_closed_bet(f"T{i}", "+3.00") for i in range(30)]
    _, lines = _board(monkeypatch, full)        # head == tree → no milestone banner
    assert "<b>Scored:</b> 30 of 30 needed · 0 still running" in lines
    assert "<b>So far:</b> 30 of 30 beat · median 3.0% ahead" in lines
    assert "<b>AT BAR — verdict time</b>" in lines   # its own line: a state change, not a suffix


def test_pass_candidate_appears_from_n10_and_is_labeled_below_bar(monkeypatch):
    """The early-shape flag can never be quoted as a pass — the label travels with it."""
    ten = [_closed_bet(f"T{i}", "+3.00") for i in range(10)]
    _, lines = _board(monkeypatch, ten)
    pc = next(l for l in lines if "Ahead of the bar" in l)
    assert "nothing passes before 30 have scored" in pc     # the caveat travels with the flag

    _, lines2 = _board(monkeypatch, ten[:9])
    assert not any("Ahead of the bar" in l for l in lines2)  # n=9: no flag, however pretty


def test_milestone_fires_only_on_a_crossing(monkeypatch):
    """Stateless: HEAD had 9 settled longs, the tree has 10 → banner. HEAD already at 10 →
    quiet. Depends on daily.sh running the digest BEFORE push_ledgers commits."""
    ten = [_closed_bet(f"T{i}", "+1.00") for i in range(10)]
    _, lines = _board(monkeypatch, ten, head_rows=ten[:9])
    assert any("🏁" in l and "10 scored" in l for l in lines)

    _, lines2 = _board(monkeypatch, ten + [_closed_bet("T11", "+1.00")], head_rows=ten)
    assert not any("🏁" in l for l in lines2)                 # 10→11 is not a crossing


def test_scoreboard_never_reads_the_book(monkeypatch):
    """v3 has no book coupling anywhere in the digest — a retired OR live book changes
    nothing. The module does not even import research.book."""
    from research import book
    def boom(*a, **k):
        raise AssertionError("the digest must not touch the book")
    monkeypatch.setattr(book, "_load", boom)
    monkeypatch.setattr(book, "equity_marks", boom)
    _, lines = _board(monkeypatch, _LIVE_POOL)
    assert any("Scored:" in l for l in lines)
    import inspect
    imports = [l for l in inspect.getsource(D).splitlines()
               if "import" in l and not l.strip().startswith("#")]
    assert not any("book" in l for l in imports), imports


def test_scoreboard_degrades_loud_not_silent_without_git(monkeypatch):
    """No git / no HEAD copy must not quietly revert the message to a shape that looks normal —
    the whole scoreboard goes DOWN through _safe (a half-degraded scoreboard that silently
    drops milestones would look completely healthy)."""
    def boom(*a, **k):
        raise RuntimeError("not a git repository")
    monkeypatch.setattr(D, "_committed", boom)
    monkeypatch.setattr(D, "_pool_scoreboard", _REAL_BOARD)
    out = D.compose()
    assert "scoreboard silo DOWN" in out and "DO NOW (1)" in out


# ------------------------------------------------------------------------ the 📈 bets line

def test_bets_line_dates_the_next_scoring(monkeypatch):
    """Under a LOW-edge prior 'nothing to do' is the honest message most days — so it comes
    with the day evidence next lands, weekday first (the owner reads days, not ISO dates).
    The open COUNT lives in the scoreboard now [2026-08-19]: down here it counted a different
    population than the scoreboard and the two could not be reconciled."""
    from research import bets
    monkeypatch.setattr(bets, "_load", lambda: [
        {"logged_at": "2026-08-04T00:00:00+00:00", "ticker": "SMCI", "horizon_d": "21",
         "status": "open", "excess_pct": "", "benchmark": "SPY", "direction": "long",
         "pattern_tag": ""}])
    actions, lines = _REAL_BETS()
    assert actions == []
    assert lines == ["📈 next scores Wed 09-02 (SMCI)"]


def test_overdue_bet_escalates_but_holiday_drift_does_not(monkeypatch):
    """A bet a day or two "overdue" is holiday drift (July 4 is why MU showed -1d while
    maturing on time). Genuinely stuck ones must become an action — v3 has no passive
    maturing list left to hide in."""
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
    actions, lines = _REAL_BETS()
    assert actions and "settlement STUCK" in actions[0] and "STUCK overdue" in actions[0]
    assert "DRIFT" not in actions[0]             # -1d is normal, not an alarm
    assert lines == []                           # both matured: nothing is scheduled to score


def test_bets_line_counts_the_rest_of_the_settle_week(monkeypatch):
    from datetime import date, timedelta
    from research import bets

    def row(ticker, busdays_left, horizon=21):
        d, back, gone = date.today(), 0, horizon - busdays_left
        while gone > 0:
            back += 1
            if (d - timedelta(days=back)).weekday() < 5:
                gone -= 1
        return {"logged_at": (d - timedelta(days=back)).isoformat(), "ticker": ticker,
                "horizon_d": str(horizon), "status": "open", "benchmark": "SPY",
                "direction": "long", "excess_pct": "", "pattern_tag": ""}

    monkeypatch.setattr(bets, "_load", lambda: [row("A", 2), row("B", 3), row("C", 4)])
    _, lines = _REAL_BETS()
    assert "· 2 more ≤5d" in lines[0]


# ------------------------------------------------------------------ alarm sections (ported)

def test_git_section_flags_uncommitted_ledgers(monkeypatch):
    """The 2026-07-27 bug: an alert claiming to be 'scored either way' while no row was
    committed. The digest now says so in the same message."""
    import subprocess
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: type(
        "R", (), {"stdout": " M research/bets_catalogue.csv\n"})())
    actions, _ = _REAL_GIT()
    assert actions and "uncommitted" in actions[0] and "NOT scored" in actions[0]


def test_git_section_silent_without_git(monkeypatch):
    """Fail-soft: no git / no upstream must never add noise or break the push."""
    import subprocess

    def boom(*a, **k):
        raise FileNotFoundError("git")
    monkeypatch.setattr(subprocess, "run", boom)
    assert _REAL_GIT() == ([], [])


def test_stranded_section_flags_a_parked_backup_ref(monkeypatch):
    """A $FAILS heartbeat fires once, on the day of the strand. 1b014cc proved that is not
    enough — the alarm was seen, nothing was done, and master ran two days without the work.
    This nags every run until a human recovers the ref and deletes it."""
    import subprocess
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: type("R", (), {
        "stdout": "1b014ccf915596594d293b823a50a05f2c017ca6\trefs/heads/settle-backup/20260731-1b014cc\n"})())
    actions, _ = _REAL_STRANDED()
    assert len(actions) == 1
    assert "STRANDED" in actions[0] and "settle-backup/20260731-1b014cc" in actions[0]
    assert "cherry-pick" in actions[0] and "--delete" in actions[0]   # paste-ready cure


def test_stranded_section_silent_when_nothing_is_parked(monkeypatch):
    """The healthy case must add ZERO noise, or the DO-NOW list trains the human to skim it."""
    import subprocess
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: type("R", (), {"stdout": "\n"})())
    assert _REAL_STRANDED() == ([], [])


def test_stranded_section_silent_without_network(monkeypatch):
    """ls-remote is the only NETWORK call in the digest. Offline must degrade to silence, not
    take the whole push down — the digest is the daily proof-of-life."""
    import subprocess

    def boom(*a, **k):
        raise subprocess.TimeoutExpired("git", 20)
    monkeypatch.setattr(subprocess, "run", boom)
    assert _REAL_STRANDED() == ([], [])


def test_feed_section_escalates_a_stale_source(tmp_path, monkeypatch):
    """A dead feed returns nothing rather than raising, so only a recorded last_ok can
    distinguish 'quiet day' from 'openinsider has been down for a week'."""
    import json
    from datetime import date, timedelta
    p = tmp_path / "feed.json"
    old = (date.today() - timedelta(days=21)).isoformat()
    p.write_text(json.dumps({"openinsider": {"last_ok": old, "last_error": "HTTP 503"}}))
    monkeypatch.setattr(D, "FEED_STATUS", str(p))
    actions, _ = _REAL_FEED()
    assert actions and "openinsider" in actions[0] and "HTTP 503" in actions[0]


def test_feed_section_never_invents_a_duration(tmp_path, monkeypatch):
    """A source with no last_ok has never succeeded — say THAT. The untested else-branch used
    a `99` sentinel, so the live alarm read "has not succeeded in 99 weekdays" when the real
    gap was 27. A fabricated number inside an alarm is how a DO-NOW list loses its authority."""
    import json
    p = tmp_path / "feed.json"
    p.write_text(json.dumps({"openinsider": {"last_error": "URLError: [Errno 111] refused"}}))
    monkeypatch.setattr(D, "FEED_STATUS", str(p))
    actions, _ = _REAL_FEED()
    assert actions and "NEVER reported a successful fetch" in actions[0]
    assert "99" not in actions[0]
    assert "Errno 111" in actions[0]        # the REAL cause, not "fetch returned no clusters"


def test_feed_section_quiet_when_fresh(tmp_path, monkeypatch):
    import json
    from datetime import date
    p = tmp_path / "feed.json"
    p.write_text(json.dumps({"openinsider": {"last_ok": date.today().isoformat()}}))
    monkeypatch.setattr(D, "FEED_STATUS", str(p))
    assert _REAL_FEED() == ([], [])
    monkeypatch.setattr(D, "FEED_STATUS", str(tmp_path / "missing.json"))
    assert _REAL_FEED() == ([], [])        # never written yet → claim nothing


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
    actions, _ = _REAL_FEED()
    assert actions and "bars last advanced" in actions[0]
    assert "denominator did not advance" in actions[0]


def test_feed_section_escalates_thin_coverage(tmp_path, monkeypatch):
    from datetime import date
    _feed_json(tmp_path, monkeypatch,
               {"last_ok": date.today().isoformat(), "n_ok": 250, "n_total": 503})
    actions, _ = _REAL_FEED()
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
    assert _REAL_FEED() == ([], [])


def test_feed_section_legacy_key_without_new_fields_silent(tmp_path, monkeypatch):
    from datetime import date
    _feed_json(tmp_path, monkeypatch, {"last_ok": date.today().isoformat()})
    assert _REAL_FEED() == ([], [])


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
    assert _REAL_FEED() == ([], [])


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
    actions, _ = _REAL_FEED()
    assert actions and "behind the last scan" in actions[0]


def test_feed_section_dead_scan_flags_on_the_second_missed_weekday(tmp_path, monkeypatch):
    """The 08-09 lag fix measures bars against the LAST scan, so a dead read routine freezes
    last_ok and last_bar together and the bar alarm can never fire — last_ok staleness is the
    only detector left, and nothing else watches the read leg (push_log alarms were
    settle-only then, the watchdog watches settle's commits). Escalation pinned at the second
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
    actions, _ = _REAL_FEED()
    assert actions and "has not succeeded" in actions[0]


# ------------------------------------------------------------------------- plain + fail-soft

def test_plain_strips_markup():
    assert D._plain("<b>SETTLE</b> &lt;fill&gt;") == "SETTLE <fill>"


def test_safe_degrades_on_error():
    """Fail-soft, but LOUD since 2026-07-27: the run survives a dead silo and now SAYS so
    in the DO-NOW list instead of degrading to a line nobody reads."""
    a, lines = D._safe(lambda: (_ for _ in ()).throw(RuntimeError("boom")), "bets")
    assert lines[0].startswith("bets: unavailable")
    assert a and "bets silo DOWN" in a[0]


# ------------------------------------------------------------------ delivery (v2 machinery,
# byte-for-byte semantics — only the composed TEXT changed in v3)

def test_run_prints_the_delivery_verdict(monkeypatch, capsys, tmp_path):
    """The verdict line is the ONLY truth about delivery [2026-08-06]: exit 1 covers both
    non-delivered states (daily.sh accounting unchanged), but only REJECTED licenses a
    re-send — an agent that re-sent on UNCONFIRMED double-posted (the 'delivery check' copy)."""
    from research import notify
    monkeypatch.setattr(D, "PUSH_LOG", str(tmp_path / "push_log.csv"))
    monkeypatch.setattr(D, "compose", lambda note: "x")
    for verdict, marker, code in [(True, "PUSH DELIVERED", 0),
                                  (None, "PUSH UNCONFIRMED", 1),
                                  (False, "PUSH REJECTED", 1)]:
        monkeypatch.setattr(notify, "send", lambda t, html=False, v=verdict: v)
        assert D.run(["--notify", "note"]) == code
        assert marker in capsys.readouterr().out


def test_run_stamps_the_push_log_and_slim_marks_the_read_leg(monkeypatch, tmp_path):
    """Every --notify push leaves one committed delivery row — the record a later run reads
    to detect a message that died in transport while the commits landed. --slim's only v3 job:
    stamp the row as the READ leg (composition no longer branches on it)."""
    import csv
    from research import notify
    p = tmp_path / "push_log.csv"
    monkeypatch.setattr(D, "PUSH_LOG", str(p))
    monkeypatch.setattr(D, "compose", lambda note: "x")
    monkeypatch.setattr(notify, "send", lambda t, html=False: True)
    D.run(["--notify", "--slim", "n"])
    monkeypatch.setattr(notify, "send", lambda t, html=False: None)
    D.run(["--notify", "n"])
    with open(p, newline="") as f:
        rows = list(csv.DictReader(f))
    assert [(r["kind"], r["verdict"]) for r in rows] == [("read", "DELIVERED"),
                                                         ("settle", "UNCONFIRMED")]


def test_slim_no_longer_changes_the_composition(monkeypatch, tmp_path):
    """v3: the headline is the leg's identity; --slim is a push-log stamp only. Same note →
    same text, flag or no flag."""
    from research import notify
    monkeypatch.setattr(D, "PUSH_LOG", str(tmp_path / "push_log.csv"))
    monkeypatch.setattr(notify, "send", lambda t, html=False: True)
    assert D.compose("📖 READ x\n🟢 card") == D.compose("📖 READ x\n🟢 card")
    sent = []
    monkeypatch.setattr(notify, "send", lambda t, html=False: sent.append(t) or True)
    D.run(["--notify", "--slim", "📖 READ x"])
    D.run(["--notify", "📖 READ x"])
    assert sent[0] == sent[1]


def test_run_survives_a_notify_death_and_still_stamps(monkeypatch, capsys, tmp_path):
    """The 2026-08-07 strand: a cold container without python-dotenv killed the notify import
    AND the heartbeat's — no stamp, no verdict, no alarm. A death anywhere in the notify block
    must now still leave a stamp and print a verdict line (FINDINGS 2026-08-08). A raising
    send() is treated as AMBIGUOUS (may be post-request) → UNCONFIRMED, never re-send."""
    import csv
    from research import notify
    p = tmp_path / "push_log.csv"
    monkeypatch.setattr(D, "PUSH_LOG", str(p))
    monkeypatch.setattr(D, "compose", lambda note: "x")

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
    assert _REAL_PUSHLOG() == ([], [])          # no file (pre-rollout) → silent
    p.write_text("date_utc,kind,verdict\n2026-08-07,read,DELIVERED\n")
    assert _REAL_PUSHLOG() == ([], [])          # no settle rows yet → silent
    p.write_text("date_utc,kind,verdict\n2026-08-07,settle,UNCONFIRMED\n")
    actions, _ = _REAL_PUSHLOG()
    assert actions and "never confirmed delivered" in actions[0]
    p.write_text("date_utc,kind,verdict\n2026-08-06,settle,DELIVERED\n")
    actions2, _ = _REAL_PUSHLOG()
    assert actions2                                      # today's due settle never stamped
    p.write_text("date_utc,kind,verdict\n2026-08-07,settle,DELIVERED\n")
    assert _REAL_PUSHLOG() == ([], [])          # healthy
    # before 23:00 UTC today's settle is not yet due — yesterday's DELIVERED row satisfies
    # (this is also the next-morning read composing at 11:42)
    monkeypatch.setattr(D, "_utcnow", lambda: datetime(2026, 8, 7, 11, 42, tzinfo=timezone.utc))
    p.write_text("date_utc,kind,verdict\n2026-08-06,settle,DELIVERED\n")
    assert _REAL_PUSHLOG() == ([], [])


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
    of its own — so the next morning's brief still opened with an all-clear. The read leg is
    the one that carries the TRADE ALERTS. FEED_STALE_D=1 cannot cover it: the run was alive
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
