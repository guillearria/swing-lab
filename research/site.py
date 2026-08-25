"""P7a — the PUBLIC DASHBOARD: the catalogue rendered as ONE static end-user page.

AUDIENCE CONTRACT (owner, 2026-08-15 — supersedes the first, verbose cut): the end user gets
PREDICTIONS and a SUMMARY OF PERFORMANCE SO FAR, nothing else. Method notes, pre-registration
mechanics, bar/verdict language, diagnostics and every other explanation are for the OWNER'S
eyes and live in the repo docs — a public surface that narrates its own reasoning is a leak,
not a feature. What the page keeps, by construction:

- The FULL catalogue, always — every prediction (open, closed, the historic shorts), none
  removed. Filters/sorting are VIEWS on top; the row set never shrinks.
- Performance = the pooled numbers the repo already computes (bets.stats/cum_excess) —
  long-only, each vs its own benchmark. Shorts render in the table, not in the summary.
- PAPER TRACK ONLY: never imports research.book, renders no account dollars (test-enforced)
  — the page must stay publishable while the repo stays private.
- DETERMINISTIC: stdlib, NO CLOCK — the "data through" stamp derives from the ledger, so an
  unchanged ledger renders byte-identical HTML and push_ledgers' no-op skip keeps working.
- Standing "Not investment advice." framing.

  python3 -m research.site      # (re)generate docs/index.html — the only command
"""
import html
import math
import os
import sys
from datetime import date, timedelta

OUT = "docs/index.html"
_e = html.escape

# Chart palette — the validated dataviz reference instance. Single series blue for the curve;
# the diverging blue/red poles carry SIGN on the per-prediction bars. Text wears text tokens,
# never the series color; both modes are selected steps, not an automatic flip.
_CSS_TOKENS = """
:root {
  color-scheme: light;
  --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
  --muted: #6e6c66; --grid: #e1e0d9; --axis: #c3c2b7; --border: rgba(11,11,11,0.10);
  --series: #2a78d6; --barneg: #e34948; --pos: #006300; --neg: #d03b3b;
  --link: #1c5aa0;   /* link TEXT is a text token, not the series color: --series is only
                        4.19:1 on --page and AA small text needs 4.5:1. This is 6.60:1. */
}
@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
    --page: #0d0d0d; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7;
    --muted: #a3a19a; --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,0.10);
    --series: #3987e5; --barneg: #e66767; --pos: #0ca30c; --neg: #e66767;
    --link: #3987e5;   /* dark already clears AA at 5.34:1 on --page */
  }
}
"""

_JS = """
(function () {
  var tb = document.querySelector("#cat tbody");
  var mains = Array.prototype.slice.call(tb.querySelectorAll("tr.main"));
  var dets = {};
  tb.querySelectorAll("tr.det").forEach(function (d) { dets[d.dataset.for] = d; });
  function collapse(r) {
    dets[r.dataset.i].hidden = true;
    r.querySelector(".chev").textContent = "\\u25b8";
  }
  mains.forEach(function (r) {
    r.addEventListener("click", function () {
      var d = dets[r.dataset.i];
      d.hidden = !d.hidden;
      r.querySelector(".chev").textContent = d.hidden ? "\\u25b8" : "\\u25be";
    });
  });
  var fs = "all", ft = "all";
  function apply() {
    mains.forEach(function (r) {
      var ok = (fs === "all" || r.dataset.status === fs) &&
               (ft === "all" || r.dataset.tag === ft);
      r.style.display = ok ? "" : "none";
      dets[r.dataset.i].style.display = ok ? "" : "none";
      if (!ok) collapse(r);
    });
  }
  document.querySelectorAll("#chips button").forEach(function (b) {
    b.addEventListener("click", function () {
      fs = b.dataset.f;
      document.querySelectorAll("#chips button").forEach(function (x) {
        x.classList.toggle("on", x === b);
      });
      apply();
    });
  });
  var sel = document.querySelector("#tagsel");
  if (sel) sel.addEventListener("change", function () { ft = sel.value; apply(); });
  var last = -1, dir = 1;
  document.querySelectorAll("#cat th").forEach(function (th, i) {
    if (!th.dataset.type) return;                 // the chevron column does not sort
    th.addEventListener("click", function () {
      dir = (i === last) ? -dir : (th.dataset.type === "n" ? -1 : 1);
      last = i;
      mains.sort(function (a, b) {
        var x = a.cells[i].dataset.v, y = b.cells[i].dataset.v;
        if (th.dataset.type === "n") {
          x = x === "" ? -1e9 : parseFloat(x); y = y === "" ? -1e9 : parseFloat(y);
          return dir * (x - y);
        }
        return dir * String(x).localeCompare(String(y));
      });
      mains.forEach(function (r) {                // a detail row travels with its prediction
        tb.appendChild(r);
        tb.appendChild(dets[r.dataset.i]);
      });
      document.querySelectorAll("#cat th").forEach(function (x) {
        x.removeAttribute("aria-sort");
      });
      th.setAttribute("aria-sort", dir === 1 ? "ascending" : "descending");
    });
  });
  // Tabs: both panels render visible so the page reads whole without JS; scripting only
  // narrows the view to the selected panel (predictions first, matching the tab order).
  var tabs = document.querySelectorAll("#tabs button");
  function show(name) {
    tabs.forEach(function (b) {
      b.classList.toggle("on", b.dataset.tab === name);
      document.getElementById(b.dataset.tab).hidden = b.dataset.tab !== name;
    });
  }
  tabs.forEach(function (b) {
    b.addEventListener("click", function () { show(b.dataset.tab); });
  });
  if (tabs.length) show(tabs[0].dataset.tab);
})();
"""


def _fnum(s: str) -> float:
    return float(s)


def _sign_cls(v: float) -> str:
    return "pos" if v > 0 else ("neg" if v < 0 else "")


def _add_busdays(iso: str, n: int) -> str:
    """`iso` + n trading days (weekends only — holidays make this a hair early, which is fine:
    it ORDERS the charts, it is never displayed as a settlement date)."""
    d = date.fromisoformat(iso)
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d.isoformat()


def curve_points(bets_rows: list[dict]) -> list[dict]:
    """Closed summary-population predictions (longs) in maturity order, with the running Σ.
    PURE (testable). Ordered by approximate maturity (entry + horizon−1 trading days — the
    exit bar), ledger order breaking ties; dates ride the tooltips."""
    from research import bets
    closed = [r for r in bets.verdict_rows(bets_rows)
              if r["status"] == "closed" and r["excess_pct"]]
    matured = {id(r): _add_busdays(r["entry_date"][:10], int(r["horizon_d"]) - 1)
               for r in closed}
    closed.sort(key=lambda r: (matured[id(r)], r["logged_at"]))
    out, cum = [], 0.0
    for r in closed:
        ex = _fnum(r["excess_pct"])
        cum += ex
        out.append({"ticker": r["ticker"], "entry_date": r["entry_date"][:10],
                    "horizon_d": r["horizon_d"], "benchmark": r["benchmark"],
                    "matured": matured[id(r)], "excess": ex, "cum": cum})
    return out


def _nice_step(span: float) -> float:
    """Smallest of {1,2,5}×10^k giving ≤ ~5 gridlines over `span`."""
    raw = max(span, 1e-9) / 4
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 5, 10):
        if m * mag >= raw:
            return m * mag
    return 10 * mag


def _scale(vals: list[float]) -> tuple[float, float, float]:
    """(lo, hi, step): a zero-anchored y range on clean tick boundaries."""
    lo, hi = min(0.0, min(vals)), max(0.0, max(vals))
    step = _nice_step(hi - lo if hi > lo else abs(hi) or 1.0)
    lo, hi = math.floor(lo / step) * step, math.ceil(hi / step) * step
    if lo == hi:
        lo, hi = -step, step
    return lo, hi, step


def _grid(lo: float, hi: float, step: float, ML: int, MT: int, W: int, MR: int,
          H: int, MB: int) -> tuple[list[str], callable]:
    """Shared hairline grid + y ticks; the ZERO line is the one emphasized rule — polarity
    comes from the baseline, never from recoloring a series."""
    def Y(v: float) -> float:
        return MT + (H - MT - MB) * (hi - v) / (hi - lo)
    parts, t = [], lo
    while t <= hi + step / 2:
        y = Y(t)
        zero = abs(t) < step / 2
        parts.append(f'<line x1="{ML}" y1="{y:.1f}" x2="{W - MR}" y2="{y:.1f}" '
                     f'stroke="{"var(--axis)" if zero else "var(--grid)"}" stroke-width="1"/>')
        parts.append(f'<text x="{ML - 8}" y="{y + 4:.1f}" text-anchor="end" class="tick">'
                     f'{"0" if zero else f"{t:+g}"}</text>')
        t += step
    return parts, Y


_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def _datelab(iso: str) -> str:
    """'2026-07-22' → 'Jul 22' (static map — strftime %b is locale-dependent and the
    render must stay deterministic)."""
    return f"{_MONTHS[int(iso[5:7]) - 1]} {int(iso[8:10])}"


def _svg_curve(pts: list[dict]) -> str:
    """Running total as a single-series line (2px, ≥8px markers with a 2px surface ring,
    native <title> tooltips as the zero-JS hover layer; one series → no legend)."""
    if not pts:
        return '<p class="muted">No settled predictions yet.</p>'
    W, H, ML, MR, MT, MB = 760, 280, 56, 18, 18, 44
    lo, hi, step = _scale([p["cum"] for p in pts])
    parts, Y = _grid(lo, hi, step, ML, MT, W, MR, H, MB)
    parts.insert(0, f'<svg viewBox="0 0 {W} {H}" role="img" '
                    f'aria-label="Running total of excess return, percentage points">')
    def X(i: int) -> float:
        return ML + (W - ML - MR) * (i / (len(pts) - 1) if len(pts) > 1 else 0.5)
    if len(pts) > 1:
        line = " ".join(f"{X(i):.1f},{Y(p['cum']):.1f}" for i, p in enumerate(pts))
        parts.append(f'<polyline points="{line}" fill="none" stroke="var(--series)" '
                     f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, p in enumerate(pts):
        x, y = X(i), Y(p["cum"])
        tip = (f"{p['ticker']} {p['excess']:+.2f}% · running {p['cum']:+.2f}pp · "
               f"entered {p['entry_date']} ({p['horizon_d']}d vs {p['benchmark']})")
        parts.append(f'<g><circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="transparent"/>'
                     f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="var(--series)" '
                     f'stroke="var(--surface)" stroke-width="2"/>'
                     f'<title>{_e(tip)}</title></g>')
    ex, ey = X(len(pts) - 1), Y(pts[-1]["cum"])
    anchor = "end" if ex > W - 90 else "start"
    ey = min(max(ey - 10, MT + 10), H - MB - 6)
    parts.append(f'<text x="{ex + (-10 if anchor == "end" else 10):.1f}" y="{ey:.1f}" '
                 f'text-anchor="{anchor}" class="endlab">{pts[-1]["cum"]:+.1f}pp</text>')
    ticks = {0: "start", len(pts) - 1: "end"} if len(pts) > 1 else {0: "middle"}
    if len(pts) >= 5:
        ticks[(len(pts) - 1) // 2] = "middle"
    for i, anc in ticks.items():
        parts.append(f'<text x="{X(i):.1f}" y="{H - 12}" text-anchor="{anc}" '
                     f'class="tick">{_e(_datelab(pts[i]["matured"]))}</text>')
    parts.append("</svg>")
    return "".join(parts)


def _bar_path(x: float, w: float, y0: float, y1: float) -> str:
    """A column from the baseline y0 to the data end y1: 4px rounded at the DATA end only,
    square at the baseline (the dataviz mark spec). Works for both signs."""
    r = min(4.0, w / 2, abs(y0 - y1))
    if y1 <= y0:   # positive bar (SVG y grows downward)
        return (f"M{x:.1f},{y0:.1f} L{x:.1f},{y1 + r:.1f} Q{x:.1f},{y1:.1f} {x + r:.1f},{y1:.1f} "
                f"L{x + w - r:.1f},{y1:.1f} Q{x + w:.1f},{y1:.1f} {x + w:.1f},{y1 + r:.1f} "
                f"L{x + w:.1f},{y0:.1f} Z")
    return (f"M{x:.1f},{y0:.1f} L{x:.1f},{y1 - r:.1f} Q{x:.1f},{y1:.1f} {x + r:.1f},{y1:.1f} "
            f"L{x + w - r:.1f},{y1:.1f} Q{x + w:.1f},{y1:.1f} {x + w:.1f},{y1 - r:.1f} "
            f"L{x + w:.1f},{y0:.1f} Z")


def _svg_bars(pts: list[dict]) -> str:
    """Each settled prediction's excess as a column around the zero baseline — sign carried by
    the diverging blue/red poles. Direct labels only while they fit (≤12 bars); tooltips and
    the table carry everything at any n."""
    if not pts:
        return ""
    W, H, ML, MR, MT, MB = 760, 260, 56, 18, 18, 34
    lo, hi, step = _scale([p["excess"] for p in pts])
    parts, Y = _grid(lo, hi, step, ML, MT, W, MR, H, MB)
    parts.insert(0, f'<svg viewBox="0 0 {W} {H}" role="img" '
                    f'aria-label="Excess return per settled prediction, percent">')
    slot = (W - ML - MR) / len(pts)
    w = min(24.0, slot * 0.6)
    y0 = Y(0.0)
    labeled = len(pts) <= 12
    for i, p in enumerate(pts):
        x = ML + slot * i + (slot - w) / 2
        y1 = Y(p["excess"])
        color = "var(--series)" if p["excess"] >= 0 else "var(--barneg)"
        tip = (f"{p['ticker']} {p['excess']:+.2f}% vs {p['benchmark']} ({p['horizon_d']}d), "
               f"entered {p['entry_date']}")
        parts.append(f'<g><path d="{_bar_path(x, w, y0, y1)}" fill="{color}"/>'
                     f'<rect x="{ML + slot * i:.1f}" y="{MT}" width="{slot:.1f}" '
                     f'height="{H - MT - MB}" fill="transparent"/>'
                     f'<title>{_e(tip)}</title></g>')
        if labeled:
            cx = x + w / 2
            vy = y1 - 6 if p["excess"] >= 0 else y1 + 13
            parts.append(f'<text x="{cx:.1f}" y="{vy:.1f}" text-anchor="middle" class="tick">'
                         f'{p["excess"]:+.1f}</text>')
            parts.append(f'<text x="{cx:.1f}" y="{H - 10}" text-anchor="middle" class="tick">'
                         f'{_e(p["ticker"])}</text>')
    parts.append("</svg>")
    return ('<h3>Each settled prediction</h3>'
            '<p class="muted">Excess return vs that prediction’s benchmark, %.</p>' +
            "".join(parts))


def data_through(bets_rows: list[dict]) -> str:
    """Newest date visible in the ledger — the page's ONLY timestamp (data-derived, so the
    render is deterministic and an unchanged ledger produces an unchanged page)."""
    dates = [r["logged_at"][:10] for r in bets_rows if r.get("logged_at")]
    dates += [r["entry_date"][:10] for r in bets_rows if r.get("entry_date")]
    return max(dates) if dates else ""


def _tiles(bets_rows: list[dict]) -> str:
    from research import bets
    s = bets.stats(bets_rows)
    n_open = sum(1 for r in bets_rows if r["status"] == "open")
    def tile(label, value, sub, cls=""):
        return (f'<div class="tile"><div class="tlabel">{label}</div>'
                f'<div class="tvalue{" " + cls if cls else ""}">{value}</div>'
                f'<div class="tbar">{sub}</div></div>')
    if s:
        n, _, md, beat = s
        sig = bets.cum_excess(bets_rows)
        perf = [tile("settled", f"{n}", "scored vs benchmark"),
                tile("median excess", f"{md:+.2f}%", "per settled prediction",
                     _sign_cls(md)),
                tile("beat rate", f"{beat:.0f}%", "finished ahead of benchmark"),
                tile("total excess", f"{sig:+.1f}pp" if sig is not None else "—",
                     "sum across settled", _sign_cls(sig) if sig is not None else "")]
    else:
        perf = [tile("settled", "0", "scored vs benchmark")]
    note = ""
    if any(r.get("direction") == "short" for r in bets_rows):
        note = ('<p class="muted">The summary counts long predictions; short entries appear '
                'in the table but are not scored into it.</p>')
    return ('<div class="tiles">' + "".join(perf)
            + tile("open", f"{n_open}", "awaiting outcome") + "</div>" + note)


def _taglabel(tag: str) -> str:
    """Display label for a pattern tag — the raw tag stays in every data attribute (it is
    the filter/sort value); only the rendered text is humanized."""
    if tag == "untagged":
        return "early (untagged)"
    return (tag[:1].upper() + tag[1:]).replace("-", " ")


def _catalogue_table(bets_rows: list[dict]) -> str:
    """Every prediction, one compact row — sortable columns, status/tag filters as VIEWS.
    The thesis rides a hidden detail row (click the prediction to expand): the full record
    stays on the page without its prose crowding the table. Filters hide, never remove."""
    tags = sorted({r.get("pattern_tag") or "untagged" for r in bets_rows})
    rows_html = []
    for i, r in enumerate(sorted(bets_rows, key=lambda r: r.get("logged_at", ""),
                                 reverse=True)):
        ex = r.get("excess_pct") or ""
        tag = r.get("pattern_tag") or "untagged"
        short = r.get("direction") == "short"
        if ex and short:   # rendered, never summed — the muted cell says so at a glance
            exc, extip = "num unscored", ' title="Shown, not scored into the summary"'
        else:
            exc, extip = (f"num {_sign_cls(_fnum(ex))}" if ex else "num"), ""
        if r.get("pattern_tag"):
            tagcell = f'<td data-v="{_e(tag)}">{_e(_taglabel(tag))}</td>'
        else:              # pre-tag-era rows stay blank in the ledger, by rule — label,
            tagcell = ('<td class="early" data-v="untagged" '   # never backfill
                       'title="Logged before type labels were introduced">early</td>')
        prefix = "(short — shown, not scored into the summary) " if short else ""
        rows_html.append(
            f'<tr class="main" data-status="{_e(r["status"])}" data-tag="{_e(tag)}" '
            f'data-i="{i}">'
            f'<td class="chev">▸</td>'
            f'<td data-v="{_e(r["logged_at"][:10])}">{_e(r["logged_at"][:10])}</td>'
            f'<td data-v="{_e(r["ticker"])}">{_e(r["ticker"])}</td>'
            f'<td data-v="{_e(r["direction"])}">{_e(r["direction"])}</td>'
            f'<td class="num" data-v="{_e(r["horizon_d"])}">{_e(r["horizon_d"])}d</td>'
            f'<td data-v="{_e(r["benchmark"])}">{_e(r["benchmark"])}</td>'
            f'{tagcell}'
            f'<td data-v="{_e(r["status"])}">{_e(r["status"])}</td>'
            f'<td class="{exc}" data-v="{_e(ex)}"{extip}>'
            f'{_e(ex) + "%" if ex else "—"}</td></tr>'
            f'<tr class="det" data-for="{i}" hidden>'
            f'<td colspan="9">{prefix}{_e(r.get("thesis", ""))}</td></tr>')
    chips = ('<div id="chips"><button data-f="all" class="on">All</button>'
             '<button data-f="open">Open</button><button data-f="closed">Closed</button>'
             '</div>')
    sel = ('<select id="tagsel"><option value="all">all types</option>'
           + "".join(f'<option value="{_e(t)}">{_e(_taglabel(t))}</option>' for t in tags)
           + "</select>")
    return (f'<div class="controls">{chips}{sel}</div>'
            '<p class="muted">Click a prediction for its thesis; click a column heading '
            'to sort. Every prediction ever logged is listed — filters change the view, '
            'never the record.</p>'
            '<div class="scroll"><table id="cat"><thead><tr><th></th>'
            '<th data-type="s">logged</th><th data-type="s">ticker</th>'
            '<th data-type="s">side</th><th data-type="n">horizon</th>'
            '<th data-type="s">benchmark</th><th data-type="s">type</th>'
            '<th data-type="s">status</th><th data-type="n">excess</th>'
            '</tr></thead><tbody>' + "".join(rows_html) + "</tbody></table></div>")


def render(bets_rows: list[dict]) -> str:
    """The whole page from the catalogue. PURE (no I/O — testable)."""
    through = data_through(bets_rows)
    pts = curve_points(bets_rows)
    return f"""<!doctype html>
<!-- GENERATED by `python3 -m research.site` from the committed ledgers — never hand-edit. -->
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Swing Lab — the forward ledger</title>
<meta name="description" content="A public research ledger of timestamped market predictions.
Every call is published before its outcome is known and scored mechanically against a
benchmark — wins and losses alike — so the record cannot be cherry-picked.
Not investment advice.">
<link rel="canonical" href="https://guillearria.github.io/swing-lab/">
<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2032%2032%22%3E%3Crect%20width%3D%2232%22%20height%3D%2232%22%20rx%3D%227%22%20fill%3D%22%231a1a19%22%2F%3E%3Cpolyline%20points%3D%226%2C22%2013%2C12%2019%2C17%2026%2C7%22%20fill%3D%22none%22%20stroke%3D%22%233987e5%22%20stroke-width%3D%223.2%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%2F%3E%3C%2Fsvg%3E">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Swing Lab">
<meta property="og:title" content="Swing Lab — the forward ledger">
<meta property="og:description" content="Timestamped market predictions, published before the
outcome is known and scored mechanically. Wins and losses both count. Not investment advice.">
<meta property="og:url" content="https://guillearria.github.io/swing-lab/">
<meta name="twitter:card" content="summary">
<style>
{_CSS_TOKENS}
* {{ box-sizing: border-box; margin: 0; }}
body {{ background: var(--page); color: var(--ink); line-height: 1.5; padding: 24px 16px 48px;
       font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width: 860px; margin: 0 auto; display: grid; gap: 16px; }}
/* The page carried no links until 2026-08-21, so it had no link rule either — without one
   the UA default (#0000EE) is near-invisible on the dark surface. */
a {{ color: var(--link); text-decoration: underline; text-underline-offset: 3px; }}
a:hover {{ text-decoration-thickness: 2px; }}
a:focus-visible {{ outline: 2px solid var(--link); outline-offset: 2px; border-radius: 2px; }}
.masthead {{ max-width: 860px; margin: 0 auto 14px; display: flex; align-items: flex-start;
             justify-content: space-between; gap: 12px; flex-wrap: wrap; }}
h1.brand {{ display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 26px;
            letter-spacing: -0.01em; }}
.brand svg {{ width: 28px; height: 28px; display: block; }}
.masthead nav {{ display: flex; gap: 14px; font-size: 13.5px; padding-top: 8px; }}
.tagline {{ color: var(--ink-2); font-size: 14.5px; margin: 6px 0 2px; max-width: 62ch; }}
.frame {{ color: var(--ink-2); font-size: 14px; margin: 10px 0 2px;
          border-left: 2px solid var(--border); padding-left: 12px; }}
section {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
           padding: 18px 20px; }}
h2 {{ font-size: 17px; margin-bottom: 8px; }}
h3 {{ font-size: 15px; margin: 16px 0 0; }}
p {{ margin: 6px 0; }} .muted {{ color: var(--ink-2); font-size: 13.5px; }}
.tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(128px, 1fr));
          gap: 10px; margin: 8px 0; }}
.tile {{ border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; }}
.tlabel {{ color: var(--ink-2); font-size: 13px; }}
.tvalue {{ font-size: 26px; font-weight: 600; margin: 2px 0; }}
.tbar {{ color: var(--muted); font-size: 12.5px; }}
svg {{ width: 100%; height: auto; display: block; }}
.tick {{ fill: var(--muted); font-size: 11px; font-variant-numeric: tabular-nums; }}
.endlab {{ fill: var(--ink-2); font-size: 12.5px; font-weight: 600; }}
#tabs {{ display: flex; gap: 8px; }}
.controls {{ display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin: 8px 0 4px; }}
#chips button, #tabs button {{ background: none; border: 1px solid var(--border);
                 border-radius: 999px; color: var(--ink-2); padding: 4px 12px;
                 cursor: pointer; font-size: 13.5px; }}
#tabs button {{ padding: 6px 16px; font-size: 14px; }}
#chips button.on, #tabs button.on {{ border-color: var(--series); color: var(--ink);
                                     font-weight: 600; }}
#tagsel {{ background: var(--surface); color: var(--ink); border: 1px solid var(--border);
           border-radius: 6px; padding: 4px 8px; font-size: 13.5px; }}
.scroll {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
th {{ text-align: left; color: var(--ink-2); font-weight: 600; cursor: pointer;
      border-bottom: 1px solid var(--axis); white-space: nowrap; }}
th[data-type]::after {{ content: " ↕"; color: var(--muted); font-weight: 400; }}
th[aria-sort="ascending"]::after {{ content: " ▲"; }}
th[aria-sort="descending"]::after {{ content: " ▼"; }}
th, td {{ padding: 5px 8px; vertical-align: top; }}
td {{ border-bottom: 1px solid var(--grid); }}
td.num {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}
.pos {{ color: var(--pos); }} .neg {{ color: var(--neg); }}
td.unscored, td.early {{ color: var(--muted); }}
tr.main {{ cursor: pointer; }}
tr.main:hover td {{ background: var(--page); }}
td.chev {{ color: var(--muted); width: 18px; padding-right: 0; }}
tr.det td {{ color: var(--ink-2); font-size: 13.5px; padding: 2px 8px 10px 32px; }}
footer {{ color: var(--muted); font-size: 13px; text-align: center; }}
@media (max-width: 600px) {{
  body {{ padding: 16px 10px 40px; }}
  section {{ padding: 14px 12px; }}
}}
</style></head><body>

<header class="masthead">
  <div>
    <h1 class="brand"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect width="32" height="32" rx="7" fill="#1a1a19"/><polyline points="6,22 13,12 19,17 26,7" fill="none" stroke="#3987e5" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg> Swing Lab</h1>
    <p class="tagline">The forward ledger — timestamped market predictions, logged before
the outcome and scored mechanically against a benchmark. None are removed.</p>
    <p class="muted">Data through {_e(through) or "—"} · Not investment advice.</p>
  </div>
  <nav><a href="https://github.com/guillearria/swing-lab">Code</a><a
    href="https://github.com/guillearria">Guillermo Arria-Devoe</a></nav>
</header>

<main>

<section>
{_tiles(bets_rows)}
</section>

<div id="tabs"><button data-tab="predictions" class="on">Predictions</button><button
  data-tab="performance">Performance</button></div>

<section id="predictions">
<h2>Predictions</h2>
{_catalogue_table(bets_rows)}
</section>

<section id="performance">
<h2>Performance so far</h2>
<p class="frame">This is the complete record of these predictions, not a highlight reel: each
one is logged before its outcome and scored mechanically against a benchmark, wins and losses
alike, and none are removed or revised after the fact. The project is at the hypothesis stage;
no signal here has been shown to make money.</p>
<h3>Running total of excess return</h3>
<p class="muted">Across settled predictions, percentage points.</p>
{_svg_curve(pts)}
{_svg_bars(pts)}
</section>

<footer>Project code on <a href="https://github.com/guillearria/swing-lab">GitHub</a> ·
Built by <a href="https://github.com/guillearria">Guillermo Arria-Devoe</a> ·
Not investment advice.</footer>
</main>
<script>
{_JS}
</script></body></html>
"""


def write(path: str = OUT) -> dict:
    """Render from the live ledger and write the page. Returns a summary for the CLI."""
    from research import bets
    bets_rows = bets._load()
    html_text = render(bets_rows)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html_text)
    longs = bets.excess_values(bets.verdict_rows(bets_rows))
    return {"path": path, "settled_longs": len(longs), "bets": len(bets_rows),
            "through": data_through(bets_rows)}


def run(argv: list[str]) -> int:
    if argv:
        print(f"site: unknown argument {argv[0]!r} — the only command is a bare "
              f"`python3 -m research.site` (regenerates {OUT})")
        return 1
    s = write()
    print(f"site: wrote {s['path']} ({s['settled_longs']} settled longs, {s['bets']} "
          f"predictions, data through {s['through']})")
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
