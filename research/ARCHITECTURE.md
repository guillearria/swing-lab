# claude_trader — architecture (the layer map)

How the branches fit together and talk to each other. One rule above all (see `CLAUDE.md`):
**single source of truth** — every number lives in exactly ONE silo; everything else references
it by command/link. This doc is the map; it holds NO live numbers.

## The layers

| Layer | Silo | Role |
|---|---|---|
| Mechanical (CLOSED) | `engine.py` + Arc-1/2 probe `*.py` | backtest fixed rules on history → scoreboard |
| Reasoning | `cases/*.md` | document WHY/HOW a live move happened → a reusable pattern |
| Track record | `bets.py` (+ `bets_catalogue.csv`) | scored % predictions vs a benchmark; `pattern_tag` = scenario type [Arc 5 #8] |
| Candidate denominator | `movers.py` (+ `movers_ledger.csv`) | daily mover scan, 2 cohorts (S&P 500 + 400/600 tail [ARC 5 #11]) → SEEN take/skip; the general track's denominator [Arc 5 #8] |
| Money | `book.py` (+ `book.csv`, tracked in git) | the sized REAL-MONEY portfolio, P&L vs SPY AND dual-mom |
| Banked signal | `dualmom.py` | the one usable result (risk shape, not alpha) |

Docs: `FINDINGS.md` = research/science audit log (closed-arc entries archived verbatim in
`FINDINGS_ARCHIVE.md`) · `SKILL.md` = method + patterns · `BACKLOG.md` = engineering changelog +
backlog + stale map · `LOOP.md`/`READ_LOOP.md` = generation contracts · `README.md` = command
index · `ARCHITECTURE.md` = this map.

## The data flow

```
idea / live move
   ├─ mechanical & backtestable?  → probe + engine.py  (scoreboard)            [CLOSED MINE]
   └─ judgment / reading?         → cases/*.md  (WHY · HOW · reusable pattern)
                                         │  births one falsifiable call
                                         ▼
                                    bets.py   (scored % vs benchmark)
                                         │  if conviction, size it
                                         ▼
                                  orders.py   (the WORKING ORDER: a limit + an expiry, computed
                                         │    by code; re-pushed daily until it fills or dies.
                                         │    Logs fills AND no-fills so the band is scorable —
                                         │    DIAGNOSTIC, never an edge verdict)
                                         │  the HUMAN places the limit at the broker
                                         ▼
                                    book.py   ($ vs SPY AND dual-mom — the only $-sized layer)
                                         │
              ┌──────────────────────────┴───────────────────────────┐
              ▼                                                        ▼
   engine.py (verdicts + multiple-testing N)                  FINDINGS.md (audit)
              └───────────────► durable lessons ──────────────► SKILL.md (method)
```

A case is the REASONING; the bet is the scored PREDICTION; the book is the MONEY. One move can
flow all the way down, or stop at any layer (most reads never reach the book).

**SCOPE — the two realms [2026-08-02].** This repo is the SHORT-SWING realm: days-to-weeks reads,
scored against a benchmark, accruing toward a verdict. The book holds ONLY capital that is tradeable
AND chosen. **Long-horizon personal assets (equity comp, retirement/compounding accounts) are OUT
OF SCOPE** and live in the fully-private long-realm repo — separate research, separate actions,
markdown pointers only, no code coupling. The two realms see each other; neither decides for the
other. Enforced because it failed once: a long-realm holding was seeded into the book and dragged
multi-YEAR questions (cost basis, lockup tranches, plan tax milestones) into a days-to-weeks
process for five weeks, and the position turned out not to exist (FINDINGS 2026-08-02).

**Convergence [ARC 5 #7]** — *scoped to swing capital only; a long-term holding is not a "legacy
holding awaiting redirect", it is in the other realm:* the book was seeded from PRE-SYSTEM human
positions, so today the book ≠ the edge. Its standing job is to CONVERGE onto the edge — redirect legacy/underwater
holdings into edge-driven high-conviction reads as catalysts/conviction allow (HOLD on
conviction; recycle when a thesis/catalyst breaks or a better read needs the capital; never dump
merely to dump). Every legacy holding carries a hold / redirect-on-catalyst verdict. The silos
stay SEPARATE (skill verdict mustn't be polluted by sized churn); the case→bet→book bridge is the
channel. Judge the book in DOLLARS vs the real opportunity cost (same-$ SPY AND dual-mom), floored
by the whole-pool stop (`book.POOL_STOP`).

## Orchestration
- `python3 -m research` — the status panel: stitches engine + bets + movers + book + dualmom,
  and lists `cases/`. The one dashboard.
- Cloud routines (`/schedule`), THREE: **read** (pre-market weekdays — generate bets via
  `READ_LOOP.md`), **settle** (daily — score matured bets via `scripts/daily.sh`), and
  **watchdog** (daily, own hour, fresh session — 🚨 if no ledger commit in 36h; deliberately
  outside `daily.sh`, since a check that runs inside the thing it watches cannot report that
  thing dying). They never overlap.
- Telegram contract (2026-07-03; v1.1 2026-07-10; reshaped 2026-08-05/06): EVERY scheduled run
  pushes exactly ONE message — silence = broken; a clean weekday = settle's 📋 + read's 📖.
  Both come from `digest.py` (HTML, fail-soft per silo); DO-NOW actions ride in every shape.
  Settle's 📋 is the day's FULL photo: 💰 SINCE-LAST band + full book + orders + bets/movers
  state. Read's `--slim` 📖 is the MORNING BRIEF: DO-NOW + the full book (each position with
  $ P&L + stop/target distance) + the run note + a 🟢 working order when cash is idle — it
  drops the band/one-liners/ORDERS block/banner, which settle owns [2026-08-06]. The band
  answers "what CHANGED" by diffing the ledgers against **git HEAD** — no state file, no
  `settled_at` column [2026-08-04]. A PENDING order is re-pushed daily with today's spot beside
  its limit [2026-08-03] — unless its fill is already booked, which flips the nag to an FYI
  (`orders.booked` [2026-08-06]); plus 🚨 per scored settlement. The 🚨 heartbeat
  (`heartbeat.py`) is the FALLBACK — fires only when a step or the digest push failed.
  Transport: `notify.py` (HTML, newline-safe truncation, plain retry on rejected HTML;
  tri-state result). `digest --notify` prints the delivery VERDICT (the only truth about
  delivery — re-send ONLY on `PUSH REJECTED`) and stamps `research/data/push_log.csv`
  (committed), from which the next delivered message flags a settle push that died in
  transport — the failure the commit-watching watchdog cannot see [2026-08-06].

## Integrity guards (never loosened — FINDINGS `[ARC 5 #6]`)
Pre-registration (immovable timestamp) + log-every-candidate (take AND skip) + multiple-testing
N — the only thing dividing this from a false-positive machine. The whole-pool stop (`book.POOL_STOP`, floor via `book.pool_floor`; the digest prints its LEVEL
daily and escalates a breach while risk is still on)
is the money circuit breaker. Everything else (sizing, throughput, approval) is loosened for
the experimental phase.

**Model independence (no same-context self-validation) — AMENDED 2026-08-07 (owner):** reviews
use BLIND micro-independent runs of the strongest available model (fresh context, adversarial
lens; the reviewer re-derives its own verdicts and never sees the generator's conclusions —
disagreement is the signal) plus ONE cross-model control run (Opus/Sonnet/Haiku, substitute
freely). Audit #1 (2026-08-08) validated the shape: the control caught items the same-model
lenses missed. The live pipeline stays safe by construction: settling is DETERMINISTIC price
math — no model judges its own trade.
