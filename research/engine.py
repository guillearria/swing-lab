"""The falsification ENGINE — the asset (Path A).

NOT an alpha printer. This is the self-auditing scoreboard of every pre-registered
probe the project ran and its verdict, plus the multiple-testing reality check. Its
job is to red-team our OWN results: across N pre-registered tests, how many beat
buy-and-hold SPY risk-adjusted — and is that more than chance would give?

The reusable METHOD (how to run a probe, the rules earned from losses) lives in
research/SKILL.md. To add a probe: pre-register it in FINDINGS.md, run it, then append
ONE row below with its honest verdict. Keep the engine in sync with the ledger.

  python3 -m research.engine

Verdict codes:
  FAIL    — did not clear its own pre-registered bar
  REAL*   — real effect, but a RISK-REDUCER: does NOT beat buy-hold SPY risk-adjusted
  NEAR    — cleared part of the bar (best-of-family), still not risk-adjusted alpha
  BLOCKED — needs paid/unavailable data
  PENDING — forward verdict still accruing
  NULL    — hit its own kill-criterion without clearing the bar; stopped expanding
"""
import sys
from datetime import date, timedelta

# (family, name, verdict, beats_spy_riskadj)   beats_spy: True/False/None(pending|blocked)
PROBES = [
    ("reversion",  "single-name momentum",                 "FAIL",    False),
    ("reversion",  "200d-trend-filtered momentum",          "FAIL",    False),
    ("reversion",  "oversold / index dip-fade (200d gate)", "REAL*",   False),
    ("reversion",  "crypto dip-fade",                       "FAIL",    False),
    ("reversion",  "VIX>30 gate on the fade",               "FAIL",    False),
    ("trend",      "crypto trend-following",                "REAL*",   False),
    ("trend",      "asset-class DUAL MOMENTUM",             "NEAR",    False),
    ("sizing",     "vol-targeting SPY (risk-mgmt, ≤2x)",     "REAL*",   False),
    ("fear",       "extreme-VIX deep-fear buy",             "REAL*",   False),
    ("fear",       "crypto Fear&Greed sentiment-fade",      "FAIL",    False),
    ("fear",       "200d-slope regime proxy",               "FAIL",    False),
    ("disaster",   "disaster -20% entry (global+graveyard)","REAL*",   False),
    ("portfolio",  "multi-edge stack (SPY+GLD+crypto)",     "FAIL",    False),
    ("portfolio",  "global disaster portfolio (utilization)","FAIL",   False),
    ("forced-flow","S&P 500 index-deletion bounce",         "FAIL",    False),
    ("forced-flow","post-IPO lockup-expiry",                "FAIL",    False),
    ("forced-flow","Russell 2000 reconstitution",           "BLOCKED", None),
    ("vol-premium","selling vol / short variance",          "FAIL",    False),
    ("factors",    "cross-sectional factor ETFs (MTUM…)",   "NEAR",    False),
    ("seasonality","calendar (Halloween, turn-of-month)",   "FAIL",    False),
    ("carry",      "bond curve carry (TLT/SHY)",            "FAIL",    False),
    ("reading",    "insider-cluster bare trigger",          "FAIL",    False),
    # NULL, not PENDING: [ARC 3 #1]'s kill-criterion was "N=20 settled OR 2026-12-31, whichever
    # first". At a 126d horizon the last take that could settle by the deadline had to be logged
    # by ~2026-07-08; only 2 were ever logged. The N=20 branch became unreachable on the calendar,
    # so the deadline branch decided it: log NULL, stop expanding. FINDINGS 2026-08-02.
    ("reading",    "insider-cluster + agent read (forward)","NULL",    False),
]


def _agg(vals: list[float]):
    """(n, mean, median, beat%) for a list of excess returns, or None if empty."""
    from statistics import mean, median
    if not vals:
        return None
    return len(vals), mean(vals), median(vals), sum(1 for x in vals if x > 0) / len(vals) * 100


def _add_trading_days(d: date, n: int) -> date:
    """Approx: step n weekdays forward from d (ignores holidays — a maturity HINT, not exact)."""
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5:  # Mon-Fri
            n -= 1
    return d


def _first_maturity(rows, horizon_of) -> date | None:
    """Earliest an OPEN bet could settle = min(logged_at + horizon trading days). Computed,
    not hardcoded (single source of truth) so '0 settled' reads as in-flight, not stuck."""
    out = []
    for r in rows:
        if r["status"] != "open" or not r.get("logged_at"):
            continue
        try:
            out.append(_add_trading_days(date.fromisoformat(r["logged_at"][:10]), horizon_of(r)))
        except ValueError:
            continue
    return min(out) if out else None


def forward_track():
    """Live forward-READING track vs its pre-registered bars (FINDINGS Arc 5 / Arc 3).

    The active frontier (mechanical mine is closed). CSV-only — no network."""
    from research import bets, movers
    print("\n  FORWARD READING TRACK (live, accruing — the active frontier):")

    # ONE pooled general verdict [Arc 5 #7] — fast (≤30d) merged into core; horizon is now a
    # DIAGNOSTIC label, not a separate goalpost (halves time-to-verdict, no scientific loss).
    b = bets._load()
    bopen = sum(1 for r in b if r["status"] == "open")
    mat = _first_maturity(b, lambda r: int(r["horizon_d"]))
    matstr = f", first settles ~{mat}" if mat else ""
    bar = (f"N≥{bets.BAR_N} & median>+{bets.BAR_MEDIAN:.0f}% & beat>{bets.BAR_BEAT:.0f}% "
           f"& Wilcoxon p≤{bets.WILCOXON_ALPHA} [Arc 5 #7 · long-only #12a · #14 ONE LOOK]")
    s = bets.stats(b)
    if s:
        n, _, med, beat = s
        # The FULL bar, all four gates — the Wilcoxon is computed, not decorative [ARC 5 #12a].
        if n >= bets.BAR_N and med > bets.BAR_MEDIAN and beat > bets.BAR_BEAT:
            p = bets.wilcoxon_p(bets.excess_values(bets.verdict_rows(b)))
            verdict = (f"PASS (p={p:.4f} ≤ α)" if p is not None and p <= bets.WILCOXON_ALPHA
                       else f"shape passes but p={'n/a' if p is None else f'{p:.3f}'} > α — NOT significant")
        else:
            verdict = "accruing"
        print(f"    general catalogue (pooled long-only): {n} settled (+{bopen} open{matstr}) | "
              f"median {med:+.2f}% beat {beat:.0f}% → bar {bar}: {verdict}")
    else:
        print(f"    general catalogue (pooled long-only): 0 settled (+{bopen} open{matstr}) | bar {bar}")
    # Group renderer for every diagnostic split. BOTH counts, BOTH unit labels, every branch —
    # until 2026-08-04 a group with ≥1 closed row rendered only "Ncl med X%" and silently
    # dropped its open count: post-earnings-drift showed "1cl" while hiding ~20 open bets, so
    # the surface built to make concentration visible understated exactly the biggest tag.
    def _grp(label: str, grp: list) -> str:
        st = bets._agg(grp)  # RAW aggregation: diagnostics keep shorts visible [ARC 5 #12a]
        op = sum(1 for r in grp if r["status"] == "open")
        return (f"{label} {st[0]}cl med {st[2]:+.1f}% {op}op" if st
                else f"{label} 0cl {op}op")

    csplit = [_grp(tag, grp)
              for tag, grp in (("core", [r for r in b if not bets.is_fast(r)]),
                               ("fast", [r for r in b if bets.is_fast(r)]))]
    print(f"      diagnostic split (not a goalpost): {' · '.join(csplit)}")
    # per-SCENARIO-TYPE decomposition [Arc 5 #8] — a DIAGNOSTIC lens, never a per-tag bar (a type
    # earns its own verdict only at a Bonferroni-clearing N; per-type goalposts = N× false positives).
    tags: dict[str, list] = {}
    for r in b:
        tags.setdefault(r.get("pattern_tag") or "untagged", []).append(r)
    # `*` = no case file behind the tag [ARC 5 #14b] — the decomposition is only meaningful for
    # tags that name a documented mechanism; the rest are phrases coined at generation time.
    cased = bets.tags_with_cases()
    _mark = lambda t: t if (t in cased or t == "untagged") else t + "*"
    print(f"      by scenario (diagnostic, not a goalpost): "
          f"{' · '.join(_grp(_mark(t), grp) for t, grp in sorted(tags.items()))}")
    loose = sorted(t for t in tags if t not in cased and t != "untagged")
    if loose:
        print(f"      * = no case file ({len(loose)} of {len(tags)}): a tag with no mechanism "
              f"behind it decomposes a LABEL [ARC 5 #14b]")
    # per-UNIVERSE decomposition [ARC 5 #11] — same diagnostic-only rule. Classified against the
    # CURRENT committed caches (CSV-only — sp500_cached/tail, never the fetching sp500()), so a
    # ticker promoted/demoted between indices can misclassify an old bet: acceptable for a
    # diagnostic, never for a verdict.
    from research import universe
    sp5, tl = set(universe.sp500_cached()), set(universe.tail())
    usplit: dict[str, list] = {}
    for r in b:
        u = "sp500" if r["ticker"] in sp5 else ("tail" if r["ticker"] in tl else "other")
        usplit.setdefault(u, []).append(r)
    print(f"      by universe (diagnostic, not a goalpost) [ARC 5 #11]: "
          f"{' · '.join(_grp(u, grp) for u, grp in sorted(usplit.items()))}")
    # by stated conviction [ARC 5 #15] — tiers PRESENT only ("unstated" = pre-#15 rows and
    # flag-less adds); read at the #14 look points as a lens, never a per-tier bar.
    csplit2: dict[str, list] = {}
    for r in b:
        csplit2.setdefault(r.get("conviction") or "unstated", []).append(r)
    print(f"      by conviction (diagnostic, not a goalpost) [ARC 5 #15]: "
          f"{' · '.join(_grp(c, grp) for c, grp in sorted(csplit2.items()))}")
    # candidate DENOMINATOR [Arc 5 #8]: the mover-scan logs every big mover take/skip → bounds the
    # selection the [Arc 5 #7] caveat warned about (reduced, NOT eliminated — universe ≠ all reads).
    m = movers._load()
    if m:
        mc = lambda s: sum(1 for r in m if r["status"] == s)
        mu = lambda u: sum(1 for r in m if r["universe"] == u)
        print(f"      denominator [Arc 5 #8]: mover scan logged {len(m)} candidates "
              f"(sp500 {mu('sp500')} / tail {mu('tail')}; {mc('taken')} taken / "
              f"{mc('skip')} skipped / {mc('seen')} unread) → selection BOUNDED by the two "
              f"scan cohorts [ARC 5 #11], reduced not eliminated (universe ≠ all reads).")
    else:
        print("      caveat: UNBOUNDED news scan, no candidate denominator yet → a pass is "
              "CONDITIONAL (selection, not skill) until the mover-scan denominator is populated [Arc 5 #7/#8].")

    # The insider ledger used to print here as the SECOND verdict silo. It is CLOSED (Arc 3
    # retired 2026-08-02) and the line is kept — a silo that quietly disappears reads as one that
    # never existed, and the whole point of this surface is that a cold session sees the honest
    # state first. This project runs on ONE verdict silo; say so rather than showing one bar.
    print("    insider ledger: CLOSED 2026-08-02 — Arc 3 logged NULL on its own deadline branch\n"
          "       (126d horizon vs a 2026-12-31 kill date ⇒ N=20 unreachable after ~2026-07-08;\n"
          "       2 takes ever logged). The candidate stream itself audited CLEAN ([ARC 3 #1d]:\n"
          "       0-2 entity-stack artifacts of 18 vs a ≥7 threshold) — it ran out of calendar,\n"
          "       not credibility. → ONE verdict silo, not two.")
    print("    Generate more: one iteration of research/READ_LOOP.md (scheduled). "
          "Log every take; never drop losers.")


def main():
    n = len(PROBES)
    beat = sum(1 for *_, b in PROBES if b is True)
    fails = sum(1 for _, _, v, _ in PROBES if v == "FAIL")
    real = sum(1 for _, _, v, _ in PROBES if v in ("REAL*", "NEAR"))
    leads = sum(1 for _, _, v, _ in PROBES if v == "PASS*")
    pend = sum(1 for _, _, v, _ in PROBES if v in ("PENDING", "BLOCKED"))
    settled = n - pend

    print(f"\n=== FALSIFICATION ENGINE — project scoreboard ({n} pre-registered probes) ===")
    fam = None
    for f, name, v, b in PROBES:
        if f != fam:
            print(f"  [{f}]"); fam = f
        flag = {True: "beats SPY", False: "ties/loses SPY", None: "—"}[b]
        print(f"      {v:<8} {name:<40} {flag}")

    print(f"\n  settled: {settled} | FAIL {fails} | REAL-but-risk-reducer {real} | "
          f"PASS*-unconfirmed lead {leads} | pending/blocked {pend}")
    print(f"  >>> CONFIRMED beat buy-hold SPY risk-adjusted: {beat} / {settled}  <<<")
    if leads:
        print(f"  >>> {leads} PASS* LEAD awaiting OOS confirmation (vol-targeting) — the loop's next job  <<<")

    exp_fp = settled * 0.05
    print("\n  MULTIPLE-TESTING HONESTY:")
    print(f"    {settled} pre-registered tests; at α=0.05 chance alone yields "
          f"~{exp_fp:.1f} false positives.")
    print(f"    Our {real} 'real' results are CORRELATED risk-reducers (same fear/timing/trend "
          "family),")
    print("    and ZERO beat SPY risk-adjusted — fully consistent with NO true free alpha.")
    print("\n  CONCLUSION: the free mechanical edge is not there for us. Banked usable result:")
    print("    dual momentum = SPY return, HALF the drawdown (ret/|DD| 2.2×) — a better risk")
    print("    SHAPE, not alpha. Live signal: `python3 -m research.dualmom current`.")
    print("    Method/asset: research/SKILL.md. Audit trail: research/FINDINGS.md.")
    forward_track()
    print()


if __name__ == "__main__":
    sys.exit(main())
