"""Guard the public page's construction rules [BACKLOG P7a, audience contract 2026-08-15]:
render() is pure, so test it directly — the summary must match bets.stats (long-only), the
FULL catalogue must be on the page (filters are views, never removals), ledger prose must be
escaped, internal method language must NOT leak to the end user, and the module must never
touch the real-dollar book (publishable by construction)."""
import inspect

from research import site


def _long(ticker, excess, entry="2026-01-06", logged="2026-01-05", h="21", status="closed"):
    return {"logged_at": f"{logged}T12:00:00+00:00", "ticker": ticker, "direction": "long",
            "horizon_d": h, "benchmark": "SPY", "thesis": f"{ticker} thesis",
            "status": status, "entry_date": entry if status == "closed" else "",
            "entry": "100.00", "excess_pct": excess if status == "closed" else "",
            "pattern_tag": "test-tag", "notified": ""}


BETS = [
    _long("AAA", "+5.00", entry="2026-01-06"),
    _long("BBB", "-3.00", entry="2026-01-07"),
    {**_long("CCC", "+9.00", entry="2026-01-08"), "direction": "short"},  # table-only
    _long("DDD", "", status="open"),
]


def test_summary_is_long_only():
    page = site.render(BETS)
    assert '<div class="tvalue">2</div>' in page      # settled = 2 longs, never the short
    assert "+1.00%" in page                           # median of (+5, −3)
    assert "50%" in page                              # beat rate
    assert "+2.0pp" in page                           # total excess, verdict population only
    assert "short entries appear in the table but are not scored" in page


def test_full_catalogue_is_on_the_page_with_views_not_removals():
    page = site.render(BETS)
    for t in ("AAA", "BBB", "CCC", "DDD"):            # open + short included, always
        assert t in page
    assert 'data-status="open"' in page and 'data-status="closed"' in page
    assert 'id="chips"' in page and 'id="tagsel"' in page   # filters
    assert 'data-type="n"' in page                          # sortable numeric columns
    assert "AAA thesis" in page                             # the full record stays on the page…
    assert 'class="det"' in page and "hidden" in page and "▸" in page  # …behind a click
    assert "Not investment advice" in page


def test_no_internal_method_language_leaks_to_the_end_user():
    """The audience contract (owner, 2026-08-15): explanations are for the OWNER's eyes.
    The repo's internal vocabulary must never render on the public surface."""
    page = site.render(BETS)
    for jargon in ("pre-register", "Wilcoxon", "diagnostic", "[ARC", "Arc 5", "verdict",
                   "denominator", "survivorship", "bar N", "PASS-CANDIDATE", "BELOW BAR"):
        assert jargon not in page, jargon


def test_tabs_and_table_annotations():
    """The 2026-08-24 redesign: predictions/performance tabs; a closed short's excess is
    muted 'unscored', never sign-colored (the table must not contradict the long-only
    summary count); pre-tag-era rows label as 'early' (never backfilled); tag labels
    humanize in display while the raw tag stays the filter/sort value."""
    rows = BETS + [dict(_long("EEE", "+2.00"), pattern_tag="")]
    page = site.render(rows)
    assert 'id="tabs"' in page and 'data-tab="predictions"' in page
    assert 'class="num unscored"' in page                    # CCC, the closed short
    assert 'title="Shown, not scored into the summary"' in page
    assert '(short — shown, not scored into the summary)' in page
    assert '>early</td>' in page                             # EEE, blank tag
    assert '<option value="test-tag">Test tag</option>' in page
    assert 'data-tag="test-tag"' in page


def test_ledger_prose_is_escaped():
    rows = [dict(_long("GGG", "+1.00"), thesis='<script>alert("x")</script>')]
    page = site.render(rows)
    assert '<script>alert' not in page
    assert "&lt;script&gt;" in page


def test_curve_points_order_and_cumsum():
    pts = site.curve_points(BETS)
    assert [p["ticker"] for p in pts] == ["AAA", "BBB"]    # maturity order; short/open excluded
    assert [p["cum"] for p in pts] == [5.0, 2.0]


def test_charts_render_with_sign_split_bars():
    page = site.render(BETS)
    # role="img" counts the CHARTS only — the masthead brand mark (added 2026-08-21) is a
    # third <svg> and is deliberately aria-hidden, so a raw "<svg" count no longer works.
    assert page.count('role="img"') == 2                    # curve + per-prediction bars
    assert 'fill="var(--barneg)"' in page                   # BBB's negative bar
    assert 'fill="var(--series)"' in page


def test_empty_ledger_still_renders():
    page = site.render([])
    assert "No settled predictions yet" in page and "Not investment advice" in page


def test_never_touches_the_real_dollar_book():
    """Publishable by construction: the page must survive being public, so the module may
    read the bets catalogue only — never research.book or its CSVs."""
    src = inspect.getsource(site).replace(site.__doc__, "", 1)  # the docstring NAMES the rule
    assert "import book" not in src and "book.csv" not in src and "book_equity" not in src


def test_write_creates_the_page(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)                    # empty ledger → still a valid page
    s = site.write()
    out = tmp_path / "docs" / "index.html"
    assert out.exists() and s["bets"] == 0
    html = out.read_text()
    # Identity, not just the ledger name: a visitor arriving from the profile README must be
    # able to tell whose work this is (renamed 2026-08-21 — the page was titled "Forward
    # Ledger" with no owner, no repo link and no masthead).
    assert "Swing Lab" in html and "The forward ledger" in html
    assert "github.com/guillearria/swing-lab" in html
    assert "Not investment advice." in html
