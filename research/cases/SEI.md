# Case study: SEI — a forward number reset between reports, not at one

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-09-09  ·  **Pattern tag:** `guidance-raise-offcycle`

> The backticked tag is the SAME string passed to `bets add --tag=`. It is COINED here rather
> than borrowed, because the declared neighbours all require an earnings print this move does
> not have: `post-earnings-drift` (cases/NDSN.md, cases/EL.md) drifts FROM a report, and this
> raise landed weeks after Solstice-style quarter-end with no accompanying print;
> `guidance-cut-overreaction` (cases/MSCI.md) is the same axis in the opposite direction and
> is about the market MIS-pricing a cut, not about a company moving its own numbers;
> `analyst-rerating` (cases/MRK.md) is the sell side moving, not the company. Reusing one of
> those to dodge writing this file is the trap [ARC 5 #14b] names.
- Related: `cases/NDSN.md` (the earnings-anchored neighbour this is not), FINDINGS `[ARC 5 #1]`
  (the catalogue bar), `[ARC 5 #14b]` (the tag↔case link this file exists to honour)

## Move
Solaris spent late August drifting sideways in a narrow band on ordinary volume, then gapped
up hard on the last complete bar of this run — its heaviest session in weeks — and held most
of the gap into the close.

## Why
The company raised its adjusted EBITDA guidance for the CURRENT quarter and the next one, and
initiated a first-quarter guide well above both, off the back of demand for mobile power
generation at data centres plus two bolt-on acquisitions completed in July and September. The
size of the step matters more than the direction: the new current-quarter floor sits near the
old ceiling, and the initiated quarter two out is roughly double the current one.

## The pattern (why this is reusable)
**A guidance raise issued BETWEEN reports resets the forward model at a moment when nobody is
positioned for it.** An earnings raise arrives with a call, a deck, a full sell-side note cycle
and a room full of people already watching; an off-cycle raise arrives into stale models, on a
random Tuesday, with no transcript to argue about. The revision path is therefore slower and
the drift window longer — the estimate changes trickle in over weeks rather than landing in one
afternoon. Two conditions make it readable: (1) the raise must move the CURRENT quarter, not
just a far-out year, so it is about observed demand rather than ambition; (2) the magnitude
must exceed the normal beat-and-trim noise band, or it is housekeeping.

## What kills it
The raise may be BOUGHT rather than earned. When acquisitions closed inside the guided period,
part of the step is consolidation arithmetic, not demand — and the market re-rates that at a
much lower multiple once it separates the two. The tell is a raise whose size roughly matches
the acquired run-rate. The second killer is the theme itself: a small-cap whose numbers are
levered to data-centre capex re-rates violently in both directions on news that has nothing to
do with the company.

## Scored twin
One bet, pre-registered in `research/bets_catalogue.csv` with this tag; the numbers and the
verdict live there (`python3 -m research.bets show`), never restated in this file.
