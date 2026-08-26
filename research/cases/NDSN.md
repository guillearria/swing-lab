# Case study: NDSN — a record quarter whose ORDER BOOK, not the beat, is the signal

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `book`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-08-26  ·  **Pattern tag:** `post-earnings-drift`

> The backticked tag is the SAME string passed to `bets add --tag=`. This case exists because
> `post-earnings-drift` is the catalogue's MOST-USED tag and had NO case file backing it —
> `engine` was starring it as unbacked [ARC 5 #14b]. This file is that backing: it states what
> the shape actually claims, and — more usefully — what disqualifies a candidate from it.
- Related: FINDINGS `[ARC 5 #1]` (the catalogue bar), `[ARC 5 #14b]` (tag↔case link),
  `[ARC 5 #12a·5a]` (the mix diagnostic this tag dominates)

## Move
Nordson gapped up roughly eight percent the session after its fiscal third quarter (reported in
the third week of August) and then did the thing that matters: it HELD. Three subsequent sessions
closed inside the top of the gap-day range on unremarkable volume, with no give-back — the stock
sat at the high end of its year rather than fading back into the pre-print base.

## Why
The headline is a beat on both lines with all three segments at record quarterly sales and a
raised full-year outlook. But the beat is not the read — beats are common in August and the market
prices them within a day.

The read is the ORDER BOOK. Backlog stands more than a third above the prior year, and the
Advanced Technology segment grew organically at roughly ten times the company's blended rate.
That segment sells test, inspection and precision-dispense equipment into electronics and
semiconductor manufacturing. So the claim embedded in the print is forward: the work is already
booked, and it is booked in the part of the business the market is currently most worried about.

That timing is the whole point. This print landed in the same fortnight that the market flushed the
AI-hardware complex on capex-fear (the same flush behind `cases/FN.md`). Nordson's backlog is an
awkward fact for that narrative — it is a signed order book, not a forecast.

## How
The structure that enables the drift: estimate revisions are slow and serial. A raised full-year
guide plus a backlog figure forces analysts to re-model NEXT year, not just re-print this one, and
those revisions arrive over weeks. Institutions building a position in a mid-cap industrial cannot
do it in one session. The gap is the first repricing; the drift is the rest of the market catching
up to a number that was already public.

## Pattern (reusable)
`post-earnings-drift`: buy a beat-and-raise into the days after the gap and hold while estimate
revisions work through. This is the catalogue's default shape and therefore the one that most needs
a disqualifier list. What makes a candidate QUALIFY rather than merely beat:
- The raise is to the FULL YEAR, not a single quarter.
- There is a forward-looking quantity confirming it — backlog, bookings, book-to-bill, renewal
  rate — not just a trailing beat.
- The stock HELD the gap. A gap that fades in the first three sessions is a sell-the-news, and the
  drift thesis is already falsified before entry.
Disqualifiers, each of which cost us a bet somewhere in the catalogue: a beat carried by a one-off
(a tariff refund, an insurance recovery, a tax item), a beat on rising promotional intensity, and a
print more than about two weeks stale — the drift window is measured in weeks, so a month-old
catalyst with a stock at highs is a CHASE wearing this tag.

The trap this pattern owns, stated plainly: it is the most crowded, most-arbitraged shape we run,
and it is the reason the mix diagnostic keeps flagging concentration. Every entry is bought at or
near a 52-week high, so the pattern has no margin of safety — it is entirely a bet on revision
momentum continuing. In a market-wide de-rating, revisions stop mattering and the whole tag drifts
down together, which means these bets are far less independent of each other than their count
suggests. Medium conviction is the ceiling for this shape.

## Prediction
Long NDSN, 21d (fast sleeve — the drift window is weeks, and the print is days old), vs XLI.
Scored in `bets.py`: `python3 -m research.bets show` → row `NDSN`.

## Links
- Bet: `python3 -m research.bets show` (`NDSN`)
- Related: FINDINGS `[ARC 5 #1]`, `[ARC 5 #12a]`, `cases/FN.md` (the same AI-capex flush, read
  from the other side — FN was thrown out with the sector, NDSN's backlog contradicts it)
