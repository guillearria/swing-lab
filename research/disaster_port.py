"""Experiment #2: the GLOBAL disaster-buy PORTFOLIO — can utilization finally beat buy-hold?

Per-asset, a -20% disaster is rare (idle ~90% of the time) — that idleness is why every
edge so far ties/loses to buy-hold. But disasters DECORRELATE across countries (Greece'15
!= China'15 != US'20 != Russia'22), so across a global basket SOMETHING is almost always
wrecked. This tests whether spreading the validated disaster-buy across the world keeps us
invested enough to beat the bogey. Convergence of: validated entry + decorrelation + the
utilization bottleneck (original threat #1).

Rules (no lookahead: every decision uses info through YESTERDAY's close):
  - An asset ARMS when it closes >=20% below its trailing-1y high; DISARMS at a new 1y high
    (recovery). You only play disasters, then step aside — you don't ride forever.
  - While ARMED, a position is DEPLOYED (long) on days close>200d MA, else flat (the dynamic
    trend-exit that proved itself in true collapses).
  - SPREAD  (conservative): each deployed asset = 1/N_eligible of capital, rest CASH(0%).
  - CONCENTRATE (aggressive): each deployed asset = 1/K_deployed -> ~fully invested whenever
    ANY signal fires, cash only when none.
  - Costs: turnover x half-round-trip on every weight change. No leverage. Cash earns 0.
Basket includes the CORPSES (Russia/Greece/Argentina/Turkey) on purpose — no survivorship.

Pre-registered PASS: CONCENTRATE beats buy-hold SPY on risk-adjusted return (CAGR/|maxDD|)
AND has materially smaller maxDD. Bonus if it also matches/beats CAGR. FAIL = ties/loses
risk-adjusted (utilization still doesn't crack the wall). Honest prior: last capstone TIED
buy-hold via beta; the new ingredient is global decorrelation.

Run: python3 -m research.disaster_port
"""
import math

from research import config, prices

MA, YR, COST = config.TREND_MA, 252, config.COST_ROUNDTRIP

# Global, multi-asset, decorrelated — incl. dead/stuck markets (no survivorship).
ASSETS = [("SPY", "US"), ("EFA", "DevExUS"), ("EEM", "EM"), ("EWJ", "Japan"),
          ("FXI", "China"), ("EWZ", "Brazil"), ("EWI", "Italy"), ("GREK", "Greece"),
          ("ARGT", "Argentina"), ("TUR", "Turkey"), ("RSX", "Russia"),
          ("GLD", "gold"), ("TLT", "bonds"), ("BTC-USD", "crypto")]


def on_spine(dd, spine):
    """Forward-filled close on the spine; None before the asset's first real date."""
    out, last = [], None
    for s in spine:
        if s in dd:
            last = dd[s]
        out.append(last)
    return out


def precompute(closes):
    """Per-asset arrays on the spine: deployed[t] (no lookahead) and daily return."""
    n = len(closes)
    first = next((i for i, c in enumerate(closes) if c is not None), n)
    ma = [None] * n
    armed = [False] * n
    deployed = [False] * n
    ret = [0.0] * n
    for t in range(first, n):
        if closes[t] is not None and closes[t - 1] is not None:
            ret[t] = closes[t] / closes[t - 1] - 1
        if t - first >= MA - 1 and None not in closes[t - MA + 1:t + 1]:
            ma[t] = sum(closes[t - MA + 1:t + 1]) / MA
        if t - first >= YR - 1 and None not in closes[t - YR + 1:t + 1]:
            hi = max(closes[t - YR + 1:t + 1])
            dd = closes[t] / hi - 1
            if not armed[t - 1] and dd <= -0.20:
                armed[t] = True
            elif armed[t - 1] and dd >= 0:
                armed[t] = False
            else:
                armed[t] = armed[t - 1]
        else:
            armed[t] = armed[t - 1] if t > first else False
    eligible = [t >= first + YR for t in range(n)]
    for t in range(1, n):
        deployed[t] = (eligible[t] and armed[t - 1] and ma[t - 1] is not None
                       and closes[t - 1] is not None and closes[t - 1] > ma[t - 1])
    return deployed, ret, eligible


def metrics(eq, n_days):
    yrs = n_days / 252
    cagr = (eq[-1] ** (1 / yrs) - 1) * 100 if yrs > 0 and eq[-1] > 0 else -100.0
    peak, mdd = eq[0], 0.0
    for v in eq:
        peak = max(peak, v); mdd = min(mdd, v / peak - 1)
    rets = [eq[i] / eq[i - 1] - 1 for i in range(1, len(eq))]
    mu = sum(rets) / len(rets)
    sd = (sum((r - mu) ** 2 for r in rets) / len(rets)) ** 0.5
    sharpe = mu / sd * math.sqrt(252) if sd > 0 else 0.0
    return cagr, mdd * 100, sharpe


# --- load + align ---
raw = {sym: {b["date"]: b["close"] for b in prices.daily_history(sym, "max")} for sym, _ in ASSETS}
spine = sorted(raw["SPY"])
T = len(spine)
dep, ret, elig = {}, {}, {}
for sym, _ in ASSETS:
    dep[sym], ret[sym], elig[sym] = precompute(on_spine(raw[sym], spine))

# --- simulate both variants ---
print(f"Global disaster portfolio | {len(ASSETS)} assets | {spine[0]} -> {spine[-1]} ({T} days)")
print(f"  (eligible at end: {sum(elig[s][-1] for s, _ in ASSETS)} of {len(ASSETS)})")
for variant in ("SPREAD", "CONCENTRATE"):
    eq, prev, tim, depsum = [1.0], {}, 0, 0
    for t in range(1, T):
        live = [s for s, _ in ASSETS if dep[s][t]]
        ne = sum(elig[s][t] for s, _ in ASSETS) or 1
        K = len(live)
        if K:
            tim += 1; depsum += K
        w = {s: (1.0 / ne if variant == "SPREAD" else 1.0 / K) for s in live}
        r = sum(w[s] * ret[s][t] for s in live)
        turn = sum(abs(w.get(s, 0) - prev.get(s, 0)) for s in set(w) | set(prev))
        eq.append(eq[-1] * (1 + r - COST / 2 * turn))
        prev = w
    cagr, mdd, sh = metrics(eq, T)
    print(f"\n{variant:11s}  CAGR {cagr:+5.1f}%  maxDD {mdd:5.1f}%  Sharpe {sh:.2f}  "
          f"ret/|DD| {cagr / abs(mdd):.2f}  end x{eq[-1]:.1f}")
    print(f"             time-in-market {tim / (T - 1) * 100:.0f}%  avg #deployed {depsum / max(tim,1):.1f}")

# --- benchmark: buy-hold SPY over the same window ---
sp = on_spine(raw["SPY"], spine)
bh = [sp[t] / sp[0] for t in range(T)]
cagr, mdd, sh = metrics(bh, T)
print(f"\n{'BUY-HOLD SPY':11s}  CAGR {cagr:+5.1f}%  maxDD {mdd:5.1f}%  Sharpe {sh:.2f}  "
      f"ret/|DD| {cagr / abs(mdd):.2f}  end x{bh[-1]:.1f}   <- the bogey")
