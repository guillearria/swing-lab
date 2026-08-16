"""ARC 4 #1 — asset-class DUAL MOMENTUM (Antonacci-style). pre-registration in FINDINGS_ARCHIVE.md [ARC 4 #1].

Monthly: hold the highest trailing-12m equity among {SPY, EFA, EEM}; if even the best
is <=0 (absolute-momentum gate, T-bill~0 proxy), hold AGG (bonds). No lookahead: the
holding for month t+1 is decided only from data through the close of month t.

  python3 -m research.dualmom
"""
import logging
import sys

from research import prices

log = logging.getLogger(__name__)

EQ = ["SPY", "EFA", "EEM"]
DEF = "AGG"
LOOKBACK_M = 12
COST = 0.001  # per-switch round-trip (liquid ETFs)


def _monthly(sym: str) -> dict:
    """ym ('YYYY-MM') -> month-end adjusted close."""
    me = {}
    for b in prices.daily_history(sym, "max"):   # bars ascending → last per month = month-end
        me[b["date"][:7]] = b["close"]
    return me


def backtest():
    series = {s: _monthly(s) for s in EQ + [DEF]}
    months = sorted(set.intersection(*[set(series[s]) for s in EQ + [DEF]]))
    strat, spy, holds = [], [], []
    held = None
    for i in range(LOOKBACK_M, len(months) - 1):
        m0, m1, mback = months[i], months[i + 1], months[i - LOOKBACK_M]
        moms = {s: series[s][m0] / series[s][mback] - 1 for s in EQ}
        best = max(moms, key=moms.get)
        pick = best if moms[best] > 0 else DEF      # absolute-momentum gate
        r = series[pick][m1] / series[pick][m0] - 1
        if held is not None and pick != held:
            r -= COST
        held = pick
        strat.append(r); spy.append(series["SPY"][m1] / series["SPY"][m0] - 1)
        holds.append((m1, pick))
    return months[LOOKBACK_M], months[-1], strat, spy, holds


def _metrics(rets: list[float]):
    n = len(rets)
    eq, curve = 1.0, [1.0]
    for r in rets:
        eq *= (1 + r); curve.append(eq)
    mean = sum(rets) / n
    sd = (sum((x - mean) ** 2 for x in rets) / (n - 1)) ** 0.5
    peak, mdd = -1.0, 0.0
    for v in curve:
        peak = max(peak, v); mdd = min(mdd, v / peak - 1)
    return {"cagr": eq ** (12 / n) - 1, "sharpe": (mean / sd) * (12 ** 0.5) if sd else 0.0,
            "mdd": mdd, "mult": eq}


def _ranks() -> tuple[str, dict, str]:
    """(as-of month, trailing-12m moms, pick) from latest data. PURE — the one place the
    current holding is computed (single source of truth)."""
    series = {s: _monthly(s) for s in EQ + [DEF]}
    months = sorted(set.intersection(*[set(series[s]) for s in EQ + [DEF]]))
    m0, mback = months[-1], months[-1 - LOOKBACK_M]
    moms = {s: series[s][m0] / series[s][mback] - 1 for s in EQ}
    best = max(moms, key=moms.get)
    return m0, moms, (best if moms[best] > 0 else DEF)


def current_hold() -> str:
    """What to hold THIS month (the ticker only) — for callers that just need the pick
    (e.g. book.py's same-$-in-dual-mom yardstick)."""
    return _ranks()[2]


def current():
    """The banked, usable output: what to hold THIS month (as of latest data)."""
    m0, moms, pick = _ranks()
    print(f"\n=== DUAL MOMENTUM — current signal (as of {m0}) ===")
    for s in EQ:
        print(f"  {s}: trailing-12m {moms[s] * 100:+.1f}%")
    gate = "" if pick != DEF else "  (absolute-momentum gate: best equity ≤ 0 → bonds)"
    print(f"  -> HOLD: {pick}{gate}")
    print("  (monthly check; switch only when this changes. Risk shape, not alpha.)")


def main():
    start, end, strat, spy, holds = backtest()
    s, b = _metrics(strat), _metrics(spy)
    print(f"\n=== ARC 4 #1 DUAL MOMENTUM ({start}..{end}, {len(strat)} months, net {COST*100:.1f}%/switch) ===")
    print(f"  dual-mom : CAGR {s['cagr']*100:+5.1f}%  Sharpe {s['sharpe']:.2f}  "
          f"maxDD {s['mdd']*100:4.0f}%  x{s['mult']:.1f}")
    print(f"  buy-hold : CAGR {b['cagr']*100:+5.1f}%  Sharpe {b['sharpe']:.2f}  "
          f"maxDD {b['mdd']*100:4.0f}%  x{b['mult']:.1f}")
    bar = s["cagr"] > b["cagr"] and s["sharpe"] > b["sharpe"] and s["mdd"] > b["mdd"]
    print(f"  pre-registered bar (beat SPY on CAGR AND Sharpe AND maxDD): {'PASS' if bar else 'FAIL'}")
    # per-decade CAGR (OOS regimes)
    from collections import defaultdict
    dec = defaultdict(lambda: [[], []])
    for (m1, _), rs, rb in zip(holds, strat, spy):
        d = m1[:3] + "0s"
        dec[d][0].append(rs); dec[d][1].append(rb)
    print("  per-decade CAGR (dual-mom vs SPY):")
    for d in sorted(dec):
        rs, rb = dec[d]
        cs = (_metrics(rs)["cagr"] if len(rs) > 1 else 0) * 100
        cb = (_metrics(rb)["cagr"] if len(rb) > 1 else 0) * 100
        print(f"    {d}: {cs:+5.1f}%  vs  {cb:+5.1f}%   ({'win' if cs > cb else 'lose'})")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    (current if len(sys.argv) > 1 and sys.argv[1] == "current" else main)()
