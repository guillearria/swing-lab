# Case study: JBHT — a diesel spike that the contract recovers, priced as a permanent margin reset

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. The case NARRATES; every number lives in its silo (`bets show`)
> and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-09-17  ·  **Pattern tag:** `passthrough-cost-lag-overreaction`

> The backticked tag is the SAME string passed to `bets add --tag=`. It is COINED here rather
> than reused [ARC 5 #14b]. The nearest existing tag is `guidance-cut-overreaction`
> (`cases/MSCI.md`) and the shapes rhyme — expense-driven, demand intact, the whole multiple
> repriced off a cost delta — but MSCI's opex is a cost the company simply now carries, while
> the cost here is recovered from the customer BY CONTRACT on a lag. That difference is the
> entire read, so folding it into MSCI's tag would delete the information the by-scenario
> diagnostic exists to carry [ARC 5 #12a·5a].

## Move
J.B. Hunt fell double digits in a single session on heavy volume after its finance chief, at a
mid-quarter investor conference, flagged a sequential third-quarter earnings decline. There was
no earnings report and no change to the demand outlook. Trucking peers fell in sympathy; the
move took the stock to the low end of a three-month range it had already been drifting down.

## Why
The warning is entirely input-cost: incremental driver recruiting, training and signing-bonus
expense, plus a record-diesel fuel headwind that stepped higher in most weeks of the quarter.
Both are sequential, both are cost-side, and neither says anything about freight demand. The
implied quarterly hit is a rounding error against the company's market value — but the share
reaction is close to what you would get by capitalising that hit in perpetuity at a normal
multiple. The market chose the permanent reading of a cost line that has a contractual path
back.

## How
Two structural features make this repricing wrong in a way we can name:

1. **Fuel is a contractual pass-through with a lag, not a margin loss.** Intermodal and
   dedicated contracts carry fuel surcharges that reset behind the pump price. When diesel
   steps up eight weeks running, the surcharge collects the difference in the FOLLOWING
   quarter. The company's own last reported quarter shows the machinery working at scale —
   fuel surcharge revenue nearly doubled year over year. A lag is a timing item; the market
   priced it as a level.
2. **The same diesel spike is a demand tailwind for the largest profit engine.** Rail moves a
   container on a fraction of the fuel a truck burns, so expensive diesel widens intermodal's
   cost advantage and pulls freight off the highway. The last reported quarter said exactly
   this out loud — intermodal demand rose THROUGH the quarter, explicitly amid higher fuel
   prices and constrained driver capacity, and that segment's operating income grew sharply.
   The driver-cost line is largely the cost of onboarding that growing book, not damage to it.

The third feature is the one that makes it tradeable rather than merely wrong: the warning
RESET the bar. Consensus for the quarter came down roughly a sixth in a day, so the print that
lands inside our window is judged against a number management itself supplied.

## Pattern (reusable)
`passthrough-cost-lag-overreaction`: a company pre-announces a cost-driven earnings shortfall
in an input it recovers from customers CONTRACTUALLY on a lag, the market capitalises the lag
as a permanent margin reset, and the same input move is neutral-to-favourable for the
company's demand. To spot it on the next name, all four must hold:

- the disclosed hit is an INPUT cost, disclosed off-cycle, with no change to demand guidance;
- a contractual recovery mechanism exists and is demonstrably working (surcharge revenue,
  an index-linked price escalator, a tariff pass-through clause) — not merely hoped for;
- the implied permanent-capitalisation value of the hit is a large multiple of the hit itself;
- the input move does not destroy the company's own demand.

Disqualifiers, stated up front so this tag cannot be stretched later: a cost the company eats
(no contract path) is `guidance-cut-overreaction`, not this; a warning that also trims volume
or revenue guidance is a demand break and neither tag applies; a recovery mechanism that the
company says is being renegotiated away is not a recovery mechanism; and a pass-through that
lags by more than the bet's horizon cannot resolve inside the window, which makes the read
untestable rather than wrong.

## Prediction
Long JBHT, 21d (fast sleeve — a surcharge lag closes over a quarter-end and the reset print
lands inside the window), benchmarked against IYT so the trucking group's sympathy bounce is
subtracted rather than collected as edge. The honest risk: diesel keeps climbing and the lag
never closes, and the quarter's report sits inside the window carrying whatever else is wrong.
Scored in `bets.py`: `python3 -m research.bets show` → row `JBHT`.

## Links
- Bet: `python3 -m research.bets show` (`JBHT`)
- Related: `cases/MSCI.md` (the adjacent tag this one had to be separated from), FINDINGS
  `[ARC 5 #1]` (the catalogue bar), `[ARC 5 #14b]` (the tag↔case link this file honours),
  `[ARC 5 #12a·5a]` (the mix diagnostic a wrong tag would corrupt)
