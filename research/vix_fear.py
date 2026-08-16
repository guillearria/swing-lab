"""One-off: does "buy extreme FEAR, hold weeks-to-months" beat buy-any-day on SPY?

We already tested VIX as a 5-day GATE to cut the dip-fade's losers -> FAILED (high
VIX was the BEST trades, n=7; see FINDINGS). This is the DIFFERENT, a-priori claim
from the social-fear file: extreme fear as an ENTRY, held longer. Cleanest free fear
gauge (^VIX), longest free history (SPY from 1993 -> spans 2000/2008/2020/2022).

Pre-registered: two a-priori "extreme" defs -- (i) VIX>=30 absolute (same line as the
failed gate, directly comparable); (ii) VIX>=trailing-1y 90th pctile (regime-relative,
VIX baseline drifts). Entry NEXT-day close (no lookahead), hold H in {20,40,60}d,
de-overlapped, net of cost. PASS = beats the all-days H-day baseline at a MAJORITY of
horizons for >=1 def, independent N>=20, positive across major fear events (not 2020
alone -> by-decade check). Distinct from the failed gate (5d hold to CUT losers; this
is a longer-hold ENTRY).

Caveats: clustered episodes (de-overlapped); mega-events may dominate (decade split);
long holds carry real drawdown the mean hides (worst-episode shown).

Run: python3 -m research.vix_fear
"""
from research import config, prices

COST = config.COST_ROUNDTRIP
HOLDS = (20, 40, 60)
CANON = 40


def pctl(xs, q):
    s = sorted(xs); k = (len(s) - 1) * q; lo = int(k)
    return s[lo] if lo + 1 >= len(s) else s[lo] + (k - lo) * (s[lo + 1] - s[lo])


def trades(dates, closes, sig, H):
    """De-overlapped: sig(i) True -> enter NEXT close, hold H. -> [(entry_date, net)]."""
    out, held, exit_i, entry, ei = [], False, -1, 0.0, 0
    n = len(closes)
    for i in range(n):
        if held:
            if i >= exit_i:
                out.append((dates[ei], closes[i] / entry - 1 - COST)); held = False
        elif sig(i) and i + 1 < n:
            entry, ei, exit_i, held = closes[i + 1], i + 1, i + 1 + H, True
    return out


def baseline(closes, H):
    r = [closes[i + H] / closes[i] - 1 - COST for i in range(len(closes) - H)]
    return sum(r) / len(r) if r else 0.0


def stat(ts):
    rets = [r for _, r in ts]
    n = len(rets)
    if not n:
        return "no trades"
    return (f"n={n:>3}  mean={sum(rets) / n * 100:+6.2f}%  "
            f"win={sum(1 for r in rets if r > 0) / n * 100:4.0f}%  worst={min(rets) * 100:+6.1f}%")


sp = {b["date"]: b["close"] for b in prices.daily_history("SPY", "max")}
vx = {b["date"]: b["close"] for b in prices.daily_history("^VIX", "max")}
dates = sorted(set(sp) & set(vx))
closes = [sp[d] for d in dates]
vix = [vx[d] for d in dates]
print(f"SPY+VIX aligned: {dates[0]} -> {dates[-1]} ({len(dates)} days)")

defs = {
    "VIX>=30 abs   ": lambda i: vix[i] >= 30,
    "VIX>=1y-90pctl": lambda i: i >= 252 and vix[i] >= pctl(vix[i - 252:i], 0.90),
}
for name, sig in defs.items():
    print(f"\n== {name.strip()} ==")
    for H in HOLDS:
        ts = trades(dates, closes, sig, H)
        print(f"  H={H:>2}d  signal {stat(ts)}   | baseline mean={baseline(closes, H) * 100:+6.2f}%")
    ts = trades(dates, closes, sig, CANON)
    dec = {}
    for d, r in ts:
        dec.setdefault(d[:3] + "0s", []).append(r)
    print(f"  by-decade @H={CANON} (guard vs one mega-event carrying it):")
    for k in sorted(dec):
        rs = dec[k]
        print(f"     {k}  n={len(rs):>2}  mean={sum(rs) / len(rs) * 100:+6.2f}%  cum={sum(rs) * 100:+7.1f}%")
