"""WORKING ORDERS — the bridge from a read to real money, with a limit instead of a guess.

WHY THIS EXISTS (2026-08-03). The read routine runs PRE-MARKET, so the newest price it can
honestly quote is yesterday's close (READ_LOOP.md "WHEN this runs"). It used to emit that close
as a point entry ("5 sh @ ~83.45") and the human executed hours — sometimes days — later. Two
measured costs, both on the 40 taken movers with price history:

  median |gap| reference close -> next OPEN   1.07%
  median |move| reference close -> next CLOSE 2.42%     (so waiting costs MORE than the gap)

and a fat tail: PNR gapped -23.4% through its alert, SMCI +13.3%, DLR +5.9%. On those names a
point price is not a level, it is prose. Worse, the "suggestion registry" was a `SIZED SUGGESTION:`
marker inside a free-text thesis that NO code read: two were ever issued and NEITHER was executed
(FINDINGS 2026-08-01) — a 0% conversion rate nothing in the daily loop noticed.

THE FIX. A suggestion becomes a working order: a LIMIT computed by code from the reference close
and the stop, an expiry in sessions, and a daily re-check against real bars. A limit is
age-invariant — that is precisely why it can be re-pushed every day and why the human can place
it whenever he wakes up, which the point price never survived.

WHAT THIS IS NOT. Not a verdict silo. bets.py still owns the edge question and its scoring is
untouched (it enters at the first complete bar strictly after pre-registration, lookahead-guarded
— the science was never exposed to this, only the money was). This ledger answers an EXECUTION
question, DIAGNOSTIC only, on the take/skip pattern movers.py already uses: we log fills AND
no-fills so the band itself can be scored.

PRE-REGISTERED (written 2026-08-03, BEFORE any order data accrued — no goalpost-moving): at N>=20
resolved orders, if EXPIRED orders' median 21d excess beats FILLED orders' by more than +3pp, the
band is TOO TIGHT -> widen it with evidence; otherwise the band is vindicated. This never moves
the Arc 5 #7 edge bar.

COUNTERFACTUAL MODE [ARC 5 #12a, 2026-08-14]: the book is retired, so there is no broker leg —
every order is a modelled counterfactual by construction (the same place→check cycle against the
same real bars, so the [ORDERS #1] diagnostic keeps accruing on an UNCHANGED fill model). The
`placed`/`pulled` verbs and the sizing logic (cash + risk unit, which read the live book) are
retired with the broker; `placed_at`/`pulled_at` stay as HISTORICAL columns on the pre-#12a rows.
Stated caveat (#12a): with no broker there is no fill-vs-broker-truth check — a band verdict at
N>=20 is model-vs-model and is read that way; re-validation happens live if money ever returns.

  place TICKER long|short STOP HORIZON_d BENCH [--shares=N] [--ref=P] [--note=...]
  check                     resolve pending orders against real bars (filled/expired) + score
  cancel TICKER "why"       kill a still-PENDING order by hand
  show                      the ledger + the filled-vs-expired diagnostic
"""
import csv
import logging
import os
import sys
from datetime import date, datetime, timedelta, timezone

from research import config

log = logging.getLogger(__name__)

LEDGER = "research/orders.csv"
FIELDS = ["logged_at", "ticker", "direction", "shares", "ref", "ref_date", "scan_from",
          "limit_px", "stop_px", "horizon_d", "benchmark", "status", "resolved_on",
          "fill_px", "x21_pct", "placed_at", "pulled_at", "note"]
# placed_at / pulled_at are HISTORICAL columns [ARC 5 #12a]: they separated a real broker order
# from a modelled counterfactual while the book was live (a `filled` row WITH placed_at was money
# that moved). The broker leg is retired — no new row ever stamps them — but the pre-#12a rows
# keep theirs, because rewriting an evidence ledger is how audit trails die.
SCORE_H = 21   # forward window for the band diagnostic (fast-sleeve length; ONE fixed ruler so
               # filled and expired orders stay comparable, exactly like movers' 21/63d contrast)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _load() -> list[dict]:
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER, newline="") as f:
        # Backfill columns added after a row was written, so a schema change can never make an
        # older row raise KeyError mid-pass and take the whole resolve with it.
        rows = [{**{k: "" for k in FIELDS}, **r} for r in csv.DictReader(f)]
    for i, r in enumerate(rows, 1):
        # A row with MORE fields than the header (csv parks the overflow under None) is an
        # unquoted comma from a hand-edit. Refuse BY NAME before any command runs — on
        # 2026-08-18 this surfaced instead as DictWriter dying cryptically mid-save.
        if None in r:
            raise ValueError(f"{LEDGER} row {i} ({r.get('ticker') or '?'}): more fields than "
                             f"the header — unquoted comma in a hand-edit? Fix the row; "
                             f"nothing was modified")
    return rows


def _save(rows: list[dict]) -> None:
    # Write-then-replace: a crash mid-write leaves the real ledger untouched. Writing in place
    # is how the 2026-08-18 settle truncated this file to 2 of 6 rows (the writer raised on a
    # malformed row after the header was already down) and the cloud run committed the damage.
    tmp = LEDGER + ".tmp"
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, LEDGER)


def pending(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["status"] == "pending"]


# booked()/booked_lot() (the order↔book fill reconciliation, DXCM 2026-08-06 / DVA 2026-08-11)
# were deleted in digest v2 [ARC 5 #12a] — the last caller went with the broker-era digest
# branches. Git history has them; a re-fund resurrects with a fresh look, never a blind revert.


# ---------------------------------------------------------------- pure band math (testable)

def limit_price(ref: float, stop: float, direction: str) -> float:
    """The most we will chase past the reference close. PURE (no I/O).

    band = min(ENTRY_BAND_MAX, ENTRY_BAND_FRAC x the entry->stop distance).

    The cap is the binding term almost always; the stop-distance term only bites on a TIGHT
    stop, where paying up eats a large fraction of the risk budget. Both constants live in
    config.py — this function is the only place the formula exists, so the arithmetic is
    deterministic code and not something an LLM re-derives per run (CLAUDE.md: keep the model
    out of the decision path).
    """
    if ref <= 0:
        raise ValueError(f"reference price must be positive, got {ref}")
    band = config.ENTRY_BAND_MAX
    if stop > 0:
        band = min(band, config.ENTRY_BAND_FRAC * abs(ref - stop) / ref)
    sgn = 1 if direction == "long" else -1
    return round(ref * (1 + sgn * band), 2)


def _touched(bar: dict, limit: float, direction: str) -> bool:
    """Did this session trade through our limit?"""
    return bar["low"] <= limit if direction == "long" else bar["high"] >= limit


def _fill_at(bar: dict, limit: float, direction: str) -> float:
    """A gap THROUGH the limit fills at the open, not at the limit — real broker behaviour,
    and it happens to be in our favour, so modelling it the other way would flatter us."""
    return min(bar["open"], limit) if direction == "long" else max(bar["open"], limit)


def resolve(bars: list[dict], limit: float, direction: str,
            expiry_d: int = None) -> tuple[str, str, float] | None:
    """(status, resolved_on, fill_px) for a pending order, or None while still working. PURE.

    `bars` must already be COMPLETE sessions strictly after the order's scan_from anchor —
    see _complete(). Fewer than expiry_d bars with no touch means the order is still live, not
    expired: an order cannot die before its sessions have actually elapsed.
    """
    expiry_d = config.ORDER_EXPIRY_D if expiry_d is None else expiry_d
    for b in bars[:expiry_d]:
        if _touched(b, limit, direction):
            return "filled", b["date"][:10], _fill_at(b, limit, direction)
    if len(bars) >= expiry_d:
        return "expired", bars[expiry_d - 1]["date"][:10], 0.0
    return None


def _complete(bars: list[dict], today: str = None) -> list[dict]:
    """Drop the in-progress session.

    Same guard as bets._score (bets.py:84-93): the price feed returns today's still-moving bar
    as a "close", and a high/low that is still being made would resolve an order against a range
    that has not finished happening. Deliberately conservative — a run after the 16:00 ET close
    but before midnight UTC also defers a day. Correctness beats immediacy.
    """
    today = today or _today()
    return [b for b in bars if b["date"][:10] < today]


def sessions_left(row: dict, bars: list[dict]) -> int:
    """Complete sessions remaining before this order expires (for the digest countdown)."""
    return max(0, config.ORDER_EXPIRY_D - len(bars))


def _weekdays_between(start: str, end: str) -> int:
    """Weekdays strictly after `start` and strictly before `end` (ISO dates). PURE.
    = how many COMPLETE sessions can exist for an order anchored at `start` when today is
    `end` — modulo market holidays, which is why callers demand ≥2, not ≥1."""
    d0, d1 = date.fromisoformat(start), date.fromisoformat(end)
    return sum(1 for i in range(1, max(0, (d1 - d0).days))
               if (d0 + timedelta(days=i)).weekday() < 5)


# ---------------------------------------------------------------- commands

def place(rows: list[dict], ticker: str, direction: str, stop: float, horizon_d: int,
          bench: str, shares: int = None, ref: float = None, note: str = "") -> bool:
    """Pre-register ONE COUNTERFACTUAL working order. Returns True if a row was written.

    No sizing since [ARC 5 #12a]: there is no cash and no equity to size against — the band
    diagnostic scores fill-vs-no-fill per order, which never needed a share count. `--shares`
    remains only as an explicit annotation; unset, the column stays blank.
    """
    from research import prices
    ticker, bench, direction = ticker.upper(), bench.upper(), direction.lower()
    if direction not in ("long", "short"):
        print("direction must be long|short"); return False
    if any(r["ticker"] == ticker for r in pending(rows)):
        print(f"{ticker} already has a working order — cancel it first"); return False

    bars = prices.daily_bars(ticker, 5)
    if not bars:
        print(f"no price data for {ticker} — cannot set a reference"); return False
    done = _complete(bars)
    if not done:
        print(f"no COMPLETE session for {ticker} yet — cannot set a reference"); return False
    ref = float(ref) if ref is not None else done[-1]["close"]
    ref_date = done[-1]["date"][:10]
    # The EXCLUSIVE anchor resolution scans from. Placed pre-market (the designed path) the
    # newest bar IS the last complete one, so the order works from today's session. Placed
    # mid-session, an in-progress bar exists and we anchor on it instead — that session's range
    # is already partly known, so resolving against it would be lookahead dressed as a fill.
    scan_from = ref_date if len(bars) == len(done) else bars[-1]["date"][:10]

    limit = limit_price(ref, float(stop), direction)
    rows.append({"logged_at": _now(), "ticker": ticker, "direction": direction,
                 "shares": str(int(shares)) if shares is not None else "",
                 "ref": f"{ref:.2f}", "ref_date": ref_date,
                 "scan_from": scan_from, "limit_px": f"{limit:.2f}", "stop_px": f"{float(stop):.2f}",
                 "horizon_d": str(int(horizon_d)), "benchmark": bench, "status": "pending",
                 "resolved_on": "", "fill_px": "", "x21_pct": "", "placed_at": "", "note": note})
    verb, rel = ("BUY", "<=") if direction == "long" else ("SELL SHORT", ">=")
    print(f"COUNTERFACTUAL ORDER {verb} {ticker} · LIMIT {rel} {limit:.2f} · stop {float(stop):.2f}\n"
          f"  ref {ref:.2f} = {ref_date} close (NOT a live quote) · {config.ORDER_EXPIRY_D} sessions "
          f"· {horizon_d}d vs {bench} · scored either way; nothing to execute [ARC 5 #12a]")
    return True


def check(rows: list[dict]) -> tuple[int, list[str]]:
    """Resolve every pending order against real bars. Returns (n_resolved, tickers that failed).

    Per-row isolation, same reason as bets.settle: one dead ticker must not abort the pass.

    The booked-fill precedence (a real broker fill outranking the bar model, the DVA 2026-08-11
    fix) retired with the book [ARC 5 #12a]: with no broker there is no real fill to outrank the
    model — bars are the only resolver, which is exactly what "counterfactual" means. Its
    historical rows (fill_px = the book entry, not the modelled touch) stay as written.
    """
    from research import prices
    n, failed = 0, []
    for r in pending(rows):
        try:
            bars = _complete(prices.bars_after(r["ticker"], r["scan_from"],
                                               config.ORDER_EXPIRY_D + 5))
            # bars_after fails SOFT to [] (prices.py yfinance fallback), which resolve() reads
            # as "still working" — a silent feed flake strands a row pending forever with no
            # alarm (how DXCM's fill went unresolved 2026-08-06). Zero bars where ≥2 weekday
            # sessions have elapsed is loud: feed flake or back-to-back holidays (~9/yr false
            # positive, self-clears next session).
            if not bars and _weekdays_between(r["scan_from"], _today()) >= 2:
                log.warning("orders: NO complete bars for %s after %s — feed flake or market "
                            "holiday; row left pending", r["ticker"], r["scan_from"])
                failed.append(r["ticker"])
                continue
            res = resolve(bars, float(r["limit_px"]), r["direction"])
        except Exception as e:
            log.warning("orders: %s could not be checked (%s)", r["ticker"], e)
            failed.append(r["ticker"])
            continue
        if res is None:
            continue
        status, on, fill = res
        r.update(status=status, resolved_on=on, fill_px=f"{fill:.2f}" if fill else "")
        n += 1
        if status == "filled":
            print(f"FILLED {r['ticker']} @ {fill:.2f} on {on} "
                  f"(limit {float(r['limit_px']):.2f}) — counterfactual; scored at {SCORE_H}d")
        else:
            print(f"EXPIRED {r['ticker']} — limit {float(r['limit_px']):.2f} never touched "
                  f"in {config.ORDER_EXPIRY_D} sessions (as of {on}). Did NOT chase.")
    return n, failed


def score(rows: list[dict]) -> int:
    """Forward-score RESOLVED orders vs their benchmark at SCORE_H — filled AND expired.

    The expired ones are the whole point: "what did refusing to chase cost us?" is unanswerable
    unless the no-fills are scored on the same ruler as the fills. Reuses bets._score so there is
    exactly ONE direction-aware, lookahead-guarded scoring definition in the project.
    """
    from research import bets, prices
    n = 0
    for r in rows:
        if r["status"] not in ("filled", "expired") or r.get("x21_pct") or not r["resolved_on"]:
            continue
        day = r["resolved_on"]
        try:
            res = bets._score(prices.bars_after(r["ticker"], day, SCORE_H + 5),
                              prices.bars_after(r["benchmark"], day, SCORE_H + 5),
                              r["direction"], SCORE_H, day)
        except Exception as e:
            log.debug("orders score skip %s: %s", r["ticker"], e); continue
        if res is None:
            continue
        r["x21_pct"] = f"{res[2] * 100:+.2f}"
        n += 1
    return n


# `placed`/`pulled` lived here until [ARC 5 #12a] — the two verbs that reconciled OUR model of
# an order with the BROKER's reality. With no broker there is no reality to reconcile; a re-fund
# would resurrect them from git history with a fresh look, not blind revert.


def cancel(rows: list[dict], ticker: str, why: str) -> bool:
    live = [r for r in pending(rows) if r["ticker"] == ticker.upper()]
    if not live:
        print(f"no working order for {ticker.upper()}"); return False
    live[-1].update(status="cancelled", resolved_on=_today(), note=why)
    print(f"CANCELLED {ticker.upper()} — {why}")
    return True


def stats(rows: list[dict], status: str) -> tuple | None:
    """(n, median, beat%) of scored 21d excess for one resolution status, or None."""
    v = [float(r["x21_pct"]) for r in rows if r["status"] == status and r.get("x21_pct")]
    if not v:
        return None
    from statistics import median
    return len(v), median(v), sum(1 for x in v if x > 0) / len(v) * 100


def summary(rows: list[dict]) -> None:
    st = lambda s: [r for r in rows if r["status"] == s]
    live, fill, exp = pending(rows), st("filled"), st("expired")
    print(f"\nworking orders ({LEDGER}): {len(live)} pending | "
          f"{len(fill)} filled / {len(exp)} expired / {len(st('cancelled'))} cancelled")
    for r in live:
        rel = "<=" if r["direction"] == "long" else ">="
        print(f"  PENDING {r['ticker']:>5} {r['shares'] or '—'}sh {rel} {float(r['limit_px']):.2f} "
              f"· stop {float(r['stop_px']):.2f} · ref {float(r['ref']):.2f} ({r['ref_date']})")
    for r in fill + exp:
        px = f"@ {float(r['fill_px']):.2f}" if r["fill_px"] else "no fill"
        print(f"  {r['status'].upper():>7} {r['ticker']:>5} {px} on {r['resolved_on']}"
              f"{'  x21 ' + r['x21_pct'] + '%' if r.get('x21_pct') else ''}")
    print("\nband diagnostic (21d excess vs benchmark — DIAGNOSTIC, never an edge verdict):")
    for s, label in (("filled", "filled"), ("expired", "expired")):
        st_ = stats(rows, s)
        print(f"  {label:>8}: " + (f"n={st_[0]} median {st_[1]:+.2f}% beat {st_[2]:.0f}%"
                                   if st_ else "n=0"))
    print(f"  PRE-REGISTERED: at N>=20 resolved, expired median beating filled median by >+3pp "
          f"⇒ band too tight; else vindicated. Band/expiry live in config.py.")


def run(argv: list[str]) -> int | None:
    """Default is SHOW, and an unknown command is an ERROR — neither writes.

    Same guard movers.run carries, for the same reason: a read-only-looking command that
    silently mutates a ledger is how a denominator gets corrupted.
    """
    rows = _load()
    cmd = argv[0] if argv else "show"
    if cmd == "show":
        summary(rows); return
    if cmd == "place":
        opt = lambda k: next((a.split("=", 1)[1] for a in argv if a.startswith(f"--{k}=")), None)
        sh, rf = opt("shares"), opt("ref")
        pos = [a for a in argv[1:] if not a.startswith("--")]
        if place(rows, pos[0], pos[1], float(pos[2]), int(pos[3]), pos[4],
                 shares=int(sh) if sh else None, ref=float(rf) if rf else None,
                 note=opt("note") or ""):
            _save(rows)
        return
    if cmd == "cancel":
        if cancel(rows, argv[1], " ".join(argv[2:])):
            _save(rows)
        return
    if cmd != "check":
        # `placed`/`pulled` land here too since [ARC 5 #12a] — retired with the broker leg.
        log.error("orders: unknown command %r (place|check|cancel|show) — nothing written", cmd)
        return
    n, failed = check(rows)
    n += score(rows)
    _save(rows)
    log.info("orders: resolved/scored %d rows%s", n, f" (failed: {', '.join(failed)})" if failed else "")
    summary(rows)
    # Nonzero on any unresolved ticker so daily.sh's `|| FAILS` sees it and the 🚨 heartbeat
    # fires — the check itself staying quiet is what let a feed flake strand DXCM [2026-08-06].
    return 1 if failed else 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(run(sys.argv[1:]))
