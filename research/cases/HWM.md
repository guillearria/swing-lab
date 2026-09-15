# Case study: HWM — one customer says it will build the part itself, and the whole franchise is marked down

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-09-15  ·  **Pattern tag:** `insourcing-threat-overreaction`

> The backticked tag is the SAME string passed to `bets add --tag=`. It is COINED here rather
> than borrowed, and the near neighbours are all the wrong mechanism: `guidance-cut-overreaction`
> (cases/MSCI.md) needs a guidance cut — guidance here was RAISED and never withdrawn;
> `sector-sympathy-selloff` (cases/FN.md) needs the damage to come from a peer's print, and the
> trigger here is a customer's own announcement about a customer's own factory;
> `narrative-stage-transition` (cases/AKAM.md) runs the other way, a story improving rather than
> a moat being questioned. Reusing one of those to avoid writing this file is the trap
> [ARC 5 #14b] names.
- Related: `cases/MSCI.md` and `cases/FN.md` (the two neighbours this is not), FINDINGS
  `[ARC 5 #1]` (the catalogue bar), `[ARC 5 #14b]` (the tag↔case link this file exists to honour)

## Move
Howmet printed a very strong second quarter in early August — EBITDA, margin, EPS and free cash
flow all up sharply, and the full-year outlook raised — and the stock closed at a 52-week high
on the day of the print. Four weeks later it gave back more than a quarter of its value, ending
the last complete bar of this run at a three-month low, and underperformed its sector ETF by
roughly eleven points over the month. Nothing in the reported numbers changed in between.

## Why
On the last day of August, SpaceX said it intends to cast gas-turbine blades and vanes in-house.
Howmet is the dominant supplier of exactly that part — more than half the world market — so the
headline reads as a direct attack on the franchise, and the stock fell on the day.

The slide then kept going for two weeks without any fresh company news, and the final leg of it
arrived on a day when the entire AI-power and AI-capex complex sold off together on an unrelated
narrative shock about AI regulation. Howmet sells into that complex through industrial gas
turbines, so it was swept along with names whose business models actually are the AI build-out.

The two things the announcement does not say are the whole read. It is ONE customer, not a
market entrant selling to others. And the capacity behind it does not exist: management has said
the earliest any of it lands is 2028, against a book of long-term agreements and Howmet's own
capacity expansions already under way in three regions. Sell-side targets sat far above the
traded price after the drop, with at least one house calling the threat minimal.

## The pattern (why this is reusable)
**When a single customer announces it will make a part itself, the market frequently prices the
announcement as if the supplier's whole market had been entered — immediately. The gap between
"one buyer, years out, capacity not built" and "the moat is gone" is measurable against the
supplier's own most recent guidance, which is the part that has not changed.** Three conditions
make it readable: (1) the announcer is a CUSTOMER insourcing for itself, not a rival arming to
sell to the supplier's other customers; (2) the stated timeline puts first output far enough out
that no guided period is affected — so the guide the company just gave is still the company's
own live claim about the near term; (3) the supplier's share is protected by long-term
agreements rather than by spot re-ordering.

The confirming tell is the ABSENCE of a withdrawal: if the threat were near-term and material,
the supplier would have to touch its outlook, and it has not.

## What kills it
The headline may be the trigger rather than the reason. If demand for industrial gas turbines is
genuinely rolling over with AI-datacenter power capex, then a premium-multiple industrial
de-rates on the numbers no matter how wrong the insourcing scare was — and the scare merely gave
the selling a story. The tell is the next quarterly print: an outlook that holds says the read
was right; an outlook that softens says the multiple, not the moat, was the problem, and a name
that has already made new lows can keep making them for a long time.

A second kill is spread: if other large customers announce the same intent, "one customer" stops
being the load-bearing part of the argument.

## Scored twin
One bet, pre-registered in `research/bets_catalogue.csv` with this tag; the numbers and the
verdict live there (`python3 -m research.bets show`), never restated in this file.
