"""Arc 2, probe #2: the post-IPO LOCKUP-EXPIRY effect (a forced-flow inefficiency).

After an IPO, insiders/early backers are barred from selling for a lockup (~180 days).
At expiry a wall of shares becomes sellable -> anticipated/forced selling -> the classic
"lockup expiration effect" (documented abnormal NEGATIVE returns ~−1 to −3% around expiry,
even though it's anticipated). Tradeable angle (if real): short into expiry, or buy the
post-expiry overshoot once the forced selling exhausts.

Data: operating-company IPOs 2014-2023 from the NASDAQ IPO calendar (research/data/ipos.csv),
SPACs/units filtered out. The list records the ticker AT IPO -> includes names that later
DIED (no list-survivorship); delisted names just drop from the priceable set (reported).
Prices via yfinance. KEY APPROXIMATION: real lockup dates live in each S-1 (90/180/365/
staggered); we use the MODAL 180 calendar days as a proxy -> wrong-lockup IPOs just dilute
the signal toward zero, so a clear result despite the proxy is real; a null may be blurred.
Paid/harder-data trigger (if promising): exact lockup dates parsed from S-1 filings.

Windows (trading days vs expiry index E ≈ IPO+180d): into=[E−10,E], event=[E−3,E+7] (robust
to proxy slop), post=[E+7,E+37]. Metric = excess return vs SPY over the identical dates.

Pre-registered PASS (effect exists): event-window excess NEGATIVE on mean AND median,
>50% negative, consistent across eras. Then tradeable IF post-window is positive (the
overshoot rebound). Honest prior: the effect has likely decayed (anticipated, staggered
lockups now common) — null is plausible. FAIL = event excess ~flat/positive.

Run: python3 -m research.lockup
"""
import csv
import datetime as dt
import json
import os
import statistics as st
import sys
import time

from research import prices

CACHE = os.path.join(os.path.dirname(__file__), "data", "_lockup_closes.json")  # gitignored

IPO_PATH = os.path.join(os.path.dirname(__file__), "data", "ipos.csv")
LOCKUP_DAYS = 180
WIN = {"into": (-10, 0), "event": (-3, 7), "post": (7, 37)}


def load_ipos():
    with open(IPO_PATH) as f:
        return [(r["date"], r["ticker"]) for r in csv.DictReader(f)]


def load_spy():
    """SPY benchmark, fetched FIRST and with retries so a throttled bulk never loses it."""
    for _ in range(4):
        spy = {b["date"]: b["close"] for b in prices.daily_history("SPY", "max")}
        if spy:
            return spy
        time.sleep(20)
    return {}


def fetch_closes(tickers):
    """{ticker: [(date,close)...]}. Disk-cached (fetch Yahoo ONCE); gentle (no threads, paced)."""
    if os.path.exists(CACHE):
        with open(CACHE) as f:
            return {k: [tuple(x) for x in v] for k, v in json.load(f).items()}
    import yfinance as yf
    out, uniq = {}, sorted(set(tickers))
    for i in range(0, len(uniq), 60):
        chunk = uniq[i:i + 60]
        try:
            df = yf.download(chunk, period="max", auto_adjust=True, group_by="ticker",
                             threads=False, progress=False)
        except Exception:
            time.sleep(30); continue
        for tk in chunk:
            try:
                s = df[tk]["Close"].dropna() if len(chunk) > 1 else df["Close"].dropna()
            except Exception:
                continue
            rows = [(ts.date().isoformat(), float(v)) for ts, v in s.items()]
            if rows:
                out[tk] = rows
        time.sleep(1.5)
    if len(out) > 100:                      # only cache a genuinely successful pull
        with open(CACHE, "w") as f:
            json.dump(out, f)
    return out


def excess(s, spy, a, b):
    da, ca = s[a]; db, cb = s[b]
    if da not in spy or db not in spy:
        return None
    return (cb / ca - 1) - (spy[db] / spy[da] - 1)


def main():
    ipos = load_ipos()
    spy = load_spy()                        # FIRST — secure the benchmark before the heavy bulk
    if not spy:
        print("ERROR: SPY benchmark failed (rate-limited?)"); sys.exit(1)
    closes = fetch_closes([t for _, t in ipos])

    res = {w: [] for w in WIN}
    eras = {w: {"2010s": [], "2020s": []} for w in WIN}
    priced = censored = 0

    for ipo_date, tk in ipos:
        s = closes.get(tk)
        if not s or len(s) < 80:
            censored += 1
            continue
        target = (dt.date.fromisoformat(ipo_date) + dt.timedelta(days=LOCKUP_DAYS)).isoformat()
        e = next((i for i, (d, _) in enumerate(s) if d >= target), None)
        if e is None or e + WIN["post"][1] >= len(s) or e + WIN["into"][0] < 0:
            censored += 1
            continue
        priced += 1
        for w, (a, b) in WIN.items():
            x = excess(s, spy, e + a, e + b)
            if x is not None:
                res[w].append(x)
                eras[w]["2020s" if s[e][0] >= "2020" else "2010s"].append(x)

    print(f"Post-IPO lockup (~{LOCKUP_DAYS}d) | {len(ipos)} IPOs 2014-23 | "
          f"priceable-through-window {priced}, censored(delisted/short) {censored} "
          f"({censored / len(ipos) * 100:.0f}%)\n")
    print(f"  {'window':16s} {'n':>4} {'mean':>8} {'median':>8} {'%neg':>6}   by-era mean (2010s|2020s)")
    for w, (a, b) in WIN.items():
        xs = res[w]
        if not xs:
            continue
        neg = sum(1 for x in xs if x < 0) / len(xs) * 100
        e10 = st.mean(eras[w]["2010s"]) * 100 if eras[w]["2010s"] else float("nan")
        e20 = st.mean(eras[w]["2020s"]) * 100 if eras[w]["2020s"] else float("nan")
        print(f"  {w:8s}[{a:+d},{b:+d}] {len(xs):>4} {st.mean(xs) * 100:>+7.2f}% "
              f"{st.median(xs) * 100:>+7.2f}% {neg:>5.0f}%   {e10:>+6.2f}% | {e20:>+6.2f}%")
    print("\n  (event NEG => forced-selling dip; post POS => overshoot rebound to buy.)")


if __name__ == "__main__":
    main()
