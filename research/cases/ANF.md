# Case study: ANF — the one-time item that made a clean beat look hollow

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-08-28  ·  **Pattern tag:** `one-time-item-obscured-beat`

> The backticked tag is the SAME string passed to `bets add --tag=`. This case exists because the
> tag is COINED here [ARC 5 #14b]: `cases/NDSN.md` lists "a beat carried by a one-off (a tariff
> refund, an insurance recovery, a tax item)" as an explicit DISQUALIFIER for
> `post-earnings-drift`. Reusing that tag here would have been the ill-fitting reuse the doc
> warns about, because the claim of this trade is the OPPOSITE of the disqualifier: the one-off
> is in the headline, not in the beat.
- Related: `cases/NDSN.md` (the parent shape and its disqualifier list), FINDINGS `[ARC 5 #1]`
  (the catalogue bar), `[ARC 5 #14b]` (tag↔case link), `[ARC 5 #12a·5a]` (the mix diagnostic)

## Move
Abercrombie & Fitch reported fiscal Q2 before the open on 26 August and gapped roughly a third
higher in one session on about fourteen times its normal volume. The next session it gave back
almost nothing — a shade over one percent, on a quarter of the gap-day volume. It went up, and
then it sat there.

## Why
The headline is a freak. Reported net income per diluted share came in at more than twice the
consensus and more than twice the company's own prior guidance range, because roughly a hundred
million dollars of refunded IEEPA tariffs landed as a reduction in cost of sales. Every wire
story led with the refund, and the refund is genuinely non-recurring.

That framing is the opportunity. Strip the refund out and the quarter still beat consensus by
about a fifth on earnings, revenue still grew mid-single digits and still beat, and the raised
full-year outlook still rises meaningfully above the prior range on an ex-refund basis — the
company attributed the raise to first-half execution and a strong start to August, not to the
refund. The forward quarter is guided above consensus on both lines. None of that is a one-off.

The valuation is the second half of the read, and it is what separates this from the ordinary
drift trade. Even after the gap, and even after stripping the refund entirely out of the
full-year guide, the stock trades at a low-teens multiple of earnings. The published analyst
price-target consensus at the time of entry sits BELOW the market price — the sell side has not
re-modelled yet.

## How
The structure that enables the drift: a contaminated headline slows the machinery that normally
prices a beat in a day. Screens, wire summaries and quant revision feeds ingest the reported
number, flag it as low-quality, and discount it. Analysts have to rebuild the model by hand to
find the clean number, and only then publish. So the repricing arrives in two stages — the
mechanical gap on day one, then the human revision wave over the following weeks — and the
second stage is the one that is buyable.

The tell that the second stage is still ahead: published price targets below the traded price.
When the sell side is behind the tape, the revisions have not happened yet.

## Pattern (reusable)
`one-time-item-obscured-beat`: buy the days after a gap where a NON-RECURRING item dominates the
headline but the EX-ITEM result independently beats, and hold while the sell side re-models.
What makes a candidate QUALIFY:
- The ex-item number is computable and is stated by a credible source — not estimated by us.
- The ex-item result beats on its OWN, without the item. If the beat needs the item, this is
  the NDSN disqualifier and the candidate is a SKIP, not a re-tag.
- The forward guide (next quarter and full year) also rises ex-item. A raise that is purely the
  item passed through is not a raise.
- Published price targets are still BELOW the traded price — the revision wave is ahead of us.
- The stock HELD the gap. A fade in the first sessions falsifies the thesis before entry.

Disqualifiers: the item is the beat (see above); the item is expected to recur, in which case
the market is right to capitalise it and there is no misframing; a legal or political item whose
CASH is still reversible, which is a different trade with a different risk.

The trap this pattern owns, stated plainly: "the market has misread the quality of the print" is
the single easiest thing in markets to tell yourself, and it is unfalsifiable at entry. It is
also a shape with an obvious selection problem — we will notice it exactly when the ex-item
number happens to look good. The discipline that keeps it honest is the qualify list above,
every item of which is checkable from the press release before the bet is written, plus the fact
that the skip ledger scores the ones we pass on. And the ex-item cushion is not a floor: a
low multiple did not save any retailer in a genuine consumer rollover, and two large athletic
and off-price retailers broke down badly in the same week this bet was written.

## Prediction
Long ANF, 21d (fast sleeve — the revision wave is a weeks-long window and the print is days
old), vs XRT. Scored in `bets.py`: `python3 -m research.bets show` → row `ANF`.

## Links
- Bet: `python3 -m research.bets show` (`ANF`)
- Counterfactual order: `python3 -m research.orders show` (`ANF`)
- Related: `cases/NDSN.md` (the disqualifier that forced this tag to exist), FINDINGS
  `[ARC 5 #1]`, `[ARC 5 #12a]`
