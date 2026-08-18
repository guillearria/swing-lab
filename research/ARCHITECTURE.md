# swing_lab — architecture (the layer map)

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
| Money (CLOSED 2026-08-18) | `book.py` (+ `book.csv`, tracked in git) | the FORMER real-money portfolio — TERMINAL, frozen evidence [ARC 5 #12; closure #13/#13a]; every command prints one BOOK CLOSED line |
| Public surface | `site.py` (+ `docs/index.html`) · `pulse.py` | the Pages dashboard (predictions + performance only [P7a]) · the X autopost path (inert until keys [P7b]) |
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
                                         │  highest-conviction take, one per run
                                         ▼
                                  orders.py   (the COUNTERFACTUAL working order [ARC 5 #12a]: a
                                         │    limit + an expiry, computed by code, blank shares —
                                         │    nothing to execute. Fills AND no-fills resolved vs
                                         │    real bars — band DIAGNOSTIC, never an edge verdict)
                                         │
                                         │   (book.py sat below here in the live era — CLOSED
                                         │    [ARC 5 #12/#13]; frozen evidence, no live $ layer)
              ┌──────────────────────────┴───────────────────────────┐
              ▼                                                        ▼
   engine.py (verdicts + multiple-testing N)                  FINDINGS.md (audit)
              └───────────────► durable lessons ──────────────► SKILL.md (method)
```

A case is the REASONING; the bet is the scored PREDICTION; the order is the counterfactual
EXECUTION MODEL. (In the live era the book was the MONEY below all three — closed [ARC 5 #12].)

**SCOPE — the two realms [2026-08-02].** This repo is the SHORT-SWING realm: days-to-weeks reads,
scored against a benchmark, accruing toward a verdict. The book holds ONLY capital that is tradeable
AND chosen. **Long-horizon personal assets (equity comp, retirement/compounding accounts) are OUT
OF SCOPE** and live in the fully-private long-realm repo — separate research, separate actions,
markdown pointers only, no code coupling. The two realms see each other; neither decides for the
other. Enforced because it failed once: a long-realm holding was seeded into the book and dragged
multi-YEAR questions (cost basis, lockup tranches, plan tax milestones) into a days-to-weeks
process for five weeks, and the position turned out not to exist (FINDINGS 2026-08-02).

**Convergence [ARC 5 #7] — SUPERSEDED-HISTORICAL [2026-08-18]: the book converged by CLOSING
([ARC 5 #12]; liquidated 08-17, closure #13/#13a — the account number was the owner's inherited
book, never the system's verdict). Kept as the record of the doctrine that governed the live
era:** — *scoped to swing capital only; a long-term holding is not a "legacy
holding awaiting redirect", it is in the other realm:* the book was seeded from PRE-SYSTEM human
positions, so today the book ≠ the edge. Its standing job is to CONVERGE onto the edge — redirect legacy/underwater
holdings into edge-driven high-conviction reads as catalysts/conviction allow (HOLD on
conviction; recycle when a thesis/catalyst breaks or a better read needs the capital; never dump
merely to dump). Every legacy holding carries a hold / redirect-on-catalyst verdict. The silos
stay SEPARATE (skill verdict mustn't be polluted by sized churn); the case→bet→book bridge is the
channel. Judge the book in DOLLARS vs the real opportunity cost (same-$ SPY AND dual-mom), floored
by the whole-pool stop (`book.POOL_STOP`).

## Orchestration
- `python3 -m research` — the status panel: stitches engine + bets + movers + book (one
  BOOK CLOSED line) + dualmom, and lists `cases/`. The one LOCAL dashboard.
- `site.py` → `docs/index.html` (GitHub Pages) — THE PUBLIC dashboard [P7a]: predictions +
  performance only per the audience contract; deterministic render, re-committed by settle
  only when its data changed. `pulse.py` [P7b] — the X autopost path, INERT until API keys
  land (dry-run: `python3 -m research.pulse`).
- Cloud routines (`/schedule`), THREE: **read** (pre-market weekdays — generate bets via
  `READ_LOOP.md`), **settle** (daily — score matured bets via `scripts/daily.sh`), and
  **watchdog** (daily, own hour, fresh session — 🚨 if no ledger commit in 36h; deliberately
  outside `daily.sh`, since a check that runs inside the thing it watches cannot report that
  thing dying). They never overlap.
- Telegram contract (2026-07-03; v1.1 2026-07-10; reshaped 2026-08-05/06; **v2 2026-08-14
  [ARC 5 #12a], code P4**): EVERY scheduled run pushes exactly ONE message — silence = broken;
  a clean weekday = settle's 📋 + read's 📖, BOTH led by the 🎯 POOL SCOREBOARD (n settled
  long-only · median · beat · Σ pp vs own benchmarks · Wilcoxon p · distance to bar, 🏁
  milestone banners at n=10/20/30). Both come from `digest.py` (HTML, fail-soft per silo);
  DO-NOW actions ride in every shape. Settle's 📋 = the full photo: scoreboard + Δ-since-HEAD
  + orders + bets/movers state + the mix mirror. Read's `--slim` 📖 = the MORNING BRIEF:
  scoreboard + DO-NOW + run note + the 🟢 system take (informational — no broker leg). The 💰
  band and the live-book blocks retired with the book [#12]. Δ-since-HEAD answers "what
  CHANGED" by diffing the ledgers against **git HEAD** — no state file, no `settled_at` column
  [2026-08-04]. A PENDING counterfactual order is re-shown daily with today's spot beside its
  limit [2026-08-03]; plus 🚨 per scored settlement. The 🚨 heartbeat
  (`heartbeat.py`) is the FALLBACK — fires only when a step or the digest push failed.
  Transport: `notify.py` (HTML, newline-safe truncation, plain retry on rejected HTML;
  tri-state result). `digest --notify` prints the delivery VERDICT (the only truth about
  delivery — re-send ONLY on `PUSH REJECTED`) and stamps `research/data/push_log.csv`
  (committed), from which the next delivered message flags a settle push that died in
  transport — the failure the commit-watching watchdog cannot see [2026-08-06].

## Integrity guards (never loosened — FINDINGS `[ARC 5 #6]`)
Pre-registration (immovable timestamp) + log-every-candidate (take AND skip) + multiple-testing
N — the only thing dividing this from a false-positive machine. (The whole-pool stop was the
live era's money circuit breaker — retired WITH the pool at book closure [ARC 5 #12]: on a
swept book it would fire forever, and an unclearable alarm is forbidden.) Everything else
(throughput, approval) stays loosened for the experimental phase.

**Model independence (no same-context self-validation) — AMENDED 2026-08-07 (owner):** reviews
use BLIND micro-independent runs of the strongest available model (fresh context, adversarial
lens; the reviewer re-derives its own verdicts and never sees the generator's conclusions —
disagreement is the signal) plus ONE cross-model control run (Opus/Sonnet/Haiku, substitute
freely). Audit #1 (2026-08-08) validated the shape: the control caught items the same-model
lenses missed. The live pipeline stays safe by construction: settling is DETERMINISTIC price
math — no model judges its own trade.
