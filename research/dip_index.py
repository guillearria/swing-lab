"""One-off probe: index dip-buying, and whether a 200-day trend gate helps.

Q1: does the INDEX itself bounce after its own 5-day dip? (is the stock
    'market-wide oversold' edge just index timing / beta?)
Q2: does gating dip-buys on price > 200-day MA dodge the 2022 bear?

Run: python3 -m research.dip_index [period]   # e.g. 20y, max (default config)
"""
import sys

from research import config, prices, outcome

PERIOD = sys.argv[1] if len(sys.argv) > 1 else config.BACKTEST_PERIOD
SYMBOLS = sys.argv[2:] or ("SPY", "QQQ")
H = config.HORIZON_DAYS
T = config.TREND_DAYS          # 5d dip window
MA = config.TREND_MA           # 200-day trend gate
COST = config.COST_ROUNDTRIP * 100


def stats(items):
    n = len(items)
    if not n:
        return None
    rets = [r for _, r, _ in items if r is not None]
    maes = [m for _, _, m in items if m is not None]
    tp = sum(1 for h, _, _ in items if h == 1) / n * 100
    stp = sum(1 for h, _, _ in items if h == 0) / n * 100
    net = sum(rets) / n * 100 - COST
    win = sum(1 for r in rets if r > 0) / n * 100
    mae = sum(maes) / len(maes) * 100 if maes else 0.0
    return n, tp, stp, net, win, mae


def row(label, items):
    s = stats(items)
    if not s:
        return
    n, tp, stp, net, win, mae = s
    print(f"{label:>16} {n:>6} {tp:>5.1f}% {stp:>5.1f}% {net:>6.2f}% {win:>5.1f}% {mae:>6.1f}%")


for sym in SYMBOLS:
    bars = prices.daily_history(sym, PERIOD)
    closes = [b["close"] for b in bars]
    b = {k: [] for k in ("base", "d2", "d2_up", "d2_dn", "d5", "d5_up", "d5_dn")}
    yr = {}
    for i in range(MA, len(bars) - H):
        oc = outcome.settle(closes[i], bars[i + 1:i + 1 + H])
        if oc is None:
            continue
        it = (oc["hit_tp1_before_stop"], oc["ret_5d"], oc["max_adverse"])
        chg = (closes[i] - closes[i - T]) / closes[i - T]
        up = closes[i] > sum(closes[i - MA + 1:i + 1]) / MA      # above 200d MA?
        y = yr.setdefault(bars[i]["date"][:4], {"base": [], "d2_up": []})
        b["base"].append(it); y["base"].append(it)
        if chg <= -0.02:
            b["d2"].append(it)
            (b["d2_up"] if up else b["d2_dn"]).append(it)
            if up:
                y["d2_up"].append(it)
        if chg <= -0.05:
            b["d5"].append(it)
            (b["d5_up"] if up else b["d5_dn"]).append(it)
    print(f"\n==== {sym} ====")
    print(f"{'bucket':>16} {'n':>6} {'%TP':>6} {'%stop':>6} {'net5d':>6} {'win%':>6} {'avgMAE':>7}")
    row("baseline", b["base"])
    row("dip<=-2%", b["d2"]); row("  & >200d", b["d2_up"]); row("  & <200d", b["d2_dn"])
    row("dip<=-5%", b["d5"]); row("  & >200d", b["d5_up"]); row("  & <200d", b["d5_dn"])
    print("  -- dip<=-2% & >200d by year (the gated strategy) --")
    for y in sorted(yr):
        d = stats(yr[y]["d2_up"]); base = stats(yr[y]["base"])
        if d:
            print(f"    {y}  n={d[0]:>3}  net={d[3]:>6.2f}%  win={d[4]:>5.1f}%  base={base[3]:>6.2f}%")
