# Case study: UTHR — a court removes the only competitor the estimates were already discounting

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-10-02  ·  **Pattern tag:** `competitor-blocked-estimate-reversal`

> The backticked tag is the SAME string passed to `bets add --tag=`. It is COINED here rather
> than borrowed, because every declared neighbour describes a different mechanism and reusing one
> to dodge writing this file is the trap [ARC 5 #14b] names:
> `lost-option-overmark` (cases/ENVA.md) is the SUBJECT losing an option it was over-marked for —
> here a RIVAL loses and the subject gains, the inverse;
> `insourcing-threat-overreaction` (cases/HWM.md) is a competitive threat TO the subject that the
> market over-priced — here the threat is removed outright, not over-priced;
> `dead-deal-acquirer-rerating` (cases/SOLS.md) is the closest in shape, a transaction dying and
> the subject re-rating, but a withdrawn deal is not a court narrowing a competitor's label;
> `analyst-rerating` (cases/MRK.md) would make the sell side the driver, and the driver is a
> district court whose ruling the sell side has not yet modelled.

## Move
A large profitable biotech, flat for roughly six months and sitting just under its one-year high,
re-rated sharply on a single session after a district court ruled in its favour in a patent suit
against the only recently-launched competitor to its largest franchise. The competitor fell by
roughly half on the same ruling, and the two moves were close to equal and opposite in dollar
terms — the market transferred the value across the pair in one day.

## Why
The ruling held the asserted claims valid and infringed for the indication that mattered: the
newer, faster-growing of the two uses of the drug class. The competitor said it would appeal AND
that it would amend its own pending application to remove that indication from its label. That
second half is the important part — it is the loser conceding the near-term commercial ground
without waiting for the appeal, which means the incumbent's share-loss assumptions do not merely
pause, they reverse.

## How
The structure that enables it: sell-side models had already been cut to reflect a competitor that
was launching and taking share. Those cuts are an ASSUMPTION about future quarters, not a realised
fact, and a court order is the one event that can delete an assumption outright. The incumbent's
reported revenue has not changed yet; what changed is the forward line, and the forward line is
revised on a quarterly-report cadence, not in a single session. So the one-day move prices the
headline, while the estimate reversal lands over the following weeks and is confirmed (or not) at
the next print.
The bear's counter, and it is real: the appeal is live, the competitor can still sell into the
other indication, and the remedies judgment is due within days — a royalty-only remedy rather
than an injunction would let the competitor keep shipping into the blocked indication pending
appeal and would partly undo the move. That dated, two-sided event sits INSIDE the window, which
is why this is a MEDIUM-conviction read and not a high one.

## Pattern (reusable)
**When a court or regulator blocks a competitor's product in the indication the incumbent's
estimates were already discounting, the one-day move prices the headline and the estimate
reversal drifts.** To spot it on the next name, require all four:
(1) the blocked competitor was ALREADY in the incumbent's consensus as share loss — if nobody had
modelled it, there is nothing to reverse;
(2) the block covers the economically dominant indication or channel, not a peripheral one;
(3) the loser CONCEDES operationally — withdraws, amends its label, pulls guidance — rather than
only appealing, because an appeal alone leaves the assumption intact; and
(4) the incumbent is not already extended — a name at the top of a momentum run has no room for a
revision cycle to show up in price.
Two traps. First, the remedies or implementation ruling usually comes AFTER the liability ruling,
and it is a second coin flip: check whether it lands inside your window before choosing a
horizon. Second, if the pair's two moves are roughly equal and opposite in dollar terms — as they
were here — the market has already transferred the value once, so the only thing left to capture
is the revision cycle. That is a real but modest edge, and it is the whole bet.

## Prediction
Long, 63d (the revision cycle is quarterly-report-paced and the next print falls inside the
window), benchmarked to the large-cap biotech index so sector beta nets out. Scored in `bets.py`:
`python3 -m research.bets show` → row `UTHR`. Outcome accrues to the engine + FINDINGS bar.
Kill: a remedies judgment that stops short of blocking the competitor's sales into the disputed
indication, an appellate stay, or a next print showing the franchise still losing share — any of
those makes the ruling a headline rather than an estimate event and the read wrong.

## Links
- Bet: `python3 -m research.bets show` (`UTHR`)
- Related: `cases/SOLS.md` (the dead-deal sibling this is not), `cases/HWM.md` (the mirror case:
  a threat TO the subject, over-priced), `cases/ENVA.md` (the subject losing its own option),
  FINDINGS `[ARC 5 #1]` (the catalogue bar), `[ARC 5 #14b]` (the tag↔case link this file honours)
