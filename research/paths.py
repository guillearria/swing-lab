"""Settled-bet PATH diagnostic — what does the calendar exit cost? DESCRIPTIVE, never a verdict.

Walks each SETTLED bet's daily excess-vs-benchmark path and reports where it peaked against
where the pre-registered horizon scored it: peak day, max favorable excursion (MFE), final,
give-back (MFE − final), plus a driftless-noise reference E[max] ≈ σ·√(2T/π) — because the
maximum of ANY noisy path is positive in expectation, a raw peak always whispers "money left
on the table", including on pure noise. The reference is a MAGNITUDE, deliberately not a test
statistic: printing a p-value here daily would be the repeated look [ARC 5 #14] forbids.

Contract [PATHS #1]:
- SETTLED rows only — walking open bets is watching positions mid-flight, the itch to
  intervene the fixed-horizon design exists to remove.
- Position-indexed walk, matching bets._score exactly (which never date-aligns the two legs);
  each row self-checks final vs the ledger's excess_pct and entry vs entry_date, printing a
  named caveat on drift (re-fetched adjusted closes can differ from at-settle bars).
- No bar, no threshold, no action. An exit-rule change requires its OWN fresh
  pre-registration citing these numbers. Never wired into daily.sh or the digest.
- Read-only: bare invocation = show; unknown command = error; NOTHING writes.

  python3 -m research.paths            # the report (network: ~2 fetches per settled bet)
"""
import logging
import math
import statistics
import sys

from research import bets, prices

log = logging.getLogger(__name__)


def walk(stock: list[dict], bench: list[dict], direction: str, horizon: int) -> list | None:
    """Daily excess path ex_t = sgn·((S_t/S_0−1) − (B_t/B_0−1)), t = 0..horizon−1. PURE.

    Position-indexed like bets._score — index t, not date — so ex[-1] reproduces the settled
    number. None when either leg is short of the horizon (feed flake / dropped bars)."""
    if len(stock) < horizon or len(bench) < horizon:
        return None
    sgn = 1 if direction == "long" else -1
    return [sgn * ((stock[t]["close"] / stock[0]["close"] - 1)
                   - (bench[t]["close"] / bench[0]["close"] - 1))
            for t in range(horizon)]


def path_stats(ex: list) -> dict:
    """Peak day (argmax), MFE, final, give-back. PURE."""
    peak_t = max(range(len(ex)), key=lambda t: ex[t])
    mfe = ex[peak_t]
    return {"peak_t": peak_t, "mfe": mfe, "final": ex[-1], "give_back": mfe - ex[-1]}


def noise_ref(ex: list) -> float | None:
    """E[max] of a driftless random walk with this path's increment vol: σ·√(2T/π). PURE.

    The honesty device: a raw MFE flatters dynamic exits by construction (maxima of noise are
    positive). This is what chance alone would peak at — a reference magnitude, NOT a test.
    None below 3 points (stdev needs ≥2 increments)."""
    if len(ex) < 3:
        return None
    inc = [ex[t] - ex[t - 1] for t in range(1, len(ex))]
    return statistics.stdev(inc) * math.sqrt(2 * len(ex) / math.pi)


def report(rows: list[dict]) -> int:
    """Fetch + walk every settled row (long AND short — the path is a property of the bet,
    not the verdict population). Per-row isolation: a bad row is named and skipped, never
    fatal (the bets.settle lesson). Returns count reported."""
    closed = [r for r in rows if r["status"] == "closed"]
    print("\nSETTLED-BET PATH DIAGNOSTIC — DESCRIPTIVE, never an edge verdict [PATHS #1]")
    print("  (peak vs final excess per bet; noise = a driftless walk's expected peak — the")
    print("   reference a raw MFE must beat before it means anything but volatility)")
    if not closed:
        print("  no settled rows yet")
        return 0
    stats, shown = [], 0
    for r in closed:
        h, day = int(r["horizon_d"]), r["logged_at"][:10]
        try:
            ex = walk(prices.bars_after(r["ticker"], day, h + 5),
                      prices.bars_after(r["benchmark"], day, h + 5), r["direction"], h)
        except Exception as e:                    # one poisoned row must not kill the report
            print(f"  CAVEAT {r['ticker']}: walk failed ({e}) — skipped")
            continue
        if ex is None:
            print(f"  CAVEAT {r['ticker']}: short history after {day} — skipped "
                  f"(feed flake or dropped bars)")
            continue
        st, ref = path_stats(ex), noise_ref(ex)
        stock0 = prices.bars_after(r["ticker"], day, 1)
        if stock0 and r.get("entry_date") and stock0[0]["date"] != r["entry_date"]:
            print(f"  CAVEAT {r['ticker']}: first bar {stock0[0]['date']} != entry_date "
                  f"{r['entry_date']} — the dropped-bar offset [PATHS #1]; row still shown")
        drift = abs(st["final"] * 100 - float(r["excess_pct"]))
        dnote = f"  DRIFT {drift:.2f}pp vs ledger" if drift > 0.01 else ""
        print(f"  {r['ticker']:>5} {r['direction']:>5} {h:>3}d: peak day {st['peak_t']:>2} "
              f"of {h} at {st['mfe'] * 100:+6.2f}% → final {st['final'] * 100:+6.2f}% "
              f"(gave back {st['give_back'] * 100:5.2f}pp) | noise E[max] "
              f"{'n/a' if ref is None else f'{ref * 100:5.2f}%'}{dnote}")
        stats.append((st, ref))
        shown += 1
    if stats:
        med = lambda k: statistics.median(s[k] for s, _ in stats)
        refs = [x for _, x in stats if x is not None]
        print(f"  ── medians over {shown} settled: peak day {med('peak_t'):.0f} · MFE "
              f"{med('mfe') * 100:+.2f}% · final {med('final') * 100:+.2f}% · give-back "
              f"{med('give_back') * 100:.2f}pp · noise E[max] "
              f"{'n/a' if not refs else f'{statistics.median(refs) * 100:.2f}%'}")
        print("  DESCRIPTIVE ONLY: a driftless walk with these σ's peaks near the noise "
              "column by chance alone. No bar, no action — an exit-rule change needs its own "
              "fresh pre-registration citing these numbers [PATHS #1].")
    return shown


def run(argv: list[str]) -> int:
    """Default is SHOW, and an unknown command is an ERROR — NOTHING here writes.

    Same guard movers.run carries, for the same reason: a read-only-looking command must be
    read-only, and a typo must not become an action."""
    cmd = argv[0] if argv else "show"
    if cmd != "show":
        log.error("paths: unknown command %r (show) — nothing written, nothing fetched", cmd)
        return 1
    report(bets._load())
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(run(sys.argv[1:]))
