"""Arc 2, probe #1: the S&P 500 INDEX-DELETION bounce (a forced-flow inefficiency).

When a stock is removed from the S&P 500, index funds are FORCED to dump ~all of it
around the effective date — a large non-economic sell into one name. Hypothesis: that
forced selling overshoots, so deleted names REBOUND vs the market over the next 1-6
months. This is an edge a small operator can reach precisely because it's born of index
mechanics, not fundamentals.

Data: real historical removals 1996-2026 derived from fja05680/sp500 membership history
(research/data/sp500_deletions.csv) — INCLUDES names that later died, so the LIST has no
survivorship bias. Prices via yfinance. The residual bias we CAN'T fully kill for free:
delisted/acquired tickers have no post-deletion data, so they drop out of the priceable
set — we REPORT that censored count loudly (it biases the bounce UPWARD). If the edge looks
real, the paid trigger is point-in-time delisting-inclusive prices (CRSP/Norgate).

Entry: first close on/after the deletion effective date. Horizons 21/63/126 trading days
(~1/3/6 months). Metric: EXCESS return vs SPY over the identical window.

Pre-registered PASS: positive MEAN and MEDIAN excess vs SPY at a MAJORITY of horizons,
%-beating-SPY > 50%, consistent across the 2010s and 2020s — AND large enough that the
censored deaths can't plausibly be the whole story. Honest prior: the deletion effect has
weakened as it got known; a null/small result is likely. FAIL = flat/negative excess.

Run: python3 -m research.index_deletion
"""
import csv
import os
import statistics as st

START = "2010-01-01"          # data coverage for delisted tickers is poor before ~2010
HORIZONS = (21, 63, 126)
DEL_PATH = os.path.join(os.path.dirname(__file__), "data", "sp500_deletions.csv")


def load_deletions():
    with open(DEL_PATH) as f:
        return [(r["date"], r["ticker"]) for r in csv.DictReader(f) if r["date"] >= START]


def fetch_closes(tickers):
    """{ticker: [(date, close)...]} via one bulk yfinance download (threaded)."""
    import yfinance as yf
    out = {}
    uniq = sorted(set(tickers) | {"SPY"})
    for i in range(0, len(uniq), 80):                       # chunk to stay robust
        chunk = uniq[i:i + 80]
        df = yf.download(chunk, period="max", auto_adjust=True, group_by="ticker",
                         threads=True, progress=False)
        for tk in chunk:
            try:
                s = df[tk]["Close"].dropna() if len(chunk) > 1 else df["Close"].dropna()
            except Exception:
                continue
            rows = [(ts.date().isoformat(), float(v)) for ts, v in s.items()]
            if rows:
                out[tk] = rows
    return out


def main():
    dels = load_deletions()
    closes = fetch_closes([t for _, t in dels])
    spy = {d: c for d, c in closes.get("SPY", [])}

    excess = {h: [] for h in HORIZONS}          # excess vs SPY, by horizon
    eras = {h: {"2010s": [], "2020s": []} for h in HORIZONS}
    no_data = died_within = priced_events = 0

    for ddate, tk in dels:
        s = closes.get(tk)
        if not s:
            no_data += 1
            continue
        i0 = next((i for i, (d, _) in enumerate(s) if d >= ddate), None)
        if i0 is None:
            no_data += 1
            continue
        priced_events += 1
        reached_max = False
        for h in HORIZONS:
            j = i0 + h
            if j >= len(s):
                continue
            d0, c0 = s[i0]; dj, cj = s[j]
            if d0 not in spy or dj not in spy:
                continue
            ex = (cj / c0 - 1) - (spy[dj] / spy[d0] - 1)
            excess[h].append(ex)
            eras[h]["2020s" if d0 >= "2020" else "2010s"].append(ex)
            reached_max = h == HORIZONS[-1]
        if not reached_max and i0 + HORIZONS[-1] >= len(s):
            died_within += 1                    # priced at entry but ran out within ~6mo

    print(f"S&P 500 deletion bounce | {len(dels)} removals since {START[:4]} | "
          f"priceable {priced_events}, no-data(delisted/acquired) {no_data}, "
          f"died-within-6mo {died_within}")
    print(f"  CENSORED = {no_data}/{len(dels)} ({no_data/len(dels)*100:.0f}%) have no post-deletion "
          f"data -> excluded -> biases the bounce UPWARD (the honest gap).\n")
    print(f"  {'horizon':9s} {'n':>4} {'mean_excess':>12} {'median':>8} {'%beat_SPY':>10}   by-era mean (2010s|2020s)")
    for h in HORIZONS:
        xs = excess[h]
        if not xs:
            continue
        beat = sum(1 for x in xs if x > 0) / len(xs) * 100
        e10 = st.mean(eras[h]["2010s"]) * 100 if eras[h]["2010s"] else float("nan")
        e20 = st.mean(eras[h]["2020s"]) * 100 if eras[h]["2020s"] else float("nan")
        print(f"  {h:>3}d{'':5} {len(xs):>4} {st.mean(xs)*100:>+11.2f}% {st.median(xs)*100:>+7.2f}% "
              f"{beat:>9.0f}%   {e10:>+6.2f}% | {e20:>+6.2f}%")


if __name__ == "__main__":
    main()
