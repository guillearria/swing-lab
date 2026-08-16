"""Experiment #1: is "disaster = generational buy" real — and only WITH a dynamic exit?

Thesis (user): buying a wrecked asset is a generational entry. His upgrade: you must
be DYNAMIC — Japan 1989 / Argentina stay underwater for decades if you just hold. So
we test entry AND exit together, with a SURVIVORSHIP stress (the graveyard).

Disaster entry (mechanical, NO date-picking = no hindsight): first day an asset closes
>=20% below its trailing 1-year high. De-overlapped — re-arms only after it climbs back
above the -20% line. From each entry, over a 1/2/3-year window, compare:
  A STATIC  : hold through anything (the "stuck in Japan" approach)
  B DYNAMIC : long while close>200d MA else cash (decided on prior close; switch costs)
and per-asset BUY-HOLD over the whole span as context. Report end-multiple and the
worst drawdown-AFTER-entry (the "where it gets worse" pain you must stomach).

SURVIVORSHIP RE-TEST (pre-registered): re-run the SAME engine on a GRAVEYARD of dead/
stuck markets, in USD (currency collapse IS part of the disaster; local indices hide it).
  PASS "disaster-buy is real, not hindsight" = graveyard STATIC 3y stays net-positive
    across MOST corpses.
  PASS "dynamic exit earns its keep" = in the graveyard, DYNAMIC beats STATIC on RETURN
    (not just drawdown) — the REVERSE of the survivors — because here "stays down" is the
    norm and getting out matters.
  If graveyard static is flat/negative AND dynamic doesn't help -> disaster-buy was
    largely survivorship; be far more skeptical.
Known blind spot (stated, not hidden): true go-to-zero (Russia '22) is only partly visible
because free data stops at the trading HALT, not at zero. The graveyard mostly stresses
"stayed stuck for a decade+", which is the realistic survivorship threat.

Run: python3 -m research.disaster
"""
from research import config, prices

MA, COST = config.TREND_MA, config.COST_ROUNDTRIP
DD, YR = -0.20, 252
HORIZONS = (1, 2, 3)

SURVIVORS = [("SPY", "US stocks"), ("QQQ", "US tech"), ("GLD", "gold"),
             ("TLT", "long bonds"), ("BTC-USD", "bitcoin"), ("^N225", "Nikkei (yen)")]

# Markets that DIED or STAYED DEAD, in USD. Mostly "stuck a decade+" with no US/BTC-style
# bull; RSX (Russia) is the lone near-zero corpse (data ends at the '22 halt -> understates).
GRAVEYARD = [("EWJ", "Japan USD"), ("FXI", "China USD"), ("EWI", "Italy USD"),
             ("GREK", "Greece USD"), ("ARGT", "Argentina USD"), ("TUR", "Turkey USD"),
             ("EWZ", "Brazil USD"), ("RSX", "Russia USD halted'22")]


def disaster_entries(closes):
    """Indices where close first crosses >=20% below the trailing 1y high (de-overlapped)."""
    out, armed = [], True
    for i in range(YR, len(closes)):
        dd = closes[i] / max(closes[i - YR:i + 1]) - 1
        if armed and dd <= DD:
            out.append(i); armed = False
        elif not armed and dd > DD:
            armed = True
    return out


def _maxdd(seg):
    peak, mdd = seg[0], 0.0
    for x in seg:
        peak = max(peak, x); mdd = min(mdd, x / peak - 1)
    return mdd * 100


def static_path(closes, e, H):
    seg = closes[e:min(e + H, len(closes) - 1) + 1]
    return seg[-1] / seg[0] * (1 - COST), _maxdd(seg)


def dynamic_path(closes, e, H):
    """Long while close>200d MA (prior-close decision) else cash; pay cost on each switch."""
    end = min(e + H, len(closes) - 1)
    v, inpos, path = 1.0, False, [1.0]
    for i in range(e + 1, end + 1):
        want = closes[i - 1] > sum(closes[i - MA:i]) / MA
        v *= 1 + (closes[i] / closes[i - 1] - 1 if inpos else 0.0)
        if want != inpos:
            v *= 1 - COST
        inpos = want
        path.append(v)
    return v, _maxdd(path)


def avg(xs):
    return sum(xs) / len(xs) if xs else 0.0


def run(assets):
    for sym, label in assets:
        bars = prices.daily_history(sym, "max")
        closes, dates = [b["close"] for b in bars], [b["date"] for b in bars]
        if len(closes) < YR + 300:
            print(f"\n==== {sym} {label}: too little/no data ({len(closes)}d) ===="); continue
        ents = disaster_entries(closes)
        bh, bhdd = closes[-1] / closes[YR], _maxdd(closes[YR:])
        yrs = sorted({dates[e][:4] for e in ents})
        print(f"\n==== {sym}  {label}  ({dates[0][:4]}-{dates[-1][:4]})  "
              f"buy-hold x{bh:.1f} (worst {bhdd:.0f}%) ====")
        print(f"   {len(ents)} disaster entries: {', '.join(yrs)}")
        for n in HORIZONS:
            H = n * YR
            full = [e for e in ents if e + H <= len(closes) - 1]
            if not full:
                print(f"   {n}y  (no completed episodes yet)"); continue
            sm = [static_path(closes, e, H) for e in full]
            dm = [dynamic_path(closes, e, H) for e in full]
            spos = sum(1 for m, _ in sm if m > 1)
            dpos = sum(1 for m, _ in dm if m > 1)
            print(f"   {n}y  STATIC  x{avg([m for m, _ in sm]):.2f} worst{avg([d for _, d in sm]):+5.0f}% "
                  f"({spos}/{len(full)} up)   |   DYNAMIC x{avg([m for m, _ in dm]):.2f} "
                  f"worst{avg([d for _, d in dm]):+5.0f}% ({dpos}/{len(full)} up)")


if __name__ == "__main__":
    print("################  SURVIVORS (the markets we remember)  ################")
    run(SURVIVORS)
    print("\n################  GRAVEYARD (the markets we'd rather forget)  ################")
    run(GRAVEYARD)
