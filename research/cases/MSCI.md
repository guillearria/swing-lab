# Case study: MSCI — the whole multiple repriced off a 4-cent expense miss

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. The case NARRATES; every number lives in its silo (`bets show`)
> and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-08-24  ·  **Pattern tag:** `guidance-cut-overreaction`

> The backticked tag is the SAME string passed to `bets add --tag=`. This file backs the
> catalogue's second-most-used tag, unbacked since its first row [ARC 5 #14b]. Written from
> the LOGGED theses — every anchor row is still open, outcomes unknown, no hindsight.

## Move
MSCI fell double digits the session after its Q2 print (rpt 7/21) — a drop more than double
the options-implied swing — on a four-cent non-GAAP EPS miss with revenue in line. Lennox
(LII, rpt 7/29) is the corroborating instance: a ~-23% single-day move on a low-single-digit
percentage trim of FY EPS guidance, with its commercial segment still growing.

## Why
The miss was EXPENSE-driven, not a demand break: revenue grew and stayed in line while opex
ran hot and the FY opex guide was raised. The sell side's price targets sat far above the
post-print price. The market repriced the entire multiple of a wide-moat recurring-revenue
business off a marginal, cost-side delta — a margin headline read as a growth story ending.

## How
The structure that enables the overreaction: a premium multiple leaves no tolerance for any
guide-line softness, so mechanical de-rating (options hedging, momentum exits, PT-anchored
sellers) overshoots what the actual estimate revision justifies. The gap between the small
fundamental delta and the large price delta is the mispricing — IF the delta is genuinely
marginal (cost timing, one segment) and not the first print of a demand break.

## Pattern (reusable)
`guidance-cut-overreaction`: a headline miss/trim that is SMALL relative to the price
reaction, at a name whose demand engine is intact → bet the multiple partially rebuilds as
estimates settle. Spot it: single-day drop ≥2x the implied move · the miss confined to
expenses or ONE segment while the core grows · guide trimmed by a low-single-digit
percentage, not withdrawn. The trap this pattern owns: the market is sometimes early, not
wrong — a "cost quarter" can be the first quarter of structural margin erosion (the
valuation-deflation mechanism, `cases/IRM.md`, cutting the other way). That is the stated
risk on the anchor row itself.

## Prediction
Long, 63d (the multiple rebuilds over a quarter, not a week), vs the sector benchmark.
Scored in `bets.py`: `python3 -m research.bets show` → rows `MSCI`, `LII` and siblings.

## Links
- Bets: `python3 -m research.bets show` (tag `#guidance-cut-overreaction`)
- Related: `cases/IRM.md` (the opposing mechanism) · FINDINGS `[ARC 5 #14b]` (tag↔case link)
