"""One-off: does crypto REVERT on sentiment extremes (even though it TRENDS on price)?

Fade-the-panic failed on crypto PRICE (dips keep dipping; see FINDINGS) and trend-
following won there instead. Different question: the Crypto Fear & Greed index
(alternative.me, free, daily from 2018) is a SENTIMENT gauge. Hypothesis: extreme
fear (F&G<=20) marks bottoms -> buying it and holding beats buy-any-day, AND fires
where the 200d trend rule sits in CASH (so it COMPLEMENTS trend, catching the low the
trend rule re-enters too late to get).

Pre-registered (no goalpost-moving): entry on F&G<=20, enter NEXT-day close (F&G for
day D is only known end-of-D -> next-day kills lookahead), hold H in {20,40,60}d, net
of cost, de-overlapped per H. PASS = beats the all-days H-day baseline at a MAJORITY
of horizons, positive on BTC, AND a majority of episodes fire while price<200d MA. 20
is the index's own "extreme fear" band; 25 (its published boundary) reported only.

Caveats: ~3 cycles (suggestive); F&G is partly price/volatility-derived (not purely
social); BTC/ETH majors-only (mild survivorship).

Run: python3 -m research.fng_crypto
"""
import json
import os

from research import config, prices

COST, MA = config.COST_ROUNDTRIP, config.TREND_MA
EXTREME, PUBLISHED = 20, 25
HOLDS = (20, 40, 60)
CANON = 40
FNG_PATH = os.path.join(os.path.dirname(__file__), "data", "fng.json")


def load_fng():
    with open(FNG_PATH) as f:
        return {r["date"]: r["value"] for r in json.load(f)}


def aligned(sym, fng):
    """(dates, closes, fng) on the date-intersection, oldest->newest."""
    ds, cs, fs = [], [], []
    for b in prices.daily_history(sym, "max"):
        if b["date"] in fng:
            ds.append(b["date"]); cs.append(b["close"]); fs.append(fng[b["date"]])
    return ds, cs, fs


def trades(dates, closes, fvals, thresh, H):
    """De-overlapped: F&G<=thresh -> enter NEXT close, hold H. -> [(entry_date, net)]."""
    out, held, exit_i, entry, ei = [], False, -1, 0.0, 0
    n = len(closes)
    for i in range(n):
        if held:
            if i >= exit_i:
                out.append((dates[ei], closes[i] / entry - 1 - COST)); held = False
        elif fvals[i] <= thresh and i + 1 < n:
            entry, ei, exit_i, held = closes[i + 1], i + 1, i + 1 + H, True
    return out


def baseline(closes, H):
    """Buy-any-day, hold H, net of cost -> mean return."""
    r = [closes[i + H] / closes[i] - 1 - COST for i in range(len(closes) - H)]
    return sum(r) / len(r) if r else 0.0


def stat(ts):
    rets = [r for _, r in ts]
    n = len(rets)
    if not n:
        return "no trades"
    return (f"n={n:>3}  mean={sum(rets) / n * 100:+6.2f}%  "
            f"win={sum(1 for r in rets if r > 0) / n * 100:4.0f}%  cum={sum(rets) * 100:+7.0f}%")


fng = load_fng()
for sym in ("BTC-USD", "ETH-USD"):
    dates, closes, fvals = aligned(sym, fng)
    di = {d: k for k, d in enumerate(dates)}
    print(f"\n==== {sym}  ({dates[0]} -> {dates[-1]}, {len(closes)} aligned days) ====")
    for thresh in (EXTREME, PUBLISHED):
        tag = "F&G<=20 (extreme)" if thresh == EXTREME else "F&G<=25 (published)"
        print(f"  -- {tag} --")
        for H in HOLDS:
            ts = trades(dates, closes, fvals, thresh, H)
            print(f"    H={H:>2}d  signal {stat(ts)}   | baseline mean={baseline(closes, H) * 100:+6.2f}%")
    # complementarity + lumpiness on the canonical hold @ extreme
    ts = trades(dates, closes, fvals, EXTREME, CANON)
    below = sum(1 for d, _ in ts
                if di[d] >= MA and closes[di[d]] < sum(closes[di[d] - MA:di[d]]) / MA)
    print(f"  complementarity @H={CANON} extreme: {below}/{len(ts)} entries below 200d MA "
          f"(where the trend rule sits in CASH)")
    yr = {}
    for d, r in ts:
        yr.setdefault(d[:4], []).append(r)
    print(f"  lumpiness @H={CANON} extreme (cum by entry-year — is it one cycle?):")
    for y in sorted(yr):
        rs = yr[y]
        print(f"     {y}  n={len(rs):>2}  cum={sum(rs) * 100:+7.1f}%")
