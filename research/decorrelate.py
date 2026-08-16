"""One-off gate: does the dip rule's DEPLOYMENT decorrelate across asset classes?

The validated dip rule on a single ETF sits in cash ~87% of the time (13% time-in-
market) — that low utilization is why it loses to buy-and-hold standalone (see
FINDINGS). If the SAME rule on UNCORRELATED assets (equity/bonds/gold) fires on
DIFFERENT days, a basket stays deployed far more and utilization (the bottleneck)
opens up. This is the gate BEFORE building any portfolio wealth curve.

Pre-registered: union time-in-market >= 25% => decorrelated, proceed. ~13-18% =>
they co-dip, stop and pivot. (Bounds: ~max(single) if identical, 1-prod(1-tim) if
independent.) The rule is applied AS-IS to each asset — no per-asset re-tuning.

Run: python3 -m research.decorrelate
"""
from itertools import combinations

from research import config, prices

ASSETS = ["SPY", "TLT", "GLD"]          # equity / long bonds / gold
DIP, T, MA, HOLD = config.MR_MKT_DROP, config.TREND_DAYS, config.TREND_MA, config.HORIZON_DAYS


def held_dates(closes, dates):
    """Dates the one-at-a-time dip rule holds (buy on 5d dip while >200d MA, hold 5d)."""
    out, held, exit_i = set(), False, -1
    for i in range(MA, len(closes)):
        if held:
            out.add(dates[i])
            if i >= exit_i:
                held = False
        elif (closes[i] - closes[i - T]) / closes[i - T] <= DIP and \
                closes[i] > sum(closes[i - MA + 1:i + 1]) / MA:
            held, exit_i = True, i + HOLD
    return out


bars = {s: prices.daily_history(s, "20y") for s in ASSETS}
held = {s: held_dates([b["close"] for b in bars[s]], [b["date"] for b in bars[s]])
        for s in ASSETS}
actionable = {s: {b["date"] for b in bars[s][MA:]} for s in ASSETS}
common = set.intersection(*actionable.values())
N = len(common)

print(f"common trading days (all 3 alive): {N}  (~{N / 252:.0f}y)")
print("\nper-asset time-in-market:")
tims = {}
for s in ASSETS:
    tims[s] = len(held[s] & common) / N
    print(f"  {s}: {tims[s] * 100:5.1f}%")

union = set.union(*held.values()) & common
prod = 1.0
for s in ASSETS:
    prod *= (1 - tims[s])
print(f"\nUNION (>=1 asset deployed): {len(union) / N * 100:5.1f}%")
print(f"  reference bounds:  identical -> {max(tims.values()) * 100:.1f}%"
      f"   independent -> {(1 - prod) * 100:.1f}%")

print("\npairwise overlap (Jaccard = shared deployed days / either deployed):")
for a, b in combinations(ASSETS, 2):
    ha, hb = held[a] & common, held[b] & common
    j = len(ha & hb) / len(ha | hb) * 100 if (ha | hb) else 0
    print(f"  {a}-{b}: {j:5.1f}%")
