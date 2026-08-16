"""One-off: does the fade-the-panic dip edge hold PER ASSET — incl. crypto — and is
it stable across years (regimes), or a one-regime artifact?

Two questions, one cheap probe:
  CORE (utilization): are TLT/GLD dip-edges actually net-positive? The portfolio only
    helps if the idle capital buys WINNING trades, not merely uncorrelated ones.
  PSYCHOLOGY (the bridge): the validated edge is really FADE-THE-PANIC (buy market-wide
    fear while the trend holds — see FINDINGS). Crypto is the purest sentiment market.
    Does the same fear-fade survive there? If yes, the mechanical core IS a psychological
    edge and confluence is near. If no, crypto psychology is momentum, not reversion.

Per-year is the answer to "history doesn't dictate the future": an edge that lives in
one or two years is regime-fragile, not durable. The rule is applied AS-IS (no per-asset
re-tuning). Crypto bars are 7/week, so its "5-day" is 5 calendar days.

Run: python3 -m research.sleeves
"""
from research import config, prices

DIP, T, MA, HOLD = config.MR_MKT_DROP, config.TREND_DAYS, config.TREND_MA, config.HORIZON_DAYS
COST = config.COST_ROUNDTRIP
ASSETS = [("SPY", "20y"), ("TLT", "20y"), ("GLD", "20y"), ("BTC-USD", "max"), ("ETH-USD", "max")]


def trades(closes, dates):
    """One-at-a-time dip rule -> list of (year, net_return) per independent trade."""
    out, held, exit_i, entry, ei = [], False, -1, 0.0, 0
    for i in range(MA, len(closes)):
        if held:
            if i >= exit_i:
                out.append((dates[ei][:4], closes[i] / entry - 1 - COST))
                held = False
        elif (closes[i] - closes[i - T]) / closes[i - T] <= DIP and \
                closes[i] > sum(closes[i - MA + 1:i + 1]) / MA:
            held, entry, ei, exit_i = True, closes[i], i, i + HOLD
    return out


def line(label, rets):
    n = len(rets)
    if not n:
        print(f"  {label}: no trades"); return
    net = sum(rets) / n * 100
    win = sum(1 for r in rets if r > 0) / n * 100
    print(f"  {label}  n={n:>4}  net={net:+5.2f}%/trade  win={win:4.1f}%  cum={sum(rets)*100:+6.1f}%")


for sym, period in ASSETS:
    bars = prices.daily_history(sym, period)
    if len(bars) < MA + HOLD + 1:
        print(f"\n{sym}: too little history"); continue
    ts = trades([b["close"] for b in bars], [b["date"] for b in bars])
    print(f"\n==== {sym} ({bars[0]['date'][:4]}-{bars[-1]['date'][:4]}) ====")
    line("ALL ", [r for _, r in ts])
    for y in sorted({y for y, _ in ts}):
        line(f"  {y}", [r for y2, r in ts if y2 == y])
