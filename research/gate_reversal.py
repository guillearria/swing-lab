"""GATE R1 — is the short-term reversal premium alive after 2015 in mid and small caps, net of a
realistic cost, and carried by the long (buy-the-losers) leg?

The one lead that survived the 2026-10-16 review [ARC 5 #20] was a benchmark-free within-day
spread: S&P 400/600 up-movers trailed down-movers. That is the shape of short-term reversal, the
oldest effect in the literature — and the one most often reported as eaten by costs
(research/LITERATURE.md). Two independent periods from a discovery sample earn ONE cheap check on
official, survivorship-free history before anything is built. The bar is pre-registered in
FINDINGS [GATE R1]; this module must not be run before that entry is committed.

Data (official, free): Kenneth R. French Data Library, "25 Portfolios Formed on Size and Short-Term
Reversal (5 x 5)", monthly, value-weighted (the file's first block). Construction per the library:
NYSE/AMEX/NASDAQ stocks; NYSE size quintiles × NYSE prior (1-1) month return quintiles; monthly.
Size quintiles 2–4 stand in for the S&P 400/600 cap range (quintile 1 is micro-cap dominated,
quintile 5 is mega-cap). Columns are row-major: ME1 PRIOR1…PRIOR5, ME2 PRIOR1…, …, ME5 PRIOR5.

  spread_t = mean over q∈{2,3,4} of (ME_q PRIOR1 − ME_q PRIOR5)   last month's losers − winners
  long_t   = mean over q∈{2,3,4} of (ME_q PRIOR1 − ME_q PRIOR3)   losers − the middle: the leg a
                                                                   long-only account could hold

  python3 -m research.gate_reversal          # download, evaluate the pre-registered window, print
Stdlib only. Nothing is written to disk.
"""
import csv
import io
import math
import statistics
import sys
import urllib.request
import zipfile

URL = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
       "25_Portfolios_ME_Prior_1_0_CSV.zip")
# ---- Pre-registered in FINDINGS [GATE R1]; change none of these after the first run. ----
START, END = 201501, 202605     # ends the month BEFORE the ledger that produced the lead began
SIZE_Q = (2, 3, 4)
NW_LAGS = 3
ALPHA = 0.05                    # a SCREEN: a PASS licenses only a fresh pre-registration, whose own
                                # bar carries the correction over every gate opened [GATE R1]
COST_PER_MONTH = 0.54           # % per month: Novy-Marx & Velikov (2016) NBER WP 20721 Table 10 —
                                # value-weighted decile short-run reversal with all three cost-
                                # mitigation techniques, 1963–2012: gross 0.38, cost 0.54, net −0.17
STRESS_COSTS = (1.25, 1.65)     # NON-gating, harsher only: their Table 13 small-size bin (10%/50%
                                # band) and Table 3 plain decile — never a softer reading


def fetch(url: str = URL) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        blob = r.read()
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
        return z.read(name).decode("latin-1")


def parse_first_block(text: str) -> tuple[list[str], list[tuple[int, list[float]]]]:
    """The file's FIRST block (value-weighted monthly): its header row and YYYYMM rows. PURE."""
    cols, rows = None, []
    for rec in csv.reader(io.StringIO(text)):
        cells = [c.strip() for c in rec]
        if cols is None:
            if len(cells) > 2 and any("PRIOR" in c.upper() for c in cells[1:]):
                cols = cells[1:]
            continue
        if cells and len(cells[0]) == 6 and cells[0].isdigit():
            rows.append((int(cells[0]), [float(x) for x in cells[1:1 + len(cols)]]))
        elif rows:
            break
    if cols is None or not rows:
        raise ValueError("no first (value-weighted monthly) block found")
    return cols, rows


def col_index(cols: list[str], q: int, p: int) -> int:
    """Position of size quintile q × prior-return quintile p, VALIDATED against the header —
    a silent column mix-up would be a wrong verdict, so a mismatch raises. PURE."""
    i = (q - 1) * 5 + (p - 1)
    name = " ".join(cols[i].upper().split())
    size_ok = f"ME{q}" in name or (q == 1 and "SMALL" in name) or (q == 5 and "BIG" in name)
    prior_ok = (f"PRIOR{p}" in name or (p == 1 and "LOPRIOR" in name)
                or (p == 5 and "HIPRIOR" in name))
    if len(cols) != 25 or not (size_ok and prior_ok):
        raise ValueError(f"unexpected column layout at q={q} p={p}: {cols[i]!r} of {len(cols)}")
    return i


def series(cols: list[str], rows) -> tuple[dict[int, float], dict[int, float]]:
    """(spread, long leg) per month in %, averaged over SIZE_Q; months with any missing
    (−99.99) input are dropped from both. PURE."""
    idx = {(q, p): col_index(cols, q, p) for q in SIZE_Q for p in (1, 3, 5)}
    spread, long_ = {}, {}
    for ym, v in rows:
        if any(v[i] <= -99 for i in idx.values()):
            continue
        spread[ym] = statistics.mean(v[idx[q, 1]] - v[idx[q, 5]] for q in SIZE_Q)
        long_[ym] = statistics.mean(v[idx[q, 1]] - v[idx[q, 3]] for q in SIZE_Q)
    return spread, long_


def nw_t(x: list[float], lags: int = NW_LAGS) -> tuple[float, float, float, float]:
    """(mean, Newey-West s.e. of the mean, t, one-sided p for mean > 0). Bartlett kernel;
    normal approximation for p. PURE."""
    n = len(x)
    m = sum(x) / n
    d = [v - m for v in x]
    var = sum(v * v for v in d) / n
    for l in range(1, lags + 1):
        g = sum(d[t] * d[t - l] for t in range(l, n)) / n
        var += 2 * (1 - l / (lags + 1)) * g
    se = math.sqrt(max(var, 0.0) / n)
    t = m / se if se > 0 else float("inf")
    p = 0.5 * (1 - math.erf(t / math.sqrt(2)))
    return m, se, t, p


def evaluate(spread: dict[int, float], long_: dict[int, float], start: int = START,
             end: int = END, cost: float | None = COST_PER_MONTH) -> dict:
    """The pre-registered verdict over [start, end]. PURE. PASS needs ALL five:
    (1) spread mean > 0 at one-sided NW p ≤ ALPHA; (2) both halves (by month count) positive;
    (3) spread mean with the single best month removed > 0; (4) long-leg mean > 0;
    (5) spread mean > the pre-registered monthly cost."""
    if cost is None:
        raise ValueError("COST_PER_MONTH is unset — the gate cannot run before its bar is written")
    months = sorted(ym for ym in spread if start <= ym <= end)
    x = [spread[ym] for ym in months]
    m, se, t, p = nw_t(x)
    h = len(x) // 2
    first, second = x[:h], x[h:]
    trimmed = sorted(x)[:-1]
    lg = [long_[ym] for ym in months]
    checks = {"significant": m > 0 and p <= ALPHA,
              "both_halves": statistics.mean(first) > 0 and statistics.mean(second) > 0,
              "not_one_month": statistics.mean(trimmed) > 0,
              "long_leg": statistics.mean(lg) > 0,
              "beats_cost": m > cost}
    return {"n": len(x), "first": months[0], "last": months[-1], "mean": m, "se": se, "t": t,
            "p": p, "median": statistics.median(x), "pos": sum(v > 0 for v in x) / len(x),
            "half1": (months[0], months[h - 1], statistics.mean(first)),
            "half2": (months[h], months[-1], statistics.mean(second)),
            "trimmed": statistics.mean(trimmed), "long": statistics.mean(lg),
            "long_median": statistics.median(lg), "cost": cost, "net": m - cost,
            "checks": checks, "verdict": "PASS" if all(checks.values()) else "FAIL"}


def _line(label: str, r: dict) -> str:
    return (f"  {label}: {r['first']}–{r['last']} n={r['n']} spread mean {r['mean']:+.3f}%/mo "
            f"(NW t={r['t']:.2f}, one-sided p={r['p']:.4f}) median {r['median']:+.3f}% "
            f"positive {100 * r['pos']:.0f}% of months · long leg mean {r['long']:+.3f}%")


def expected_months(start: int = START, end: int = END) -> list[int]:
    """Every YYYYMM in [start, end] — the window must be complete before a verdict prints. PURE."""
    out, y, m = [], start // 100, start % 100
    while y * 100 + m <= end:
        out.append(y * 100 + m)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def run(argv: list[str]) -> int:
    cols, rows = parse_first_block(fetch())
    sp, lg = series(cols, rows)
    missing = [ym for ym in expected_months() if ym not in sp]
    if missing:
        raise SystemExit(f"GATE R1 refuses to print a verdict: {len(missing)} window month(s) "
                         f"missing from the file ({missing[:3]}…) — the series is incomplete")
    r = evaluate(sp, lg)
    print("GATE R1 — short-term reversal, NYSE size quintiles 2–4, PRIOR1 − PRIOR5 "
          "(French 5x5, value-weighted, monthly)")
    print(_line("pre-registered window", r))
    print(f"  halves: {r['half1'][0]}–{r['half1'][1]} mean {r['half1'][2]:+.3f}% · "
          f"{r['half2'][0]}–{r['half2'][1]} mean {r['half2'][2]:+.3f}% · best month removed: "
          f"mean {r['trimmed']:+.3f}%")
    print(f"  cost {r['cost']:.2f}%/mo → net {r['net']:+.3f}%/mo")
    marks = " · ".join(f"{k} {'✓' if v else '✗'}" for k, v in r["checks"].items())
    print(f"  bar: {marks}  →  VERDICT {r['verdict']}")
    # Descriptive only, never part of the bar: the same series before the window (decay), and
    # the net at Novy-Marx & Velikov's 1963–2012 small-stock cost (a harsher, older estimate).
    pre = evaluate(sp, lg, start=min(sp), end=201412, cost=r["cost"])
    print(_line("descriptive, before the window", pre))
    print("  stress (non-gating, harsher only): " + " · ".join(
        f"net at {c:.2f}%/mo {r['mean'] - c:+.3f}" for c in STRESS_COSTS))
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
