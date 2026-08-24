# Case study: AKAM — a value-trap re-rates when its story changes shelf

> A **case study** documents a notable price MOVE so its mechanism becomes a REUSABLE pattern
> we can spot on the next name. The case NARRATES; every number lives in its silo (`bets show`)
> and is referenced by command, never restated.

**Status:** open  ·  **Date:** 2026-08-24  ·  **Pattern tag:** `narrative-stage-transition`

> The backticked tag is the SAME string passed to `bets add --tag=`. AKAM is the ORIGIN row
> of this tag (logged 2026-07-13) and it was unbacked until now [ARC 5 #14b]. Written from
> the LOGGED theses — all three rows are still open, outcomes unknown, no hindsight.

## Move
Akamai began re-rating upward on a cluster of name-specific AI catalysts — an agentic-AI
security framework launched with marquee partners, a security acquisition closed, and a
sell-side upgrade carrying a price target far above spot. Gartner (IT) and Charles River
(CRL) later joined the tag: each a beat-and-raise print at a name the market had filed under
a stale, cheaper story.

## Why
The market prices a company off the STORY it currently sits on — "legacy CDN", "consulting
in an AI world", "post-COVID preclinical hangover" — and holds that story until forced off
it. A dense-enough cluster of catalysts (product + M&A + analyst re-frame + numbers that fit
the NEW story) forces the transition, and the multiple migrates from the old story's shelf
to the new one's. The repricing is slow because consensus narratives change holder by holder.

## How
The structure that enables it: years of underperformance concentrate ownership in value
holders who anchor to the old story, while the new business line grows quietly inside the
old wrapper. When the external catalysts land, there is no fast mechanism to reprice — no
single print "proves" a narrative — so the move extends over weeks as coverage, screens and
mandates catch up. That slow diffusion is what a 63d horizon is built to capture.

## Pattern (reusable)
`narrative-stage-transition`: a name-specific re-rating driven by the STORY changing, not by
one quarter's numbers → bet the multiple keeps migrating toward the new story. Spot it:
multiple simultaneous catalysts pointing at the SAME new identity · a sell-side re-frame
("underappreciated X") · the old story's multiple still dominant in the price. The trap this
pattern owns: chronic value traps generate false transitions — an AI-flavored press cycle on
an unchanged business fades with the tape (the anchor row's own stated risk: the AI premium
can unwind in an AI-unwind tape). Demand at least one catalyst that is CONTRACTUAL (product
shipped, deal closed), not narrative-only.

## Prediction
Long, 63d (narratives migrate over quarters), vs the sector benchmark. Scored in `bets.py`:
`python3 -m research.bets show` → rows `AKAM`, `IT`, `CRL`.

## Links
- Bets: `python3 -m research.bets show` (tag `#narrative-stage-transition`)
- Related: `cases/FN.md` (sector-driven mispricing, the converse) · FINDINGS `[ARC 5 #14b]`
