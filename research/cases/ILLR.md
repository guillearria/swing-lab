# Case study: ILLR (Triller Group) — a borrowed-narrative pump on a broken shell

> See `cases/_TEMPLATE.md` for what a case study is. Single source of truth: the scored bet
> lives in `bets.py`; nothing here restates a P&L or excess number.

**Status:** open  ·  **Date:** 2026-06-26  ·  **Pattern tag:** `real-vehicle-vs-meme` / `spent-catalyst-pump`

## Move
ILLR exploded multi-hundred-percent over a few days on heavy volume with repeated halts —
from sub-$1 to a multiple of that — then gave much of it back inside the same window. A
vertical spike with no durable base; the round-trip was already underway by 2026-06-26.

## Why
The trigger was a 2026-06-25 announcement that Triller entered definitive agreements to
**acquire a significant SpaceX position as a "strategic treasury asset"** — putting SpaceX
exposure on its balance sheet. This borrows the SAME hot narrative (private-SpaceX valuation)
lifting genuine SpaceX-exposure vehicles like **SPCX** (see `cases/SPCX.md`). It is a
story change, not an earnings change — it moves the narrative, not the cash flows.

## How
The move sits on a structurally broken shell, which is what makes it a *pump*, not a re-rating:
- **1:10 reverse split** effective 2026-06-23 — a delisting-avoidance mechanic, not strength.
- **Nasdaq compliance exception to 2026-06-30** (needs a $1+ closing bid for 10 straight days).
- **Negative equity, shrinking revenue, heavy losses** — no fundamental floor under price.

A thin, beaten-down float + a viral narrative + forced day-trader attention = a vertical move
that mean-reverts once the headline is digested.

## Pattern (reusable)
**Real vehicle vs meme.** When a hot theme runs, two things rally: the *real* exposure and the
*borrowed-narrative* impostors that staple the theme onto a broken balance sheet (the
"treasury-asset" gimmick — cf. the crypto-treasury playbook). Own the real vehicle; fade the
borrow. The fade-able tell-stack: reverse split + delist deadline + negative equity + a
narrative (not cash-flow) catalyst + a spike that already round-trips = **spent-catalyst
spike-fade** (FINDINGS `[ARC 5 #3]`; the XRP "good news that can't hold price = distribution"
tell, `[ARC 5 #4]`). Generalizes to the next "X-treasury-asset" pump on any shell.

## Prediction
**SHORT ILLR, 21d, vs IWM** (paper-scored only — a real short is impractical: halted,
hard-to-borrow micro-cap). Thesis: the pump fades faster than small-caps over the next ~month.
Scored in `bets.py`: `python3 -m research.bets show` → row `ILLR`.

## Links
- Bet: `python3 -m research.bets show` (`ILLR`, short 21d vs IWM, fast sleeve)
- Contrast case: `cases/SPCX.md` (the real SpaceX vehicle — the pattern's long side)
- Prior art: FINDINGS `[ARC 5 #3]` (spike-fade screen), `[ARC 5 #4]` (XRP spent-catalyst tell)
