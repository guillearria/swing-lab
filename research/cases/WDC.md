# Case study: WDC — a rival says it will double its factory, and the market prices it as if the shortage were over

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-10-05  ·  **Pattern tag:** `competitor-capacity-threat-overreaction`

> The backticked tag is the SAME string passed to `bets add --tag=`. It is COINED here rather
> than borrowed, and the near neighbours are all the wrong mechanism:
> `insourcing-threat-overreaction` (cases/HWM.md) requires a CUSTOMER choosing to make the part
> itself, and the party expanding here is a RIVAL arming to sell to the same buyers — a
> different question (share, not demand); `sector-sympathy-selloff` (cases/FN.md) needs the
> damage to arrive through a peer's own PRINT, and there was no print, only a newspaper report
> about a third company's capital budget; `guidance-cut-overreaction` (cases/MSCI.md) needs a
> guidance cut, and the live guide was never touched. Reusing one of those to avoid writing this
> file is the trap [ARC 5 #14b] names.
- Related: `cases/HWM.md` (the neighbour this is not — customer vs rival), `cases/FN.md`,
  FINDINGS `[ARC 5 #1]` (the catalogue bar), `[ARC 5 #14b]` (the tag↔case link)

## Move
Western Digital had been one of the strongest large-cap names of the year, re-rated on an
AI-datacenter storage shortage that let it sell capacity years forward. On the last complete bar
of this run it fell about a tenth in a single session on nearly four times its normal volume,
with Seagate falling harder still. Nothing came from either company.

## Why
A Nikkei report said Toshiba — the third and smallest of the three remaining hard-drive makers —
will spend roughly sixty billion yen to expand its Philippine plant and nearly double its annual
capacity by fiscal 2027, and that it wants its capacity share to reach about thirty per cent over
the medium term.

The thirty is what the tape traded. It is an aspiration with no date, and the sell-side
immediately put numbers on the part that does have one: Bernstein's read of the same plan has
Toshiba going from a shade over eleven per cent to under seventeen by the end of fiscal 2027 —
a few points of share, not a tripling. Morgan Stanley, Rosenblatt and Citi each kept positive
ratings and said the plan does not close the industry's supply gap. Evercore's point is the
sharpest: the incremental drives arrive into a market where Seagate has already allocated most
of its nearline capacity into calendar 2028 and Western Digital is negotiating agreements out to
calendar 2031. New supply cannot compete for volume that is already contracted.

So the thing that moved was the fear of future price competition, and the thing that did not
move was the company's own live claim about the near term — a quarter guided weeks earlier at
revenue up strongly year on year with gross margin in the mid-fifties, reiterated and not
withdrawn.

## How
The structure that made the move this large is crowding plus a single thesis axis. Hard-drive
pricing IS the bull case here; there is no second leg. A name held by momentum money for one
reason gaps on any headline that touches that reason, and the three-maker oligopoly means a
story about any one of them is read as a story about the price. The report also arrived as the
rest of the semiconductor complex was ripping higher, so the selling had no sector cover and
concentrated in two tickers.

## The pattern (why this is reusable)
**When a smaller RIVAL announces a capacity expansion into a shortage, the market frequently
prices the announcement as if the supply had already landed and as if the announcer's stated
ambition were its contracted plan. The gap is measurable: compare the share the expansion
actually adds inside the guided period against the share of the incumbent's volume that is
already sold forward under long-term agreements.** Three conditions make it readable: (1) the
expanding party is the smallest of a concentrated field, so even doubling moves industry supply
by a few points; (2) the first output lands outside every period the incumbent has guided; and
(3) the incumbent's book is contracted rather than spot, so new capacity cannot bid for volume
that is already committed.

The confirming tell is the same one HWM's case names — the ABSENCE of a withdrawal. If the
threat were near-term and material, the incumbent would have to touch its outlook. It has not.

## What kills it
The headline may be the trigger rather than the reason. If the storage cycle is topping, a
name that re-rated entirely on price does not need Toshiba to de-rate; the report merely gave
a crowded trade its excuse, and this one is near its highs with no second leg to fall back on.
The read is explicitly a claim about the near term only — the supply IS coming, and a few points
of share compounding into calendar 2028 is a real headwind we are choosing to be the wrong side
of later rather than now.

The second kill is the print itself, which lands inside the fast window: if the quarter's
long-term-agreement commentary softens on pricing or duration, the market was reading the right
risk off the wrong document and the gap does not close.

## Scored twin
One bet, pre-registered in `research/bets_catalogue.csv` with this tag; the numbers and the
verdict live there (`python3 -m research.bets show`), never restated in this file.
