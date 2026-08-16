"""The LIVE book — the user's REAL-MONEY account (~$6-8k, capital being added), tracked so we
learn to run it well. REAL money as of 2026-07-06 — no more "paper/roleplay" framing.

SEPARATE from bets.py on purpose: bets.py scores forward PREDICTIONS (%-excess vs a
benchmark) and feeds the ARC5#1 skill verdict; this tracks DOLLARS — sized positions, stops,
cash, realized P&L. The user executes on Robinhood/E*Trade and reports fills; we record and
weigh each as a real financial decision. Keeping the two silos separate is MORE important now,
not less: real-money churn must never pollute the honest skill-verdict N. Goal = real growth
UNDER the honest prior (LOW edge) — don't-lose-it + cheap beta + capped experiments while the
forward ledgers accrue evidence. Harnesses pre-registered in FINDINGS [ARC 5 #4].

  python3 -m research.book seed         one-time: load real holdings at cost + cash baseline
  python3 -m research.book open  TICKER long|short SHARES ENTRY STOP TARGET HORIZON_d "thesis"
  python3 -m research.book close TICKER EXIT [SHARES]   (SHARES omitted = close full)
  python3 -m research.book stop  TICKER PRICE [note]    set/replace an exit rule on an open lot
  python3 -m research.book target TICKER PRICE [note]   set/replace the exit-into-strength level (0 clears)
  python3 -m research.book mark         fetch live prices -> equity, P&L, vs same-$-in-SPY
  python3 -m research.book show         print the book (no network)
"""
import csv
import logging
import os
import sys
from datetime import datetime, timezone

from research import prices

log = logging.getLogger(__name__)
BOOK = "research/book.csv"
EQUITY_LOG = "research/book_equity.csv"   # daily mark, one row per date (tracked in git)
EQUITY_FIELDS = ["date", "equity", "cash", "unrealized", "realized",
                 "spy_equiv", "dualmom_equiv"]
CASH_T, SEED_T = "__CASH__", "__SEED__"
RETIRED_T = "__RETIRED__"  # terminal meta row [ARC 5 #12]: the book is CLOSED, capital exited;
                           # its `entry` cell records the swept cash, its opened_at the date.
                           # Same meta-row pattern as __CASH__/__SEED__ — state lives in the
                           # ledger itself, never in a side file.
POOL_STOP = 0.40          # whole-pool hard stop: halt if equity < (1-0.40)*seed [ARC5#4] —
                          # the ONE circuit breaker kept after the [ARC5#6] harness loosening;
                          # the 35%-max-play sizing cap was LIFTED there (deploy aggressively).
MARK_EPS = 1.00           # $ — two marks this close are THE SAME MARK. This is the resolution of
                          # the equity curve's own columns (feed noise + 2dp rounding across a
                          # handful of positions), NOT a policy threshold, which is why it lives
                          # here beside them rather than in config.py.
PMAP = {"XRP": "XRP-USD"}  # yfinance crypto suffix
FIELDS = ["opened_at", "ticker", "side", "shares", "entry", "stop", "target",
          "horizon_d", "thesis", "status", "closed_at", "exit", "realized_pnl"]

# PRIVATE seed: real holdings live in a GITIGNORED file, NEVER hardcoded in this committed source.
# Format (CSV): ticker,shares,cost,note  — plus one row `__CASH__,,<amount>,` for blended free cash.
# List a locked lot BEFORE its liquid twin so a default `close TICKER` targets the tradeable lot.
SEED_FILE = "research/book_seed.csv"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load() -> list[dict]:
    if not os.path.exists(BOOK):
        return []
    with open(BOOK, newline="") as f:
        return list(csv.DictReader(f))


def _save(rows: list[dict]) -> None:
    with open(BOOK, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(rows)


def _spot(ticker: str) -> float | None:
    bars = prices.daily_bars(PMAP.get(ticker, ticker), 1)
    return bars[-1]["close"] if bars else None


def through_stop(side: str, spot: float | None, stop: float) -> bool:
    """Has price crossed the exit rule? ONE direction-aware definition, shared.

    Lived inline in digest._book_section until 2026-08-03, when orders.py needed the same
    test — a second copy of a sign-sensitive predicate is how a short silently stops reporting.
    """
    if not spot or stop <= 0:
        return False
    return spot <= stop if side == "long" else spot >= stop


def through_target(side: str, spot: float | None, target: float) -> bool:
    """Has price reached the exit-into-strength band? through_stop's mirror [2026-08-04].

    0/blank target = "no target", same convention as a retired stop. Meta rows never reach
    this: __SEED__ overloads its target cell with the seed-date SPY close (see equity_marks),
    but position logic filters to status=="open" tickers first.
    """
    if not spot or target <= 0:
        return False
    return spot >= target if side == "long" else spot <= target


def _cash(rows: list[dict]) -> float:
    for r in rows:
        if r["ticker"] == CASH_T:
            return float(r["entry"])
    return 0.0


def _set_cash(rows: list[dict], v: float) -> None:
    for r in rows:
        if r["ticker"] == CASH_T:
            r["entry"] = f"{v:.2f}"; return
    rows.append({**{k: "" for k in FIELDS}, "ticker": CASH_T, "status": "cash", "entry": f"{v:.2f}"})


def _seed_row(rows: list[dict]) -> dict | None:
    return next((r for r in rows if r["ticker"] == SEED_T), None)


def _retired_row(rows: list[dict]) -> dict | None:
    return next((r for r in rows if r.get("ticker") == RETIRED_T), None)


def is_retired(rows: list[dict]) -> bool:
    """Terminal state [ARC 5 #12]: every position closed, cash swept out, experiment over."""
    return _retired_row(rows) is not None


def retired_line(rows: list[dict]) -> str:
    """The ONE line a closed book ever prints. No network, no marks — the POOL-STOP print and
    the stop/target logic are unreachable from here, which is the point: a swept book sits
    below the pool floor forever, and an unclearable alarm is forbidden [FINDINGS 2026-08-02]."""
    r = _retired_row(rows)
    day = (r.get("opened_at") or "")[:10] if r else ""
    return (f"BOOK CLOSED {day} — capital exited [ARC 5 #12]; verdict: FINDINGS closing entry · "
            f"book.csv/book_equity.csv frozen as evidence")


def retire(rows: list[dict]) -> bool:
    """Close the book for good: sweep remaining cash to $0 and stamp the __RETIRED__ meta row.
    Returns True if the ledger changed. Refuses while ANY position is open (close them with
    real fills first — the closing verdict needs the final numbers) and refuses twice."""
    if is_retired(rows):
        print(retired_line(rows)); return False
    if _open_positions(rows):
        print(f"refusing to retire: {len(_open_positions(rows))} position(s) still open — "
              f"`book close` each with its real fill first"); return False
    swept = _cash(rows)
    _set_cash(rows, 0.0)
    rows.append({**{k: "" for k in FIELDS}, "ticker": RETIRED_T, "status": "meta",
                 "opened_at": _now()[:10], "entry": f"{swept:.2f}",
                 "thesis": "capital exited [ARC 5 #12] — closing verdict in FINDINGS"})
    print(f"RETIRED — swept ${swept:,.2f} out; book is terminal. Log the CLOSING VERDICT entry "
          f"in FINDINGS (final mark vs SPY/dual-mom) if not already done.")
    return True


def _open_positions(rows: list[dict]) -> list[dict]:
    return [r for r in rows if r["status"] == "open"]


def seed(rows: list[dict]) -> None:
    if rows:
        print("book already seeded — refusing to overwrite"); return
    if not os.path.exists(SEED_FILE):
        print(f"no {SEED_FILE} (gitignored, private) — create it from your FINANCES: "
              f"ticker,shares,cost,note rows + a __CASH__,,<amount>, row"); return
    with open(SEED_FILE, newline="") as f:
        spec = list(csv.DictReader(f))
    spy, equity, cash, n = _spot("SPY"), 0.0, 0.0, 0
    for s in spec:
        if s["ticker"] == CASH_T:
            cash = float(s["cost"]); equity += cash; continue
        sh, cost = float(s["shares"]), float(s["cost"])
        rows.append({"opened_at": _now()[:10], "ticker": s["ticker"], "side": "long",
                     "shares": str(sh), "entry": f"{cost:.2f}", "stop": "", "target": "",
                     "horizon_d": "", "thesis": s.get("note", ""), "status": "open",
                     "closed_at": "", "exit": "", "realized_pnl": ""})
        spot = _spot(s["ticker"]); equity += sh * (spot if spot else cost); n += 1
    _set_cash(rows, cash)
    rows.append({**{k: "" for k in FIELDS}, "ticker": SEED_T, "status": "meta",
                 "opened_at": _now()[:10], "entry": f"{equity:.2f}",
                 "target": f"{spy:.2f}" if spy else ""})
    print(f"SEEDED from {SEED_FILE}: {n} positions + ${cash:.0f} cash | "
          f"baseline equity ${equity:,.0f} (today's market) | SPY ref {spy:.2f}")


def open_(rows, ticker, side, shares, entry, stop, target, horizon, thesis) -> None:
    if side not in ("long", "short"):
        print("side must be long|short"); return
    shares, entry, stop, target = float(shares), float(entry), float(stop), float(target)
    cost = shares * entry
    cash = _cash(rows)
    if side == "long" and cost > cash + 1e-6:
        print(f"insufficient cash: play ${cost:,.0f} > free ${cash:,.0f}"); return
    # Sizing cap lifted [ARC5#6] — size aggressively on conviction; the -40% POOL_STOP
    # (checked in mark) is the only backstop. Cash-sufficiency above still binds.
    _set_cash(rows, cash - cost if side == "long" else cash + cost)
    rows.append({"opened_at": _now(), "ticker": ticker.upper(), "side": side, "shares": str(shares),
                 "entry": f"{entry:.4f}", "stop": f"{stop:.4f}", "target": f"{target:.4f}",
                 "horizon_d": str(horizon), "thesis": thesis, "status": "open",
                 "closed_at": "", "exit": "", "realized_pnl": ""})
    print(f"OPEN {side} {shares:g} {ticker.upper()} @ {entry:.2f} stop {stop:.2f} "
          f"target {target:.2f} | free cash now ${_cash(rows):,.0f}")
    _warn_no_twin(ticker, side)


def _warn_no_twin(ticker: str, side: str) -> None:
    """WARN (never block) when a position has no pre-registered bet twin [2026-08-02, user call].

    A real-money position with no scored twin produces P&L but no learning: it can never reach
    the pooled verdict, so the book churns while the skill question stays at n=6. READ_LOOP 5b
    already pre-registers read-generated trades; this covers the DISCRETIONARY ones, which is
    where the rule actually bites.

    Deliberately non-blocking. The book's job is to record what really happened at the broker —
    refusing a real fill because its paperwork is missing would corrupt the ledger to enforce a
    process rule, which is backwards. Fail-soft on a bad/absent catalogue for the same reason.
    """
    try:
        from research import bets
        twin = [r for r in bets._load()
                if r["ticker"].upper() == ticker.upper()
                and r["direction"] == side and r["status"] == "open"]
    except Exception:
        return
    if not twin:
        print(f"  ⚠️  no pre-registered bet for {side} {ticker.upper()} — this position scores "
              f"$ P&L but contributes NOTHING to the verdict. Register the twin:\n"
              f"     python3 -m research.bets add {ticker.upper()} {side} 63 SPY "
              f'"<thesis>" --tag=<scenario>')


def close_(rows, ticker, exit_price, qty=None) -> None:
    """Close a position fully, or partially if qty < shares held (real fills arrive in pieces)."""
    exit_price = float(exit_price)
    pos = [r for r in rows if r["ticker"] == ticker.upper() and r["status"] == "open"]
    if not pos:
        print(f"no open position in {ticker}"); return
    r = pos[-1]
    held, en, side = float(r["shares"]), float(r["entry"]), r["side"]
    sh = held if qty is None else float(qty)
    if sh > held + 1e-9:
        print(f"only {held:g} {ticker.upper()} held — can't close {sh:g}"); return
    pnl = sh * (exit_price - en) if side == "long" else sh * (en - exit_price)
    _set_cash(rows, _cash(rows) + (sh * exit_price if side == "long" else -sh * exit_price))
    if sh < held - 1e-9:                       # partial: shrink open row, append closed slice
        rows.append({**r, "shares": f"{sh:g}", "status": "closed", "closed_at": _now(),
                     "exit": f"{exit_price:.4f}", "realized_pnl": f"{pnl:.2f}"})
        r["shares"] = f"{held - sh:g}"
        tag = f" (partial — {held - sh:g} left open)"
    else:
        r.update(status="closed", closed_at=_now(), exit=f"{exit_price:.4f}", realized_pnl=f"{pnl:.2f}")
        tag = ""
    print(f"CLOSE {side} {sh:g} {ticker.upper()} @ {exit_price:.2f} -> realized ${pnl:+,.0f}{tag} | "
          f"free cash now ${_cash(rows):,.0f}")


def stop_(rows, ticker, price, note=None) -> None:
    """Set/replace the stop on the latest open position for TICKER. Documentation of the
    exit rule — enforcement is manual (surfaced by digest / checked at mark), like every
    other stop here. Optional note is appended to the thesis."""
    price = float(price)
    pos = [r for r in rows if r["ticker"] == ticker.upper() and r["status"] == "open"]
    if not pos:
        print(f"no open position in {ticker}"); return
    r = pos[-1]
    r["stop"] = f"{price:.4f}"
    if note:
        r["thesis"] = (r["thesis"] + " | " + note).strip(" |")
    print(f"STOP {ticker.upper()} set {price:.2f}" + (f" — {note}" if note else "")
          + f" (position {float(r['shares']):g} @ {float(r['entry']):.2f})")


def target_(rows, ticker, price, note=None) -> None:
    """Set/replace the exit TARGET (the sell-into-strength level) on the latest open position.

    stop_'s mirror. The `target` column existed since seed and was write-only — NIO's exit
    band lived in thesis PROSE, the market touched it (high 4.94 vs band 4.85-5.15, 7/24-8/4)
    and nothing noticed [FINDINGS 2026-08-04]. Structured facts get a column. 0 clears it.
    Enforcement stays manual: the digest nags, the human works the limit at the broker.
    """
    price = float(price)
    pos = [r for r in rows if r["ticker"] == ticker.upper() and r["status"] == "open"]
    if not pos:
        print(f"no open position in {ticker}"); return
    r = pos[-1]
    r["target"] = f"{price:.4f}" if price > 0 else ""
    if note:
        r["thesis"] = (r["thesis"] + " | " + note).strip(" |")
    print((f"TARGET {ticker.upper()} set {price:.2f}" if price > 0
           else f"TARGET {ticker.upper()} cleared") + (f" — {note}" if note else "")
          + f" (position {float(r['shares']):g} @ {float(r['entry']):.2f})")


def equity_marks(rows: list[dict]) -> dict:
    """Mark the book once: equity, P&L, and both opportunity-cost yardsticks.

    The single computation behind BOTH the `mark` display and the `snapshot` row, so the
    printed number and the logged number can never disagree. Per-position display lines are
    returned alongside the totals rather than printed, keeping the math out of the I/O.
    Missing prices degrade to None fields — never an exception, this runs unattended.
    """
    cash = _cash(rows)
    equity, unreal, lines, spots = cash, 0.0, [], {}
    for r in _open_positions(rows):
        sh, en = float(r["shares"]), float(r["entry"])
        spot = _spot(r["ticker"])
        spots[r["ticker"]] = spot          # every caller's per-position price, fetched ONCE here
        if spot is None:
            lines.append(f"  {r['side']:>5} {r['ticker']:>5} {sh:g} @ {en:.2f}  (no price)")
            continue
        pnl = sh * (spot - en) if r["side"] == "long" else sh * (en - spot)
        equity += sh * spot * (1 if r["side"] == "long" else -1)
        unreal += pnl
        # a retired stop is stored as 0 (see the SPCX stub) — that is "no stop", not a stop at
        # zero, so it must not print as one
        stp = f" stop {float(r['stop']):.2f}" if r["stop"] and float(r["stop"]) > 0 else ""
        lines.append(f"  {r['side']:>5} {r['ticker']:>5} {sh:g} @ {en:6.2f} -> {spot:6.2f}  "
                     f"P&L ${pnl:+,.0f} ({pnl/(sh*en)*100:+.0f}%){stp}")
    realized = sum(float(r["realized_pnl"]) for r in rows
                   if r["status"] == "closed" and r["realized_pnl"])
    m = {"cash": cash, "equity": equity, "unrealized": unreal, "realized": realized,
         "lines": lines, "spots": spots, "seed": None, "spy_equiv": None,
         "dualmom_equiv": None, "dualmom_hold": None}
    sr = _seed_row(rows)
    if not (sr and sr["entry"]):
        return m
    seed_eq = float(sr["entry"])
    m["seed"] = seed_eq
    if sr["target"]:                       # seed-date SPY close, stored at seed time
        spy = _spot("SPY")
        if spy:
            m["spy_equiv"] = seed_eq * spy / float(sr["target"])
    # 2nd yardstick: same-$-in-(current dual-mom hold) — the real passive opp cost [ARC5#7].
    try:
        from research import dualmom
        hold = dualmom.current_hold()
        base, spot = prices.bars_after(hold, sr["opened_at"][:10], 5), _spot(hold)
        if base and spot:
            m["dualmom_hold"] = hold
            m["dualmom_equiv"] = seed_eq * spot / base[0]["close"]
    except Exception as e:
        log.debug("dual-mom yardstick skipped: %s", e)
    return m


def pool_floor(seed_eq: float) -> float:
    """The equity level at which the whole-pool circuit breaker trips [ARC5#4]. ONE definition,
    shared by `mark`'s check and the digest's daily display — a threshold with two call sites is
    a threshold that eventually disagrees with itself."""
    return (1 - POOL_STOP) * seed_eq


def _f(v) -> float | None:
    """A CSV cell or a marks field as a float — None when absent or blank."""
    return None if v is None or v == "" else float(v)


def mark_delta(prev: dict, m: dict) -> dict:
    """Change from a COMMITTED equity row to a live mark. PURE (no I/O), so it is testable
    against the real curve rather than a fixture.

    -> {d_equity, d_perf, unexplained, pct, gap, d_gap, flat, clean}

    **A period's P&L is `d_unrealized + d_realized`. Never `d_equity`.** Equity moves for reasons
    that are not performance, and this function exists to keep those out of a money message:

      - a DEPOSIT or withdrawal moves equity and cash together (the book takes real deposits);
      - a SCOPE correction removes a position by fiat — 2026-08-02→03 took a long-realm holding
        out and left a -$1,950 step that reads as a -35.7% day that never happened;
      - opening or closing a position moves cash and basis against each other.

    An earlier attempt tested `d_equity == d_cash + d_unrealized` (basis untouched) and used
    that to refuse a %. It got BOTH of the first two wrong: a deposit satisfies that identity
    exactly (so it printed as a gain), while an ordinary `book open` violates it (so a real
    trading day printed as "not P&L"). Both were caught in review before shipping. Measured on
    the real curve, `d_unrealized + d_realized` equals `d_equity` on every clean day and reports
    the scope-removal day as its true **-$30.01**.

    `unexplained = d_equity - d_perf` is then exactly the money that entered or left by fiat —
    worth SAYING, but never counted as a result. `clean` is `unexplained ~= 0`. When it is not
    clean, `d_gap` is None: `spy_equiv` is anchored to the seed, so a deposit or a restatement
    moves the gap without anyone winning or losing a race.
    """
    p_eq, p_unreal = _f(prev.get("equity")), _f(prev.get("unrealized"))
    p_real, p_spy = _f(prev.get("realized")), _f(prev.get("spy_equiv"))
    eq, unreal = _f(m.get("equity")), _f(m.get("unrealized"))
    real, spy = _f(m.get("realized")), _f(m.get("spy_equiv"))
    out = {"d_equity": None, "d_perf": None, "unexplained": 0.0, "pct": None, "gap": None,
           "d_gap": None, "flat": False, "clean": True}
    if p_eq is None or eq is None:
        return out
    out["d_equity"] = out["d_perf"] = eq - p_eq
    if None not in (p_unreal, unreal, p_real, real):
        out["d_perf"] = (unreal - p_unreal) + (real - p_real)
        out["unexplained"] = out["d_equity"] - out["d_perf"]
        out["clean"] = abs(out["unexplained"]) < MARK_EPS
    out["flat"] = abs(out["d_perf"]) < MARK_EPS
    if spy is not None:
        out["gap"] = eq - spy                      # standing vs same-$-in-SPY, always meaningful
    if p_eq:
        out["pct"] = out["d_perf"] / p_eq * 100    # always a REAL return — d_perf excludes fiat
    if spy is not None and p_spy is not None and out["clean"]:
        out["d_gap"] = out["gap"] - (p_eq - p_spy)     # ground GAINED/LOST on SPY this step
    return out


def mark(rows: list[dict]) -> None:
    """Live mark-to-market: equity, unrealized P&L, vs same-$-in-SPY, pool-stop check."""
    if is_retired(rows):
        print(retired_line(rows)); return
    if not rows:
        print("book empty — run: python3 -m research.book seed"); return
    m = equity_marks(rows)
    equity = m["equity"]
    print(f"\nLIVE BOOK ({BOOK})  —  free cash ${m['cash']:,.0f}")
    for line in m["lines"]:
        print(line)
    print(f"  {'-'*52}\n  EQUITY ${equity:,.0f}  | unrealized ${m['unrealized']:+,.0f}  "
          f"realized ${m['realized']:+,.0f}")
    if m["seed"] is None:
        return
    seed_eq = m["seed"]
    line = f"  vs baseline ${seed_eq:,.0f}: {(equity / seed_eq - 1) * 100:+.1f}%"
    if m["spy_equiv"]:
        line += (f"  |  same-$-in-SPY ${m['spy_equiv']:,.0f} "
                 f"({m['spy_equiv'] / seed_eq - 1:+.1%}) ")
        line += "→ BEATING SPY" if equity > m["spy_equiv"] else "→ lagging SPY"
    print(line)
    if m["dualmom_equiv"]:
        tag = "BEATING" if equity > m["dualmom_equiv"] else "lagging"
        print(f"  vs same-$-in-dual-mom ({m['dualmom_hold']}) ${m['dualmom_equiv']:,.0f} "
              f"({m['dualmom_equiv'] / seed_eq - 1:+.1%}) → {tag} dual-mom")
    if equity < pool_floor(seed_eq):
        print(f"  ** POOL STOP HIT (< -{POOL_STOP*100:.0f}%) — halt + log verdict [ARC5#4] **")


def snapshot(rows: list[dict], path: str = EQUITY_LOG) -> dict | None:
    """Append today's mark to the equity curve — idempotent per date (a re-run overwrites).

    `mark` was display-only, so the book was judged point-in-time forever: no path, no
    drawdown, no way to see WHEN it fell behind SPY [ARC5#7 judges the book in dollars vs
    same-$-in-SPY AND same-$-in-dual-mom]. Tracked in git (private repo), which also makes
    the last row a liveness clock: a daily run that stops leaves a visibly stale date.
    """
    if is_retired(rows):
        # The curve's honest endpoint is the LAST pre-retire snapshot (equity == the swept
        # proceeds). A daily $0 row after that would draw an instant -100% cliff that never
        # happened to the capital — it left, it wasn't lost. Frozen means frozen.
        print(retired_line(rows)); return None
    if not rows:
        return None
    m = equity_marks(rows)
    today = datetime.now(timezone.utc).date().isoformat()
    row = {"date": today,
           "equity": f"{m['equity']:.2f}", "cash": f"{m['cash']:.2f}",
           "unrealized": f"{m['unrealized']:.2f}", "realized": f"{m['realized']:.2f}",
           "spy_equiv": f"{m['spy_equiv']:.2f}" if m["spy_equiv"] else "",
           "dualmom_equiv": f"{m['dualmom_equiv']:.2f}" if m["dualmom_equiv"] else ""}
    hist = [r for r in _load_equity(path) if r["date"] != today]
    hist.append(row)
    hist.sort(key=lambda r: r["date"])
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=EQUITY_FIELDS)
        w.writeheader(); w.writerows(hist)
    print(f"snapshot {today}: equity ${m['equity']:,.0f}  cash ${m['cash']:,.0f}"
          + (f"  same-$-SPY ${m['spy_equiv']:,.0f}" if m["spy_equiv"] else ""))
    return row


def _load_equity(path: str = EQUITY_LOG) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def show(rows: list[dict]) -> None:
    if is_retired(rows):
        print(retired_line(rows)); return
    if not rows:
        print("book empty — run: python3 -m research.book seed"); return
    op, cl = _open_positions(rows), [r for r in rows if r["status"] == "closed"]
    print(f"\nlive book ({BOOK}): {len(op)} open, {len(cl)} closed, free cash ${_cash(rows):,.0f}")
    for r in op:
        h = f" {r['horizon_d']}d" if r["horizon_d"] else ""
        print(f"  OPEN  {r['opened_at'][:10]} {r['side']:>5} {r['ticker']:>5} {float(r['shares']):g} "
              f"@ {float(r['entry']):.2f}{h}  {r['thesis'][:60]}")
    for r in cl:
        print(f"  CLOSED {r['ticker']:>5} {r['side']} @ {float(r['entry']):.2f}->{float(r['exit']):.2f} "
              f"realized ${float(r['realized_pnl']):+,.0f}")


def run(argv: list[str]) -> None:
    rows = _load()
    cmd = argv[0] if argv else "show"
    if is_retired(rows) and cmd in ("seed", "open", "close", "stop", "target"):
        # A terminal ledger accepts no mutations — the evidence is frozen [ARC 5 #12].
        print(retired_line(rows)); return
    if cmd == "retire":
        if retire(rows):
            _save(rows)
        return
    if cmd == "seed":
        seed(rows); _save(rows)
    elif cmd == "open":
        open_(rows, argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], " ".join(argv[8:]))
        _save(rows)
    elif cmd == "close":
        close_(rows, argv[1], argv[2], argv[3] if len(argv) > 3 else None); _save(rows)
    elif cmd == "stop":
        stop_(rows, argv[1], argv[2], " ".join(argv[3:]) or None); _save(rows)
    elif cmd == "target":
        target_(rows, argv[1], argv[2], " ".join(argv[3:]) or None); _save(rows)
    elif cmd == "mark":
        mark(rows)
    elif cmd == "snapshot":
        snapshot(rows)
    else:
        show(rows)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    run(sys.argv[1:])
