"""Capstone: do the two uncorrelated edges compound better TOGETHER than alone?

Sleeves, equal-weight, rebalanced monthly (the simple, defensible allocation — no
dynamic priority/sizing to p-hack):
  SPY-fade, GLD-fade    (validated mean-reversion — buy 5d dip while >200d, hold 5d)
  BTC-trend, ETH-trend  (PROVISIONAL momentum — long >200d else cash; thin 2-3 cycles)

Two portfolios so crypto's contribution is honest and removable:
  CORE = SPY-fade + GLD-fade
  FULL = CORE + BTC-trend + ETH-trend
Monthly returns (sidesteps the crypto-7d / equity-5d calendar mismatch). FULL vs CORE
is shown on the SAME (crypto-length) window so it's a fair comparison. Cash earns 0%
(conservative). Caveat: monthly maxDD understates intra-month; this is in-sample
assembly of edges already found — the real test is forward.

Run: python3 -m research.portfolio
"""
from research import config, prices

T, MA, HOLD, COST = config.TREND_DAYS, config.TREND_MA, config.HORIZON_DAYS, config.COST_ROUNDTRIP
DIP = config.MR_MKT_DROP


def fade_equity(closes, dates):
    """Daily equity of the one-at-a-time dip-fade (cash except during 5d holds)."""
    eq, held, exit_i, entry, eq0, de, dd = 1.0, False, -1, 0.0, 1.0, [], []
    for i in range(MA, len(closes)):
        if held:
            eq = eq0 * closes[i] / entry
            if i >= exit_i:
                eq *= (1 - COST); held = False
        elif (closes[i] - closes[i - T]) / closes[i - T] <= DIP and \
                closes[i] > sum(closes[i - MA + 1:i + 1]) / MA:
            held, entry, eq0, exit_i = True, closes[i], eq, i + HOLD
        de.append(eq); dd.append(dates[i])
    return dd, de


def trend_equity(closes, dates):
    """Daily equity of long-while->200d-MA-else-cash (for crypto). No lookahead."""
    eq, inpos, de, dd = 1.0, False, [], []
    for i in range(MA, len(closes)):
        ret = closes[i] / closes[i - 1] - 1
        want = closes[i - 1] > sum(closes[i - MA:i]) / MA
        eq *= (1 + (ret if inpos else 0.0))
        if want != inpos:
            eq *= (1 - COST)
        de.append(eq); dd.append(dates[i]); inpos = want
    return dd, de


def bh_equity(closes, dates):
    return dates[MA:], [closes[i] / closes[MA - 1] for i in range(MA, len(closes))]


def monthly(dates, equity):
    """{YYYY-MM: month-end-to-month-end return} from a daily equity curve."""
    me = {}
    for d, e in zip(dates, equity):
        me[d[:7]] = e
    mo = sorted(me)
    return {mo[k]: me[mo[k]] / me[mo[k - 1]] - 1 for k in range(1, len(mo))}


def load(sym, period, fn):
    bars = prices.daily_history(sym, period)
    return monthly(*fn([b["close"] for b in bars], [b["date"] for b in bars]))


def combine(sleeves, months=None):
    common = set.intersection(*[set(s) for s in sleeves])
    if months is not None:
        common &= set(months)
    common = sorted(common)
    return common, [sum(s[m] for s in sleeves) / len(sleeves) for m in common]


def metrics(months, rets):
    eq = [1.0]
    for r in rets:
        eq.append(eq[-1] * (1 + r))
    yrs = len(rets) / 12
    cagr = (eq[-1] ** (1 / yrs) - 1) * 100
    mu = sum(rets) / len(rets)
    sd = (sum((r - mu) ** 2 for r in rets) / len(rets)) ** 0.5
    sharpe = mu / sd * (12 ** 0.5) if sd else 0
    peak, mdd = eq[0], 0.0
    for v in eq:
        peak = max(peak, v); mdd = min(mdd, v / peak - 1)
    return cagr, sd * (12 ** 0.5) * 100, sharpe, mdd * 100


def report(name, months, rets):
    c, v, s, dd = metrics(months, rets)
    print(f"  {name:<24} CAGR {c:+6.1f}%  vol {v:5.1f}%  Sharpe {s:+5.2f}  "
          f"maxDD {dd:6.1f}%  ({months[0]}..{months[-1]}, {len(rets)}mo)")


spy_f = load("SPY", "20y", fade_equity)
gld_f = load("GLD", "20y", fade_equity)
btc_t = load("BTC-USD", "max", trend_equity)
eth_t = load("ETH-USD", "max", trend_equity)
spy_bh = load("SPY", "20y", bh_equity)

m_full, _ = combine([spy_f, gld_f, btc_t, eth_t])
print("== same window (crypto-length), monthly, net of costs ==")
report("SPY-fade alone", *combine([spy_f], m_full))
report("CORE (SPY+GLD fade)", *combine([spy_f, gld_f], m_full))
report("FULL (+crypto trend)", *combine([spy_f, gld_f, btc_t, eth_t], m_full))
report("buy-hold SPY", *combine([spy_bh], m_full))
print("\n== full 20y window (context; no crypto) ==")
report("CORE (SPY+GLD fade)", *combine([spy_f, gld_f]))
report("buy-hold SPY", *combine([spy_bh]))
