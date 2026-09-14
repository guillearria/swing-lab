# Case study: CASY — a beat priced as if it were a cut, because the guide only held

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-09-14  ·  **Pattern tag:** `guidance-hold-punished-as-cut`

> The backticked tag is the SAME string passed to `bets add --tag=`. It is COINED here rather
> than borrowed, because every declared neighbour misdescribes the mechanism and reusing one to
> dodge writing this file is the trap [ARC 5 #14b] names:
> `guidance-cut-overreaction` (cases/MSCI.md) requires a CUT — there was none, the guide was
> reiterated; `post-earnings-drift` (cases/EL.md, cases/NDSN.md) drifts in the direction of the
> price reaction to a beat, and here price and surprise point OPPOSITE ways, which is the whole
> point; `revenue-miss-overreaction` (cases/BURL.md) needs a miss; `guidance-raise-offcycle`
> (cases/SEI.md) is the company moving its own numbers UP, the mirror of this.

## Move
A convenience-store compounder reported its fifth consecutive EPS beat, beat on both lines, and
fell by roughly a fifth inside a week — straight to a three-month low, with three consecutive
lower closes and no stabilisation by Friday. The sell side cut price targets *after* the beat.

## Why
Nothing in the reported quarter deteriorated. Management simply REITERATED the full-year EBITDA
growth range instead of raising it, one quarter into the fiscal year, after a quarter whose own
EBITDA growth ran roughly double the full-year range. A stock priced for an upgrade treats the
absence of one as news, and marks down to the guide it was already given.

## How
The structure that enables it: a premium multiple built on a habit of raising, met by a company
whose habit is to hold at Q1 and raise later. The bear's counter is that the beat's quality was
fuel-margin-led — genuinely volatile, genuinely non-recurring — so the hold is honest rather
than conservative. That is the falsifiable fork, and it is why this is a MEDIUM-conviction read
rather than a high one.

## Pattern (reusable)
**A positive earnings surprise with a negative price reaction is the setup; a guidance HOLD is
the usual cause.** Post-earnings drift keys on the SURPRISE, not on the day's price reaction, so
the interesting case is exactly the one where the two disagree. To spot it on the next name, ask
three questions: (1) did the company beat, on both lines? (2) was the guide CUT, or merely not
raised? (3) is the quarter's own growth running ahead of the full-year range it reaffirmed?
Three yeses and the market is pricing a deceleration the company has not reported. One "cut"
in answer to (2) and this is not the pattern — it is `guidance-cut-overreaction` or nothing.
The trap to avoid: this pattern says nothing about the MULTIPLE. A name can be correctly
re-rated down and still have beaten; if the read depends on the multiple recovering rather than
on the guide proving conservative, it is not this pattern and should be skipped.

## Prediction
Long, 63d, benchmarked to its sector ETF. Scored in `bets.py`:
`python3 -m research.bets show` → row `CASY`. Outcome accrues to the engine + FINDINGS bar.
Kill: a genuine guidance CUT at the next print, or the fuel-margin line confirming the beat was
non-recurring — either makes the hold correct and the read wrong.

## Links
- Bet: `python3 -m research.bets show` (`CASY`)
- Related: `cases/MSCI.md` (the cut this is not), `cases/SEI.md` (the off-cycle raise, its
  mirror), `cases/EL.md` / `cases/NDSN.md` (the drift neighbours whose price and surprise agree),
  FINDINGS `[ARC 5 #1]` (the catalogue bar), `[ARC 5 #14b]` (the tag↔case link this file honours)
