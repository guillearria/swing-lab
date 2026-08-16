"""One-off: does a VIX fear-gate cut the equity fade's lumpy losers?

The SPY dip-fade is real but lumpy — loses 2010/11/22/23 (see FINDINGS). Hypothesis:
those losers cluster in a high-fear REGIME the 200d gate misses. Pre-registered SINGLE
gate (round number, NOT optimized): skip dip-buys when VIX > 30 on entry. PASS = the
VIX<=30 bucket lifts net/trade and drops the worst years vs all trades, while the
VIX>30 bucket is where the losers concentrate. One a-priori threshold, judged win or
lose — no sweeping to the best (anti-p-hacking).

Run: python3 -m research.vix_gate
"""
from research import config, prices

DIP, T, MA, HOLD = config.MR_MKT_DROP, config.TREND_DAYS, config.TREND_MA, config.HORIZON_DAYS
COST = config.COST_ROUNDTRIP
VIX_HI = 30.0


def dip_trades(closes, dates):
    """One-at-a-time dip rule -> list of (entry_date, net_return)."""
    out, held, exit_i, entry, ei = [], False, -1, 0.0, 0
    for i in range(MA, len(closes)):
        if held:
            if i >= exit_i:
                out.append((dates[ei], closes[i] / entry - 1 - COST)); held = False
        elif (closes[i] - closes[i - T]) / closes[i - T] <= DIP and \
                closes[i] > sum(closes[i - MA + 1:i + 1]) / MA:
            held, entry, ei, exit_i = True, closes[i], i, i + HOLD
    return out


def stat(ts):
    n = len(ts)
    if not n:
        return "no trades"
    rets = [r for _, r, _ in ts]
    return (f"n={n:>3}  net={sum(rets) / n * 100:+5.2f}%/trade  "
            f"win={sum(1 for r in rets if r > 0) / n * 100:4.1f}%  cum={sum(rets) * 100:+6.1f}%")


spy = prices.daily_history("SPY", "20y")
vix = {b["date"]: b["close"] for b in prices.daily_history("^VIX", "20y")}
trades = [(d, r, vix[d]) for d, r in dip_trades([b["close"] for b in spy], [b["date"] for b in spy])
          if d in vix]

lo = [t for t in trades if t[2] <= VIX_HI]
hi = [t for t in trades if t[2] > VIX_HI]
print(f"SPY dip-fade, split by VIX on entry day (gate = skip VIX>{VIX_HI:.0f}):")
print(f"  ALL       {stat(trades)}")
print(f"  VIX<=30   {stat(lo)}")
print(f"  VIX>30    {stat(hi)}   <- the skipped bucket")
print("\n  VIX>30 trades by year (do the lumpy losers cluster here?):")
yr = {}
for d, r, v in hi:
    yr.setdefault(d[:4], []).append(r)
for y in sorted(yr):
    rs = yr[y]
    print(f"    {y}  n={len(rs):>2}  net={sum(rs) / len(rs) * 100:+6.2f}%  cum={sum(rs) * 100:+6.1f}%")
