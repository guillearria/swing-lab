"""[CRASH #2] — the forward PAPER ledger for the crash-day rule (owner, 2026-10-31).

Same trigger as [CRASH #1] (close-to-close <= -20% on >= 3x the prior-20 mean volume, prior-20
median $ volume >= $1M, one per ticker per 63 sessions, share-class twins once), scanned daily
over the CURRENT S&P 500. Tagged at log time: PANIC if SPY closed >= 10% below its 252-session
high that day, else CALM. Paper only: buy the next open, sell the close of session 63, vs SPY
over the same dates, net 0.40%. Survivorship-free by construction: every settle run stamps each
open row's last price, so a name that stops trading settles at its last stamped close instead
of vanishing from the data. Bars + the one-look rule: FINDINGS [CRASH #2].

  python3 -m research.crash_ledger           show (read-only)
  python3 -m research.crash_ledger log       scan the last 10 sessions, append new triggers
  python3 -m research.crash_ledger settle    stamp open rows, score matured ones
"""
import csv
import os
import statistics as st
import sys
from datetime import date

from research import prices, universe
from research.crash_buy import COST, DROP, H, H_DIAG, MIN_DOLLAR_VOL, TWINS, VOL_N, VOL_X

LEDGER = os.path.join(os.path.dirname(__file__), "crash_ledger.csv")
FIELDS = ["trigger_date", "ticker", "drop", "vol_x", "spy_dd", "arm", "beta", "status",
          "last_date", "last_close", "entry_date", "entry", "exit_date", "exit",
          "spy_ret", "x21", "x63", "logged_at"]
FORWARD_START = "2026-11-02"       # first session after the pre-registration
PANIC_DD = -0.10
LOOKBACK = 10                      # sessions re-scanned each run, so a missed day is caught
LOOKS = {"PANIC": 20, "ALL": 30}   # ONE look each: the first N triggers by date …
MIN_MONTHS = 4                     # … extended until they span >= 4 calendar months
MIN_FEED = 0.8                     # fewer members priced than this = a dead feed, exit 1
BENCH = "SPY"


def _load() -> list[dict]:
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER) as f:
        return list(csv.DictReader(f))


def _save(rows: list[dict]) -> None:
    rows.sort(key=lambda r: (r["trigger_date"], r["ticker"]))
    with open(LEDGER, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def _beta(stock: list[dict], spy: list[dict]):
    """Daily-return beta over 250 sessions ending 21 sessions before the trigger (last bar)."""
    s = {b["date"]: b["close"] for b in stock}
    m = {b["date"]: b["close"] for b in spy}
    days = [d for d in sorted(s) if d in m][-(21 + 251):-21]
    if len(days) < 61:
        return ""
    rs = [s[b] / s[a] - 1 for a, b in zip(days, days[1:])]
    rm = [m[b] / m[a] - 1 for a, b in zip(days, days[1:])]
    ms, mm = st.mean(rs), st.mean(rm)
    var = sum((y - mm) ** 2 for y in rm)
    return round(sum((x - ms) * (y - mm) for x, y in zip(rs, rm)) / var, 3) if var else ""


def _triggers(bars: list[dict]) -> list[tuple]:
    out = []
    for i in range(max(VOL_N, len(bars) - LOOKBACK), len(bars)):
        prior = bars[i - VOL_N:i]
        c0, c1 = bars[i - 1]["close"], bars[i]["close"]
        avg = sum(b["volume"] for b in prior) / VOL_N
        dv = sorted(b["close"] * b["volume"] for b in prior)[VOL_N // 2]
        if (c0 > 0 and avg > 0 and c1 / c0 - 1 <= DROP and bars[i]["volume"] >= VOL_X * avg
                and dv >= MIN_DOLLAR_VOL):
            out.append((i, c1 / c0 - 1, bars[i]["volume"] / avg))
    return out


def log(rows: list[dict], members: list[str] | None = None) -> int:
    members = members or universe.sp500()
    spy = prices.daily_history(BENCH, "2y")
    spy_c = {b["date"]: b["close"] for b in spy}
    spy_days = [b["date"] for b in spy]
    have = {(r["ticker"], r["trigger_date"]) for r in rows}
    last_by_tk: dict[str, str] = {}
    for r in rows:
        last_by_tk[r["ticker"]] = max(last_by_tk.get(r["ticker"], ""), r["trigger_date"])
    new, priced = [], 0
    for tk in members:
        bars = prices.daily_history(tk, "6mo")
        if len(bars) < VOL_N + 2:
            continue
        priced += 1
        for i, drop, vx in _triggers(bars):
            d = bars[i]["date"]
            if d < FORWARD_START or (tk, d) in have or d not in spy_c:
                continue
            prev = last_by_tk.get(tk)
            if prev and sum(1 for b in bars if prev < b["date"] <= d) < H:
                continue                                  # one per ticker per 63 sessions
            j = spy_days.index(d)
            dd = spy_c[d] / max(spy_c[x] for x in spy_days[max(0, j - 251):j + 1]) - 1
            new.append({"trigger_date": d, "ticker": tk, "drop": f"{drop:.4f}",
                        "vol_x": f"{vx:.2f}", "spy_dd": f"{dd:.4f}",
                        "arm": "PANIC" if dd <= PANIC_DD else "CALM",
                        "beta": _beta(prices.daily_history(tk, "2y"), spy), "status": "open",
                        "last_date": bars[-1]["date"], "last_close": f"{bars[-1]['close']:.4f}",
                        "logged_at": date.today().isoformat()})
            last_by_tk[tk] = d
            have.add((tk, d))
    if members and priced < MIN_FEED * len(members):
        raise SystemExit(f"crash_ledger log: only {priced}/{len(members)} members priced — feed degraded")
    keys = {(r["trigger_date"], r["ticker"]) for r in rows + new}
    new = [r for r in new if (r["trigger_date"], TWINS.get(r["ticker"])) not in keys]
    rows.extend(new)
    return len(new)


def settle(rows: list[dict]) -> int:
    scored = 0
    for r in rows:
        if r["status"] != "open":
            continue
        bars = prices.bars_after(r["ticker"], r["trigger_date"], H + 5)
        spy = prices.bars_after(BENCH, r["trigger_date"], H + 5)
        if bars:                                           # the survivorship stamp
            r["last_date"], r["last_close"] = bars[-1]["date"], f"{bars[-1]['close']:.4f}"
            if not r["entry"]:
                r["entry_date"], r["entry"] = bars[0]["date"], f"{bars[0]['open']:.4f}"
        if len(spy) < H:
            continue                                       # not matured on the market calendar
        m = {b["date"]: b for b in spy}
        if not r["entry"]:
            r["status"] = "nofill"                         # never traded after the trigger
            continue
        if len(bars) >= H and bars[H - 1]["date"] in m and r["entry_date"] in m:
            ex, r["status"] = bars[H - 1], "settled"
        elif r["last_date"] < spy[H - 1]["date"] and r["last_date"] in m:
            ex, r["status"] = {"date": r["last_date"], "close": float(r["last_close"])}, "delisted"
        else:
            continue                                       # alignment gap — retry next run
        entry, s0 = float(r["entry"]), m[r["entry_date"]]["open"]
        spy_ret = m[ex["date"]]["close"] / s0 - 1
        r["exit_date"], r["exit"], r["spy_ret"] = ex["date"], f"{ex['close']:.4f}", f"{spy_ret:.4f}"
        r["x63"] = f"{ex['close'] / entry - 1 - spy_ret:.4f}"
        if len(bars) >= H_DIAG and bars[H_DIAG - 1]["date"] in m:
            b = bars[H_DIAG - 1]
            r["x21"] = f"{b['close'] / entry - 1 - (m[b['date']]['close'] / s0 - 1):.4f}"
        scored += 1
    return scored


def _net(r: dict) -> float:
    return float(r["x63"]) - COST


def _beta_adj(r: dict) -> float:
    beta = float(r["beta"]) if r["beta"] else 1.0
    return float(r["x63"]) + float(r["spy_ret"]) * (1 - beta) - COST


def verdict(rows: list[dict], arm: str) -> str:
    """The ONE look: a sample fixed by trigger order (never by outcome), scored once settled."""
    sub = sorted((r for r in rows if r["status"] != "nofill" and (arm == "ALL" or r["arm"] == arm)),
                 key=lambda r: (r["trigger_date"], r["ticker"]))
    n = LOOKS[arm]
    while n <= len(sub) and len({r["trigger_date"][:7] for r in sub[:n]}) < MIN_MONTHS:
        n += 1
    if n > len(sub):
        return f"{arm} look: pending — {len(sub)} of {LOOKS[arm]}+ triggers (spanning ≥{MIN_MONTHS} months)"
    s = sub[:n]
    waiting = sum(r["status"] == "open" for r in s)
    if waiting:
        return f"{arm} look: sample fixed at n={n}, {waiting} still settling"
    x, bx = [_net(r) for r in s], [_beta_adj(r) for r in s]
    ok = st.mean(x) > 0 and st.median(x) > 0 and sum(v > 0 for v in x) / n > 0.5 and st.mean(bx) > 0
    return (f"{arm} look: {'PASS' if ok else 'FAIL'} (n={n}) — net mean {st.mean(x):+.2%}, median "
            f"{st.median(x):+.2%}, beat {sum(v > 0 for v in x) / n:.0%}, beta-adj {st.mean(bx):+.2%}")


def show(rows: list[dict]) -> None:
    print(f"[CRASH #2] forward paper ledger — {len(rows)} trigger(s) since {FORWARD_START}")
    for arm in ("PANIC", "CALM", "ALL"):
        sub = [r for r in rows if arm == "ALL" or r["arm"] == arm]
        done = [r for r in sub if r["status"] in ("settled", "delisted")]
        line = f"  {arm:5} triggers {len(sub):3d} · settled {len(done):3d}"
        if done:
            x = [_net(r) for r in done]
            line += (f" · net mean {st.mean(x):+.2%} median {st.median(x):+.2%} "
                     f"beat {sum(v > 0 for v in x) / len(x):.0%}")
        print(line)
    for arm in LOOKS:
        print("  " + verdict(rows, arm))
    for r in [r for r in rows if r["status"] == "open"][-10:]:
        print(f"  open: {r['trigger_date']} {r['ticker']:6} {float(r['drop']):+.1%} {r['arm']}")
    for r in [r for r in rows if r["status"] == "delisted"]:
        print(f"  delisted (settled at last stamped close — verify by hand): {r['ticker']} {r['exit_date']}")


def main(argv: list[str]) -> None:
    rows = _load()
    cmd = argv[1] if len(argv) > 1 else "show"
    if cmd == "log":
        print(f"logged {log(rows)} new trigger(s)")
        _save(rows)
    elif cmd == "settle":
        print(f"scored {settle(rows)}")
        _save(rows)
    elif cmd != "show":
        sys.exit(f"unknown command {cmd!r} — show | log | settle")
    show(rows)


if __name__ == "__main__":
    main(sys.argv)
