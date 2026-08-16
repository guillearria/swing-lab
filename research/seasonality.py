"""LOOP — SEASONALITY on SPY (BACKLOG mechanical idea).

Two classic calendar effects, each as a timing rule vs buy-hold SPY:
  - Halloween / "Sell in May": in market Nov-Apr, cash May-Oct.
  - Turn-of-month: in market only the last trading day + first 3 of each month, else cash.
Pre-registered bar: beat buy-hold SPY on Sharpe AND CAGR, net (cash earns 0% here — a
conservative proxy that, if anything, helps the seasonal rule).

  python3 -m research.seasonality
"""
import sys
from collections import defaultdict

from research import prices
from research.voltarget import _metrics


def main():
    bars = prices.daily_history("SPY", "max")
    rets, dates = [], []
    for i in range(1, len(bars)):
        rets.append(bars[i]["close"] / bars[i - 1]["close"] - 1)
        dates.append(bars[i]["date"])
    bh = _metrics(rets, 252)

    hal = [r if int(d[5:7]) in (11, 12, 1, 2, 3, 4) else 0.0 for r, d in zip(rets, dates)]

    month_idx = defaultdict(list)
    for i, d in enumerate(dates):
        month_idx[d[:7]].append(i)
    tom_in = set()
    for idxs in month_idx.values():
        tom_in.update(idxs[:3])      # first 3 trading days
        tom_in.add(idxs[-1])         # last trading day
    tom = [rets[i] if i in tom_in else 0.0 for i in range(len(rets))]

    print(f"\n=== ARC 4 #5 SEASONALITY on SPY ({dates[0]}..{dates[-1]}, {len(rets)} days) ===")
    print(f"  buy-hold   : CAGR {bh['cagr']*100:+5.1f}%  Sharpe {bh['sharpe']:.2f}  maxDD {bh['mdd']*100:4.0f}%")
    for label, series in (("Halloween", hal), ("turn-of-month", tom)):
        m = _metrics(series, 252)
        beat = m["cagr"] > bh["cagr"] and m["sharpe"] > bh["sharpe"]
        print(f"  {label:11}: CAGR {m['cagr']*100:+5.1f}%  Sharpe {m['sharpe']:.2f}  "
              f"maxDD {m['mdd']*100:4.0f}%  {'BEATS' if beat else 'fails'}")
    print("  pre-registered bar (beat SPY on CAGR AND Sharpe): see per-row (PASS only if a row BEATS)")


if __name__ == "__main__":
    sys.exit(main())
