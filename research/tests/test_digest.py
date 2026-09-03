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
_REAL_STRANDED, _REAL_EVENTS = D._stranded_section, D._pool_events
_REAL_SCORED, _REAL_QUIET = D._scored_section, D._quiet_line
_REAL_PUSHLOG, _REAL_BETS = D._pushlog_section, D._bets_section


@pytest.fixture(autouse=True)
def _neutralize_environment_sections(monkeypatch):
    """Every section inspects the actual repo, remote, ledgers or data dir — un-stubbed they
    make each compose test depend on this checkout's live state (and _stranded_section would
    hit the NETWORK). Stub them all by default; each has its own dedicated test."""
    for name in ("_bets_section", "_git_section", "_stranded_section",
                 "_feed_section", "_pushlog_section", "_pool_events",
                 "_scored_section", "_quiet_line"):
        monkeypatch.setattr(D, name, lambda *a, **k: ([], []))


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
    monkeypatch.setattr(D, "_pool_events", lambda: ([], ["<b>AT BAR — verdict time</b>"]))
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
    monkeypatch.setattr(D, "_quiet_line", lambda: ([], ["Nothing matured today — 62 bets running."]))
    monkeypatch.setattr(D, "_bets_section", lambda: ([], ["📈 62 open"]))
    out = D.compose()
    assert "\n\n\n" not in out
    assert out.rstrip("\n") == out and not out.startswith("\n")
    # the quiet settle day [v4] is banner · one sentence · 📈 — three blocks, two blank lines
    assert out.split("\n")[1:] == ["", "Nothing matured today — 62 bets running.", "", "📈 62 open"]


def test_an_empty_section_adds_no_blank_line(monkeypatch):
    """A silo that returns nothing must not leave its separator behind — that is how a message
    grows a blank wall one dead section at a time."""
    monkeypatch.setattr(D, "_bets_section", lambda: ([], []))
    assert "\n" not in D.compose()            # every silo empty → the banner alone [v4]


def test_run_note_headline_tops_and_cards_ride_above_the_bets_line(monkeypatch):
    """The note's first line is the leg's identity (Telegram preview); its body — the 🟢 NEW
    BET cards — is the morning's news and lands after the scoreboard and any ⚠️ list, ABOVE the
    📈 line. v2 demoted the cards to a bottom RUN NOTE block; v3 does not."""
    monkeypatch.setattr(D, "_pool_events", lambda: ([], ["<b>AT BAR — verdict time</b>"]))
    monkeypatch.setattr(D, "_bets_section", lambda: (["X STUCK"], ["📈 63 open"]))
    lines = D.compose("📖 READ Wed 2026-08-19 pre-market: 1 bet\n"
                      "🟢 NEW BET #69 — CAVA long · 21d vs XLY\nWHY: capitulation").split("\n")
    assert lines[0] == "<b>📖 READ Wed 2026-08-19 pre-market: 1 bet</b>"
    assert "📋" not in "\n".join(lines)                     # headline replaces the banner
    assert "Nothing matured" not in "\n".join(lines)        # a note owns its narrative [v4]
    i_do = lines.index("⚠️ <b>DO NOW (1)</b>")
    i_card = lines.index("<blockquote><b>🟢 NEW BET #69 — CAVA long · 21d vs XLY</b>")
    i_bets = lines.index("📈 63 open")
    assert lines.index("<b>AT BAR — verdict time</b>") < i_do < i_card < i_bets


def test_narrative_lines_merge_into_one_paragraph():
    """[MSG v4.1, owner 2026-08-25]: the run's results read "in natural speech in one single
    paragraph at most" — the digest enforces the PARAGRAPH structurally by merging every
    loose line before the first 🟢 into one block, so a listy note can never render as a
    stack of bullets. Fossil lines still drop first; escaping still holds through the join."""
    out = D.compose("📖 READ\nRead 42 movers; took FN.\nSkips were macro noise.\n"
                    "movers: 42 seen\n"
                    "🟢 NEW BET #1 — FN long\nWhy: beat flushed")
    lines = out.split("\n")
    assert "Read 42 movers; took FN. Skips were macro noise." in lines   # ONE line, merged
    assert not any(l == "Skips were macro noise." for l in lines)        # never its own bullet
    assert "movers: 42 seen" not in out                                  # fossil still dropped
    merged = D.compose("📖 READ\na & b\nc <i>d</i>")
    assert "a &amp; b c &lt;i&gt;d&lt;/i&gt;" in merged                  # escape survives join


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
    monkeypatch.setattr(D, "_pool_events", _REAL_EVENTS)
    monkeypatch.setattr(D, "_scored_section", _REAL_SCORED)
    monkeypatch.setattr(D, "_quiet_line", _REAL_QUIET)
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


# ------------------------------------- event flags · scored cards · the quiet line (v4)

_L = {"logged_at": "2026-06-01T00:00:00+00:00", "direction": "long", "horizon_d": "21",
      "benchmark": "SPY", "thesis": "t", "pattern_tag": "", "notified": "x",
      "entry_date": "2026-06-02", "entry": "10.00", "conviction": ""}


def _closed_bet(ticker, excess, direction="long", **kw):
    return {**_L, "ticker": ticker, "direction": direction, "status": "closed",
            "excess_pct": excess, **kw}


def _open_bet(ticker, direction="long"):
    return {**_L, "ticker": ticker, "direction": direction, "status": "open",
            "excess_pct": "", "entry_date": "", "entry": ""}


# The lock-time live vector [ARC 5 #12a]: long-only n=5 median −7.99% beat 20%, plus the ILLR
# short that the long-only rule strips from the verdict (and v3 strips from Telegram entirely).
_LIVE_POOL = [_closed_bet("MU", "-7.99"), _closed_bet("ON", "+15.28"),
              _closed_bet("AYI", "-6.17"), _closed_bet("BB", "-33.30"),
              _closed_bet("CIEN", "-19.09"), _closed_bet("ILLR", "+69.74", "short")]


def _events(monkeypatch, rows, head_rows=None):
    """Drive the real _pool_events with a faked catalogue + faked HEAD copy."""
    from research import bets
    monkeypatch.setattr(bets, "_load", lambda: list(rows))
    monkeypatch.setattr(D, "_committed",
                        lambda p: list(head_rows if head_rows is not None else rows))
    return _REAL_EVENTS()


def _scored(monkeypatch, rows):
    from research import bets
    monkeypatch.setattr(bets, "_load", lambda: list(rows))
    return _REAL_SCORED()


def test_the_static_pool_rows_are_gone(monkeypatch):
    """[MSG v4, owner 2026-08-25]: the Scored/So-far/To-pass rows "repeat themselves almost
    daily" — they are OFF Telegram (CLI keeps them). On an ordinary day between crossings the
    events section is EMPTY, which is the whole point."""
    pool = _LIVE_POOL + [_open_bet(f"O{i}") for i in range(53)]
    actions, lines = _events(monkeypatch, pool)
    assert actions == [] and lines == []
    joined = " ".join(lines)
    for fossil in ("Scored:", "So far:", "To pass:"):
        assert fossil not in joined


def test_at_bar_flag_fires_only_at_the_bar(monkeypatch):
    full = [_closed_bet(f"T{i}", "+3.00") for i in range(30)]
    _, lines = _events(monkeypatch, full)        # head == tree → no milestone banner
    assert lines == ["<b>AT BAR — verdict time</b>"]


def test_pass_candidate_appears_from_n10_and_is_labeled_below_bar(monkeypatch):
    """The early-shape flag can never be quoted as a pass — the label travels with it."""
    ten = [_closed_bet(f"T{i}", "+3.00") for i in range(10)]
    _, lines = _events(monkeypatch, ten)
    pc = next(l for l in lines if "Ahead of the bar" in l)
    assert "nothing passes before 30 have scored" in pc     # the caveat travels with the flag

    _, lines2 = _events(monkeypatch, ten[:9])
    assert not any("Ahead of the bar" in l for l in lines2)  # n=9: no flag, however pretty


def test_milestone_fires_only_on_a_crossing(monkeypatch):
    """Stateless: HEAD had 9 settled longs, the tree has 10 → banner. HEAD already at 10 →
    quiet. Depends on daily.sh running the digest BEFORE push_ledgers commits."""
    ten = [_closed_bet(f"T{i}", "+1.00") for i in range(10)]
    _, lines = _events(monkeypatch, ten, head_rows=ten[:9])
    assert any("🏁" in l and "10 scored" in l for l in lines)

    _, lines2 = _events(monkeypatch, ten + [_closed_bet("T11", "+1.00")], head_rows=ten)
    assert not any("🏁" in l for l in lines2)                 # 10→11 is not a crossing


def test_scored_card_renders_result_and_read_lines(monkeypatch):
    """[MSG v4] A settled bet arrives as a 📊 blockquote card — the same card grammar as 🟢 —
    with the Read line carrying the tag · conviction the row was registered under, and ONE
    tally sentence after the card(s): the pool numbers appear exactly when they changed."""
    rows = list(_LIVE_POOL) + [_closed_bet("HAE", "+3.20", notified="",
                                           pattern_tag="post-earnings-drift",
                                           conviction="high")]
    actions, lines = _scored(monkeypatch, rows)
    assert actions == []
    out = "\n".join(lines)
    assert "<blockquote><b>📊 SCORED — HAE long 21d vs SPY</b>" in out
    assert "<b>Result:</b> 3.2% ahead ✓" in out
    assert "<b>Read:</b> post-earnings-drift · conviction high</blockquote>" in out
    assert "Now 6 of 30 scored · 2 of 6 beat" in out          # the tally rides the card block
    for line in lines:                                        # tags never span lines except
        assert line.count("<b>") == line.count("</b>")        # the blockquote (compose rule)


def test_scored_card_without_tag_or_conviction_omits_the_read_line(monkeypatch):
    rows = [_closed_bet("MU", "-7.99", notified="")]
    _, lines = _scored(monkeypatch, rows)
    out = "\n".join(lines)
    assert "<b>Read:</b>" not in out
    assert "<b>Result:</b> 8.0% behind</blockquote>" in out   # no ✓ on a loss


def test_scored_short_is_labeled_diagnostic_and_tally_stays_long_only(monkeypatch):
    """A settling SHORT is announced (diagnostic row) but the tally is always the long-only
    verdict population [ARC 5 #12a] — s=None (no longs settled yet) must not kill the card."""
    _, lines = _scored(monkeypatch, [_closed_bet("ILLR", "+69.74", "short", notified="")])
    out = "\n".join(lines)
    assert "📊 SCORED — ILLR short 21d vs SPY" in out
    assert "(short — diagnostic, outside the pool)" in out
    assert "0 of 30 scored." in out


def test_no_unannounced_settlements_means_no_scored_block(monkeypatch):
    assert _scored(monkeypatch, list(_LIVE_POOL)) == ([], [])


def test_quiet_line_counts_the_verdict_pool(monkeypatch):
    """One population everywhere [2026-08-19 owner report, carried into v4]: the quiet
    sentence's running count is the verdict pool's open longs — the same rows the tally and
    the flags count — never every open row including shorts."""
    from research import bets
    rows = list(_LIVE_POOL) + [_open_bet(f"O{i}") for i in range(53)] + [_open_bet("S", "short")]
    monkeypatch.setattr(bets, "_load", lambda: list(rows))
    assert _REAL_QUIET() == ([], ["Nothing matured today — 53 bets running."])


def test_quiet_sentence_yields_to_scored_cards_and_to_a_note(monkeypatch):
    """[MSG v4] the narrative slot has one occupant: a note's own sentences, else the 📊
    cards, else the synthesized quiet line — never two of them."""
    monkeypatch.setattr(D, "_quiet_line", lambda: ([], ["Nothing matured today — 5 bets running."]))
    assert "Nothing matured" in D.compose()                   # noteless, scoreless → sentence
    monkeypatch.setattr(D, "_scored_section",
                        lambda: ([], ["<blockquote><b>📊 SCORED — X long 21d vs SPY</b></blockquote>"]))
    out = D.compose()
    assert "Nothing matured" not in out and "📊 SCORED" in out  # cards ARE the news
    assert "Nothing matured" not in D.compose("📖 READ\nRead 40 movers; took none.")


def test_events_never_read_the_book(monkeypatch):
    """v3's no-book-coupling rule survives v4 — the module does not even import research.book."""
    from research import book
    def boom(*a, **k):
        raise AssertionError("the digest must not touch the book")
    monkeypatch.setattr(book, "_load", boom)
    monkeypatch.setattr(book, "equity_marks", boom)
    _events(monkeypatch, _LIVE_POOL)
    import inspect
    imports = [l for l in inspect.getsource(D).splitlines()
               if "import" in l and not l.strip().startswith("#")]
    assert not any("book" in l for l in imports), imports


def test_events_degrade_loud_not_silent_without_git(monkeypatch):
    """No git / no HEAD copy must not quietly revert the message to a shape that looks normal —
    the whole section goes DOWN through _safe (a half-degraded section that silently drops
    milestones would look completely healthy)."""
    def boom(*a, **k):
        raise RuntimeError("not a git repository")
    monkeypatch.setattr(D, "_committed", boom)
    monkeypatch.setattr(D, "_pool_events", _REAL_EVENTS)
    out = D.compose()
    assert "pool-events silo DOWN" in out and "DO NOW" in out


def test_delivered_push_stamps_the_scored_rows(monkeypatch, tmp_path, capsys):
    """[MSG v4] the 📊 delivery guarantee, transferred: mark_notified fires ONLY on the
    DELIVERED verdict — a REJECTED or UNCONFIRMED push leaves the rows unstamped so their
    cards re-render in the next delivered digest."""
    from research import bets, notify
    calls = []
    monkeypatch.setattr(bets, "mark_notified", lambda: calls.append(1) or 1)
    for i, verdict in enumerate((True, False, None)):
        calls.clear()
        # a fresh log per verdict: the same-day guard [2026-09-01] would otherwise SKIP every
        # push after the first DELIVERED one and the later cases would test nothing
        monkeypatch.setattr(D, "PUSH_LOG", str(tmp_path / f"push_log{i}.csv"))
        monkeypatch.setattr(notify, "send", lambda t, html=False, _v=verdict: _v)
        D.run(["--notify"])
        assert len(calls) == (1 if verdict is True else 0), verdict


# ------------------------------------------------------------------------ the 📈 bets line

def test_bets_line_dates_the_next_scoring(monkeypatch):
    """Under a LOW-edge prior 'nothing to do' is the honest message most days — so it comes
    with the day evidence next lands, weekday first (the owner reads days, not ISO dates).
    The open COUNT lives in the scoreboard now [2026-08-19]: down here it counted a different
    population than the scoreboard and the two could not be reconciled."""
    from datetime import date

    from research import bets

    class _Aug21(date):                 # this row matures 09-02 and next_maturity() skips
        @classmethod                    # matured rows — on the real clock this test dies 09-03
        def today(cls):
            return cls(2026, 8, 21)

    monkeypatch.setattr(D, "date", _Aug21)      # _bets_section reads digest's date...
    monkeypatch.setattr(bets, "date", _Aug21)   # ...next_maturity reads bets' own
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
    monkeypatch.setattr(D, "compose", lambda note, leg="settle": "x")
    for verdict, marker, code in [(True, "PUSH DELIVERED", 0),
                                  (None, "PUSH UNCONFIRMED", 1),
                                  (False, "PUSH REJECTED", 1)]:
        # fresh log per case — the same-day guard [2026-09-01] would SKIP after the first
        monkeypatch.setattr(D, "PUSH_LOG", str(tmp_path / f"push_log_{marker[5:]}.csv"))
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
    monkeypatch.setattr(D, "compose", lambda note, leg="settle": "x")
    monkeypatch.setattr(notify, "send", lambda t, html=False: True)
    D.run(["--notify", "--slim", "n"])
    monkeypatch.setattr(notify, "send", lambda t, html=False: None)
    D.run(["--notify", "n"])
    with open(p, newline="") as f:
        rows = list(csv.DictReader(f))
    assert [(r["kind"], r["verdict"]) for r in rows] == [("read", "DELIVERED"),
                                                         ("settle", "UNCONFIRMED")]


def test_second_same_day_push_is_skipped_never_sent(monkeypatch, tmp_path, capsys):
    """[2026-09-01] The deterministic half of "exactly ONE message per leg": once today's
    push_log holds a DELIVERED (or UNCONFIRMED — never re-send) row for a leg, --notify
    prints PUSH SKIPPED, sends nothing, stamps nothing, exits 0. The other leg is untouched
    and a REJECTED row does not block (nothing was sent — the one sanctioned retry stays
    open). Four of six nights double-posted (08-26..09-01) with the rule living only in the
    routine prompt; a cloud agent re-ran daily.sh and hand-fired this module."""
    import csv
    from research import notify
    p = tmp_path / "push_log.csv"
    monkeypatch.setattr(D, "PUSH_LOG", str(p))
    monkeypatch.setattr(D, "compose", lambda note, leg="settle": "x")
    sent = []
    monkeypatch.setattr(notify, "send", lambda t, html=False: sent.append(t) or True)

    assert D.run(["--notify"]) == 0 and len(sent) == 1           # first settle: delivered
    assert D.run(["--notify"]) == 0 and len(sent) == 1           # second: SKIPPED, not sent
    assert "PUSH SKIPPED" in capsys.readouterr().out
    assert D.run(["--notify", "--slim", "n"]) == 0 and len(sent) == 2   # read leg unaffected
    with open(p, newline="") as f:
        rows = [(r["kind"], r["verdict"]) for r in csv.DictReader(f)]
    assert rows == [("settle", "DELIVERED"), ("read", "DELIVERED")]  # no SKIPPED stamp

    # REJECTED does not block the retry; UNCONFIRMED does (the 2026-08-06 rule, now in code)
    q = tmp_path / "push_log2.csv"
    monkeypatch.setattr(D, "PUSH_LOG", str(q))
    monkeypatch.setattr(notify, "send", lambda t, html=False: False)
    assert D.run(["--notify"]) == 1                              # REJECTED, nothing sent
    monkeypatch.setattr(notify, "send", lambda t, html=False: None)
    assert D.run(["--notify"]) == 1                              # retry allowed → UNCONFIRMED
    monkeypatch.setattr(notify, "send", lambda t, html=False: sent.append(t) or True)
    assert D.run(["--notify"]) == 0 and len(sent) == 2           # blocked: never re-send
    assert "PUSH SKIPPED" in capsys.readouterr().out


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
    monkeypatch.setattr(D, "compose", lambda note, leg="settle": "x")

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


def test_the_composing_leg_never_accuses_itself(monkeypatch, tmp_path):
    """[2026-09-02] The settle digest composed at 23:24 UTC (due-hour 23) and flagged ITS OWN
    day as never delivered — its stamp is written after the text. Past its due-hour the
    composing leg judges itself only up to yesterday; the other leg keeps the full calendar,
    and a settle composing before its due-hour still flags a dead yesterday (weekend cover)."""
    from datetime import datetime, timezone
    p = tmp_path / "push_log.csv"
    monkeypatch.setattr(D, "PUSH_LOG", str(p))
    at = lambda *w: monkeypatch.setattr(D, "_utcnow", lambda: datetime(*w, tzinfo=timezone.utc))
    p.write_text("date_utc,kind,verdict\n2026-09-01,settle,DELIVERED\n2026-09-02,read,DELIVERED\n")
    at(2026, 9, 2, 23, 24)
    assert _REAL_PUSHLOG(composing="settle") == ([], [])          # the 09-02 false alarm
    assert "2026-09-02" in _REAL_PUSHLOG(composing="read")[0][0]   # the other leg still holds it
    p.write_text("date_utc,kind,verdict\n2026-08-31,settle,DELIVERED\n2026-09-02,read,DELIVERED\n")
    at(2026, 9, 2, 22, 55)
    assert "2026-09-01" in _REAL_PUSHLOG(composing="settle")[0][0]   # yesterday's death still flagged
    # compose() and run() thread the leg through: settle by default, read under --slim
    seen = []
    monkeypatch.setattr(D, "_pushlog_section", lambda composing="": seen.append(composing) or ([], []))
    D.compose(); D.compose("📖 READ x", leg="read"); D.run(["--slim", "n"]); D.run([])
    assert seen == ["settle", "read", "read", "settle"]


def test_stamp_and_guard_use_the_leg_day(monkeypatch, tmp_path):
    """[2026-09-02] A settle that ends after midnight UTC must stamp the day it settled, or the
    same-day guard would SKIP the next evening's real digest (the 09-02 run ended 23:24)."""
    import csv
    from datetime import datetime, timezone
    from research import notify
    p = tmp_path / "push_log.csv"
    monkeypatch.setattr(D, "PUSH_LOG", str(p))
    monkeypatch.setattr(D, "compose", lambda note, leg="settle": "x")
    sent = []
    monkeypatch.setattr(notify, "send", lambda t, html=False: sent.append(t) or True)
    monkeypatch.setattr(D, "_utcnow", lambda: datetime(2026, 9, 3, 0, 30, tzinfo=timezone.utc))
    assert D.run(["--notify"]) == 0 and len(sent) == 1
    monkeypatch.setattr(D, "_utcnow", lambda: datetime(2026, 9, 3, 22, 50, tzinfo=timezone.utc))
    assert D._pushed_today("settle") == ""                        # not blocked by the late run
    assert D.run(["--notify"]) == 0 and len(sent) == 2
    with open(p, newline="") as f:
        assert [r["date_utc"] for r in csv.DictReader(f)] == ["2026-09-02", "2026-09-03"]


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
