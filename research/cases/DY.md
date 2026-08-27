# Case study: DY — a timing shift in already-booked work, priced as a demand break

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. It is the REASONING layer (see `research/ARCHITECTURE.md`): a
> case is born from a live move, states a falsifiable read, and **births one scored bet** in
> `research/bets.py`. Single source of truth — the case NARRATES; every number lives in its
> silo (`bets show`, `orders show`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-08-27  ·  **Pattern tag:** `revenue-deferral-overreaction`

> The backticked tag is the SAME string passed to `bets add --tag=`. This tag is COINED here
> rather than borrowed: the catalogue's nearest neighbour, `guidance-cut-overreaction`
> (`cases/MSCI.md`), requires a headline miss or trim, and this name did neither — it beat and
> lifted its full-year revenue guide. Reusing that tag would have been the ill-fitting reuse
> [ARC 5 #14b] warns about, and it would corrupt the mix diagnostic [ARC 5 #12a·5a].

## Move
Dycom fell roughly a fifth over five sessions into and through its fiscal second-quarter print,
with the largest single day coming on the report itself, on volume many multiples of normal.
The stock had already given back a chunk the prior week alongside the rest of the specialty
engineering-and-construction complex, so the earnings day landed on an already-broken tape and
closed near the session low.

## Why
The quarter itself was a record: revenue and adjusted earnings both above consensus, revenue
growing at a rate far above the market's model, and total backlog at an all-time high more than
half again the prior year's. The board also authorized a new repurchase.

What broke the stock was the NEXT quarter's earnings guide, whose midpoint came in modestly
below consensus while the revenue guide came in essentially in line. The cause management gave
is specific and checkable: a slice of wireless revenue has been **deferred out of the back half
of this fiscal year into the next one**. The company stated the associated scope and backlog are
unchanged and that the program is running ahead of plan operationally — the work is signed, it
is simply invoiced later.

Alongside that sits a genuine negative that is NOT timing: margin compressed on expansion
investment, wireless project delays and higher fuel. That is the part of the bear case that
deserves respect, and it is the reason this read is not high conviction.

## How
The structure that enables the overreaction is the mismatch between how a deferral is DISCLOSED
and how it is TRADED. A revenue shift arrives inside a forward EPS guide, which is the single
number that screens, headline generators and momentum systems read. Those consumers cannot
distinguish "revenue moved a year" from "revenue did not materialize" — both print as a guide
below consensus. Meanwhile the quantity that actually contradicts the demand-break reading —
backlog — sits in the release body and does not screen.

The de-rating then compounds mechanically: the name had already been sold with its sector, so
the print lands on holders who are already offside, and the exit is one-way for a session.

## Pattern (reusable)
`revenue-deferral-overreaction`: a forward guide falls short **because booked revenue moved
between periods**, the market prices it as demand lost, and the position is that the gap closes
as the backlog converts. How to spot it on the next name:
- Management names the shift explicitly and quantifies it, and says scope/backlog are unchanged.
  A vague "timing" with no figure is a euphemism, not a deferral — skip it.
- A forward-looking quantity moves the OTHER way: backlog, bookings, or book-to-bill at a record.
- The shortfall is on the EARNINGS line while the revenue guide holds. If both fall, it is a
  demand break wearing a deferral's clothes.
- The price reaction is a large multiple of the guide delta.

Disqualifiers, stated up front so this tag cannot be stretched later: a deferral that recurs
(the second consecutive quarter of "pushed to next year" is a demand break being disclosed
slowly); a deferral used to explain away a margin decline as well as a revenue one; and a name
whose customer concentration means one deferred program IS the demand.

The trap this pattern owns: a deferral is only worth what the backlog is worth, and backlog at
a contractor is a promise priced at the customer's capital-budget discretion, not a receivable.
If the end market — here, carrier and data-center network build — de-rates, the backlog converts
later and at worse margin, and the deferral turns out to have been the first crack rather than
an accounting boundary. That is the same de-rating that took the whole peer group down in the
same week, which means this bet is less independent of the tape than its name-specific framing
suggests.

## Prediction
Long DY, 21d (fast sleeve — a misread of a disclosure resolves over weeks, as the next set of
estimates and the peer prints land, not over a quarter), vs XLI. Medium conviction: the timing
half of the bear case looks wrong, the margin half may not be.
Scored in `bets.py`: `python3 -m research.bets show` → row `DY`.

## Links
- Bet: `python3 -m research.bets show` (`DY`)
- Counterfactual order: `python3 -m research.orders show` (`DY`) — [ORDERS #1] band diagnostic
- Related: `cases/MSCI.md` (the adjacent shape this one is deliberately NOT filed under) ·
  FINDINGS `[ARC 5 #1]` (the catalogue bar), `[ARC 5 #14b]` (tag↔case link), `[ARC 5 #11]`
  (the tail cohort's higher read bar this take had to clear)
