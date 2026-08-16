"""Human/regime layer (cheap, falsifiable): does the fade's tail live in a FRAGILE
trend regime a human would recognize — a flat/falling 200d — vs a healthy rising one?

We ALREADY observed (FINDINGS) the losers were "sharp dips near the 200d line." This
makes that human judgment testable WITHOUT new data: split the SPY fade trades by the
SIGN of the 200d slope at entry (rising = 200d MA above its value ~3 months ago). One
a-priori, sign-based split — no tuned threshold, judged win or lose.

Pre-registered PASS: 'rising' beats 'falling' on net AND the lumpy losers (2011/2022)
concentrate in 'falling', so gating to rising-only cuts the tail while keeping winners.
This is the LAST cheap mechanical regime proxy; if it fails (like VIX), the verdict is
"the regime edge is discretionary -> forward human-in-the-loop test", not a 3rd filter.

Run: python3 -m research.regime
"""
from research import config, prices

DIP, T, MA, HOLD = config.MR_MKT_DROP, config.TREND_DAYS, config.TREND_MA, config.HORIZON_DAYS
COST = config.COST_ROUNDTRIP
SLOPE_LB = 63   # ~3 months: is the 200d MA higher than it was a quarter ago?


def fade_trades(closes, dates):
    """Dip trades -> (entry_date, net_ret, rising) ; rising = 200d MA > its value SLOPE_LB ago."""
    ma = [None] * len(closes)
    for i in range(MA - 1, len(closes)):
        ma[i] = sum(closes[i - MA + 1:i + 1]) / MA
    out, held, exit_i, entry, ei = [], False, -1, 0.0, 0
    for i in range(MA, len(closes)):
        if held:
            if i >= exit_i:
                rising = ma[ei] > ma[ei - SLOPE_LB] if ei - SLOPE_LB >= MA - 1 else None
                out.append((dates[ei], closes[i] / entry - 1 - COST, rising))
                held = False
        elif (closes[i] - closes[i - T]) / closes[i - T] <= DIP and closes[i] > ma[i]:
            held, entry, ei, exit_i = True, closes[i], i, i + HOLD
    return out


def stat(ts):
    n = len(ts)
    if not n:
        return "no trades"
    r = [x[1] for x in ts]
    return (f"n={n:>3}  net={sum(r) / n * 100:+5.2f}%/trade  "
            f"win={sum(1 for x in r if x > 0) / n * 100:4.1f}%  cum={sum(r) * 100:+6.1f}%")


bars = prices.daily_history("SPY", "20y")
trades = fade_trades([b["close"] for b in bars], [b["date"] for b in bars])
up = [t for t in trades if t[2] is True]
dn = [t for t in trades if t[2] is False]
print("SPY fade, split by 200d SLOPE at entry (rising = 200d MA > its value ~3mo ago):")
print(f"  ALL       {stat(trades)}")
print(f"  RISING    {stat(up)}")
print(f"  FALLING   {stat(dn)}   <- the regime a human would distrust?")
print("\n  per-year net/trade (n):       rising      |     falling")
for y in sorted({d[:4] for d, _, _ in trades}):
    u = [x[1] for x in up if x[0][:4] == y]
    d = [x[1] for x in dn if x[0][:4] == y]
    us = f"{sum(u) / len(u) * 100:+6.2f}% ({len(u)})" if u else "—"
    ds = f"{sum(d) / len(d) * 100:+6.2f}% ({len(d)})" if d else "—"
    print(f"    {y}   {us:>14}  |  {ds:>14}")
