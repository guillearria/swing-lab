# Case study: HUM — a regulator handed back the bonus it took away three years ago

**Status:** open  ·  **Date:** 2026-10-12  ·  **Pattern tag:** `regulatory-rating-restored`

## Move
Humana gapped up hard on the CMS 2027 Medicare Advantage star-ratings release (published
after the close on 2026-10-08, first full session 10-09) — the largest one-day move in the
name since March 2020, on roughly five times normal volume. Managed-care peers did not move
together: at least one smaller MA insurer fell the same day, so this was a name-specific
re-rating inside a sector that was otherwise flat.

## Why
CMS re-rated Humana's national PPO contract H5216 from 3.5 to 4.0 stars. That single contract
carries the bulk of Humana's MA membership, and the 4.0 threshold is the cliff at which the
quality-bonus payment switches on. The company's own release puts about 95% of its MA members
in 4-star-or-better plans for 2027, against roughly 20% for 2026. Sell-side work circulating
on the day sized the restored bonus stream in the multiple-billions for the 2028 payment year.

## How
The structure that makes this different from a sentiment pop: star ratings are an
ADMINISTRATIVE determination, already published, with a mechanical payment consequence in a
fixed future year. Nothing further has to go right at the company for the money to arrive —
no product launch, no share gain, no macro. The de-rating being reversed is the same one that
removed H5216's bonus three years ago and drove a multi-year compression in the multiple; the
market has carried that loss as permanent long enough for it to be embedded in consensus.

## Pattern (reusable)
`regulatory-rating-restored` — a regulator or standards body restores a rating, licence or
designation whose LOSS was previously capitalised into the price, and the restoration carries
a mechanical cash consequence in a year beyond the usual two-year model window. Spot it by
three marks: (1) the catalyst is an administrative fact, not a forecast; (2) the money lands
in a payment year most published models do not yet carry; (3) the prior loss was large enough
to have been treated as structural. The read is that the day-one move prices the headline
while the estimate revisions arrive over the following weeks. Distinct from
`expired-exogenous-headwind` (a drag that merely rolls off) and from `analyst-rerating`
(where the analysts move first).

## Prediction
Long, 21 days, vs XLV. Scored in `bets.py`: `python3 -m research.bets show` → row `HUM`.
Falsified if HUM fails to beat XLV over the window — most directly if the Q3 print inside the
window resets 2027 guidance, or if the market judges that the bonus is reinvested into member
benefits rather than margin.

## Links
- Bet: `python3 -m research.bets show` (`HUM`)
- Counterfactual order: `python3 -m research.orders show` (`HUM`)
- Related: FINDINGS `[ARC 5 #18]` (the pooled verdict this row accrues behind), `cases/_TEMPLATE.md`
