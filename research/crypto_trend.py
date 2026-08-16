"""One-off: does TREND-following beat buy-and-hold in crypto (the sentiment market)?

Fade-the-panic FAILED in crypto (see FINDINGS) — dips keep dipping. Opposite
hypothesis: reflexive/sentiment markets TREND, so ride them. Long while close > 200d
MA (decided on yesterday's close — no lookahead), flat/cash below; switch costs applied.

Pre-registered PASS: beats buy-hold risk-adjusted (CAGR/|maxDD|) AND sidesteps the
brunt of BOTH bears (2018 and 2022) — not just one (guard vs one-cycle fit). Caveat:
only ~2-3 crypto cycles exist; suggestive, not proven.

Run: python3 -m research.crypto_trend
"""
from research import config, prices

MA, COST = config.TREND_MA, config.COST_ROUNDTRIP
ASSETS = [("BTC-USD", "max"), ("ETH-USD", "max")]


def curves(closes):
    """Trend (long >200d MA else cash) and buy-hold, indexed to 1.0. No lookahead."""
    strat, bh, inpos = [1.0], [1.0], False
    for i in range(MA, len(closes)):
        ret = closes[i] / closes[i - 1] - 1
        ma = sum(closes[i - MA:i]) / MA            # 200d MA through yesterday
        want = closes[i - 1] > ma                  # decide on yesterday's close
        s = strat[-1] * (1 + (ret if inpos else 0.0))
        if want != inpos:
            s *= (1 - COST)                        # pay round-trip cost on each switch
        strat.append(s)
        bh.append(bh[-1] * (1 + ret))
        inpos = want
    return strat, bh


def cagr(c, n):
    y = n / 252
    return (c[-1] ** (1 / y) - 1) * 100 if y > 0 else 0


def maxdd(c):
    peak, mdd = c[0], 0.0
    for v in c:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    return mdd * 100


for sym, period in ASSETS:
    bars = prices.daily_history(sym, period)
    closes = [b["close"] for b in bars]
    dates = [b["date"] for b in bars]
    if len(closes) < MA + 30:
        print(f"{sym}: too little history"); continue
    strat, bh = curves(closes)
    n = len(strat)
    print(f"\n==== {sym} ({dates[0][:4]}-{dates[-1][:4]}) ====")
    print(f"  trend:    CAGR {cagr(strat, n):+6.1f}%  maxDD {maxdd(strat):6.1f}%  end x{strat[-1]:6.1f}")
    print(f"  buy-hold: CAGR {cagr(bh, n):+6.1f}%  maxDD {maxdd(bh):6.1f}%  end x{bh[-1]:6.1f}")
    yr = {}
    for k in range(1, n):
        y = dates[MA + k - 1][:4]
        d = yr.setdefault(y, [1.0, 1.0])
        d[0] *= strat[k] / strat[k - 1]
        d[1] *= bh[k] / bh[k - 1]
    print("    year    trend   buy-hold   (bears: 2018, 2022)")
    for y in sorted(yr):
        print(f"    {y}  {(yr[y][0] - 1) * 100:+8.1f}%  {(yr[y][1] - 1) * 100:+8.1f}%")
