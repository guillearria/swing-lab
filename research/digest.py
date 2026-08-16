"""ONE legible, actionable digest — the 'what happened + what needs MY input' surface [plan W4].

Shape, in order [digest v2, ARC 5 #12a]: the 🎯 POOL scoreboard (the verdict headline — n
settled long-only / median / beat / Σ / p vs the pre-registered bar, milestone banners, the
short contrast, and a Δ-since-HEAD line saying what CHANGED), then the DO-NOW list (the only
part meant to pull the human back in, with paste-ready commands), then book / orders / bets /
movers state. Composed from the existing silos FAIL-SOFT per section — a broken or dep-missing
silo degrades to an "unavailable" note, it never crashes a scheduled run.

The settle run, the read run and the CLI share this one composer, but they no longer emit the
same text: the Δ line diffs against HEAD, so settle (whose scoring is still uncommitted) reports
what it just scored while read (which commits before it pushes) correctly reports nothing new.
They WERE the same text until 2026-08-04 — 69% byte-identical lines, measured.

Sent as Telegram HTML (bold headers, tap-to-copy <code> commands); printed locally with the
tags stripped. Rule: HTML tags never span lines (notify truncates at a newline). All dynamic
free text is escaped here — notify stays transport-only.

Numbers stay single-source: the detailed verdicts live in `book mark` / `bets show`; this
digest points at those commands and only surfaces the glance + the decisions.

  python3 -m research.digest                       # print it
  python3 -m research.digest --notify              # print + Telegram push (exit 1 on failed send)
  python3 -m research.digest --notify "📖 read …"  # + a run note: 1st line on top as the headline,
                                                  #   the rest as a RUN NOTE block at the bottom
"""
import functools
import html
import logging
import re
import subprocess
import sys
from datetime import date, timedelta


def _busdays(start: date, end: date) -> int:
    """Weekday count in [start, end) — stdlib, no numpy (digest stays dependency-light)."""
    full, rem = divmod(max((end - start).days, 0), 7)
    n = full * 5
    for i in range(rem):
        if (start + timedelta(days=full * 7 + i)).weekday() < 5:
            n += 1
    return n

log = logging.getLogger(__name__)
CASH_EQUIV = {"SGOV", "BIL", "SHV", "SHY"}   # cash parks — never nag these for a missing stop
LEDGERS = ("research/bets_catalogue.csv", "research/movers_ledger.csv", "research/orders.csv")
FEED_STATUS = "research/data/_feed_status.json"   # written by each scan; read here
PUSH_LOG = "research/data/push_log.csv"   # date_utc,kind,verdict — one row per --notify push,
                                          # committed with the ledgers (daily.sh / READ_LOOP
                                          # step 7) so a stranded push is visible to the NEXT
                                          # delivered message [2026-08-06]
FEED_STALE_D = 1   # weekdays without a successful fetch → DO-NOW. 1, not 3 [2026-08-09 control
                   # review]: the bar-lag check below now measures against last_ok, so a DEAD
                   # scan freezes both fields at healthy values and THIS is the only alarm for
                   # a read that doesn't RUN — at 3 it rode 3 weekdays behind an all-clear
                   # DO-NOW (the watchdog watches settle's commits, not this leg). A read that
                   # RUNS but can't SPEAK is the other failure mode, and _pushlog_section owns
                   # it since 2026-08-11 (the 08-10 brief died UNCONFIRMED behind this check's
                   # all-clear: healthy feed, dead push). Complementary, not redundant.
                   # Weekends stay silent: busdays(Fri→Sat
                   # or Sun) = 1, and a healthy Monday scan resets to 0 before Monday's settle.
FEED_BAR_STALE_D = 1   # weekdays the newest COMPLETED bar may trail the last SUCCESSFUL scan
                       # (last_ok, NOT today — vs today every Sat/Sun read busdays(Thu→wknd)=2
                       # and both cohorts false-alarmed all weekend 08-08/09, first weekend the
                       # field was live). A healthy pre-market run reads yesterday's close = 1;
                       # 2 is the 2026-08-04 failure shape ("ok" while bars sat at 07-31).
                       # Known false positive: the first weekday after a market holiday (~9/yr)
                       # — named in the alarm text, self-clears next day.
FEED_COVERAGE_MIN = 0.90   # fraction of universe names that must return bars; below = partial
                           # outage (or a rotten universe cache) — either way the denominator is
                           # short and a quiet-looking scan is not to be trusted.
OVERDUE_D = 3        # business-day slack before a matured-but-unscored bet is called STUCK
                     # (market holidays make the busday count outrun real trading bars)
# EQUITY_STALE_D + IDLE_CASH_MIN were deleted [ARC 5 #12a]: the liveness clock died with the
# frozen equity curve (push-log + watchdog cover it), and the sized-suggestion bridge retired
# with the broker leg (the read logs one counterfactual order per take-carrying run).
_e = html.escape


def _git(*args: str) -> str:
    """One git read. Raises on any failure — each caller decides what silence means."""
    return subprocess.run(("git",) + args, capture_output=True, text=True,
                          timeout=20, check=True).stdout


@functools.lru_cache(maxsize=1)
def _marks() -> dict:
    """The live mark, computed ONCE per process.

    Two callers must never quote two different equities. `book.equity_marks` exists precisely
    so the printed number and the logged number cannot diverge, and this digest used to be a
    THIRD copy of that arithmetic (its own equity accumulation, its own SPY arrow, its own
    dual-mom try/except). Under v2 the book section is the only reader left; the rule stands.
    """
    from research import book
    return book.equity_marks(book._load())


def _committed(path: str) -> list[dict]:
    """A ledger as of HEAD — the last state this repo PUBLISHED. Raises if git can't answer.

    Deliberately NOT a state file. A cloud checkout is ephemeral, so anything the digest wrote
    would have to be committed to survive, and the read run commits BEFORE it pushes
    (READ_LOOP steps 6 then 7) — its own write could never land. git already holds the previous
    copy of every ledger, and the commit state is exactly the answer to "since when": on settle
    the scoring is still uncommitted (so the diff is what THIS run just scored), on read it is
    already committed (so the diff is empty, which is right — its bets are in its own headline).
    Same trick and the same reason as watchdog.last_commit_epoch.
    """
    import csv
    import io
    return list(csv.DictReader(io.StringIO(_git("show", f"HEAD:{path}"))))


def _pnl_pct(r: dict, spot: float | None) -> str:
    if not spot:
        return "n/a"
    pct = (spot / float(r["entry"]) - 1) * (1 if r["side"] == "long" else -1) * 100
    return f"{pct:+.0f}%"


def _book_section() -> tuple[list, list, list]:
    from research import book
    rows = book._load()
    # Terminal state [ARC 5 #12] — checked BEFORE _marks(): a closed book fetches no spots,
    # no SPY, no dual-mom, and raises no stop/target/pool-stop asks, ever.
    if book.is_retired(rows):
        return [], [], ["💼 <b>BOOK</b> CLOSED — capital exited [ARC 5 #12] · "
                        "verdict: FINDINGS closing entry · ledgers frozen"]
    if not rows:
        return [], [], ["book: empty (run book seed)"]
    # ONE mark for the whole message [2026-08-04]. This used to accumulate its own equity, fetch
    # its own SPY, and run its own dual-mom block — a THIRD copy of the arithmetic that
    # book.equity_marks exists to centralize, and three copies is how the band and this header
    # would eventually quote two different equities.
    m = _marks()
    actions, cash, equity = [], m["cash"], m["equity"]
    open_, lines = book._open_positions(rows), []
    for r in open_:
        t, side, sh, en = r["ticker"], r["side"], float(r["shares"]), float(r["entry"])
        spot = m["spots"].get(t)
        stop = float(r["stop"]) if r["stop"] else 0.0
        # TICKER-keyed, never prose-keyed [2026-08-02]. This used to also sniff the thesis
        # for "lock"/"park", which meant a position's alarm state depended on its prose: SPCX
        # rendered 🔒 locked purely because its thesis contained the word "lock" — inside
        # sentences saying the OPPOSITE ("NO lockup"). Reword a thesis, start nagging for a
        # stop on an un-stoppable position; write the word "lock" into any thesis, silence a
        # real one. The book now holds only tradeable swing capital (long-realm personal assets
        # live in the private long-term repo), so the only legitimate no-stop holding is a cash park.
        locked = stop <= 0 and t in CASH_EQUIV
        if locked:
            flag = "🔒 locked"                              # cash park / locked — no stop expected
        elif book.through_stop(side, spot, stop):
            flag = f"⚠️THRU {stop:.2f}"
            actions.append(f"{t} THROUGH stop {stop:.2f} (spot {spot:.2f}) — exit:\n"
                           f"<code>python3 -m research.book close {t} &lt;fill&gt;</code>")
        elif stop <= 0:
            flag = "NO STOP"
            actions.append(f"{t} ({side}, {_pnl_pct(r, spot)}) has NO stop — set:\n"
                           f"<code>python3 -m research.book stop {t} &lt;price&gt;</code>")
        else:
            flag = f"stop {stop:.2f}"
            if spot:
                flag += f" ({(stop / spot - 1) * 100:+.1f}% away)"
        # Exit TARGET — the sell-into-strength level [2026-08-04]. Structured, not prose: NIO's
        # exit band lived in its thesis, the market touched it (high 4.94 vs 4.85-5.15) and
        # nothing noticed. The nag repeats daily while spot stays through (a limit is
        # age-invariant); it clears when the position closes or the target is cleared.
        tgt = float(r["target"]) if r.get("target") else 0.0
        tgt_txt = ""
        if tgt > 0:
            tgt_txt = f" · exit {'≥' if side == 'long' else '≤'}{tgt:.2f}"
            if spot:
                tgt_txt += f" ({(tgt / spot - 1) * 100:+.1f}% away)"
            if book.through_target(side, spot, tgt):
                actions.append(f"{t} exit band TOUCHED — spot {spot:.2f} through target "
                               f"{tgt:.2f}: verify the sell limit is working at the broker; "
                               f"when it fills:\n"
                               f"<code>python3 -m research.book close {t} &lt;fill&gt;</code>")
        spot_txt = f"{spot:.2f}" if spot else "n/a"
        # $ P&L beside the % [2026-08-06]: the % alone made the reader open book mark to learn
        # what a move cost in money — the one question the morning read of a line answers.
        pnl_txt = (f" {_money(sh * (spot - en) * (1 if side == 'long' else -1))}"
                   if spot else "")
        lines.append(f"{t} {sh:g} @ {en:.2f}→{spot_txt}{pnl_txt} "
                     f"({_pnl_pct(r, spot)}) · {flag}{tgt_txt}")
    cash_line = f"cash ${cash:,.0f}"
    lines.append(cash_line)
    # The idle-cash nag retired with the broker leg [ARC 5 #12a]: there is no sized suggestion
    # to execute anymore — the read run logs ONE counterfactual order per take-carrying batch
    # unconditionally, so "cash is idle" stopped being an actionable state.
    head = f"💼 <b>BOOK</b> ${equity:,.0f}"
    if m["seed"]:
        seed_eq = m["seed"]
        head += f" · {(equity / seed_eq - 1) * 100:+.1f}% vs seed"
        # The pool stop is the project's ONE circuit breaker [ARC5#4] and until now it could
        # only ever fire into cron.log: book.mark PRINTS it, and daily.sh sends that stdout to
        # a file nobody reads unattended. Showing the LEVEL every day is what makes the alarm
        # legible before it trips, not after.
        floor = book.pool_floor(seed_eq)
        head += f" · pool stop -{book.POOL_STOP * 100:.0f}% (${floor:,.0f})"
        # Gated on risk still being ON. A breach cannot be undone — equity does not climb back
        # over the floor once trading has halted — so an unconditional alarm would nag forever
        # with no way to clear it, which this project forbids [FINDINGS 2026-08-02]. The
        # instruction is HALT, so following it (flattening to cash) is what silences it. The
        # LEVEL stays on the header either way; only the ASK is conditional.
        risk_on = [r for r in open_ if r["ticker"] not in CASH_EQUIV]
        if equity < floor and risk_on:
            actions.append(f"POOL STOP HIT — equity ${equity:,.0f} is below ${floor:,.0f} "
                           f"(-{book.POOL_STOP * 100:.0f}% of seed) with "
                           f"{len(risk_on)} position(s) still open. HALT: close them and log the "
                           f"verdict [ARC5#4]:\n<code>python3 -m research.book close "
                           f"{risk_on[0]['ticker']} &lt;fill&gt;</code>")
        if m["spy_equiv"]:
            head += " · " + ("↑SPY" if equity > m["spy_equiv"] else "↓SPY")
        if m["dualmom_equiv"]:     # 2nd yardstick [ARC5#7] — arrow only here, detail in book mark
            head += " · " + ("↑dual-mom" if equity > m["dualmom_equiv"] else "↓dual-mom")
    # Position rows ride in EVERY push [2026-08-06 — reversing the 08-05 slim cut]: the 7:42am
    # 📖 is the message the human actually reads, and it showed him a DXCM order nag with no
    # DXCM position line — "where do I stand?" had no answer in the only message he saw. What
    # slim drops now lives in compose(): the scoreboard one-liners, not the book.
    return actions, [], [head] + lines


def _orders_section(slim: bool = False) -> tuple[list, list, list]:
    """Counterfactual working orders [ARC 5 #12a] — display, NEVER a DO-NOW.

    Until 2026-08-14 this was the most actionable block in the push: place-at-broker asks,
    fill confirmations, the stale-GTC alarm. All of that reconciled OUR order model with the
    BROKER's book, and the broker is gone — an order here is a modelled 🟢 system take that
    resolves on its own against real bars and feeds the [ORDERS #1] band diagnostic. What
    remains informational: the pending line (with live spot + expiry countdown, the same intel,
    stripped of instructions) and the recent unplaced-fill counterfactual lines.
    """
    from research import book, config, orders
    rows = orders._load()
    live = orders.pending(rows)
    fills = [r for r in rows if r["status"] == "filled"]
    if not rows:
        return [], [], [] if slim else ["🎫 <b>ORDERS</b> none working"]
    lines = [f"🎫 <b>ORDERS</b> (counterfactual) {len(live)} working · "
             f"{len(fills)} filled / "
             f"{sum(1 for r in rows if r['status'] == 'expired')} expired"]
    pend_lines = []
    for r in live:
        t, lim = r["ticker"], float(r["limit_px"])
        spot, rel = book._spot(t), "≤" if r["direction"] == "long" else "≥"
        # Distance is signed AGAINST us: positive = the limit is out of reach right now.
        away = ((spot / lim - 1) * (1 if r["direction"] == "long" else -1) * 100) if spot else None
        spot_txt = (f"last {spot:.2f} ({away:+.1f}% {'above' if away > 0 else 'below'})"
                    if spot else "last n/a")
        verb = "BUY" if r["direction"] == "long" else "SELL SHORT"
        reach = "IN RANGE" if away is not None and away <= 0 else "no fill yet"
        try:
            from research import prices
            left = orders.sessions_left(r, orders._complete(prices.bars_after(
                r["ticker"], r["scan_from"], config.ORDER_EXPIRY_D + 5)))
            clock = f" · {left} of {config.ORDER_EXPIRY_D} sessions left"
        except Exception as e:
            log.debug("order countdown skipped for %s: %s", r["ticker"], e)
            clock = ""
        pend_lines.append(f"🟢 system take (counterfactual): {t} {verb} {rel} {lim:.2f} · "
                          f"stop {float(r['stop_px']):.2f}{clock} · {spot_txt} — {reach}; "
                          f"resolves on its own")
    # An unplaced fill is the regime's data point, not a missed trade — one line, no ask, and
    # only while RECENT (the ledger accrues counterfactual fills forever; the daily photo is
    # not the place they accumulate — `orders show` is). Historical placed+booked fills (the
    # pre-#12a real-money rows) render nothing: they are the frozen book's story.
    cutoff = (date.today() - timedelta(days=5)).isoformat()
    lines += pend_lines
    for r in fills:
        if not r.get("placed_at") and r["resolved_on"] >= cutoff:
            lines.append(f"{r['ticker']} would have filled @ {float(r['fill_px']):.2f} "
                         f"({r['resolved_on']}) — counterfactual, scored at 21d")
    fs, xs = orders.stats(rows, "filled"), orders.stats(rows, "expired")
    lines.append(f"[ORDERS #1] band: filled n={fs[0] if fs else 0} · "
                 f"expired n={xs[0] if xs else 0} — bar N≥20 by 2026-12-31 · "
                 f"config.ENTRY_BAND_MAX {config.ENTRY_BAND_MAX * 100:g}% · "
                 f"{config.ORDER_EXPIRY_D} sessions · full: orders show")
    # slim v2 [ARC 5 #12a]: the 🟢 system-take line(s) ride the morning 📖 too (they replaced
    # the old DO-NOW copy of the pending order); counts + diagnostics stay settle's.
    return [], [], pend_lines if slim else lines


def _bets_section() -> tuple[list, list, list]:
    from research import bets
    rows = bets._load()
    open_ = [r for r in rows if r["status"] == "open"]
    closed = [r for r in rows if r["status"] == "closed"]
    # No verdict numbers here since v2 [ARC 5 #12a] — the 🎯 POOL scoreboard is their single
    # source; a second copy in the state block is how two lines drift apart. Counts + dates only.
    head = f"<b>BETS</b> {len(open_)} open / {len(closed)} closed"
    # "Nothing to do" is the honest message most days under a LOW-edge prior. Saying WHEN the
    # scoreboard can next move on its own turns that into a dated expectation instead of a
    # shrug — and it is the one number that tells the human waiting IS the plan.
    nxt = bets.next_maturity(rows)
    if nxt:
        head += f" · next score ≥{nxt[0]} ({_e(nxt[1])})"
    # The MIX MIRROR's number [ARC 5 #12a]: shares of the last-15 rows' tags, so the >50%
    # drift rule in READ_LOOP has its input printed daily. A mirror, never a quota.
    mix = bets.tag_mix(rows)
    lines = [head]
    if mix:
        lines.append("mix(last 15): " + " · ".join(f"{_e(t)} {c}" for t, c in mix[:4]))
    soon, stuck = [], []
    for r in open_:
        try:
            # horizon_d counts TRADING days (bets.settle scores on trading bars), so the
            # elapsed side must too — a calendar-day count reported live bets as ~8d overdue
            # and made settlement look broken (fixed 2026-07-24). Weekends only; the handful
            # of market holidays just make this a hair conservative.
            days_left = int(r["horizon_d"]) - _busdays(date.fromisoformat(r["logged_at"][:10]),
                                                       date.today())
            # A SMALL negative is normal: market holidays make the business-day count run
            # ahead of real trading bars (July 4 is why MU displayed -1d while maturing dead
            # on time). Past that buffer it is not holiday drift — the bet is not scoring, and
            # a genuinely stuck one (bad/delisted ticker, dead price feed) used to be
            # indistinguishable from a healthy one and just drift further negative in this
            # same list forever.
            if days_left < -OVERDUE_D:
                stuck.append(f"{_e(r['ticker'])} overdue {-days_left}d")
            elif days_left <= 5:
                soon.append(f"{r['ticker']}({days_left}d)")
        except Exception:
            pass
    if soon:
        lines.append("maturing ≤5d (auto-settle): " + ", ".join(soon))
    actions = ([f"settlement STUCK: {', '.join(stuck)} — matured but not scoring; "
                f"check the ticker + price feed (<code>python3 -m research.bets settle</code>)"]
               if stuck else [])
    return actions, [], lines


def _movers_section() -> tuple[list, list, list]:
    from research import movers
    rows = movers._load()
    st = lambda s: sum(1 for r in rows if r["status"] == s)
    sk = movers.outcome_stats(rows, "skip", "x63_pct")
    sk_txt = (f"skip-63d median {sk[1]:+.2f}% beat {sk[2]:.0f}% n={sk[0]}"
              if sk else "skip-63d n=0")
    return [], [], [f"📡 <b>MOVERS</b> (|5d| moves) {st('taken')} take / {st('skip')} skip "
                    f"(denom {len(rows)}) · {sk_txt}"]


def _money(v: float) -> str:
    """`+$91` / `-$1,303` — sign OUTSIDE the currency, the way money is actually written.
    `f"${v:+,.0f}"` renders `$+91`, which reads as a typo in a message about dollars."""
    return f"{'-' if v < 0 else '+'}${abs(v):,.0f}"


def _row_id(r: dict) -> tuple:
    """Identity of a ledger row across two copies of the file.

    (logged_at|seen_at, ticker) — NOT the timestamp alone. A batch write stamps every row in it
    with the same second, and 11 timestamps in the live catalogue are shared by two bets each
    (META/NFLX, AVGO/ON, BB/OXM…). Keying on the timestamp collapses those pairs, and the
    survivor gets compared against the wrong row — which reported a bet as newly SCORED on a day
    nothing settled at all. Caught by this band's first live render [2026-08-04]. Verified unique
    across all three ledgers. Blind to DELETIONS by construction: this asks what a row became,
    not whether one vanished (a truncated append-only ledger is the git section's problem).
    """
    return (r.get("logged_at") or r.get("seen_at", ""), r.get("ticker", ""))


def _by_id(rows: list[dict]) -> dict:
    return {_row_id(r): r for r in rows}


def _pool_scoreboard() -> tuple[list, list, list]:
    """🎯 POOL — the verdict scoreboard that LEADS BOTH legs [ARC 5 #12a digest v2].

    Replaces the 💰 SINCE-LAST band: the band's book half (equity delta, blind-price guard,
    mark_delta) retired with the book, and performance-vs-bar is the one thing the owner asked
    the daily message to lead with. What survives from the band, verbatim: the row-level
    ledger diff vs git HEAD (the batch-write identity lesson [2026-08-04] included) as the
    Δ-since-HEAD line — the message still says what CHANGED, not only what IS.

    Display only — the scoreboard never asks for anything. It goes through _safe, so a broken
    scoreboard is a loud DO-NOW, never a silent shape-revert.
    """
    from research import bets, movers, orders
    rows = bets._load()
    longs = bets.verdict_rows(rows)
    now_n = len(bets.excess_values(longs))
    lines = []
    # 🏁 milestone: a STATELESS crossing check vs the HEAD copy of the catalogue. Works because
    # daily.sh runs the digest BEFORE push_ledgers commits (REORDER daily.sh AND MILESTONES
    # SILENTLY STOP FIRING — this comment is the guard); the read leg commits first
    # (READ_LOOP step 6), so its diff is empty and it can never false-banner. No internal
    # try/except: dead git kills the WHOLE scoreboard loudly via _safe — the band's proven
    # contract — instead of half-degrading into a message that looks normal.
    head_rows = _committed(bets.CATALOGUE)
    prev_n = len(bets.excess_values(bets.verdict_rows(head_rows)))
    for mst in (10, 20, 30):
        if prev_n < mst <= now_n:
            lines.append(f"🏁 <b>MILESTONE</b> n={mst} settled longs — review rides the next "
                         f"read run [ARC 5 #12a]")
    bar = (f"bar N≥{bets.BAR_N}/median&gt;+{bets.BAR_MEDIAN:.0f}%/beat&gt;{bets.BAR_BEAT:.0f}%"
           f"/α{bets.WILCOXON_ALPHA}")
    s = bets.stats(rows)
    if s:
        n, _, md, beat = s
        p = bets.wilcoxon_p(bets.excess_values(longs))
        sig = bets.cum_excess(rows)
        bits = [f"n={n} settled (long-only)", f"median {md:+.2f}%", f"beat {beat:.0f}%"]
        if sig is not None:
            bits.append(f"Σ {sig:+.1f}pp (equal-wt, own benchmarks)")
        if p is not None:
            bits.append(f"p={p:.2f}")
        togo = f"{bets.BAR_N - n} to go" if n < bets.BAR_N else "AT BAR — verdict time"
        lines.append("🎯 <b>POOL</b> " + " · ".join(bits) + f" · {bar} — {togo}")
        # Below-bar shape flag from n≥10 [ARC 5 #12a]: labeled so it can never be quoted as a
        # pass — nothing passes before N≥BAR_N, and the Wilcoxon only counts AT the bar.
        if n >= 10 and md > bets.BAR_MEDIAN and beat > bets.BAR_BEAT:
            lines.append(f"PASS-CANDIDATE (below-bar, n&lt;{bets.BAR_N}): shape clears "
                         f"median/beat — nothing passes before N≥{bets.BAR_N}")
    else:
        lines.append(f"🎯 <b>POOL</b> 0 settled (long-only) · {bar}")
    sh = bets._agg([r for r in rows if r.get("direction") == "short"])
    if sh:
        lines.append(f"shorts (diagnostic, below-bar [#10/#12a]): n={sh[0]} "
                     f"median {sh[2]:+.2f}% beat {sh[3]:.0f}%")
    # Δ since HEAD — the band's surviving half. Row-level against the committed copy, so it
    # needs no settled_at/scored_at column in any silo — which is exactly the cost the
    # 2026-07-10 rejection of "fold the 🚨s into the digest" refused to pay. That rejection
    # still stands: this is the one-line summary, the 🚨 keeps the detail AND its delivery
    # guarantee.
    bits = []
    scored, added = [], 0
    was = _by_id(head_rows)          # same HEAD copy the milestone check used — one git read
    for r in rows:
        old = was.get(_row_id(r))
        if old is None:
            added += 1
        elif r["status"] == "closed" and old["status"] != "closed":
            scored.append(f"{r['ticker']} {r['excess_pct']}%")
    if scored:
        bits.append(f"{len(scored)} scored ({_e(', '.join(scored))})")
    if added:
        bits.append(f"+{added} bets")
    # daily.sh settles MOVERS too (:19). Leaving them out made the band print "nothing scored" on
    # a run that had just scored 25 rows — in the one line whose whole job is to say what changed.
    was_m, m_scored = _by_id(_committed(movers.LEDGER)), 0
    for r in movers._load():
        old = was_m.get(_row_id(r))
        if old is None:
            continue
        if ((r.get("x21_pct") and not old.get("x21_pct"))
                or (r.get("x63_pct") and not old.get("x63_pct"))):
            m_scored += 1
    if m_scored:
        bits.append(f"{m_scored} movers scored")
    moved = []
    was_o = _by_id(_committed(orders.LEDGER))
    for r in orders._load():
        old = was_o.get(_row_id(r))
        if old is not None and old["status"] != r["status"]:
            moved.append(f"{r['ticker']} {old['status']}→{r['status']}")
    if moved:
        bits.append(_e(" · ".join(moved)))
    if not scored and not added and not moved and not m_scored:
        bits.append("nothing scored")
    lines.append("Δ since HEAD: " + " · ".join(bits))
    return [], [], lines


def _safe(fn, name: str) -> tuple[list, list, list]:
    """Fail-soft per silo — but LOUD. A dead silo used to degrade to a quiet trailing line,
    so the insider ledger (meant to be the 2nd verdict silo, retired 2026-08-02 — the project
    runs on ONE) could stop accruing evidence for weeks with nothing escalating. Fail-soft keeps
    the run alive; it must not keep it quiet."""
    try:
        return fn()
    except Exception as e:
        log.debug("%s section failed: %s", name, e)
        return ([f"{name} silo DOWN ({_e(type(e).__name__)}) — evidence is NOT accruing; "
                 f"check cron.log"], [], [f"{name}: unavailable ({_e(type(e).__name__)})"])


def _git_section() -> tuple[list, list, list]:
    """DO-NOW when scored rows exist only in this container.

    The 2026-07-27 read run pushed a 🟢 TRADE ALERT saying the bet was "pre-registered and
    scored either way" — while no row had reached the catalogue and no commit had landed.
    READ_LOOP step 6 already required commit-before-push and was simply not followed, so the
    check lives here instead: a doc instruction cannot be verified, this can. Never blocks a
    send — silence is the worse failure — it just makes the message tell the truth.
    """
    try:
        dirty = bool(_git("status", "--porcelain", "--", *LEDGERS).strip())
        ahead = bool(_git("log", "--oneline", "@{upstream}..HEAD", "--", *LEDGERS).strip())
    except Exception as e:                      # no git, no upstream, detached HEAD…
        log.debug("git section skipped: %s", e)
        return [], [], []
    if dirty or ahead:
        what = "uncommitted" if dirty else "unpushed"
        return ([f"ledger changes are {what} — any bet in this message is NOT scored yet; "
                 f"commit + push research/*.csv"], [], [])
    return [], [], []


def _stranded_section() -> tuple[list, list, list]:
    """DO-NOW while a previous run's commit sits parked on a settle-backup ref.

    _git_section can only see THIS container, so it structurally cannot report work stranded
    by the one before it — which is exactly how 1b014cc nearly vanished on 2026-07-31. The
    $FAILS heartbeat fires once, on the day of the strand; this repeats until a human acts,
    the same reasoning as the `notified` column (a one-shot notification is not delivery).

    Deliberately does NOT compute whether the ref was already merged — that needs the objects
    fetched locally, and a ref that has been merged but not deleted keeps nagging. The cure is
    the last command in the line this prints. Nuisance traded for ~8 lines and one network call.
    """
    try:
        out = _git("ls-remote", "--heads", "origin", "refs/heads/settle-backup/*")
    except Exception as e:                      # offline, no remote, no git…
        log.debug("stranded section skipped: %s", e)
        return [], [], []
    actions = []
    for line in out.strip().splitlines():
        sha, _, ref = line.partition("\t")
        name = ref.removeprefix("refs/heads/")
        actions.append(
            f"STRANDED settle work on <code>{name}</code> ({sha[:9]}) — a push failed and the "
            f"run's ledgers never reached master. Recover:\n"
            f"<code>git fetch origin {name} &amp;&amp; git cherry-pick {sha[:9]} &amp;&amp; "
            f"git push origin master &amp;&amp; git push origin --delete {name}</code>")
    return actions, [], []


# _liveness_section (the book_equity.csv staleness clock) was DELETED [ARC 5 #12a]: once the
# book retires, the curve freezes and the clock would alarm unclearably within 2 weekdays —
# forbidden [FINDINGS 2026-08-02]. Its job was already covered twice over:
# _pushlog_section fires when a due push has no DELIVERED row (covers "the run never ran" AND
# "the push died"), and the watchdog covers 36h commit staleness independently. The daily
# commit cadence survives the frozen curve because every settle stamps push_log.csv.


def _feed_section() -> tuple[list, list, list]:
    """DO-NOW when an upstream feed has gone quiet.

    A dead source is not an exception — `scan` just returns nothing — so _safe cannot see it
    and the ledger silently stops growing (2026-07-27: "openinsider fetch down", reported as
    prose in a run note). Each scan records its outcome; a stale last_ok is escalated here.
    """
    import json
    try:
        with open(FEED_STATUS) as f:
            status = json.load(f)
    except Exception:
        return [], [], []                        # never written yet — nothing to claim
    out = []
    for src, st in sorted(status.items()):
        last_ok = st.get("last_ok")
        # No last_ok means this source has NEVER reported a success — say that, don't invent a
        # duration. Until 2026-08-01 the else-branch was the sentinel `99`, which rendered as
        # "has not succeeded in 99 weekdays": a fabricated number inside an alarm, and wrong by
        # ~70 (the real gap was 27). An alarm that makes up figures is one you learn to distrust.
        if last_ok is None:
            when = "has NEVER reported a successful fetch"
        else:
            stale = _busdays(date.fromisoformat(last_ok), date.today())
            if stale <= FEED_STALE_D:
                # The PIPE is fresh — now check the WATER [FINDINGS 2026-08-04 ops]: on 08-04
                # the feed was "ok" while bars had not advanced past 07-31 (0 movers, silent),
                # and a partial fetch outage looks exactly like a quiet day. Legacy keys
                # without these fields skip both checks silently.
                last_bar = st.get("last_bar")
                if last_bar:
                    # Lag vs last_ok, not today: the scan runs pre-market weekdays, so on a
                    # weekend the newest possible bar is Thursday's and a today-based count
                    # fires every Sat/Sun by construction (both cohorts, 08-08/09). A frozen
                    # bar with a LIVE scan still grows this gap; a dead scan is FEED_STALE_D's
                    # alarm above.
                    lag = _busdays(date.fromisoformat(last_bar), date.fromisoformat(last_ok))
                    if lag > FEED_BAR_STALE_D:
                        out.append(f"{_e(src)}: bars last advanced {_e(last_bar)} "
                                   f"({lag} weekdays behind the last scan) — stale feed (or a "
                                   f"market holiday just passed); the scan denominator did "
                                   f"not advance")
                n_ok, n_total = st.get("n_ok"), st.get("n_total")
                if n_total and n_ok is not None and n_ok / n_total < FEED_COVERAGE_MIN:
                    out.append(f"{_e(src)}: bars for only {n_ok}/{n_total} names — partial "
                               f"fetch outage (or a rotten universe cache — rebuild per "
                               f"[ARC 5 #11]); today's denominator is short")
                continue
            when = f"has not succeeded in {stale} weekdays (last ok {last_ok})"
        err = f" (last error: {st['last_error']})" if st.get("last_error") else ""
        out.append(f"{_e(src)} feed {_e(when)}{_e(err)} — candidates are NOT being logged")
    return out, [], []


def _utcnow():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc)


def _log_push(kind: str, verdict: str) -> None:
    """One delivery row per --notify push. Committed with the ledgers, which is what makes a
    stranded message visible to the NEXT run: settle commits its ledgers even when its 📋 dies
    in transport (08-05 AND 08-06, two consecutive nights), so the commit-watching watchdog
    can never see that failure — only a delivery record that travels in git can."""
    import csv
    import os
    new = not os.path.exists(PUSH_LOG)
    with open(PUSH_LOG, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date_utc", "kind", "verdict"])
        w.writerow([_utcnow().date().isoformat(), kind, verdict])


# UTC hour after which TODAY's push for that leg is due. settle fires 22:30 UTC daily (moved
# from ~05:08 on 2026-08-07 after three stranded nights in the 05:00 window); read fires
# pre-market on weekdays (~11:45 UTC). Each leg is held against its OWN calendar.
PUSH_DUE_H = {"settle": 23, "read": 13}


def _last_due(kind: str, now) -> date:
    """The last day a `kind` push was due, as of `now` (UTC). Read is weekdays only."""
    d = now.date() if now.hour >= PUSH_DUE_H[kind] else now.date() - timedelta(days=1)
    while kind == "read" and d.weekday() >= 5:   # Sat/Sun roll back to Friday
        d -= timedelta(days=1)
    return d


def _pushlog_section() -> tuple[list, list, list]:
    """DO-NOW when a due push was never confirmed delivered [2026-08-06; both legs 2026-08-11].

    Holds each leg's log against the last day THAT leg was due. Two corrections earned from the
    2026-08-10 incident (FINDINGS 2026-08-11):

    • BOTH kinds, not settle only. The 08-10 read ran, committed a bet (TTD) and died in
      transport (UNCONFIRMED) — and nothing anywhere alarmed, because this check filtered to
      `kind == "settle"` and the read leg has no watcher of its own. The read leg is the one
      that carries the TRADE ALERTS. FEED_STALE_D=1 does not cover this: the run was alive and
      the feed was healthy, only the push died.
    • Fires on "no DELIVERED row on/after due", not "the LAST row is DELIVERED", and names the
      FAILING row's own date. Under the old test a REJECTED->retry run alarmed about its own
      superseded first attempt, mislabelled with `due`: the 08-10 message accused 08-09, which
      the log shows was DELIVERED, and sent the human to debug a failure that had self-healed
      one line above it.

    Silent until the log holds a row of that kind (pre-rollout). A leg that stops stamping
    entirely is the watchdog's 36h commit-staleness domain, not this check's. Known false
    positive: the first weekday after a market holiday (~9/yr), when no read was due — it
    self-clears on the next delivered brief. No 📋/💰/🎯/📡 glyphs in the alarm text: shape
    tests key on those.
    """
    import csv
    import os
    if not os.path.exists(PUSH_LOG):
        return [], [], []
    with open(PUSH_LOG, newline="") as f:
        rows = list(csv.DictReader(f))
    now, out = _utcnow(), []
    for kind, label in (("settle", "settle digest"), ("read", "read brief")):
        mine = [r for r in rows if r.get("kind") == kind]
        if not mine:
            continue
        due = _last_due(kind, now).isoformat()
        if any(r["date_utc"] >= due and r["verdict"] == "DELIVERED" for r in mine):
            continue
        last = mine[-1]
        out.append(f"the {label} for {due} was never confirmed delivered (last {kind} push: "
                   f"{last['date_utc']} {last['verdict']}) — the message died in transport or "
                   f"the run died after it; check that routine's cron.log + Telegram env")
    return out, [], []


def compose(note: str = "", slim: bool = False) -> str:
    """The digest, optionally wrapped around a run note.

    The note's FIRST line is the run's headline and rides on top — it is what Telegram shows in
    the notification preview, and it is the only thing that distinguishes a read push from a
    settle push at a glance. Its BODY (the read run's 5a/5b alert blocks) goes to the BOTTOM:
    those blocks are multi-line context that duplicates the ORDERS section, and stacking them
    above the header buried the DO-NOW list — the one part meant to pull the human back in —
    ~15 lines down the message [2026-08-04].

    slim [2026-08-05, reshaped 2026-08-06, v2 2026-08-14 [ARC 5 #12a]]: the READ push's shape —
    the morning brief the human actually reads. It KEEPS the 🎯 POOL scoreboard (the verdict
    headline leads BOTH legs — the owner's one ask), the book line and the DO-NOW list + run
    note; it DROPS what settle's 📋 owns: the bets/movers state lines, the ORDERS display
    block, and the 📋 banner. Deterministic, not diff-based. DO-NOW actions are never slimmed.
    """
    head, _, body = note.partition("\n")
    bets_s, movers_s = _safe(_bets_section, "bets"), _safe(_movers_section, "movers")
    if slim:
        # The 📖 drops the bets/movers state lines — settle's 📋 owns them, and the morning
        # read of them is noise beside the positions [2026-08-06]. Display lines only: their
        # ACTIONS (stuck settlements etc.) always ride.
        bets_s, movers_s = (bets_s[0], bets_s[1], []), (movers_s[0], movers_s[1], [])
    sections = [_safe(_book_section, "book"),
                _safe(lambda: _orders_section(slim), "orders"),
                bets_s, movers_s,
                _safe(_git_section, "git"), _safe(_stranded_section, "stranded"),
                _safe(_feed_section, "feed"),
                _safe(_pushlog_section, "push-log")]
    # The scoreboard is composed SEPARATELY from the display sections because it lands above
    # the DO-NOW list rather than in the state block — but it still goes through _safe, so a
    # broken scoreboard becomes a loud DO-NOW instead of silently reverting the message shape.
    board = _safe(_pool_scoreboard, "scoreboard")
    actions = [a for s in sections for a in s[0]] + board[0]
    fyi = [f for s in sections for f in s[1]]
    out = ([f"<b>{_e(head.strip())}</b>", ""] if head.strip() else [])
    # The 📋 banner marks THE full state photo — one per day, the settle push. A slim push with
    # a run-note headline is the 📖 report; giving both messages the same banner is exactly the
    # "which one do I read?" repetition the slim shape exists to end. A headline-less slim run
    # (manual CLI) keeps the banner so the message is never anonymous.
    if not (slim and head.strip()):
        out += [f"📋 <b>DIGEST {date.today().isoformat()}</b>", ""]
    # v2: the scoreboard leads BOTH legs — performance-vs-bar is the headline everywhere.
    out += board[2] + ([""] if board[2] else [])
    if actions:
        out.append(f"⚠️ <b>DO NOW ({len(actions)})</b>")
        for i, a in enumerate(actions):
            first, *rest = a.split("\n")
            out.append(f"{i + 1}. {first}")
            out += rest
    else:
        out.append("✅ <b>DO NOW: nothing</b> — next: bet maturity or next read run")
    if fyi:
        out.append("heads-up: " + " · ".join(fyi))
    # Skip a section with nothing to show. The alarm sections (git/stranded/feed/liveness) only
    # ever return DO-NOW actions, never display lines, so an unconditional separator printed FOUR
    # blank lines into every message — a wall of dead space right where the eye stops reading.
    for s in sections:
        if not s[2]:
            continue
        out.append("")
        out += s[2]
    if body.strip():
        out += ["", "📖 <b>RUN NOTE</b>", _e(body.strip())]
    out += ["", "full: bets show · orders show"]
    return "\n".join(out)


def _plain(text: str) -> str:
    """Terminal view: drop the telegram markup."""
    return html.unescape(re.sub(r"</?(b|i|code|pre)>", "", text))


def run(argv: list[str]) -> int:
    note = " ".join(a for a in argv if not a.startswith("--"))   # optional run note (1st line = headline)
    text = compose(note, slim="--slim" in argv)
    print(_plain(text))
    if "--notify" in argv:
        # The printed verdict is the ONLY truth about delivery — exit 1 covers BOTH non-delivered
        # states so daily.sh's FAILS accounting is unchanged. A routine may re-send ONLY on
        # REJECTED: on UNCONFIRMED the message may already be delivered and a re-send
        # double-posts (the 2026-07-24 bug; improvised again 2026-08-06 as a "delivery check").
        # A death ANYWHERE below must still stamp + print a verdict: on 2026-08-07 a cold
        # container without python-dotenv killed the import here AND the heartbeat's — no
        # stamp, no verdict, no alarm, total silence (FINDINGS 2026-08-08).
        try:
            from research import notify
        except Exception as e:      # import death → nothing was ever sent → safe to re-send
            log.error("notify unavailable (%s) — push not attempted", e)
            ok = False
        else:
            try:
                ok = notify.send(text, html=True)
            except Exception as e:  # send() is documented fail-soft; an escape here MAY be
                log.error("notify.send raised (%s)", e)   # post-request → treat as ambiguous
                ok = None
        try:
            _log_push("read" if "--slim" in argv else "settle",
                      "DELIVERED" if ok else ("UNCONFIRMED" if ok is None else "REJECTED"))
        except Exception as e:   # the stamp must never cost the push path
            log.warning("push-log stamp failed (%s) — delivery verdict unrecorded", e)
        if ok:
            print("PUSH DELIVERED")
        elif ok is None:
            print("PUSH UNCONFIRMED — may be delivered; do NOT re-send")
            return 1
        else:
            print("PUSH REJECTED (nothing sent — safe to re-send once)")
            return 1
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(run(sys.argv[1:]))
