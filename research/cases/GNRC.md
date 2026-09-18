# Case study: GNRC — a weather-cyclical manufacturer signs an anchor customer and changes shelf

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. The case NARRATES; every number lives in its silo (`bets show`)
> and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-09-18  ·  **Pattern tag:** `anchor-customer-contract-rerating`

> The backticked tag is the SAME string passed to `bets add --tag=`. It is COINED here rather
> than reused [ARC 5 #14b]. The nearest existing tags are `narrative-stage-transition`
> (`cases/AKAM.md`) and `guidance-raise-offcycle` (`cases/SEI.md`), and both miss the thing
> that defines this one. AKAM's pattern is a STORY changing on a cluster of soft catalysts —
> product launches, an upgrade, a re-frame — with no contracted dollars behind it; the whole
> point here is that the dollars ARE contracted and filed. SEI's pattern is the company
> revising its OWN forecast off-cycle; here the new information comes from a third party
> signing a purchase agreement, and it arrives with that counterparty taking equity exposure.
> Folding either way would delete the information the by-scenario diagnostic exists to carry
> [ARC 5 #12a·5a].

## Move
Generac had been drifting lower through the first half of September — a soft tape for a
company the market still prices off residential standby demand and storm season. Then, after
one session's close, an 8-K disclosed a long-term supply agreement with a hyperscaler for
data-center backup power, together with a warrant issued to that customer. The stock printed a
very large after-hours gain, gave back roughly half of it by the next close, and still finished
the session above where it had traded before the de-rating started, on many times normal volume.

## Why
A cyclical manufacturer is valued on the volatility of its end demand as much as on its level.
Home standby generators sell when storms come; that is a business the market discounts for
unpredictability. A multi-year supply agreement with a named, credit-worthy, capex-committed
customer replaces part of that demand distribution with a schedule. The earnings do not change
this quarter — the DISCOUNT RATE and the multiple are what should change, and those move slowly,
because the holders who own the name for the old reason are not the holders who will own it for
the new one.

## How
The structure that enables the slow repricing: (1) the headline number is a CEILING contingent
on orders, not a booked backlog, so the disciplined buyer waits for deliveries to confirm it
while the momentum buyer front-runs — a two-sided flow that caps the first day's move; (2) the
warrant vests in tranches against cumulative payments, so each future order is its own small
catalyst rather than one clearing event; and (3) the counterparty struck its warrant above the
undisturbed price, which is a public, dated statement by an informed party about where it
expects the shares to go — information the tape digests over weeks, not in one session.

## Pattern (reusable)
`anchor-customer-contract-rerating`: a filed, dollar-quantified, multi-year purchase agreement
from a NAMED anchor customer lands on a company the market prices off a cyclical or
weather-driven demand base → bet the multiple keeps migrating as deliveries confirm the
schedule. Spot it: an 8-K, not a press release · a named counterparty with the balance sheet to
pay · a delivery schedule with dates · equity alignment (warrant, prepayment, JV) · a first-day
move that FADES from its after-hours print, which is the tell that the market split between
front-runners and wait-and-see rather than fully repricing. The trap this pattern owns: the
ceiling is not the order. A headline built on an "up to" number can stall for years if the
customer never draws it down, and the same fade that signals an incomplete repricing can
equally signal that the informed money read the ceiling correctly and sold into the pop. The
only honest discriminator is whether the NEAR-term tranche is scheduled and dated — if only the
ceiling is public, this is `narrative-stage-transition`, not this tag.

## Prediction
The falsifiable call (direction / horizon / benchmark). Scored in `bets.py`:
`python3 -m research.bets show` → row `GNRC`. Outcome accrues to the engine + FINDINGS bar.

## Links
- Bet: `python3 -m research.bets show` (`GNRC`)
- Related: `cases/AKAM.md` (`narrative-stage-transition`), `cases/SEI.md`
  (`guidance-raise-offcycle`), FINDINGS `[ARC 5 #14b]`
