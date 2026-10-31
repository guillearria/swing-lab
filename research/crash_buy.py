"""[CRASH #1] — buy an S&P 500 stock the morning after it crashes? (owner, 2026-10-31)

Trigger: an S&P 500 member (point-in-time) closes >=20% down on >=3x its prior-20-session
mean volume. Trade: buy the next open, sell at the close of the 63rd session (21 = diagnostic).
Excess = stock - SPY over the same open->close dates - 0.40% round trip. One event per ticker
per 63 sessions. Month-clustered bootstrap, alpha 0.05/3. Bars: FINDINGS [CRASH #1].

Membership: fja05680/sp500 daily lists -> research/data/sp500_intervals.csv.
Prices: yfinance (current listings only — the survivorship hole; coverage is printed).

Run: python3 -m research.crash_buy   (first run downloads ~1,200 histories to a local cache)
"""
import csv
import os
import pickle
import random
import statistics as st
import sys
from collections import defaultdict

HERE = os.path.dirname(__file__)
INTERVALS = os.path.join(HERE, "data", "sp500_intervals.csv")
CACHE = os.path.join(HERE, "data", "_crash_ohlcv.pkl")

START = "2000-01-03"
DROP, VOL_X, VOL_N = -0.20, 3.0, 20
H, H_DIAG = 63, 21
COST, COST_STRESS = 0.004, 0.010
ALPHA = 0.05 / 3                      # Bonferroni over gates R1, M1, CRASH #1
SPLIT = "2013-01-01"
CRISES = (("2008-09-01", "2009-03-31"), ("2020-02-01", "2020-04-30"))
BAD_GAP = 0.15
MIN_N = 100
BOOT, SEED = 10_000, 7


def load_intervals():
    out = defaultdict(list)
    with open(INTERVALS) as f:
        for r in csv.DictReader(f):
            out[r["ticker"]].append((r["start"], r["end"] or "9999-12-31"))
    return out


def fetch(tickers):
    """{ticker: (dates, opens, closes, volumes)} — cached locally (gitignored)."""
    if os.path.exists(CACHE):
        with open(CACHE, "rb") as f:
            raw = pickle.load(f)
    else:
        import yfinance as yf
        raw = {}
        tks = sorted(set(tickers) | {"SPY"})
        for i in range(0, len(tks), 60):
            ysym = {t: t.replace(".", "-") for t in tks[i:i + 60]}
            df = yf.download(list(ysym.values()), start="1999-06-01", auto_adjust=True,
                             group_by="ticker", threads=True, progress=False)
            for t, y in ysym.items():
                try:
                    sub = df[y][["Open", "Close", "Volume"]].dropna()
                except Exception:
                    continue
                if len(sub):
                    raw[t] = sub
        with open(CACHE, "wb") as f:
            pickle.dump(raw, f)
    out = {}
    for t, df in raw.items():
        out[t] = ([d.date().isoformat() for d in df.index], df["Open"].tolist(),
                  df["Close"].tolist(), df["Volume"].tolist())
    return out


def member(ivs, d):
    return any(s <= d < e for s, e in ivs)


def events(ivs_by_tk, px):
    spy_d, spy_o, spy_c, _ = px["SPY"]
    spy_ix = {d: i for i, d in enumerate(spy_d)}
    ev, live, unaligned = [], [], 0
    for tk, ivs in ivs_by_tk.items():
        if tk not in px or tk == "SPY":
            continue
        d, o, c, v = px[tk]
        last = -10**9
        for i in range(VOL_N, len(d)):
            if d[i] < START or not member(ivs, d[i]) or c[i - 1] <= 0:
                continue
            avg = sum(v[i - VOL_N:i]) / VOL_N
            if avg <= 0 or c[i] / c[i - 1] - 1 > DROP or v[i] < VOL_X * avg:
                continue
            if i - last < H:
                continue
            last = i
            if i + H >= len(d):
                live.append((d[i], tk, c[i] / c[i - 1] - 1))
                continue
            row = {"date": d[i], "tk": tk, "drop": c[i] / c[i - 1] - 1,
                   "gap": o[i + 1] / c[i] - 1}
            ok = True
            for h in (H, H_DIAG):
                a, b = d[i + 1], d[i + h]
                if a not in spy_ix or b not in spy_ix or o[i + 1] <= 0:
                    ok = False
                    break
                s = c[i + h] / o[i + 1] - 1
                m = spy_c[spy_ix[b]] / spy_o[spy_ix[a]] - 1
                row[f"x{h}"] = s - m              # GROSS excess
            if ok:
                ev.append(row)
            else:
                unaligned += 1
    return ev, live, unaligned


def coverage(ivs_by_tk, px):
    """Share of member-sessions (SPY calendar, from START) with a Yahoo price."""
    cal = [d for d in px["SPY"][0] if d >= START]
    have = {tk: set(px[tk][0]) for tk in ivs_by_tk if tk in px}
    tot = hit = 0
    for tk, ivs in ivs_by_tk.items():
        for s, e in ivs:
            days = [d for d in cal if s <= d < e]
            tot += len(days)
            if tk in have:
                hit += sum(1 for d in days if d in have[tk])
    return hit / tot if tot else 0.0


def boot_p(rows, key, cost, side):
    """One-sided p: share of month-resampled means on the wrong side of 0."""
    by_m = defaultdict(list)
    for r in rows:
        by_m[r["date"][:7]].append(r[key] - cost)
    months = list(by_m.values())
    rng = random.Random(SEED)
    wrong = 0
    for _ in range(BOOT):
        tot = cnt = 0
        for _ in months:
            g = months[rng.randrange(len(months))]
            tot += sum(g)
            cnt += len(g)
        m = tot / cnt
        wrong += (m <= 0) if side > 0 else (m >= 0)
    return wrong / BOOT


def summ(rows, key, cost):
    x = [r[key] - cost for r in rows]
    if not x:
        return None
    return {"n": len(x), "mean": st.mean(x), "median": st.median(x),
            "beat": sum(v > 0 for v in x) / len(x), "sd": st.pstdev(x)}


def in_crisis(d):
    return any(a <= d <= b for a, b in CRISES)


def fmt(s):
    return (f"n={s['n']:4d}  mean {s['mean']:+.2%}  median {s['median']:+.2%}  "
            f"beat {s['beat']:.0%}") if s else "n=0"


def main():
    ivs = load_intervals()
    px = fetch(ivs)
    if "SPY" not in px:
        sys.exit("REFUSED: no SPY series")
    ev, live, unaligned = events(ivs, px)
    priced = sum(1 for t in ivs if t in px)
    print(f"[CRASH #1] {len(ev)} scored events (+{len(live)} live, {unaligned} unaligned) · "
          f"{priced}/{len(ivs)} member tickers priced · member-session coverage "
          f"{coverage(ivs, px):.0%}")

    k = f"x{H}"
    net, gross = summ(ev, k, COST), summ(ev, k, 0.0)
    p_up, p_dn = boot_p(ev, k, COST, +1), boot_p(ev, k, 0.0, -1)
    h1 = summ([r for r in ev if r["date"] < SPLIT], k, COST)
    h2 = summ([r for r in ev if r["date"] >= SPLIT], k, COST)
    g1 = summ([r for r in ev if r["date"] < SPLIT], k, 0.0)
    g2 = summ([r for r in ev if r["date"] >= SPLIT], k, 0.0)
    stress = summ(ev, k, COST_STRESS)
    calm = summ([r for r in ev if not in_crisis(r["date"])], k, COST)
    print(f"  63d NET   {fmt(net)}  p(>0) {p_up:.4f}")
    print(f"  63d GROSS {fmt(gross)}  p(<0) {p_dn:.4f}")
    print(f"  halves NET   2000-12 {fmt(h1)} | 2013+ {fmt(h2)}")
    print(f"  halves GROSS 2000-12 {fmt(g1)} | 2013+ {fmt(g2)}")
    print(f"  1.0% cost {fmt(stress)} · crises removed {fmt(calm)}")
    mde = 2.8 * net["sd"] / len(ev) ** 0.5 if net else float("nan")
    print(f"  SD {net['sd']:.1%} · approx 80%-power detectable mean ±{mde:.1%} (naive, unclustered)")

    bad = [r for r in ev if r["gap"] >= BAD_GAP]
    print(f"  bad-print check: {len(bad)} events open ≥{BAD_GAP:.0%} above trigger close · "
          f"NET mean excluding them {summ([r for r in ev if r['gap'] < BAD_GAP], k, COST)['mean']:+.2%}")
    print(f"  21d NET (diagnostic) {fmt(summ(ev, f'x{H_DIAG}', COST))}")

    if len(ev) < MIN_N:
        verdict = "NULL-UNDERPOWERED"
    elif (p_up <= ALPHA and net["median"] > 0 and net["beat"] > 0.5 and h1["mean"] > 0
          and h2["mean"] > 0 and stress["mean"] > 0 and calm["mean"] > 0):
        verdict = "PASS (PROVISIONAL — survivorship hole)"
    elif (p_dn <= ALPHA and gross["median"] < 0 and gross["beat"] < 0.5 and g1["mean"] < 0
          and g2["mean"] < 0):
        verdict = "CONTINUATION"
    else:
        verdict = "NULL"
    print(f"  VERDICT: {verdict}")
    for d, tk, r in sorted(live)[-8:]:
        print(f"  live trigger (unscorable): {d} {tk} {r:+.1%}")


if __name__ == "__main__":
    main()
