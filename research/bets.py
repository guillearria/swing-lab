"""General CATALOGUE of pre-registered FORWARD bets (any experimental thesis).

The home for ideas that CAN'T be backtested honestly — Claude's judgment/reading, where
it already knows how the PAST turned out, so the only clean test is the FUTURE. Each bet
is timestamped (= pre-registration), scored later vs a benchmark, and counts toward the
multiple-testing tally. Direction-aware (long/short). NO lookahead: a bet can't be scored
unless its entry bar is strictly AFTER it was logged.

Mechanical/backtestable ideas do NOT belong here — those are fixed rules; test them on
history instantly (research/<probe>.py + the engine scoreboard).

  python3 -m research.bets add TICKER long|short HORIZON_d BENCH "thesis..."
  python3 -m research.bets settle      # score matured bets vs benchmark
  python3 -m research.bets show
"""
import csv
import logging
import math
import os
import sys
from datetime import date, datetime, timedelta, timezone
from statistics import mean, median

from research import prices

log = logging.getLogger(__name__)
CATALOGUE = "research/bets_catalogue.csv"
FIELDS = ["logged_at", "ticker", "direction", "horizon_d", "benchmark",
          "thesis", "status", "entry_date", "entry", "excess_pct", "pattern_tag", "notified"]
# notified = UTC stamp of the 📊 that ANNOUNCED this settlement, written only after telegram
# confirms the send. Blank on a closed row = the announcement never landed → the next run
# re-sends it. Before this column the retry set was "rows that were open when settle started",
# so a send that failed AFTER _save lost the message forever (that is how MU's -8.65%, the
# catalogue's first settled bet, was announced by nothing) [FINDINGS 2026-07-27].
# pattern_tag = the SCENARIO TYPE (cases/*.md `Pattern tag`). DIAGNOSTIC decomposition of the
# pooled verdict only — never a per-tag goalpost (N per-type bars = N× false positives) [Arc 5 #8].
# horizon ≤ FAST_MAX_D = the fast sleeve (21d). Pooled into ONE general verdict [FINDINGS Arc 5
# #7]; is_fast is a DIAGNOSTIC label (faster feedback in ~weeks), NOT a separately-scored bar.
FAST_MAX_D = 30
# THE pre-registered pass bar [Arc 5 #7], single-homed here — every surface (show, settle_msg,
# engine, digest) renders from these, so the bar can never fork between its printed copies.
# Population = LONG-ONLY since [ARC 5 #12a] (paper shorts carry unearnable alpha); shorts keep
# scoring as a below-bar diagnostic via _agg. Multiple-testing N still counts ALL rows.
BAR_N = 30            # settled long bets required
BAR_MEDIAN = 1.0      # median excess must exceed this (pp) — an effect-size floor
BAR_BEAT = 55.0       # % of bets beating their benchmark must exceed this
WILCOXON_ALPHA = 0.017  # one-sided signed-rank significance, computed by wilcoxon_p below


def beat_bar_count() -> int:
    """The beat bar as a COUNT at the verdict N — "17 of 30 beating", not "55% beat".

    [2026-08-19 owner review] A rate next to a count ("1 of 5 beat · 55% beat") reads as two
    different facts about the same word. Must EXCEED the rate, hence the +1.
    """
    return int(BAR_N * BAR_BEAT / 100) + 1


def gap_words(pct: float) -> str:
    """Plain English for an excess return: "8.0% behind" · "15.3% ahead".

    [2026-08-19 owner review] Every number in this project is a GAP TO A BENCHMARK, but the
    signed form hides that: "median -8.0%" reads as "we are down 8%" to anyone who does not
    already know. The words carry the meaning the sign was silently carrying.
    """
    return f"{abs(pct):.1f}% {'ahead' if pct >= 0 else 'behind'}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load() -> list[dict]:
    if not os.path.exists(CATALOGUE):
        return []
    with open(CATALOGUE, newline="") as f:
        rows = list(csv.DictReader(f))
    for i, r in enumerate(rows, 1):
        if None in r:  # overflow fields = unquoted comma in a hand-edit (orders.py, 2026-08-18)
            raise ValueError(f"{CATALOGUE} row {i} ({r.get('ticker') or '?'}): more fields "
                             f"than the header — fix the row; nothing was modified")
    return rows


def _save(rows: list[dict]) -> None:
    tmp = CATALOGUE + ".tmp"  # write-then-replace: a crash cannot truncate the ledger (2026-08-18)
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(rows)
    os.replace(tmp, CATALOGUE)


def median_dollar_vol(ticker: str, today: str | None = None) -> float | None:
    """Median close×volume over the last LIQ_WINDOW_D COMPLETED sessions, or None if that
    cannot be established (short history, fetch failure, in-progress-only data). `today` is
    injectable for tests; defaults to the real clock so the gate cannot be silently skipped."""
    from research import config
    today = today or datetime.now(timezone.utc).date().isoformat()
    try:
        bars = prices.daily_bars(ticker, config.LIQ_WINDOW_D + 5)
    except Exception:
        return None
    done = [b for b in bars if b["date"] < today][-config.LIQ_WINDOW_D:]
    if len(done) < config.LIQ_WINDOW_D:
        return None
    return median(b["close"] * b["volume"] for b in done)


def add(rows: list[dict], ticker: str, direction: str, horizon_d: int,
        bench: str, thesis: str, tag: str = "") -> bool:
    """Admit a bet into the catalogue. Returns True only if the row was appended.

    Admission rule [ARC 5 #12a], code-enforced so a groove or a hurried run can't drift past it:
    LONG ONLY (a paper short's alpha is unearnable — borrow cost/availability/buy-ins unmodeled;
    re-arming shorts requires a fresh pre-registration per the SKILL re-arm protocol, and that
    pre-registration would change this guard openly) + the liquidity floor, FAIL-CLOSED (a name
    whose liquidity can't be verified is refused — if prices are down, the whole pre-market run
    is already degraded; a gate that opens on error is not a gate).
    """
    from research import config
    if direction != "long":
        print(f"REFUSED {direction} {ticker.upper()}: catalogue admission is LONG-ONLY "
              f"[ARC 5 #12a]; shorts need a fresh pre-registration (re-arm protocol)")
        return False
    dv = median_dollar_vol(ticker)
    if dv is None:
        print(f"REFUSED {ticker.upper()}: liquidity UNVERIFIABLE "
              f"(<{config.LIQ_WINDOW_D} completed bars or fetch failed) — floor is fail-closed "
              f"[ARC 5 #12a]")
        return False
    if dv < config.LIQ_FLOOR_USD:
        print(f"REFUSED {ticker.upper()}: median ${dv:,.0f}/day over {config.LIQ_WINDOW_D} "
              f"sessions < ${config.LIQ_FLOOR_USD:,.0f} floor [ARC 5 #12a]")
        return False
    rows.append({"logged_at": _now(), "ticker": ticker.upper(), "direction": direction,
                 "horizon_d": str(horizon_d), "benchmark": bench.upper(), "thesis": thesis,
                 "status": "open", "entry_date": "", "entry": "", "excess_pct": "",
                 "pattern_tag": tag, "notified": ""})
    # "bet #N" = the row's catalogue ordinal (append-only, so it never shifts) — the number
    # the read leg's 🟢 NEW BET card carries [MSG v3], giving the owner a growing count.
    print(f"LOGGED bet #{len(rows)} — {direction} {ticker.upper()} {horizon_d}d vs "
          f"{bench.upper()}{' #' + tag if tag else ''} @ {rows[-1]['logged_at']} "
          f"(median ${dv / 1e6:,.1f}M/day)")
    return True


def _score(stock: list[dict], bench: list[dict], direction: str,
           horizon: int, logged_day: str, today: str | None = None) -> tuple | None:
    """Excess vs benchmark, sign-adjusted for direction. PURE (no I/O — testable).

    None until matured. Two symmetric gates gate the scoring window:
      - the ENTRY bar must be strictly AFTER the pre-registration day (no lookahead);
      - the EXIT bar must be a COMPLETED session (not today's still-moving bar).
    `today` is injected so this stays testable; it defaults to the real UTC date, because a
    gate that can be skipped by omitting an argument is not a gate.
    """
    if len(stock) < horizon or len(bench) < horizon:
        return None
    if not stock[0]["date"] > logged_day:
        raise ValueError(f"lookahead: entry {stock[0]['date']} not after prereg {logged_day}")
    # PARTIAL-BAR GUARD [2026-07-30]: yfinance returns the in-progress session as the latest
    # "close", so settling during market hours scores against a price that is still moving —
    # and the row then closes forever with that artifact. It happened: a mid-session run on
    # 7/27 scored MU at -8.65% off SOXX 508.49 intraday; the true number against the 516.23
    # final close is -7.99%. Deliberately conservative — a run after the 16:00 ET close but
    # before midnight UTC also defers a day. Correctness beats immediacy; None just means
    # "not matured", which the caller already handles by trying again next run.
    today = today or datetime.now(timezone.utc).date().isoformat()
    if stock[horizon - 1]["date"][:10] >= today or bench[horizon - 1]["date"][:10] >= today:
        return None
    sgn = 1 if direction == "long" else -1
    ex = (stock[horizon - 1]["close"] / stock[0]["close"] - 1) \
        - (bench[horizon - 1]["close"] / bench[0]["close"] - 1)
    return stock[0]["date"], stock[0]["close"], sgn * ex


def settle(rows: list[dict]) -> tuple[int, list[str]]:
    """Score every matured bet. Returns (n_settled, tickers that failed to score).

    Per-row isolation is the point: _score raises on lookahead and prices can fail per
    ticker, so one poisoned row used to abort scoring for the WHOLE catalogue and daily.sh
    reported only "bets failed" [FINDINGS 2026-07-27]. A bad row is now named and skipped.
    """
    n, failed = 0, []
    for r in rows:
        if r["status"] != "open":
            continue
        h, day = int(r["horizon_d"]), r["logged_at"][:10]
        try:
            res = _score(prices.bars_after(r["ticker"], day, h + 5),
                         prices.bars_after(r["benchmark"], day, h + 5), r["direction"], h, day)
        except Exception as e:
            log.warning("settle: %s could not be scored (%s)", r["ticker"], e)
            failed.append(r["ticker"])
            continue
        if res is None:
            continue
        d, px, ex = res
        r.update(status="closed", entry_date=d, entry=f"{px:.2f}", excess_pct=f"{ex * 100:+.2f}")
        n += 1
    return n, failed


def is_fast(r: dict) -> bool:
    return int(r["horizon_d"]) <= FAST_MAX_D


def unannounced(rows: list[dict]) -> list[dict]:
    """Settled bets whose 📊 was never confirmed delivered. PURE (testable).

    Derived from the LEDGER, not from what this process happened to settle — so a message
    lost to a crash, a dead token or a telegram outage is picked up by the NEXT run instead
    of vanishing with the row's open status.
    """
    return [r for r in rows if r["status"] == "closed" and not r.get("notified")]


def settle_msg(done: list[dict], s: tuple | None) -> str:
    """Telegram text for newly settled bets — 📊 SCORED, the moment-of-result pulse. PURE.

    v3 [MSG 2026-08-18]: 🚨 now means FAILURE ONLY (heartbeat/watchdog); a routine result is
    the experiment visibly working and dresses like it. Plain counts, no stats vocabulary —
    Σ/p/α stay CLI-side. A settling SHORT is announced (diagnostic row) but the tally line is
    always the long-only verdict population [ARC 5 #12a] — s=None (no longs settled yet) must
    not kill the announce."""
    lines = []
    for r in done:
        excess = float(r["excess_pct"])
        short = (" (short — diagnostic, outside the pool)"
                 if r.get("direction") == "short" else "")
        # "vs SPY: 3.2% behind" — the benchmark first, then the gap in words. The old
        # "{excess}%, miss" form left the reader to know that % was an excess [2026-08-19].
        lines.append(f"📊 SCORED — {r['ticker']} {r['horizon_d']}d vs {r['benchmark']}: "
                     f"{gap_words(excess)}{' ✓' if excess > 0 else ''}{short}")
    if s:
        n, _, md, beat = s
        c = round(n * beat / 100)          # beat% round-trips exactly back to its count
        lines.append(f"now {n} of {BAR_N} scored · {c} of {n} beat · "
                     f"median {gap_words(md)}")
    else:
        lines.append(f"0 of {BAR_N} scored")
    return "\n".join(lines)


def next_maturity(rows: list[dict]) -> tuple[str, str] | None:
    """(ISO date, ticker) of the earliest OPEN bet that can score, or None. PURE (testable).

    The honest answer to "what happens next" on a day with nothing to do — which, under a LOW
    edge prior, is most days. Nothing computed this before, so the digest could say "nothing to
    do" but never "and here is the date that changes".

    horizon_d counts TRADING days (bets.settle scores on trading bars), so this walks weekdays
    forward. Market holidays can only push a real settlement LATER, never earlier — and `_score`
    additionally needs the exit bar COMPLETE, which costs another trading day — so the digest
    renders it as ">=" rather than a promise.

    Rows that have ALREADY matured are skipped. They are not "next": a bet past its horizon and
    still open is either settling today or stuck, and the digest has a separate STUCK alarm for
    the latter. Without this, a stuck bet made the headline advertise a date in the PAST as the
    next evidence — precisely when something was already broken.
    """
    out, today = None, date.today().isoformat()
    for r in rows:
        if r["status"] != "open":
            continue
        try:
            d, left = date.fromisoformat(r["logged_at"][:10]), int(r["horizon_d"])
        except Exception:                 # a hand-edited row must not take the whole line down
            continue
        while left > 0:
            d += timedelta(days=1)
            if d.weekday() < 5:
                left -= 1
        iso = d.isoformat()
        if iso >= today and (out is None or iso < out[0]):
            out = (iso, r["ticker"])
    return out


def _agg(rows: list[dict]) -> tuple | None:
    """(n, mean, median, beat%) over the CLOSED rows given, or None. RAW — no population filter;
    diagnostic splits (tag/universe/direction/horizon) use this so shorts stay visible in them."""
    v = excess_values(rows)
    if not v:
        return None
    return len(v), mean(v), median(v), sum(1 for x in v if x > 0) / len(v) * 100


def excess_values(rows: list[dict]) -> list[float]:
    """Settled excess_pct values for the rows given, in ledger order. PURE (testable)."""
    return [float(r["excess_pct"]) for r in rows if r["status"] == "closed" and r["excess_pct"]]


def verdict_rows(rows: list[dict]) -> list[dict]:
    """The pooled verdict's POPULATION: long bets only [ARC 5 #12a — an amendment to Arc 5 #7's
    population, locked while the pool was ADVERSE (stripping the one settled winner), NOT a new
    bar]. Shorts keep scoring and appear in every diagnostic via _agg; they just cannot carry a
    pass that real money couldn't have bought (borrow cost/availability are unmodeled on paper)."""
    return [r for r in rows if r.get("direction") == "long"]


def stats(rows: list[dict]) -> tuple | None:
    """(n, mean, median, beat%) of the POOLED VERDICT = the LONG rows [ARC 5 #12a], or None.
    Every verdict surface (engine gate, digest headline, settle_msg, show) reads this one."""
    return _agg(verdict_rows(rows))


def wilcoxon_p(values: list[float]) -> float | None:
    """One-sided Wilcoxon signed-rank p-value for H1: values are shifted ABOVE zero.

    The [Arc 5 #7] bar named this test from day one but nothing ever computed it — a
    decorative-bar gap of exactly the Arc-3 class, closed here [ARC 5 #12a]. stdlib only.
    Convention: zeros dropped; ties get average ranks; EXACT null distribution for n ≤ 50 via
    subset-sum DP over doubled ranks (average ranks are multiples of 0.5, so doubling makes
    them integers — the enumeration is exact conditional on the observed tie pattern); normal
    approximation with tie correction + continuity correction above 50. None when nothing to test.
    """
    v = [x for x in values if x != 0]
    n = len(v)
    if n == 0:
        return None
    ranked = sorted((abs(x), i) for i, x in enumerate(v))
    ranks = [0.0] * n
    j = 0
    while j < n:
        k = j
        while k + 1 < n and ranked[k + 1][0] == ranked[j][0]:
            k += 1
        avg = (j + k + 2) / 2  # average of 1-based rank positions j+1..k+1
        for m in range(j, k + 1):
            ranks[ranked[m][1]] = avg
        j = k + 1
    w_plus = sum(r for r, x in zip(ranks, v) if x > 0)
    if n <= 50:
        doubled = [round(2 * r) for r in ranks]
        target = round(2 * w_plus)
        counts = {0: 1}
        for d in doubled:
            nxt = dict(counts)
            for s, c in counts.items():
                nxt[s + d] = nxt.get(s + d, 0) + c
            counts = nxt
        ge = sum(c for s, c in counts.items() if s >= target)
        return ge / 2 ** n
    mu = n * (n + 1) / 4
    tie_sizes = []
    j = 0
    srt = sorted(abs(x) for x in v)
    while j < n:
        k = j
        while k + 1 < n and srt[k + 1] == srt[j]:
            k += 1
        tie_sizes.append(k - j + 1)
        j = k + 1
    var = n * (n + 1) * (2 * n + 1) / 24 - sum(t ** 3 - t for t in tie_sizes) / 48
    if var <= 0:
        return None
    z = (w_plus - mu - 0.5) / var ** 0.5
    return 0.5 * (1 - math.erf(z / 2 ** 0.5))


def cum_excess(rows: list[dict]) -> float | None:
    """Σ settled excess over the VERDICT population (closed longs), equal-weight percentage
    points, each bet vs its OWN benchmark — never restated as "vs SPY" [ARC 5 #12a]. PURE."""
    v = excess_values(verdict_rows(rows))
    return sum(v) if v else None


def tag_mix(rows: list[dict], n: int = 15) -> list[tuple[str, int]]:
    """(tag, count) over the LAST n catalogue rows, most common first — the MIX MIRROR's
    number [ARC 5 #12a]. Generation-side (open + closed): the mirror watches what the read
    KEEPS REACHING FOR, not what happened to settle. PURE."""
    counts: dict[str, int] = {}
    for r in rows[-n:]:
        t = r.get("pattern_tag") or "untagged"
        counts[t] = counts.get(t, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def show(rows: list[dict]) -> None:
    open_ = [r for r in rows if r["status"] == "open"]
    closed = [r for r in rows if r["status"] == "closed"]
    print(f"\nforward-bet catalogue ({CATALOGUE}): {len(rows)} bets (multiple-testing N) | "
          f"open {len(open_)} closed {len(closed)}")
    # ONE pooled verdict [Arc 5 #7], population LONG-ONLY [ARC 5 #12a]; splits stay diagnostic.
    bar = (f"bar N≥{BAR_N} & median>+{BAR_MEDIAN:.0f}% & beat>{BAR_BEAT:.0f}% "
           f"& Wilcoxon α≈{WILCOXON_ALPHA} [Arc 5 #7 · #12a · #14 ONE LOOK]")
    s = stats(rows)
    if s:
        n, m, md, beat = s
        p = wilcoxon_p(excess_values(verdict_rows(rows)))
        pstr = f"  p={p:.3f}" if p is not None else ""
        print(f"  pooled LONG-ONLY [ARC 5 #12a]: mean {m:+.2f}%  median {md:+.2f}%  "
              f"beat {beat:.0f}%  n={n}{pstr}  → {bar}")
    else:
        print(f"  pooled LONG-ONLY [ARC 5 #12a]: 0 settled (+{len(open_)} open) | {bar}")
    # Diagnostic decompositions of the ONE pooled verdict, never separate bars [Arc 5 #8] — via
    # _agg (RAW) so shorts stay visible here. Direction: the [ARC 5 #10] n≥12 short bar is
    # UNREACHABLE-BY-DESIGN under long-only admission (declared, [ARC 5 #12a]) — the short line
    # is descriptive contrast only.
    for label, grp in (("core 63/126d", [r for r in rows if not is_fast(r)]),
                       ("fast ≤30d", [r for r in rows if is_fast(r)]),
                       ("long (=pooled)", [r for r in rows if r.get("direction") == "long"]),
                       ("short", [r for r in rows if r.get("direction") == "short"])):
        ds = _agg(grp)
        if ds:
            print(f"    · {label} (diagnostic): median {ds[2]:+.2f}% beat {ds[3]:.0f}% n={ds[0]}")
        else:
            print(f"    · {label} (diagnostic): 0 settled "
                  f"(+{sum(1 for r in grp if r['status'] == 'open')} open)")
    for r in open_:
        tag = f" #{r.get('pattern_tag')}" if r.get("pattern_tag") else ""
        print(f"  OPEN {r['logged_at'][:10]} {r['direction']:>5} {r['ticker']:>5} "
              f"{r['horizon_d']}d vs {r['benchmark']}{tag}: {r['thesis'][:64]}")


def run(argv: list[str]) -> int:
    """Returns a shell exit code — nonzero when scoring or the 📊 push failed, so
    scripts/daily.sh counts a LOST ANNOUNCEMENT as a failed step (it previously exited 0
    on a dropped message and no heartbeat ever fired). Mirrors digest.run."""
    rows = _load()
    cmd = argv[0] if argv else "show"
    if cmd == "add":
        # optional --tag=<scenario-type>; everything else is the thesis (back-compatible)
        tag = next((a[6:] for a in argv[5:] if a.startswith("--tag=")), "")
        thesis = " ".join(a for a in argv[5:] if not a.startswith("--tag="))
        if not add(rows, argv[1], argv[2], int(argv[3]), argv[4], thesis, tag):
            return 1                       # refused (admission rule) — nothing was written
        _save(rows)
    elif cmd == "settle":
        n, failed = settle(rows)
        log.info("settled %d", n); _save(rows); show(rows)
        # Persist FIRST (the score is the evidence), then announce. The announcement is
        # retried from the ledger, so the two no longer have to succeed together.
        todo = unannounced(rows)
        if todo:
            from research import notify
            if notify.send(settle_msg(todo, stats(rows))):
                for r in todo:
                    r["notified"] = _now()
                _save(rows)
            else:
                log.warning("settle: %d settlement(s) UNANNOUNCED — will retry next run",
                            len(todo))
                return 1
        if failed:
            log.warning("settle: could not score %s", ", ".join(failed))
            return 1
    else:
        show(rows)
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(run(sys.argv[1:]))
