# Case study: DRI — an in-line quarter marked down for a headwind that had already expired

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-09-30  ·  **Pattern tag:** `expired-exogenous-headwind`

> The backticked tag is the SAME string passed to `bets add --tag=`. It is COINED here rather
> than borrowed, because every declared neighbour misdescribes the mechanism and reusing one to
> dodge writing this file is the trap [ARC 5 #14b] names:
> `guidance-hold-punished-as-cut` (cases/CASY.md) is the closest sibling but its pattern opens
> with "did the company BEAT, on both lines?" — here the quarter was merely IN LINE, so the
> setup is a soft comp, not a positive surprise the tape disagreed with;
> `guidance-cut-overreaction` (cases/MSCI.md) requires a CUT, and the full-year guide was
> reaffirmed; `post-earnings-drift` (cases/EL.md, cases/NDSN.md) keys on a SURPRISE that here
> did not happen; `sector-sympathy-selloff` would make this a sector move, and the driver is
> specific to one brand's menu.

## Move
A large casual-dining operator reported an in-line quarter, reaffirmed its full-year EPS range,
and sold off through the rest of the week — five consecutive lower closes, each session making a
new low, into a multi-month low with no stabilisation by the last complete bar.

## Why
The flagship brand's same-restaurant sales decelerated to their weakest print in nearly two
years. Management attributed a stated portion of that deceleration to two identifiable and
DATED exogenous events: a national cyclospora outbreak traced to packaged iceberg lettuce — in
which the chain itself was never implicated, but which made customers avoid salad, forcing the
company to pull its unlimited soup-salad-breadsticks advertising campaign mid-quarter — and the
World Cup pulling evening traffic. Both had passed by quarter-end, and management said September
traffic accelerated once they did. The market marked the comp as a trend line rather than as a
quarter with a hole in it.

## How
The structure that enables it: a quarterly reporting cadence that reports a WINDOW, against a
consumer scare that resolves on a news cycle. The scare's damage lands entirely inside the
reported quarter; the recovery lands entirely inside the unreported one. Anyone extrapolating
the printed comp is extrapolating a period the company has already told you is over — and the
sell side's models key off the printed number.
The bear's counter, and it is real: casual-dining traffic is genuinely soft industry-wide, the
quarter also showed margin pressure that has nothing to do with lettuce, and "September
accelerated" is management's own unaudited characterisation of an unreported month. That is the
falsifiable fork, and it is why this is a MEDIUM-conviction read rather than a high one.

## Pattern (reusable)
**When a soft print has a NAMED, DATED, exogenous cause that has already expired, the market
often prices the print and not the calendar.** To spot it on the next name, require all four:
(1) the softness is attributed to a specific external event, not to demand or competition;
(2) the event has an END DATE that has already passed — an outbreak resolved, a tournament
finished, a port reopened, a hurricane gone;
(3) the company did NOT cut its forward guide, which is its own statement that the hole does not
recur; and
(4) the affected business is the one the event could plausibly touch — the mechanism has to
connect, or this is a story dressed as a pattern.
Two traps. First, an "expired" headwind that merely MORPHED (a lettuce scare replaced by a
beef-cost spike) is not this pattern. Second, and more expensive: this pattern says nothing
about the structural trend underneath. If the brand was losing traffic BEFORE the event, the
event is cover, not cause — check the prior prints, and skip if the pre-event line already
pointed down.

## Prediction
Long, 21d (fast sleeve — the mechanism is already resolving, not a quarter away), benchmarked to
its sector ETF. Scored in `bets.py`: `python3 -m research.bets show` → row `DRI`. Outcome
accrues to the engine + FINDINGS bar.
Kill: a guidance cut or a negative pre-announcement inside the window, or evidence the flagship
brand's traffic kept decelerating through September after the two headwinds cleared — either
makes the printed comp the trend and the read wrong.

## Links
- Bet: `python3 -m research.bets show` (`DRI`)
- Related: `cases/CASY.md` (the beat-and-hold sibling this is NOT — in line, not a beat),
  `cases/MSCI.md` (the cut this is not), `cases/JBHT.md` (the other single-name industrial
  read where a dated cost event met an unreported recovery), FINDINGS `[ARC 5 #1]` (the
  catalogue bar), `[ARC 5 #14b]` (the tag↔case link this file honours)
