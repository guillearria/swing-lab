# Case study: <TICKER> — <one-line move headline>

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. It is the REASONING layer (see `research/ARCHITECTURE.md`): a
> case is born from a live move, states a falsifiable read, and **births one scored bet** in
> `research/bets.py`. Single source of truth — the case NARRATES; every number lives in its
> silo (`bets show`, `book`, `FINDINGS`) and is referenced by command/link, never restated.

**Status:** <open | settled>  ·  **Date:** <YYYY-MM-DD>  ·  **Pattern tag:** `<reusable-tag>`

> The backticked tag above is the SAME string passed to `bets add --tag=` — that is the only
> thing connecting this reasoning layer to a scored row, and it was disjoint from the catalogue
> until 2026-08-19 [ARC 5 #14b]. `python3 -m research.engine` stars any tag with no case file.

## Move
What happened, in price terms (qualitative — no restated figures).

## Why
The catalyst / mechanism. What actually drove it.

## How
The structure that enabled it (reverse split, float, dilution, narrative borrow, squeeze, …).

## Pattern (reusable)
The generalizable lesson — the tag above — and how to spot it on the NEXT asset. Feeds `SKILL.md`.

## Prediction
The falsifiable call (direction / horizon / benchmark). Scored in `bets.py`:
`python3 -m research.bets show` → row `<TICKER>`. Outcome accrues to the engine + FINDINGS bar.

## Links
- Bet: `python3 -m research.bets show` (`<TICKER>`)
- Related: FINDINGS `[ARC … #…]`, `cases/<other>.md`, book position (`python3 -m research.book`)
