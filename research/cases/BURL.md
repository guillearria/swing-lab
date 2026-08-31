# Case study: BURL — a raised full-year guide sold to a three-month low

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. Single source of truth — the case NARRATES; every number lives
> in its silo (`bets show`, `FINDINGS`) and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-08-31  ·  **Pattern tag:** `revenue-miss-overreaction`

> The backticked tag is the SAME string passed to `bets add --tag=`. The tag already existed in
> the catalogue (VRT, 2026-07-30) but NO case file declared it, so `engine` starred it as
> unbacked [ARC 5 #14b]. This case declares it. The two declared neighbours were both wrong
> here: `sector-sympathy-selloff` (cases/FN.md) requires that the name did NOT miss on its own
> results, and BURL did miss revenue; `one-time-item-obscured-beat` (cases/ANF.md) requires a
> non-recurring item dominating the headline, and there is none.
- Related: `cases/FN.md` (the neighbour this is not), `cases/ANF.md` (the other retail bet live
  at the same time), FINDINGS `[ARC 5 #1]` (the catalogue bar), `[ARC 5 #14b]` (tag↔case link)

## Move
Burlington fell four consecutive sessions into the last complete bar of this run, giving back
roughly a sixth of its value and closing at the very low of its three-month range on the
heaviest volume of the stretch. The retail ETF it is benchmarked against fell about a fiftieth
over the same four days. Two of the four down days were before its own results: the sector was
already being sold after a large full-price sporting-goods retailer collapsed on a guidance cut.
The print took another leg out, and the session AFTER the print took a further one — the selling
had not stopped when the window closed.

## Why
The results themselves went the other way. Non-GAAP earnings per share came in roughly a third
above consensus, the fifteenth consecutive quarter of double-digit earnings growth, operating
margin expanded a full point on better merchandise margins and supply-chain productivity, and
the company RAISED its full-year outlook on both lines — revenue growth and adjusted earnings —
having entered the quarter guiding lower.

What the market punished is the revenue line and the trajectory underneath it: total sales came
in below the consensus dollar figure, and comparable-store sales decelerated sharply against a
much stronger prior-year comparison. In a week when a peer had just cut its full-year earnings
guide by a fifth, a decelerating comp read as the first crack in the same consumer.

The read is that those two facts are about different companies. The peer's collapse came from an
acquired full-price footwear chain running negative operating earnings; that is an integration
and format problem, not a demand signal. Off-price is the format that GAINS share when the
consumer trades down, so the very weakness being extrapolated onto Burlington is the condition
its model is built for. Nothing in the quarter or the raised guide says otherwise.

## How
The structure that enables the mispricing is benchmark contagion inside a narrow sector window.
A single large retailer blows up, every screen and sector fund marks the whole group down, and
then a second name reports into that tape. Its own miss — real but small, on the line the market
was already primed to punish — arrives pre-discounted by the group move, so the reaction
compounds instead of pricing the name on its merits. The result is a stock at the low of its
range while its own forward estimates are being revised UP.

The other half of the structure is where the sell side sits. Coverage had been trimmed to
neutral weeks earlier on valuation, at a target well ABOVE the current price. That cuts both
ways and must be said plainly: it means the published targets have not yet been cut, so the
"analysts are behind" tell that `one-time-item-obscured-beat` relies on is NOT available here.
The revision wave could go either direction.

## Pattern (reusable)
`revenue-miss-overreaction`: buy the days after a print where the REVENUE line missed but
earnings, margin and the FORWARD GUIDE all went up, and the price reaction is far larger than
the revision to the forward numbers. What makes a candidate QUALIFY:
- The full-year guide was RAISED — not held, not trimmed. A raise is the company's own
  statement that the miss did not change the year.
- The miss is on the top line only. If earnings or margin also missed, the market is pricing
  deterioration and this is the wrong pattern.
- The drawdown is materially larger than the drawdown of the sector benchmark over the same
  window, so there is a name-versus-sector gap to close and not just a sector move to ride.
- There is an identifiable EXTERNAL driver for part of the fall — a peer's blow-up, an index
  flush — which the name's own results contradict.

Disqualifiers: guidance cut or merely reaffirmed; a decelerating metric that management itself
flags as structural; a miss driven by lost share to a named competitor rather than by pricing,
timing or mix.

The trap this pattern owns, stated plainly: a top-line miss with a deceleration underneath it is
exactly what the FIRST quarter of a genuine demand rollover looks like, and management guidance
is the last thing to break. "The guide was raised" is weak evidence when the guide is three
weeks old. The honest version of this bet is that the price has moved further than the evidence
justifies TODAY, not that the deceleration is fake. Two further weaknesses travel with it here:
the stock closed at the low of its range with the selling still accelerating, so there is no
stabilisation to lean on, and the catalogue already carries two other long retail bets scored
against the same benchmark, which means this is partly one macro draw and not three independent
ones. Medium conviction, never high, on this shape.

## Prediction
Long BURL, 21d (fast sleeve — a sector-contagion gap closes in weeks, not quarters), vs XRT.
Scored in `bets.py`: `python3 -m research.bets show` → row `BURL`.

## Links
- Bet: `python3 -m research.bets show` (`BURL`)
- Counterfactual order: `python3 -m research.orders show` (`BURL`)
- Related: `cases/FN.md`, `cases/ANF.md`, FINDINGS `[ARC 5 #1]`, `[ARC 5 #12a]`
