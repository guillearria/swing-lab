"""LOOP iteration #3 (mechanical, untested family) — the VOLATILITY RISK PREMIUM.

"Selling insurance": option/variance sellers collect IMPLIED vol (priced by VIX) and pay
REALIZED vol. Implied usually exceeds realized, so the seller earns a premium — the way a
lot of "consistent income" traders actually make money. The question this probe settles:
does it beat SPY risk-adjusted, AND what does its left tail look like?

Proxy (free data only): each month, short a 1-month variance swap struck at the prior
month-end VIX. Monthly P&L (per unit variance notional) = implied_var − realized_var.
Sharpe is notional-invariant, so we compare Sharpe to SPY directly, then RED-TEAM the
skew / worst month (the part Sharpe hides). Pre-registered bar: VRP Sharpe > SPY Sharpe.

  python3 -m research.volrp
"""
import logging
import math
import sys
from collections import defaultdict

from research import prices

log = logging.getLogger(__name__)


def backtest():
    spy = prices.daily_history("SPY", "max")
    vix = {b["date"]: b["close"] for b in prices.daily_history("^VIX", "max")}
    rows, prev = [], None
    for b in spy:
        if prev is not None and b["date"] in vix:
            rows.append((b["date"], math.log(b["close"] / prev), vix[b["date"]]))
        prev = b["close"]
    months = defaultdict(list)
    for d, lr, v in rows:
        months[d[:7]].append((lr, v))
    keys = sorted(months)
    vrp, spy_ret = [], []
    for i in range(1, len(keys)):
        vix_start = months[keys[i - 1]][-1][1]            # prior month-end VIX (known at start)
        implied = (vix_start / 100) ** 2 / 12             # 1-month implied variance
        realized = sum(lr * lr for lr, _ in months[keys[i]])
        vrp.append(implied - realized)
        spy_ret.append(math.exp(sum(lr for lr, _ in months[keys[i]])) - 1)
    return keys[1:], vrp, spy_ret


def _stats(xs, ppy=12):
    n = len(xs); m = sum(xs) / n
    sd = (sum((x - m) ** 2 for x in xs) / (n - 1)) ** 0.5
    sharpe = (m / sd) * (ppy ** 0.5) if sd else 0.0
    skew = (sum(((x - m) / sd) ** 3 for x in xs) / n) if sd else 0.0
    return m, sd, sharpe, skew


def main():
    keys, vrp, spy = backtest()
    vm, vsd, vsh, vsk = _stats(vrp)
    _, _, ssh, _ = _stats(spy)
    pos = sum(1 for x in vrp if x > 0) / len(vrp) * 100
    worst = min(vrp); worst_k = keys[vrp.index(worst)]
    months_erased = worst / vm if vm else float("inf")

    print(f"\n=== ARC 4 #3 VOLATILITY RISK PREMIUM ({keys[0]}..{keys[-1]}, {len(vrp)} months) ===")
    print(f"  short-vol: Sharpe {vsh:.2f}  %months-positive {pos:.0f}%  skew {vsk:+.2f}")
    print(f"  buy-hold SPY: Sharpe {ssh:.2f}")
    print(f"  worst month {worst_k}: erases {abs(months_erased):.0f} months of average premium")
    bar = vsh > ssh
    print(f"  pre-registered bar (VRP Sharpe > SPY Sharpe): {'PASS' if bar else 'FAIL'}")
    print(f"  RED-TEAM: skew {vsk:+.2f} (negative = crash-prone). A high Sharpe with deep")
    print("    negative skew is COMPENSATION for crash risk, not free alpha — 'pick up")
    print("    pennies in front of a steamroller.' The Sharpe LIES for this payoff shape.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(main())
