# Case study: FN — record beat flushed by an AI-hardware sympathy selloff

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `book`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-08-24  ·  **Pattern tag:** `sector-sympathy-selloff`

> The backticked tag is the SAME string passed to `bets add --tag=`. New tag, no prior case —
> `revenue-miss-overreaction` was rejected because FN did not miss revenue (it beat +45%); the
> driver is a SECTOR/MACRO flush, a distinct mechanism that must not corrupt the mix diagnostic.
- Related: FINDINGS `[ARC 5 #1]` (the catalogue bar), `[ARC 5 #14b]` (tag↔case link)

## Move
Fabrinet dropped ~20% the session after fiscal Q4 (rpt ~8/18) and closed the 5d window down
sharply — a tail-cohort mover on above-average volume.

## Why
The sell was NOT company-specific deterioration. The print was a record beat (rev +45% YoY,
data-center 51% of rev and +68% YoY, EPS well above consensus). The stock fell on (1) a
conservative sequential Q1 guide and (2) a market "already primed to sell AI-infrastructure
names" — an Anthropic ARR-disappointment narrative and the 30-year Treasury at a 19-year high
flushed the whole AI-hardware complex (Marvell, Amphenol dragged with it). The move's WHY is
market-wide, not name-specific.

## How
A high-multiple AI-hardware supplier with concentrated end-demand: when the sector narrative
de-rates, the strongest name gets thrown out with the group regardless of its own numbers. The
gap between FN's own beat and the sympathy-driven drawdown is the mispricing.

## Pattern (reusable)
`sector-sympathy-selloff`: a fundamentally strong beat-and-guide that sells off on a SECTOR/MACRO
flush rather than its own results → bet the name-specific fundamentals reassert RELATIVE TO
PEERS. Benchmark vs the sector ETF (here SMH) so the market-wide component is removed and only
the name-vs-peer overreaction is scored. The trap this pattern owns: if the sector de-rating is
a genuine regime change (AI-capex rolling over, rates rising), the name keeps drifting with the
group and the "overreaction" was correct pricing. Medium conviction, never high, on this shape.

## Prediction
Long FN, 21d (fast sleeve — the overreaction resolves in weeks), vs SMH. Scored in `bets.py`:
`python3 -m research.bets show` → row `FN`.

## Links
- Bet: `python3 -m research.bets show` (`FN`)
- Related: FINDINGS `[ARC 5 #1]`, `cases/_TEMPLATE.md`
