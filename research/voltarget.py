"""LOOP iteration #1 (auto-generated idea) — does VOL-TARGETING beat buy-hold SPY?

Tests the 'risk management / position sizing is the edge' lever (the Market-Wizards
answer we flagged but never tested). Hold SPY, but size the position so the portfolio
targets a constant volatility: shrink in turbulent times, lever up (modestly) in calm
times. Pre-registered in FINDINGS Arc 4 #2 — knobs fixed, no tuning.

  python3 -m research.voltarget
"""
import logging
import sys

from research import prices

TARGET = 0.15      # target annualized vol (15%, standard)
LOOK = 21          # trailing trading days for realized vol
CAP = 2.0          # max leverage
BORROW = 0.05      # annual financing cost on the levered portion
COST = 0.001       # per-unit-turnover rebalance cost
log = logging.getLogger(__name__)


def _metrics(rets: list[float], ppy: int = 252) -> dict:
    n = len(rets)
    eq, curve = 1.0, [1.0]
    for r in rets:
        eq *= (1 + r); curve.append(eq)
    mean = sum(rets) / n
    sd = (sum((x - mean) ** 2 for x in rets) / (n - 1)) ** 0.5
    peak, mdd = -1.0, 0.0
    for v in curve:
        peak = max(peak, v); mdd = min(mdd, v / peak - 1)
    return {"cagr": eq ** (ppy / n) - 1, "sharpe": (mean / sd) * (ppy ** 0.5) if sd else 0.0,
            "mdd": mdd, "mult": eq}


_CACHE = None


def _spy():
    global _CACHE
    if _CACHE is None:
        bars = prices.daily_history("SPY", "max")
        rets = [bars[i]["close"] / bars[i - 1]["close"] - 1 for i in range(1, len(bars))]
        dates = [bars[i]["date"] for i in range(1, len(bars))]
        _CACHE = (rets, dates)
    return _CACHE


def backtest(target=TARGET, look=LOOK, cap=CAP, borrow=BORROW):
    rets, dates = _spy()
    strat, bh, ds = [], [], []
    exposure = prev = 1.0
    for i in range(look, len(rets)):
        if dates[i][:7] != dates[i - 1][:7]:                       # first trading day of a month
            window = rets[i - look:i]
            m = sum(window) / look
            vol = (sum((x - m) ** 2 for x in window) / (look - 1)) ** 0.5 * (252 ** 0.5)
            exposure = min(cap, max(0.0, target / vol)) if vol > 0 else cap
        turn = abs(exposure - prev); prev = exposure
        strat.append(exposure * rets[i] - (borrow / 252) * max(exposure - 1, 0) - COST * turn)
        bh.append(rets[i]); ds.append(dates[i])
    return ds, strat, bh


def main():
    ds, strat, bh = backtest()
    start, end = ds[0], ds[-1]
    s, b = _metrics(strat), _metrics(bh)
    print(f"\n=== ARC 4 #2 VOL-TARGETING SPY ({start}..{end}, target {TARGET*100:.0f}% vol, "
          f"≤{CAP:.0f}x, borrow {BORROW*100:.0f}%) ===")
    print(f"  vol-target: CAGR {s['cagr']*100:+5.1f}%  Sharpe {s['sharpe']:.2f}  "
          f"maxDD {s['mdd']*100:4.0f}%  x{s['mult']:.1f}")
    print(f"  buy-hold  : CAGR {b['cagr']*100:+5.1f}%  Sharpe {b['sharpe']:.2f}  "
          f"maxDD {b['mdd']*100:4.0f}%  x{b['mult']:.1f}")
    bar = s["cagr"] > b["cagr"] and s["sharpe"] > b["sharpe"]
    print(f"  pre-registered bar (beat SPY on CAGR AND Sharpe, net): {'PASS' if bar else 'FAIL'}")


def confirm():
    """LOOP iteration #2 — OOS / robustness confirm of the vol-targeting lead."""
    from collections import defaultdict
    ds, strat, bh = backtest()
    spy = _metrics(bh)

    print("\n=== ARC 4 #2 CONFIRM — vol-targeting OOS / robustness ===")
    dec = defaultdict(lambda: [[], []])
    for d, rs, rb in zip(ds, strat, bh):
        dec[d[:3] + "0s"][0].append(rs); dec[d[:3] + "0s"][1].append(rb)
    print("  per-decade Sharpe (vol-target vs SPY):")
    dwin = dtot = 0
    for k in sorted(dec):
        rs, rb = dec[k]
        if len(rs) < 30:
            continue
        ss, sb = _metrics(rs)["sharpe"], _metrics(rb)["sharpe"]
        dwin += ss > sb; dtot += 1
        print(f"    {k}: {ss:.2f} vs {sb:.2f}   ({'win' if ss > sb else 'lose'})")

    print(f"  borrow sensitivity (full-sample vs SPY Sharpe {spy['sharpe']:.2f} / "
          f"CAGR {spy['cagr']*100:+.1f}%):")
    borrow_ok = False
    for br in (0.03, 0.05, 0.07, 0.09):
        m = _metrics(backtest(borrow=br)[1])
        ok = m["sharpe"] > spy["sharpe"]
        if abs(br - 0.07) < 1e-9:
            borrow_ok = ok
        print(f"    borrow {br*100:.0f}%: Sharpe {m['sharpe']:.2f}  CAGR {m['cagr']*100:+.1f}%  "
              f"({'beats' if ok else 'loses'})")

    print("  lookback sensitivity (no-cliff check):")
    look_ok = True
    for lk in (21, 42, 63):
        m = _metrics(backtest(look=lk)[1])
        ok = m["sharpe"] >= spy["sharpe"]
        look_ok = look_ok and ok
        print(f"    look {lk}d: Sharpe {m['sharpe']:.2f}  ({'>=' if ok else '<'} SPY)")

    passed = dwin > dtot / 2 and borrow_ok and look_ok
    print(f"\n  CONFIRM bar (decade-majority Sharpe AND beats at 7% borrow AND no lookback cliff): "
          f"{'CONFIRMED' if passed else 'NOT CONFIRMED'}")
    print(f"    decades won {dwin}/{dtot} | 7%-borrow beats: {borrow_ok} | no-cliff: {look_ok}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(confirm() if len(sys.argv) > 1 and sys.argv[1] == "confirm" else main())
