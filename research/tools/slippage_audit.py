"""Reproduce the 2026-08-03 execution-slippage numbers behind config.ENTRY_BAND_MAX / ORDER_EXPIRY_D.

The FINDINGS entry claims three things; this prints all three from the live ledger + price feed:
  1. how far a taken mover moves between the reference close the alert quoted and the human
     acting (at the open, and by the close),
  2. what a limit at ref x (1+band) would have filled, per band,
  3. how many sessions a 1% limit takes to fill (the expiry calibration).

Numbers drift as the ledger grows — that is the point of a reproduce script rather than a frozen
table. The dated FINDINGS entry keeps the then-true figures.

    python3 -m research.tools.slippage_audit
"""
import csv
import statistics as st

from research import config, prices

LEDGER = "research/movers_ledger.csv"
BANDS = (0.0, 0.01, 0.015, 0.02, 0.03)


def load():
    """(row, prior_close_bar_index) for every TAKE we can price. Skips un-priceable rows."""
    out = []
    for r in csv.DictReader(open(LEDGER)):
        if r["action"] != "take":
            continue
        bars = prices.daily_history(r["ticker"], "6mo")
        dates = [b["date"][:10] for b in bars]
        day = r["logged_at"][:10]
        if day not in dates or dates.index(day) == 0:
            continue                       # no reference bar available
        out.append((r, bars, dates.index(day)))
    return out


def main():
    data = load()
    print(f"taken movers priced: {len(data)}\n")

    gaps = [abs(b[i]["open"] / b[i - 1]["close"] - 1) * 100 for _, b, i in data]
    closes = [abs(b[i]["close"] / b[i - 1]["close"] - 1) * 100 for _, b, i in data]
    print("1. how far the quoted reference has moved by the time you act")
    print(f"   median |gap at the open|  {st.median(gaps):.2f}%")
    print(f"   median |move by the close| {st.median(closes):.2f}%   <- waiting costs MORE\n")

    print("2. fill rate on session 1, and the entry advantage over a blind close-chase")
    for band in BANDS:
        filled, adv = 0, []
        for r, b, i in data:
            lg = r["direction_hint"] == "long"
            sgn = 1 if lg else -1
            lim = b[i - 1]["close"] * (1 + sgn * band)
            if (b[i]["low"] <= lim) if lg else (b[i]["high"] >= lim):
                filled += 1
                fill = min(b[i]["open"], lim) if lg else max(b[i]["open"], lim)
                adv.append((b[i]["close"] / fill - 1) * 100 * sgn)
        print(f"   band {band * 100:4.1f}%: {filled:2d}/{len(data)} = {filled / len(data) * 100:5.1f}% "
              f"· median entry {st.median(adv):+.2f}% better")
    print()

    print(f"3. sessions to fill at the live band (config.ENTRY_BAND_MAX = "
          f"{config.ENTRY_BAND_MAX * 100:g}%), expiry = {config.ORDER_EXPIRY_D}")
    hit = {}
    for r, b, i in data:
        lg = r["direction_hint"] == "long"
        lim = b[i - 1]["close"] * (1 + (1 if lg else -1) * config.ENTRY_BAND_MAX)
        when = None
        for k in range(i, min(i + 11, len(b))):
            if (b[k]["low"] <= lim) if lg else (b[k]["high"] >= lim):
                when = k - i + 1
                break
        hit.setdefault(when, []).append(r["ticker"])
    cum = 0
    for k in sorted(x for x in hit if x is not None):
        cum += len(hit[k])
        print(f"   by session {k:2d}: {cum:2d}/{len(data)} = {cum / len(data) * 100:3.0f}%"
              f"   (+{','.join(hit[k])})")
    never = hit.get(None, [])
    print(f"   never within 10: {len(never)} -> {','.join(never) or '-'}")


if __name__ == "__main__":
    main()
