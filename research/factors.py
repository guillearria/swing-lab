"""LOOP — cross-sectional FACTOR ETFs vs SPY (BACKLOG mechanical idea).

Do the big single-factor funds (momentum/quality/value/low-vol/size) beat buy-hold SPY
risk-adjusted over their common history? Pre-registered bar: at least one factor beats SPY
on Sharpe AND CAGR, net. (Red-team: 5 factors tested = multiple comparisons.)

  python3 -m research.factors
"""
import sys

from research import prices
from research.voltarget import _metrics

FACTORS = {"MTUM": "momentum", "QUAL": "quality", "VLUE": "value",
           "USMV": "low-vol", "SIZE": "size"}


def _monthly(sym: str) -> dict:
    me = {}
    for b in prices.daily_history(sym, "max"):
        me[b["date"][:7]] = b["close"]
    keys = sorted(me)
    return {keys[i]: me[keys[i]] / me[keys[i - 1]] - 1 for i in range(1, len(keys))}


def main():
    spy = _monthly("SPY")
    series = {f: _monthly(f) for f in FACTORS}
    common = sorted(set(spy).intersection(*[set(series[f]) for f in FACTORS]))
    sm = _metrics([spy[k] for k in common], 12)
    print(f"\n=== ARC 4 #4 FACTOR ETFs vs SPY ({common[0]}..{common[-1]}, {len(common)} months) ===")
    print(f"  SPY     : CAGR {sm['cagr']*100:+5.1f}%  Sharpe {sm['sharpe']:.2f}  maxDD {sm['mdd']*100:4.0f}%")
    any_beat = False
    for f, name in FACTORS.items():
        m = _metrics([series[f][k] for k in common], 12)
        beat = m["cagr"] > sm["cagr"] and m["sharpe"] > sm["sharpe"]
        any_beat = any_beat or beat
        print(f"  {f:7}: CAGR {m['cagr']*100:+5.1f}%  Sharpe {m['sharpe']:.2f}  maxDD {m['mdd']*100:4.0f}%"
              f"  ({name}){'  BEATS' if beat else ''}")
    print(f"  pre-registered bar (a factor beats SPY on CAGR AND Sharpe): {'PASS' if any_beat else 'FAIL'}")


if __name__ == "__main__":
    sys.exit(main())
