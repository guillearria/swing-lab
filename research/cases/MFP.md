# Case study: MFP — an orphaned spin-off re-rates on its first standalone beat-and-raise

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `book`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-08-26  ·  **Pattern tag:** `post-spinoff-orphan-rerating`

> The backticked tag is the SAME string passed to `bets add --tag=`. NEW tag, no prior case.
> `post-earnings-drift` was rejected: the drift is only the trigger, not the mechanism — the
> mechanism is the ORPHAN STRUCTURE (forced spin-selling into zero sell-side coverage), and
> reusing PED here would corrupt the mix diagnostic [ARC 5 #12a·5a].
- Related: FINDINGS `[ARC 5 #1]` (the catalogue bar), `[ARC 5 #14b]` (tag↔case link),
  `[ARC 5 #11]` (the tail cohort's HIGHER read bar)

## Move
Midera Food Processing began trading as an independent company in early July 2026, spun out of
The Middleby Corporation. It opened its standalone life near the bottom of its short range, drifted
sideways for six weeks, then broke out hard over three sessions in the second half of August — a
tail-cohort mover on ordinary, not spiking, volume.

## Why
The proximate catalyst is its FIRST standalone quarter (reported mid-August): revenue beat
consensus by a mid-single-digit margin, the company RAISED its full-year revenue outlook, and the
board authorised a share repurchase. For a company with essentially no independent operating
history, one clean print is a large fraction of everything the market knows about it.

The move's WHY is name-specific, not sector or macro: food-processing equipment peers did not move
with it, and there is no commodity or rate driver behind the breakout.

## How
The structure is what makes it mispriceable. A spin-off arrives as ORPHAN EQUITY:
- Index and mandate-constrained holders of the parent receive shares in a company they do not
  want and cannot hold, and sell mechanically regardless of value. That supply is price-INSENSITIVE.
- Sell-side coverage starts at roughly zero and is rebuilt over quarters, so there is no published
  estimate for the print to beat and no analyst to broadcast the beat when it comes.
- Index membership is not yet settled, so the passive bid that normally anchors a name this size
  is absent.
The result: the forced supply clears BEFORE the first real fundamental datapoint arrives, and the
re-rating that follows is a slow discovery process — new coverage, first estimates, index
inclusion — rather than a single-day repricing. The gap between "no one owns or covers it" and
"it just raised guidance and started buying back stock" is the mispricing.

Data hygiene note that belongs with the pattern: the price feed carries one stale pre-spin bar
ahead of the real trading history. Any window that straddles a spin date is suspect — check the
first real bar before quoting a multi-month move on a newly separated company.

## Pattern (reusable)
`post-spinoff-orphan-rerating`: a recently separated company, still under-covered and still
digesting forced selling from the parent's holders, delivers its first standalone beat-and-raise →
bet that discovery (coverage initiations, first estimates, index inclusion, buyback execution)
re-rates it over a QUARTER, not a week. How to spot the next one: a separation date inside the
last two quarters, thin or absent analyst estimates, a first standalone print that beats and
raises, and a capital-return authorisation that says management thinks its own stock is cheap.

The trap this pattern owns: an orphan is orphaned for a reason. Parents spin the slower-growing,
more cyclical, more capital-hungry segment, and one good quarter cannot distinguish a genuinely
under-priced business from a structurally worse one that happened to catch an easy comparison.
Guard: require the raise to be to the FULL-YEAR outlook, not a single-quarter beat, and never rate
this shape high conviction on one print. It is also a tail-cohort name, so the higher read bar of
[ARC 5 #11] applies — spread and gappy fills are real costs here, not footnotes.

## Prediction
Long MFP, 63d (discovery is a quarter-long process, not a drift), vs XLI — benchmarking against
large-cap industrials is the harder, more honest test: it strips out the sector and leaves only
the name-specific re-rating. Scored in `bets.py`: `python3 -m research.bets show` → row `MFP`.

## Links
- Bet: `python3 -m research.bets show` (`MFP`)
- Counterfactual order: `python3 -m research.orders show` (`MFP`) — DIAGNOSTIC only [ORDERS #1]
- Related: FINDINGS `[ARC 5 #1]`, `[ARC 5 #11]`, `cases/FN.md` (the other tail-cohort read)
