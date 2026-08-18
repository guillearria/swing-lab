"""ARC 5 #8 — daily MOVER scan = the candidate DENOMINATOR for the general catalogue.

The general reading track's documented weakness [Arc 5 #7]: it draws from an UNBOUNDED news
scan with NO candidate denominator, so a future pass is conditional on SELECTION, not skill.
This logs every big mover in a DEFINED universe as a SEEN candidate with a take/skip —
with the clean-denominator discipline the (now-retired) insider ledger was built around. It
bounds selection to the scan universe; it does NOT eliminate it (universe ≠ all conceivable
reads). Since Arc 3 closed 2026-08-02 this is the project's ONLY candidate denominator.

TWO COHORTS since [ARC 5 #11]: the S&P 500 top-TOP_N (unchanged — denominator continuity) plus
a top-TAIL_TOP_N cohort from the S&P 400+600 committed caches (the under-covered tail Arc 2
pointed at). Each row's `universe` column is a DIAGNOSTIC decomposition of the pooled verdict
[Arc 5 #8] — NEVER a per-universe goalpost.

TAKES graduate to bets.py (the scored silo, carrying a pattern_tag). This file logs the
DENOMINATOR + the decisions, AND scores every DECISION (take AND skip) forward vs SPY at
21/63d — the only way to test whether the skip discipline is too conservative [plan W3].
(bets.py still owns each take's OWN-horizon/own-benchmark verdict; this ruler is a fixed
21/63d-vs-SPY contrast so takes and skips are comparable. Separate ledgers, no double-count.)

  scan                          rank movers in BOTH cohorts, log NEW ones as SEEN candidates
  decide TICKER take|skip "why" pre-register a decision on a SEEN mover (timestamped)
  settle                        score decided movers (take+skip) fwd vs SPY at 21/63d
  show                          print the ledger + seen/taken/skipped denominator + outcomes

A "mover" = |5-day % move| ≥ config.PCT_STRONG (via momentum.compute — the proven pure signal),
ranked by |move|, top-N. Bidirectional (big up AND big down) since we read both longs and shorts.
"""
import csv
import logging
import os
import sys
from datetime import datetime, timezone

from research import config, momentum, universe, feedstatus

log = logging.getLogger(__name__)

LEDGER = "research/movers_ledger.csv"
# pct_change is the 5-SESSION close-to-close move (config.TREND_DAYS via momentum.compute), NOT
# a 1-day move — verified against TPR 2026-08-14 (-20.7% = 08-06→08-13 exactly) [ARC 5 #12a].
# Label any surface that prints it "5d"; the BACKLOG item-7 "mismatch" was a misreading.
FIELDS = ["seen_at", "date", "ticker", "pct_change", "rel_volume", "direction_hint",
          "action", "logged_at", "rationale", "status", "pattern_tag", "x21_pct", "x63_pct",
          "universe"]
TOP_N = 25       # S&P 500 cohort — unchanged by [ARC 5 #11] (denominator continuity)
TAIL_TOP_N = 15  # S&P 400+600 tail cohort [ARC 5 #11]
BENCH = "SPY"
HORIZONS = (("x21_pct", 21), ("x63_pct", 63))  # forward windows scored vs SPY (direction-aware)
# Cohort order matters: sp500 runs first, so on index-promotion drift (a name in two caches)
# the sp500 label wins the (ticker, date) dedup. Universe functions are named, not captured —
# resolved at CALL time (the feedstatus path lesson: a bound reference defeats monkeypatching).
COHORTS = (("sp500", "sp500", TOP_N),
           ("tail", "tail", TAIL_TOP_N))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load() -> list[dict]:
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER, newline="") as f:
        # Backfill columns added after a row was written (orders.py pattern), so a schema
        # change can never KeyError an old row mid-pass and take a whole run with it.
        rows = [{**{k: "" for k in FIELDS}, **r} for r in csv.DictReader(f)]
    for i, r in enumerate(rows, 1):
        if None in r:  # overflow fields = unquoted comma in a hand-edit (orders.py, 2026-08-18)
            raise ValueError(f"{LEDGER} row {i} ({r.get('ticker') or '?'}): more fields than "
                             f"the header — fix the row; nothing was modified")
    for r in rows:
        # Rows written before [ARC 5 #11] predate the universe column; the scan was
        # S&P-500-only then, so the backfill is a fact, not a guess.
        r["universe"] = r["universe"] or "sp500"
    return rows


def _save(rows: list[dict]) -> None:
    tmp = LEDGER + ".tmp"  # write-then-replace: a crash cannot truncate the ledger (2026-08-18)
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, LEDGER)


def _fetch(tickers: list[str]) -> dict[str, list[dict]]:
    """Threaded OHLCV via the cloud-safe prices seam (need VOLUME for momentum.compute).

    Uses research.prices (urllib -> query1 chart endpoint) NOT yfinance: yfinance's
    download path is egress-blocked / hard rate-limited in the cloud env [same reason
    prices.py exists — BACKLOG 2026-07-02], so the scan must be able to run unattended.
    Dead/failed names -> [].
    """
    from concurrent.futures import ThreadPoolExecutor
    from research import prices
    def one(t: str) -> tuple[str, list[dict]]:
        try:
            rows = prices.daily_history(t, period="3mo")
            return t, [{"date": r["date"], "close": r["close"], "volume": r["volume"]}
                       for r in rows]
        except Exception:
            return t, []
    out: dict[str, list[dict]] = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for t, rows in ex.map(one, tickers):
            out[t] = rows
    return out


def rank(bars_by_ticker: dict[str, list[dict]], top_n: int = TOP_N) -> list[dict]:
    """PURE (no I/O — testable): rank names by |5-day move| among those clearing PCT_STRONG."""
    cands = []
    for t, b in bars_by_ticker.items():
        m = momentum.compute(b)
        if not m or abs(m["pct_change"]) < config.PCT_STRONG:
            continue
        cands.append({"ticker": t, "date": b[-1]["date"],
                      "pct_change": m["pct_change"], "rel_volume": m["rel_volume"]})
    cands.sort(key=lambda c: abs(c["pct_change"]), reverse=True)
    return cands[:top_n]


def scan(rows: list[dict], today: str | None = None) -> int:
    """Append NEW top movers as SEEN candidates (the denominator), one cohort at a time.

    Two cohorts [ARC 5 #11] (see COHORTS); a dead cohort records its own feed failure and
    must never abort the other. Dedup on (ticker, date) ACROSS cohorts. Only COMPLETED
    sessions are ranked (orders._complete — the same gate as bets._score): a mid-session
    run would otherwise log an intraday print as a 5-day close-to-close move, and the dedup
    would then block the real close from ever being recorded for that name.
    """
    from research import orders
    seen = {(r["ticker"], r["date"]) for r in rows}
    n = 0
    for univ, fn, top_n in COHORTS:
        key = f"{univ}-movers"
        syms = getattr(universe, fn)()
        if not syms:
            log.warning("%s: empty universe — cohort skipped", key)
            feedstatus.record(key, ok=False, error="universe returned empty")
            continue
        # Record the fetch outcome per cohort: an empty bar pull looks exactly like a quiet
        # day, and this scan IS the candidate denominator — a silent outage corrupts it.
        # `ok` means BARS RETURNED (the pipe); last_bar/coverage say whether the water was
        # fresh [FINDINGS 2026-08-04 ops]. A quiet day (bars, no movers) is ok=True.
        try:
            bars = {t: orders._complete(b, today) for t, b in _fetch(syms).items()}
            bars = {t: b for t, b in bars.items() if b}
            ranked = rank(bars, top_n)
            feedstatus.record(key, ok=bool(bars),
                              error="" if bars else "no bars returned for the universe",
                              last_bar=max((b[-1]["date"][:10] for b in bars.values()),
                                           default=""),
                              n_ok=len(bars), n_total=len(syms))
        except Exception as e:
            feedstatus.record(key, ok=False, error=f"{type(e).__name__}: {e}")
            raise
        for c in ranked:
            if (c["ticker"], c["date"]) in seen:
                continue
            seen.add((c["ticker"], c["date"]))
            rows.append({"seen_at": _now(), "date": c["date"], "ticker": c["ticker"],
                         "pct_change": f"{c['pct_change'] * 100:+.1f}",
                         "rel_volume": f"{c['rel_volume']:.1f}",
                         "direction_hint": "long" if c["pct_change"] > 0 else "short",
                         "action": "", "logged_at": "", "rationale": "", "status": "seen",
                         "pattern_tag": "", "universe": univ})
            n += 1
    return n


def decide(rows: list[dict], ticker: str, action: str, rationale: str) -> bool:
    """Pre-register a take/skip on a SEEN mover, timestamped now (the denominator decision)."""
    if action not in ("take", "skip"):
        print("action must be take|skip"); return False
    cands = [r for r in rows if r["ticker"] == ticker.upper() and r["status"] == "seen"]
    if not cands:
        print(f"no SEEN mover for {ticker}"); return False
    cands[-1].update(action=action, logged_at=_now(), rationale=rationale,
                     status="taken" if action == "take" else "skip")
    print(f"{action.upper()} {ticker.upper()} @ {cands[-1]['logged_at']}"
          + ("  → now log the scored bet: python3 -m research.bets add ..." if action == "take" else ""))
    return True


def settle(rows: list[dict]) -> int:
    """Score DECIDED movers — BOTH takes AND skips — forward vs SPY at 21d/63d.

    The instrument for 'are we too conservative?' [plan W3]: a skip's forward excess is
    otherwise never measured, so the discipline is untestable. Reuses bets._score (ONE
    direction-aware scoring definition, no lookahead). Assumes the candidate trade follows
    direction_hint (momentum continuation) — the standing caveat on 'would the skip have paid'.
    Fills x21_pct/x63_pct as each window matures; returns rows newly (partly) scored.

    PRE-REGISTERED THRESHOLD (locked, no goalpost-moving): at skips 63d N≥30, if median
    excess > +1% AND beat-rate > 55% vs SPY ⇒ filter too tight, loosen doctrine WITH evidence;
    else the skip discipline is vindicated. TAKES are scored on the same ruler for contrast.
    """
    from research import bets, prices
    n = 0
    for r in rows:
        if r["status"] not in ("taken", "skip"):
            continue
        day = (r["logged_at"] or r["seen_at"])[:10]
        got = False
        for col, h in HORIZONS:
            if r.get(col):
                continue
            try:
                res = bets._score(prices.bars_after(r["ticker"], day, h + 5),
                                  prices.bars_after(BENCH, day, h + 5),
                                  r["direction_hint"], h, day)
            except Exception as e:            # dead ticker / fetch fail — skip this row, don't abort
                log.debug("settle skip %s %dd: %s", r["ticker"], h, e); continue
            if res is None:                   # not matured yet
                continue
            r[col] = f"{res[2] * 100:+.2f}"
            got = True
        if got:
            n += 1
    return n


def outcome_stats(rows: list[dict], status: str, col: str) -> tuple | None:
    """(n, median, beat%) of scored `col` excess for rows of a given status, or None."""
    v = [float(r[col]) for r in rows if r["status"] == status and r.get(col)]
    if not v:
        return None
    from statistics import median
    return len(v), median(v), sum(1 for x in v if x > 0) / len(v) * 100


def settle_summary(rows: list[dict]) -> None:
    print("\nmover outcomes vs SPY (direction-aware, momentum-continuation assumption):")
    for status, label in (("taken", "takes"), ("skip", "skips")):
        parts = []
        for col, h in HORIZONS:
            s = outcome_stats(rows, status, col)
            parts.append(f"{h}d n={s[0]} median {s[1]:+.2f}% beat {s[2]:.0f}%" if s
                         else f"{h}d n=0")
        print(f"  {label:>6}:  " + "  |  ".join(parts))
    print("  PRE-REGISTERED [W3]: skips 63d N≥30 & median>+1% & beat>55% ⇒ filter too tight; "
          "else discipline vindicated.")


def summary(rows: list[dict]) -> None:
    st = lambda s: [r for r in rows if r["status"] == s]
    seen, taken, skip = st("seen"), st("taken"), st("skip")
    print(f"\nmover ledger ({LEDGER}): {len(rows)} movers SEEN (denominator) | "
          f"taken {len(taken)} skips {len(skip)} | unread {len(seen)}")
    for r in seen:
        # The universe label matters to the reader: tail names get the HIGHER read bar
        # (mechanism named or SKIP, liquidity checked) [ARC 5 #11].
        print(f"  SEEN {r['date']} {r['ticker']:>5}  {r['pct_change']}% 5d  "
              f"vol {r['rel_volume']}x  ({r['direction_hint']}, {r['universe']})")


def run(argv: list[str]) -> None:
    """Default is SHOW, and an unknown command is an ERROR — neither writes.

    Both used to fall through to `scan`: a bare `python3 -m research.movers` (the form README
    and the dashboard list as an inspection command) silently appended 25 re-scanned rows to
    the ledger, and so would any typo. That is the LEDGER COLLISION failure — it inflates the
    multiple-testing denominator, which [ARC 5 #6] names as a non-negotiable integrity guard.
    A read-only-looking command must be read-only.
    """
    rows = _load()
    cmd = argv[0] if argv else "show"
    if cmd == "show":
        summary(rows); settle_summary(rows); return
    if cmd == "decide":
        if decide(rows, argv[1], argv[2], " ".join(argv[3:])):
            _save(rows)
        return
    if cmd == "settle":
        n = settle(rows); _save(rows)
        log.info("movers: scored %d rows", n)
        settle_summary(rows); return
    if cmd != "scan":
        log.error("movers: unknown command %r (scan|decide|settle|show) — nothing written", cmd)
        return
    o = scan(rows)
    _save(rows)
    log.info("movers: new candidates %d", o)
    summary(rows)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    run(sys.argv[1:])
