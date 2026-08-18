"""ONE glanceable daily pulse + a strict alarm channel — digest v3 [MSG 2026-08-18].

WHAT TELEGRAM MEANS in the paper regime (owner rethink, 2026-08-18): the v2 message was a
broker terminal with the broker deleted — the owner skipped POOL/DO-NOW/BOOK/ORDERS/MOVERS
and the "full:" footer. v3 gives Telegram three jobs and nothing else:
  1. a PULSE of a growing experiment — 🧪 (n of 30 settled · c of n beat · median · the bar)
     leads BOTH legs in plain English, 📈 says what's open and when evidence next lands;
  2. an ALARM channel — ⚠️ DO-NOW appears ONLY when something broke or needs the human
     (an empty list prints NOTHING; 🚨 is reserved for failures: heartbeat + watchdog);
  3. later, the X mirror — at P7b activation every post mirrors here as 📣 (locked req).
Stats vocabulary (Σ pp, Wilcoxon p, α), the shorts diagnostic, orders/band state, movers
denominators and the mix mirror are CLI-side ONLY: `python3 -m research`, `bets show`,
`orders show`, `movers show`. Committed dashboards stay the public page's job.

Shape, in order: headline (read passes its own "📖 READ …" first line; settle gets the
"📋 SETTLE <dow> <date>" banner) → 🧪 scoreboard (+🏁 milestone / PASS-CANDIDATE when
crossed) → ⚠️ DO-NOW (only when nonempty, paste-ready commands) → the run note body (the
read's 🟢 NEW BET cards) → 📈 open-bets line. Composed from the silos FAIL-SOFT per section —
a broken silo degrades to a loud DO-NOW + an "unavailable" line, never a crashed run.

Sent as Telegram HTML (tags never span lines — notify truncates at a newline); printed
locally with tags stripped. All dynamic free text is escaped here — notify stays transport-only.

`--slim` marks the READ leg for the push-log calendar (research/data/push_log.csv) and no
longer changes composition: the headline is the leg's identity. Delivery machinery is
UNCHANGED from v2 — push_log stamps, delivery verdicts, the UNCONFIRMED re-send rules.

  python3 -m research.digest                       # print it
  python3 -m research.digest --notify              # print + Telegram push (exit 1 on failed send)
  python3 -m research.digest --notify "📖 READ …"  # + a run note: 1st line = the headline,
                                                  #   the rest (🟢 cards) rides after the 🧪 block
"""
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
_e = html.escape

# _book_section, _orders_section, _movers_section (+ _marks/_pnl_pct/_money/CASH_EQUIV) and
# the Δ-since-HEAD line (+ _row_id/_by_id) were DELETED in v3 [MSG 2026-08-18]: the book is
# TERMINAL [ARC 5 #12] (its tombstone line taught its lesson), orders/movers are diagnostics
# the owner never read on his phone, and the Δ line was plumbing news. Their lessons stay in
# git history and FINDINGS (SPCX prose-lock 2026-08-02, NIO target 2026-08-04, the batch-write
# row identity 2026-08-04). A re-funded book gets a fresh digest design, never a blind revert.


def _git(*args: str) -> str:
    """One git read. Raises on any failure — each caller decides what silence means."""
    return subprocess.run(("git",) + args, capture_output=True, text=True,
                          timeout=20, check=True).stdout


def _committed(path: str) -> list[dict]:
    """A ledger as of HEAD — the last state this repo PUBLISHED. Raises if git can't answer.

    Deliberately NOT a state file. A cloud checkout is ephemeral, so anything the digest wrote
    would have to be committed to survive, and the read run commits BEFORE it pushes
    (READ_LOOP steps 6 then 7) — its own write could never land. git already holds the previous
    copy of every ledger, and the commit state is exactly the answer to "since when": on settle
    the scoring is still uncommitted (so a crossing is what THIS run just scored), on read it
    is already committed (so it can never false-banner). Same trick and the same reason as
    watchdog.last_commit_epoch.
    """
    import csv
    import io
    return list(csv.DictReader(io.StringIO(_git("show", f"HEAD:{path}"))))


def _row_id(r: dict) -> tuple:
    """Identity of a ledger row across two copies of the file.

    (logged_at|seen_at, ticker) — NOT the timestamp alone. A batch write stamps every row in it
    with the same second, and timestamps in the live catalogue are shared by two bets each
    (META/NFLX, BB/OXM…). Keying on the timestamp collapses those pairs, and the survivor gets
    compared against the wrong row — which reported a bet as newly SCORED on a day nothing
    settled at all. Caught on the Δ band's first live render [2026-08-04]. The Δ line died in
    v3 [MSG 2026-08-18]; pulse.py's newly-scored gate is the surviving consumer.
    """
    return (r.get("logged_at") or r.get("seen_at", ""), r.get("ticker", ""))


def _by_id(rows: list[dict]) -> dict:
    return {_row_id(r): r for r in rows}


def _pool_scoreboard() -> tuple[list, list]:
    """🧪 — the plain-English scoreboard that LEADS BOTH legs [MSG v3; headline rule from
    ARC 5 #12a]. Counts over percentages ("2 of 6 beat"), the bar in words, and NO stats
    vocabulary — Σ/p/α live in `python3 -m research` / `bets show`, where the owner reads
    them at a desk, not on a phone.

    🏁 milestone: a STATELESS crossing check vs the HEAD copy of the catalogue. Works because
    daily.sh runs the digest BEFORE push_ledgers commits (REORDER daily.sh AND MILESTONES
    SILENTLY STOP FIRING — this comment is the guard); the read leg commits first
    (READ_LOOP step 6), so its diff is empty and it can never false-banner. No internal
    try/except: dead git kills the WHOLE scoreboard loudly via _safe instead of half-degrading
    into a message that looks normal.

    Display only — the scoreboard never asks for anything.
    """
    from research import bets
    rows = bets._load()
    now_n = len(bets.excess_values(bets.verdict_rows(rows)))
    prev_n = len(bets.excess_values(bets.verdict_rows(_committed(bets.CATALOGUE))))
    lines = []
    for mst in (10, 20, 30):
        if prev_n < mst <= now_n:
            lines.append(f"🏁 <b>MILESTONE</b> n={mst} settled longs — review rides the next "
                         f"read run [ARC 5 #12a]")
    bar = f"(bar: +{bets.BAR_MEDIAN:.0f}% median, {bets.BAR_BEAT:.0f}% beat)"
    s = bets.stats(rows)
    if s:
        n, _, md, beat = s
        c = round(n * beat / 100)          # beat% round-trips exactly back to its count
        line = f"🧪 <b>{n} of {bets.BAR_N}</b> settled · {c} of {n} beat · median {md:+.1f}% {bar}"
        if n >= bets.BAR_N:
            line += " — AT BAR: verdict time"
        lines.append(line)
        # Below-bar shape flag from n≥10 [ARC 5 #12a]: labeled so it can never be quoted as a
        # pass — nothing passes before N≥BAR_N, and the Wilcoxon only counts AT the bar.
        if n >= 10 and md > bets.BAR_MEDIAN and beat > bets.BAR_BEAT:
            lines.append(f"PASS-CANDIDATE (below-bar, n&lt;{bets.BAR_N}): shape clears "
                         f"median/beat — nothing passes before N≥{bets.BAR_N}")
    else:
        lines.append(f"🧪 <b>0 of {bets.BAR_N}</b> settled {bar}")
    return [], lines


def _bets_section() -> tuple[list, list]:
    """📈 — one line: how much is open and when evidence next lands. Under a LOW-edge prior
    "nothing to do" is the honest message most days; the dated next-settle is what tells the
    owner waiting IS the plan. The STUCK alarm survives from v2 unchanged."""
    from research import bets
    rows = bets._load()
    open_ = [r for r in rows if r["status"] == "open"]
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
            # on time). Past that buffer the bet is not scoring — a genuinely stuck one
            # (bad/delisted ticker, dead price feed) must leave the passive count and alarm.
            if days_left < -OVERDUE_D:
                stuck.append(f"{_e(r['ticker'])} overdue {-days_left}d")
            elif days_left <= 5:
                soon.append(r["ticker"])
        except Exception:
            pass
    line = f"📈 {len(open_)} open"
    nxt = bets.next_maturity(rows)
    if nxt:
        dow = date.fromisoformat(nxt[0]).strftime("%a")
        line += f" · next settle {dow} {nxt[0][5:]} ({_e(nxt[1])})"
        if len(soon) > 1:
            line += f" · {len(soon) - 1} more ≤5d"
    actions = ([f"settlement STUCK: {', '.join(stuck)} — matured but not scoring; "
                f"check the ticker + price feed (<code>python3 -m research.bets settle</code>)"]
               if stuck else [])
    return actions, [line]


def _safe(fn, name: str) -> tuple[list, list]:
    """Fail-soft per silo — but LOUD. A dead silo used to degrade to a quiet trailing line,
    so the insider ledger (meant to be the 2nd verdict silo, retired 2026-08-02 — the project
    runs on ONE) could stop accruing evidence for weeks with nothing escalating. Fail-soft keeps
    the run alive; it must not keep it quiet."""
    try:
        return fn()
    except Exception as e:
        log.debug("%s section failed: %s", name, e)
        return ([f"{name} silo DOWN ({_e(type(e).__name__)}) — evidence is NOT accruing; "
                 f"check cron.log"], [f"{name}: unavailable ({_e(type(e).__name__)})"])


def _git_section() -> tuple[list, list]:
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
        return [], []
    if dirty or ahead:
        what = "uncommitted" if dirty else "unpushed"
        return ([f"ledger changes are {what} — any bet in this message is NOT scored yet; "
                 f"commit + push research/*.csv"], [])
    return [], []


def _stranded_section() -> tuple[list, list]:
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
        return [], []
    actions = []
    for line in out.strip().splitlines():
        sha, _, ref = line.partition("\t")
        name = ref.removeprefix("refs/heads/")
        actions.append(
            f"STRANDED settle work on <code>{name}</code> ({sha[:9]}) — a push failed and the "
            f"run's ledgers never reached master. Recover:\n"
            f"<code>git fetch origin {name} &amp;&amp; git cherry-pick {sha[:9]} &amp;&amp; "
            f"git push origin master &amp;&amp; git push origin --delete {name}</code>")
    return actions, []


def _feed_section() -> tuple[list, list]:
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
        return [], []                            # never written yet — nothing to claim
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
    return out, []


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


def _pushlog_section() -> tuple[list, list]:
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
    self-clears on the next delivered brief. No 📋/🧪/📊 glyphs in the alarm text: shape
    tests key on those.
    """
    import csv
    import os
    if not os.path.exists(PUSH_LOG):
        return [], []
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
    return out, []


def compose(note: str = "") -> str:
    """The v3 message, optionally wrapped around a run note.

    The note's FIRST line is the run's headline and rides on top — it is what Telegram shows
    in the notification preview, and it is the leg's identity (READ_LOOP step 7 mandates a
    "📖 READ …" headline). No headline → the "📋 SETTLE <dow> <date>" banner, so a message is
    never anonymous. The note's BODY (the read's 🟢 NEW BET cards) lands right after the 🧪
    block and any ⚠️ list — the cards are the morning's news, not a footnote [MSG v3; the v2
    bottom-of-message RUN NOTE block buried them].

    Contiguous lines by design — the whole point is a message that fits one phone glance.
    The only blank line precedes the ⚠️ DO-NOW block, and an empty DO-NOW prints NOTHING:
    the absence of ⚠️ IS the all-clear (the owner skipped "✅ DO NOW: nothing" every day).
    DO-NOW actions are never dropped or summarized.
    """
    head, _, body = note.partition("\n")
    sections = [_safe(_bets_section, "bets"),
                _safe(_git_section, "git"), _safe(_stranded_section, "stranded"),
                _safe(_feed_section, "feed"), _safe(_pushlog_section, "push-log")]
    # The scoreboard is composed separately because it leads the message — but it still goes
    # through _safe, so a broken scoreboard is a loud DO-NOW, never a silent shape-revert.
    board = _safe(_pool_scoreboard, "scoreboard")
    actions = board[0] + [a for s in sections for a in s[0]]
    if head.strip():
        out = [f"<b>{_e(head.strip())}</b>"]
    else:
        today = date.today()
        out = [f"📋 <b>SETTLE {today.strftime('%a')} {today.isoformat()}</b>"]
    out += board[1]
    if actions:
        out += ["", f"⚠️ <b>DO NOW ({len(actions)})</b>"]
        for i, a in enumerate(actions):
            first, *rest = a.split("\n")
            out.append(f"{i + 1}. {first}")
            out += rest
    if body.strip():
        out.append(_e(body.strip()))
    for s in sections:
        out += s[1]
    return "\n".join(out)


def _plain(text: str) -> str:
    """Terminal view: drop the telegram markup."""
    return html.unescape(re.sub(r"</?(b|i|code|pre)>", "", text))


def run(argv: list[str]) -> int:
    note = " ".join(a for a in argv if not a.startswith("--"))   # optional run note (1st line = headline)
    text = compose(note)
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
        # `--slim` = the READ leg's stamp [v3: its only remaining job — composition no longer
        # branches on it; the headline is the leg's identity]. Renaming the flag would break
        # the cloud routine prompts, so it keeps its historical name.
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
