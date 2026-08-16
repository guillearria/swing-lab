"""LOOP — bond CURVE CARRY (BACKLOG mechanical idea, the cross-asset 'carry' family).

Hold long-duration bonds (TLT) when the yield curve is positive (10y > 3mo → positive
carry to duration), else short-duration (SHY). Monthly, decided from the prior month-end
curve (no lookahead). Pre-registered bar = the wealth bar: beat buy-hold SPY on Sharpe AND
CAGR. Also reported vs TLT buy-hold (its own asset) since carry is a bond strategy, not an
SPY competitor by construction.

  python3 -m research.carry
"""
import sys

from research import prices
from research.voltarget import _metrics


def _monthly_close(sym: str) -> dict:
    me = {}
    for b in prices.daily_history(sym, "max"):
        me[b["date"][:7]] = b["close"]
    return me


def main():
    tnx = _monthly_close("^TNX")   # 10y yield (percent)
    irx = _monthly_close("^IRX")   # 13-week yield (percent)
    tlt = _monthly_close("TLT")
    shy = _monthly_close("SHY")
    spy = _monthly_close("SPY")
    keys = sorted(set(tnx) & set(irx) & set(tlt) & set(shy) & set(spy))

    carry, tlt_bh, spy_bh = [], [], []
    for i in range(1, len(keys)):
        k0, k1 = keys[i - 1], keys[i]
        positive = tnx[k0] > irx[k0]                       # curve sign at prior month-end
        pick = tlt if positive else shy
        carry.append(pick[k1] / pick[k0] - 1)
        tlt_bh.append(tlt[k1] / tlt[k0] - 1)
        spy_bh.append(spy[k1] / spy[k0] - 1)

    c, t, s = _metrics(carry, 12), _metrics(tlt_bh, 12), _metrics(spy_bh, 12)
    print(f"\n=== ARC 4 #6 BOND CURVE CARRY ({keys[1]}..{keys[-1]}, {len(carry)} months) ===")
    print(f"  curve-carry: CAGR {c['cagr']*100:+5.1f}%  Sharpe {c['sharpe']:.2f}  maxDD {c['mdd']*100:4.0f}%")
    print(f"  TLT buyhold: CAGR {t['cagr']*100:+5.1f}%  Sharpe {t['sharpe']:.2f}  maxDD {t['mdd']*100:4.0f}%")
    print(f"  SPY buyhold: CAGR {s['cagr']*100:+5.1f}%  Sharpe {s['sharpe']:.2f}  maxDD {s['mdd']*100:4.0f}%")
    beat_spy = c["cagr"] > s["cagr"] and c["sharpe"] > s["sharpe"]
    print(f"  pre-registered bar (beat SPY on CAGR AND Sharpe): {'PASS' if beat_spy else 'FAIL'}")
    print(f"  (vs its own asset: {'beats' if c['sharpe'] > t['sharpe'] else 'ties/loses'} TLT buy-hold on Sharpe)")


if __name__ == "__main__":
    sys.exit(main())
