"""ARC 5 #3 evidence (NULL) — catalyst contagion in the psychedelics complex.

One-off SANITY SCREEN, kept for reproducibility (not a wired module, not in the engine).
Verdict in FINDINGS [ARC 5 #3]: peer-contagion is NULL (sympathy pop fades by +3d); the only
consistent sign is name-level post-spike REVERSION, but n is tiny + SURVIVOR-biased (MNMD
returns no data — survivorship made literal), so not tradeable. Run: python3 -m research.contagion
"""
import numpy as np, yfinance as yf, pandas as pd

BASKET = ["CMPS", "ATAI", "MNMD", "GHRS"]
BENCH = "XBI"
EVENT_RET = 0.10      # name daily ret >= +10%
IDIO = 0.07           # name ret - basket-mean ret >= +7pp (idiosyncratic, not a sector day)

px = yf.download(BASKET + [BENCH], period="3y", auto_adjust=True, progress=False)["Close"]
px = px.dropna(how="all")
ret = px.pct_change()
basket_ret = ret[BASKET]
basket_mean = basket_ret.mean(axis=1)

rows = []
for name in BASKET:
    r = basket_ret[name]
    idio = r - basket_mean
    events = r.index[(r >= EVENT_RET) & (idio >= IDIO)]
    peers = [p for p in BASKET if p != name]
    for d in events:
        loc = ret.index.get_loc(d)
        for h in (1, 3, 5):
            if loc + h >= len(ret):
                continue
            peer_fwd = (px[peers].iloc[loc + h] / px[peers].iloc[loc] - 1).mean()
            bench_fwd = px[BENCH].iloc[loc + h] / px[BENCH].iloc[loc] - 1
            rows.append({"name": name, "date": d.date(), "h": h,
                         "peer_excess": peer_fwd - bench_fwd,
                         "name_fwd_excess": (px[name].iloc[loc + h] / px[name].iloc[loc] - 1) - bench_fwd})

df = pd.DataFrame(rows)
print(f"window: {px.index[0].date()} -> {px.index[-1].date()}  basket={BASKET} bench={BENCH}")
print(f"events (idiosyncratic +10% single-name up-days): {df[df.h == 1].shape[0]}\n")
print("PEER reaction after a name's catalyst (excess vs XBI), entry=event-day close:")
for h in (1, 3, 5):
    s = df[df.h == h]["peer_excess"]
    print(f"  +{h}d  n={len(s):2d}  mean {s.mean()*100:+6.2f}%  median {s.median()*100:+6.2f}%  "
          f"hit {(s>0).mean()*100:4.0f}%")
print("\n(ref) the CATALYST NAME itself, fwd excess vs XBI after its +10% day (drift/reversion):")
for h in (1, 3, 5):
    s = df[df.h == h]["name_fwd_excess"]
    print(f"  +{h}d  n={len(s):2d}  mean {s.mean()*100:+6.2f}%  median {s.median()*100:+6.2f}%  "
          f"hit {(s>0).mean()*100:4.0f}%")
