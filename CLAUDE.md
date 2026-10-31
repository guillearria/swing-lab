# swing_lab — operating contract

Slimmed 2026-10-31 (owner). The full previous contract, with the history behind every rule, is
`research/CLAUDE_ARCHIVE.md` — read it when a rule's reason matters; this file wins on conflict.

## What this is
A short-swing trade-signal research lab. GOAL: find real, durable edges and trade them, and
learn to build well doing it. STATUS: no signal has been shown to make money. Everything is
PAPER; real money returns only after a pre-registered PASS (the book closed 2026-08-17).
**Iteration is OPEN (owner, 2026-10-31):** run a small portfolio of cheap tests in parallel,
tune them, retest, keep going.

## The one rule that makes iteration honest
Tune freely in-sample; every such number is labelled **EXPLORATORY**. A tuned variant gets its
**verdict only from data it has not seen**: a forward paper ledger or an untouched holdout.
Iterating on the same data until something passes manufactures an edge (~1 in 20 tests passes
at 5% by luck).

## The loop
1. Pre-register the question + pass/fail bar in `research/FINDINGS.md` and commit it BEFORE
   running.
2. Run it. 3. Red-team it with a separate pass (blind replication and/or adversarial review),
   especially backtests. 4. Log the result (win or loss) with its number and its weakness.
5. Commit + push.
No number, no claim. A finding with no stated weakness is not done.
**Lanes:** RUNNING the system (reads, settles, scoring, logging, doc upkeep, committing
evidence) = autonomous, report after. CHANGING it (code, rules, bars) = propose first, unless
the owner asked for that change. Moving real money = always the human.

## Backtest standards
Realistic costs; few parameters; out-of-sample or forward; guard against lookahead and
survivorship (Yahoo has no delisted names, and reused tickers return the wrong company: check
prior dollar volume). If you can't explain it in five lines it is suspect. The owner's claims get
the same test as the model's. Don't inflate one threat into a blocker: measure it, then move.

## Build discipline
No feature without a present need. Delete rather than defer. Prefer smaller systems. Reuse free
data and tools first (yfinance; `research/prices.py` is the price seam). Paid data is allowed
once evidence says it buys edge: name the trigger. Keep LLM calls out of the deterministic path
(triggers, settles, scoring, money math). One agent by default; parallel agents for genuinely
parallel work (reviews qualify).

## Guardrails (do not break)
- **Two realms.** This repo is the SHORT-SWING realm and is being prepared for public release.
  Long-term wealth, personal finances and holdings live in a separate private repo and are NEVER
  restated here; markdown pointers only, no imports either way.
- **Conflict-of-interest exclusion list:** kept in the private realm and in the cloud read
  prompt, never in this repo; a name on it is never scored, held or recommended here. The read
  trigger is disabled but must NEVER be deleted: it is the list's home.
- Secrets live in `.env`; `FINANCES.md` is private. Both gitignored. Never commit or paste them.
- **Telegram:** every scheduled run sends exactly ONE 📋 message; silence = broken. 🚨 means
  FAILURE only, never a success ping. The digest prints a delivery verdict: re-send ONLY on
  `PUSH REJECTED (nothing sent)`, never on `PUSH UNCONFIRMED` (that double-posts). The digest
  refuses a second same-day push itself; `scripts/daily.sh` holds a lock. Never re-launch a
  backgrounded `daily.sh`.
- **Single source of truth:** live numbers live in one runnable command; docs point to the
  command, never restate the figure. FINDINGS entries are append-only and keep their numbers.
- One look means one look: never recompute a decided verdict at a larger n.
- **Edge graduation:** if a test ever passes its bar, its live signal moves to a private repo
  BEFORE real capital is sized on it; the method and this ledger stay public (COMMANDS.md).

## Where things are
- `COMMANDS.md` — every live command. `README.md` — the one-screen public page.
- `python3 -m research` — status panel. `python3 -m research.engine` — the scoreboard (every
  test, its verdict, the multiple-testing check).
- `research/FINDINGS.md` — READ FIRST: every test, number and caveat (closed arcs:
  `FINDINGS_ARCHIVE.md`). `research/SKILL.md` — the method. `research/BACKLOG.md` — changelog +
  backlog + owner rulings. `research/ARCHITECTURE.md` — the layer map.
- **Live track:** `research/crash_ledger.py` — [CRASH #2] forward paper ledger: daily S&P 500
  crash-day triggers, PANIC/CALM arms, scored at 63 sessions; one look per arm. Its backtest:
  `research/crash_buy.py` [CRASH #1].
- `research/bets.py` — Arc 5's LLM forward bets: FAIL, final [ARC 5 #18]; generation retired;
  open bets settle to completion (~2027-01-13) as record. `research/movers.py` — retired scan;
  rows score until mature.
- `research/dualmom.py` — the one banked result (risk shape, not alpha).
- `research/book.py`, `research/orders.py` — TERMINAL / counterfactual evidence ledgers.
- `scripts/daily.sh` — the daily settle (cloud routine, primary). `research/digest.py` — the
  Telegram message. `research/watchdog.py` — external dead-man's switch (GitHub Action).
- `research/site.py` → `docs/index.html` — the public dashboard. `research/pulse.py` — X
  autopost, inert until keys land; never autopost before a dry-run together.
- Dormant probes (`dip_index`, `vix_fear`, `disaster`, …) stay: `FINDINGS_ARCHIVE.md`
  reproduces from them. `momentum.py` and `universe.py` are live.

## Communication
Fewest words. Answer first. Short sentences. No preamble or hedging.
