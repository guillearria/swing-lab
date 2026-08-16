"""One-off: is the dip+200d edge robust to its parameters, or a knife-edge fit?

Vary ONE knob at a time around the base (dip<=-2%, MA=200, hold=5d), pooled across
the 5-ETF universe over 20y. PASS = >200d bucket stays net-positive AND beats <200d
across neighbors, no sign-flip cliff. Reports ALL values (not a sweep-to-best).

Run: python3 -m research.robust
"""
from research import config, prices

PERIOD = "20y"
UNIVERSE = ["SPY", "QQQ", "IWM", "EFA", "EEM"]
DIPWIN = config.TREND_DAYS              # 5-day dip lookback (the dip definition, fixed)
COST = config.COST_ROUNDTRIP * 100
BASE = (-0.02, 200, 5)                  # dip, MA, hold

hist = {s: [b["close"] for b in prices.daily_history(s, PERIOD)] for s in UNIVERSE}


def cfg(dip, ma, hold):
    up, dn = [], []
    for closes in hist.values():
        for i in range(ma, len(closes) - hold):
            if (closes[i] - closes[i - DIPWIN]) / closes[i - DIPWIN] > dip:
                continue                                       # only dips
            above = closes[i] > sum(closes[i - ma + 1:i + 1]) / ma
            ret = (closes[i + hold] - closes[i]) / closes[i] * 100 - COST
            (up if above else dn).append(ret)
    def stat(x):
        return (len(x), sum(x) / len(x) if x else 0,
                sum(1 for r in x if r > 0) / len(x) * 100 if x else 0)
    return stat(up), stat(dn)


def line(label, dip, ma, hold):
    (un, unet, uwin), (_, dnet, _) = cfg(dip, ma, hold)
    base = "  <- base" if (dip, ma, hold) == BASE else ""
    print(f"{label:>12} | >200d n={un:>4} net={unet:+.2f}% win={uwin:4.1f}% "
          f"| <200d net={dnet:+.2f}%{base}")


print("== dip threshold (MA=200, hold=5) ==")
for d in (-0.01, -0.015, -0.02, -0.025, -0.03):
    line(f"dip<={d*100:.1f}%", d, 200, 5)
print("== MA length (dip=-2%, hold=5) ==")
for m in (100, 150, 200, 250):
    line(f"MA={m}", -0.02, m, 5)
print("== hold horizon (dip=-2%, MA=200) ==")
for h in (3, 5, 10):
    line(f"hold={h}d", -0.02, 200, h)
