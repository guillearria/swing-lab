# SKILL — the falsification method (the asset)

This is the reusable thing the project produced. Not a trade — a disciplined way to
kill bad trade ideas cheaply, with the multiple-testing honesty most "AI quant loops"
skip. It is the confluence of the loop-engineering pattern (heartbeat · maker/checker ·
state · hard gates) with rigor that actually holds. The engine (`research/engine.py`)
runs on this; the audit trail is `research/FINDINGS.md`.

## The loop (one probe)
1. **Pre-register** the hypothesis AND the pass/fail bar in FINDINGS.md, knobs fixed,
   BEFORE seeing the result. Commit it (timestamp = the anchor).
2. **Run** the smallest test that yields a number. Out-of-sample / walk-forward,
   realistic costs, few parameters, de-overlapped, survivorship-aware.
3. **Red-team** with a separate adversarial pass before trusting it — maker ≠ checker. AMENDED
   2026-08-07 (owner): independence = BLIND MICRO-INDEPENDENT runs of the strongest available
   model (fresh context, adversarial lens; the reviewer re-derives its own verdicts and never
   sees the generator's conclusions — disagreement is the signal) + ONE cross-model control.
   What is banned is same-CONTEXT self-validation. Evidence the pass earns its cost: audit #1's
   cross-model control caught 3 items the same-model lenses missed (2026-08-08), and on
   2026-08-04 two of three false-number bugs in the digest's money band were caught ONLY by the
   independent pass — one would have printed a fabricated +28.5% day.
4. **Log** the verdict — win OR loss — one short FINDINGS entry, and append one row to
   `engine.PROBES`. If you can't show the number, it isn't done.
5. **Multiple-testing**: every probe counts. Over N tests at α=0.05, ~0.05·N "wins"
   are chance. A marginal positive after many tries is noise until it survives fresh OOS.

## Rules earned from losses (don't relearn the hard way)
- **Free + famous = arbitraged.** Three textbook anomalies (index-deletion, IPO-lockup,
  insider-clusters) all decayed/absent on free data. Don't re-test textbook effects on
  free data expecting edge. The moat is likely DATA ACCESS or genuinely novel processing
  (conjecture at N=3). [Audit #1 2026-08-08: strong prior, NOT a law — three families, one
  regime; a family earns a re-test on regime flip or when the [ARC 5 #2] paid-data trigger
  unlocks.]
- **Risk-reducers tie SPY; they are not alpha.** Every fear/timing/trend edge we found
  cuts drawdown or wins per-trade but does NOT beat buy-hold SPY risk-adjusted. Leverage
  only helps a source with Sharpe > SPY's — ours aren't (≈0.65–0.9 ≈ SPY). [Audit #1: a
  dated summary on a sample ending in the 2026 bull — the ranking can flip in a bear;
  re-rank on regime flip before treating it as a forward ban.]
- **Survivorship censors microcaps UPWARD.** Dead/delisted names drop out of free price
  feeds; always report the censor rate, and treat a positive mean with negative median +
  high censoring as a lottery, not an edge.
- **Mean lies, median tells.** Right-skewed payoffs make the mean positive while the
  TYPICAL trade loses. Judge on median + %-beat-benchmark, not mean.
- **Utilization is not the bottleneck.** Deploying idle capital across "uncorrelated"
  edges still lost — you can't out-compound buy-hold by selling winners for losers'
  bounces. Decorrelation breaks in the crashes that matter (2008/2022). [Audit #1: N=2
  correlated portfolio probes — hypothesis, not law; the live book DOES deploy idle cash
  under [ARC 5 #6], so the question is open and currently unscored.]
- **Ask if it's the RIGHT question.** When results keep TYING the benchmark, the framing
  is the bug. We hunted clean mechanical free-data alpha — the rarest, most-arbitraged
  thing. Most real "trader profit" is levered beta + survivorship, not edge.
- **A full-sample "beat" is often ONE regime + cheap leverage.** Vol-targeting beat SPY
  over 33y but won only 1 of 4 decades (the 2008 crash) and died at 9% borrow. Always
  split by decade AND stress the borrow/cost assumption before believing a sizing/leverage
  edge — full-sample numbers hide crash-insurance masquerading as alpha.
- **% of winning periods is the most seductive lie.** Selling vol wins 84% of months yet
  Sharpe < SPY with skew −8.75 — steady income hiding ruin. Negative-skew "income" pays
  for crash risk; it is not alpha. Weight by skew and worst-case, never by hit-rate.
- **Beware an ETF whose inception postdates the factor's known crash.** MTUM "beat" SPY
  2013-2026 — but launched AFTER the 2009 momentum crash, so its worst tail is excluded by
  construction. The momentum/TREND family is our consistent near-miss (dual-mom, MTUM,
  crypto-trend, EMA-crossover) yet every win is regime-flattered: treat "closest" as "least-dead," not edge.
- **EMA/MA trend-breaks are a seatbelt, not an engine — don't re-test for alpha.** EMA
  fast/slow crossover (10/30, 20/50, 50/200) on a 12-name high-beta basket, ~5y, costs in:
  beat buy-hold risk-adjusted on ≤3/12 names, 0/12 on CAGR at 20/50, and **0/12 in the
  first (bull) half** — the "help" is regime-dependent drawdown-cutting, not edge (2026-07-24).
  Same verdict as every trend result. Use MA crosses only as a DE-RISK/EXIT overlay on beta —
  the standing default, not a permanent ban [audit #1: one 12-name bull-weighted test;
  "unpromising, cheap to re-check on regime flip", not "never"].
- **Exit into strength; never market-dump into a low.** Both realized book cuts (HELP, XRP)
  bounced +16%/+6% after we market-sold near local bottoms — one same-day liquidation into a
  June dip that recovered. The textbook disposition-effect prior (retail holds losers too long)
  was the WRONG read of OUR behavior; our leak is the opposite — capitulation. Rule: book exits
  use LIMIT orders into strength, and never liquidate multiple names into a single down day.
  (n small — a process discipline, not an edge claim; audit before trusting your own instinct.)
  [Audit #1 2026-08-08: n≈2, both June BULL-tape bounces, and the rule steers real money —
  DEMOTED TO HYPOTHESIS with a pre-registered kill-path: at N≥10 realized book exits, repeat
  the bottom-tick audit (exit price vs the following 5 sessions, limit-into-strength vs market
  cuts); no advantage → the rule dies. And in a sustained bear "strength" may never come — this
  rule never overrides a stop.]
- **Enter on a LIMIT too — a quoted price decays, a limit does not.** [2026-08-03] The exit rule
  above had no entry-side twin, so alerts quoted a point price off the last complete bar and the
  human executed hours or days later. Measured on the 40 taken movers: the median name moved
  **1.07%** by the next open and **2.42%** by the next close — waiting costs MORE than the gap —
  with a tail to −23.4% (PNR gapped straight through its alert). Fill rate is FLAT at 87.5%
  across 1.0/1.5/2.0% bands while the entry advantage decays, so the tight band is free. Rule:
  every real-money entry is a limit with an expiry (`research/orders.py`; band and sessions in
  `config.py`), and an order that expires is NOT re-issued at a new price — it expired because
  the name re-rated away from us. Corollary, and the more expensive half: **structured facts get
  a column.** The predecessor "registry" was a `SIZED SUGGESTION:` marker inside a free-text
  thesis that no code read; 2 of 2 were issued and 0 executed, and nothing in the daily loop
  could tell that from "none was issued".
- **A guard that fires on the wrong axis is not conservative — it is wrong in a direction that
  looks responsible.** [2026-08-04] The digest needed to stop reporting non-performance as P&L, so
  it tested "did the composition change?" (`d_equity == d_cash + d_unrealized`). That guard was
  satisfied EXACTLY by a deposit — which would have printed as a +28.5% day — and VIOLATED by an
  ordinary `book open`, which made a normal trading day print "RESTATED, not P&L". It was wrong in
  both directions at once while *looking* like caution. The fix was the DEFINITION, not the guard:
  a period's P&L is `Δunrealized + Δrealized`, never `Δequity`. **Before writing a guard, write
  down the quantity you actually mean and check it against every event class that can move it**
  (here: price move, deposit, withdrawal, open, close, partial close, short, scope correction,
  dead price feed). A guard is a claim about the world and gets red-teamed like any other.
- **An alarm needs a CLEAR path, and the clear must be something the human can actually do.**
  [2026-08-04] Two alarms shipped the same day. The stale-limit one got `orders pulled` — a verb
  whose only job is to let a human say "I looked, it's off the broker". The pool-stop one was
  initially unclearable: a breach is permanent (equity does not climb back over the floor after a
  halt), so it would have nagged forever, which is how a channel whose SILENCE is supposed to mean
  "broken" gets ignored. Gate an alarm on the condition its own instruction removes.
- **Our model of an order is not the broker's order.** [2026-08-04] Expiry is OUR bookkeeping —
  a GTC limit does not expire because we stopped counting sessions. An order that "expired" while
  the human really had it working can still fill days later into a position no ledger expects. The
  order-side twin of "reconcile a position against the broker before reasoning about it" below.
- **Audit your own realized decisions, not just backtests.** "Did our actual cuts beat holding?"
  is a cheap, honest test that caught the bottom-tick pattern the theory missed. Grade real
  decisions the same way you grade probes.
- **A position with no pre-registered twin is churn, not an experiment.** [2026-08-02, user call]
  Every real-money `book open` gets a `bets.py` bet — thesis, horizon, benchmark, tag, stop —
  written BEFORE the fill. Without one the trade produces $ P&L and no evidence: it can never
  reach the pooled verdict, so the book stays busy while the skill question stays at n=6. `book
  open` warns when the twin is missing; it deliberately does NOT block, because refusing to
  record a real fill would corrupt the ledger to enforce paperwork. The silos stay separate for
  SCORING (real-money churn must not pollute the skill verdict) — this rule is about coverage,
  not merging them.
- **A book P&L number is evidence about the BOOK, not about the read.** The −17% drawdown as of
  2026-08-02 was 100% legacy seed inventory plus a beta anchor — zero read-generated positions —
  so it scored the system in neither direction. Before quoting book performance as evidence
  about signal quality, check what actually generated the positions.
- **Compute the deadline against the horizon when you pre-register.** [ARC 3 #1] carried a
  126d verdict horizon and a 2026-12-31 deadline, so its N=20 branch died on the calendar
  ~2026-07-08 — four weeks before anyone noticed, while we were busy rebuilding its data feed.
  A kill-criterion of the form "N or DATE" must be checked at WRITE time: is N still reachable
  before DATE? If not, the bar is decorative.
- **RE-ARM PROTOCOL — how a dead hypothesis comes back [ARC 5 #12a].** Retesting any closed
  probe (the insider silo, shorts, a killed mechanical rule) requires all three: (1) a FRESH
  pre-registration entry in FINDINGS, (2) only data accrued SINCE the original verdict —
  true out-of-sample, never a re-run over the sample that killed it, (3) the ORIGINAL bar or
  stricter — a softened bar on a second attempt is p-hacking with extra steps. This is what
  makes "retest old ideas when it feels right" safe: the feeling may PROPOSE; only a
  pre-registration may RUN. Paid-for findings carry forward free (e.g. the insider silo's
  entity-stacking and IPO-allocation false-positive modes, FINDINGS [ARC 3 #1b]–[#1d]).
- **A repo-only grep is not a complete refactor.** The cloud routine PROMPTS are a second copy of
  the loop docs and live outside git (`/schedule`). Twice now (2026-07-02, 2026-08-02) a prompt
  kept mandating a step the repo had changed or deleted, and the prompt silently won. When a
  module name, `READ_LOOP.md`, or `daily.sh` changes, list the routines with
  `RemoteTrigger {action:"list"}` and patch them in the SAME session.
- **Reconcile a position against the broker before reasoning about it.** A seeded holding is an
  unverified human input, not a settled fact. On 2026-08-02 a third of the book turned out to be
  plan CASH held outside the brokerage, logged as 17 shares at seed and marked to the stock's price
  for five weeks — hiding 7.5 points of drawdown. We had spent half a session researching the
  LOCKUP TERMS on it before anyone asked whether we owned it. Anything that has never produced a
  confirmable fill gets re-reconciled; "it's in the ledger" is not evidence of ownership.
- **Two realms, one ledger each.** Short-swing (this repo, benchmark-scored, days-to-weeks) and
  long-term wealth (the fully-private long-realm repo: equity comp, compounding accounts, multi-year
  tax milestones) get SEPARATE research and separate actions. A position whose next decision point is
  measured in YEARS does not belong in a book judged in weeks — it has no stop, no benchmark race,
  and it distorts the vs-SPY comparison the book exists to make. The boundary had been written down
  twice and enforced zero times before it cost a session (FINDINGS 2026-08-02).
- **An employee stock plan is not a brokerage account.** Plan contributions sit as cash with the
  issuer and convert to shares on ONE scheduled Purchase Date. Between dates you hold a purchase
  right, not stock — it cannot be sold, cannot be stopped, and does not move with the share price.
  Keep it OUT of the book: payroll deductions are not trading decisions and counting them corrupts
  the benchmark comparison the book exists to make.
- **LLM out of the DETERMINISTIC path — not out of the loop.** The READ layer (READ_LOOP,
  cases, bets) is an LLM by design: it IS the hypothesis under test, scored by deterministic
  settles. What stays model-free is the mechanical path — triggers, settling, scoring, guards,
  money math — and no model ever judges its own trade. [Meaning made explicit 2026-08-08 after
  audit #1 flagged the old wording as contradicting the live READ_LOOP.]

## The one banked result (status restated honestly, audit #1)
Dual momentum: SPY-like return, half the drawdown (ret/|DD| 2.2×). A better risk SHAPE,
not alpha — it TIED its own pre-registered Sharpe bar (the engine grades it NEAR), and no
forward re-test accrues while it sits in the digest path. Treat as the least-dead default
allocation; re-validate walk-forward before ever sizing it up.
`python3 -m research.dualmom current` → what to hold this month.

## If we resume hunting
The honest levers left cost MONEY (paid survivorship-clean data) or TIME (the forward
agent-read ledger, accruing). Pre-register first, gate the spend on stated evidence,
and let the engine track it. Don't dig the empty free mine again. Re-opening anything
already closed goes through the RE-ARM PROTOCOL above; real money returns only per
FINDINGS [ARC 5 #12a] (no gate machinery — the pooled pass is the necessary condition,
everything else is decided then, in the private long-realm repo).
