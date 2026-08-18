# READ_LOOP — the reading-agent generation loop

**PAPER REGIME since [ARC 5 #12]/[#12a] (2026-08-14; step 5 rewritten 2026-08-18, P6):** there
is NO broker leg. New bets are LONG-ONLY above the $5M liquidity floor (code-enforced — a
REFUSED `bets add` is the rule working, not an error to route around).

The FORWARD half of `LOOP.md`, operationalized and SCALED. One iteration = Claude reads a
batch of live situations and **pre-registers a batch of forward bets**. This is the project's
active frontier: the mechanical free-data mine is closed (`engine.py` scoreboard: 0 confirmed), so
throughput now goes here. The brain is **Claude** (paid for via Max); no human approval per
bet — the only safeguard kept is pre-registration + log-every-candidate + multiple-testing.

## Run it
    /loop run one iteration of research/READ_LOOP.md     # by hand; watch a few first
Or scheduled (PRIMARY): the cloud `/schedule` "read" routine, **11:30 UTC Mon–Fri** (cron
`30 11 * * 1-5`). Settling is the SEPARATE "settle" routine (`scripts/daily.sh`) — never settle here.

## WHEN this runs: PRE-MARKET (read this before quoting any price)
11:30 UTC ≈ **07:30 ET, ~2h before the 09:30 ET open** (06:30 ET after the November DST shift —
still pre-market, which opens 04:00 ET). Moved here 2026-07-24 from 22:09 UTC (18:09 ET, ~2h AFTER
the close) because an alert the human cannot act on for 15+ hours is quoted at a price that no
longer exists — the [ARC5 2026-07-10] red-team note ("suggestions quoted at read time can be stale by
execution") made operational. What this means for the run:
- The **last complete daily bar is yesterday's close** — that is the correct, clean basis for every
  level you quote. Do NOT fabricate an intraday or pre-market print.
- **Label every level indicative**, off yesterday's close. There is no broker leg [ARC 5 #12] —
  levels exist for the scored record and the counterfactual order, never for execution.
- Overnight news + the prior session's after-hours earnings are all visible — that is the edge of
  this slot. A catalyst that printed after yesterday's close is fresh, not stale.
- Daily cadence (Mon–Fri) means Tue/Thu catalysts are no longer read 1–2 days late; during earnings
  season that lag was eating the first, largest days of any drift move.

## One iteration  (gather → read → pre-register → commit)
0. **DEPS GUARD [2026-08-08]** — `python3 -c "import dotenv, requests, yfinance, pandas"
   2>/dev/null || pip install -q -r requirements.txt`. A COLD cloud container sometimes lacks
   python-dotenv; without it movers/orders/digest die on the same import and the morning brief
   never sends — both 08-07 settles died exactly this way (FINDINGS 2026-08-08). `daily.sh`
   carries the same guard; this closes the read-side of the class.
1. **ORIENT** — **FIRST: `git fetch origin && git log origin/master --oneline -3` and confirm no
   read run has ALREADY committed for today.** If one has, STOP — the daily denominator is
   already logged; do not re-scan and do not re-bet. On 2026-07-24 an interactive session
   branched from a pre-run commit, re-scanned, and pre-registered DLR a SECOND time while
   logging 50 mover rows for 25 candidates — an inflated multiple-testing N and a corrupted
   denominator (reconciled by first-timestamp-wins; see BACKLOG). The scheduled run OWNS the
   daily scan; a human-driven session that wants a second opinion must add bets only, never
   re-run `movers scan`. Then read `research/SKILL.md` (the rules earned from losses) and the
   Arc 5 #1 bar in `FINDINGS.md`. Skim current open bets (`python3 -m research.bets show`) so
   you don't re-bet a ticker already live. NEVER re-test a dead end from SKILL.md. Check the book
   (`python3 -m research.book show`): free cash and open positions. Then read
   `python3 -m research.orders show`: the LEDGER owns expiry now, not this step. A PENDING order
   is still live and its cash is already committed — leave it alone and do not size a new order
   against dollars it is holding (`orders place` enforces this, but know it before you plan the
   run). A FILLED order with no matching book position means the human missed the fill or never
   placed it — say so in one line in the push. Never carry a stale entry price forward; the
   limit is the only price this loop is allowed to quote.
2. **GATHER candidates** (free, each logs a DENOMINATOR — the multiple-testing count):
   - **Daily movers (the GENERAL denominator):** `python3 -m research.movers scan` — ONE command,
     TWO cohorts [ARC 5 #11]: the S&P 500 top movers PLUS a smaller S&P 400+600 TAIL cohort
     (cohort sizes live in `movers.TOP_N`/`movers.TAIL_TOP_N` — never restate them). Each SEEN
     row carries its `universe` label; the label is a DIAGNOSTIC decomposition of the pooled
     verdict, never a goalpost. S&P 500 movers are mostly large-cap/covered (the arbitraged
     arena) → a thin read is a SKIP; the READ is what's under test, not the move.
   - **TAIL names get a HIGHER read bar, not a lower one.** The tail is the under-covered arena
     Arc 2 pointed at — but small caps carry wide spreads, gappy fills, and thin float. A tail
     take must NAME the mechanism (why is THIS mispriced, who is forced, what resolves it) or it
     is a SKIP; check liquidity/spread before any 5a/5b alert on a tail name, and size with the
     friction in mind. Do NOT tilt toward the tail to chase the story — [ARC 5 #11] forbids it.
   - **Other catalysts (beyond the scan):** readable situations with a clean forward window —
     forced flows, analyst re-ratings, washed-out valuations with an identifiable change
     (filings, news, price action). The scan is the denominator floor, not the only source.
3. **READ (the value-add UNDER TEST)** — for each candidate, read the surrounding context
   (8-Ks/filings, what changed, who's buying, valuation, the catalyst) and form a directional
   call + an HONEST conviction. The hypothesis is that the READ beats the bare trigger / a
   naive benchmark — so a thin read is a SKIP, not a coin-flip take.
4. **PRE-REGISTER every decision** (immovable timestamp = the anchor; lookahead-guarded):
   - Mover candidates → `python3 -m research.movers decide TICKER take|skip "why"` — clear the
     QUEUE: decide on EVERY unread SEEN mover (dashboard "unread" count). A TAKE then graduates to
     a scored `bets add ... --tag=` below; a SKIP stays logged (that's the denominator working).
   - General theses → `python3 -m research.bets add TICKER long|short HORIZON_d BENCH "thesis" --tag=<scenario-type>`
     Pick the benchmark the bet is measured against (its sector ETF, or QQQ/IWM/SPY). State
     conviction + event risk (e.g. earnings inside the window) in the thesis. **Tag the SCENARIO
     TYPE** (`--tag=`, kebab-case; reuse an existing tag from `cases/` when it fits — e.g.
     `guidance-cut-overreaction`, `spike-fade`, `real-vehicle-vs-meme`, `narrative-stage-transition`,
     `forced-flow`, `biotech-binary`) so the engine can decompose the verdict per scenario [Arc 5 #8]
     (diagnostic only — NOT a per-tag goalpost). NEVER drop a take once logged.
   - **Fast sleeve — MANDATORY when the catalyst is fast (tightened 2026-08-01).** If this run
     takes ANY candidate whose catalyst resolves in WEEKS rather than a quarter (post-earnings
     drift, an event pop, a forced flow that clears fast), **at least one bet this run MUST be
     pre-registered at `HORIZON_d=21`**. If no take qualifies, say so in one line in the step-7
     push — that is a claim, not a free pass.
     *Why this was tightened:* as a soft "ALSO consider 21d" it produced ONE bet in five weeks —
     since 2026-06-28, 33 of 34 new bets were 63d+. Two costs, both real: the human has nothing
     to trade week-to-week, and the pooled N crawls (the whole catalogue is back-loaded onto one
     quarter-end maturity wall). Fast + core pool into ONE general verdict [Arc 5 #7]; horizon
     (`bets.is_fast`, threshold 30d) is a DIAGNOSTIC label shown by `bets show` / `engine`, NOT
     a separate goalpost — this changes GENERATION CADENCE only, no bar and no threshold moves.
   - **Scope (a CEILING, not a quota):** ≤ ~10–15 general bets per run; default horizon 63d
     (126d for slow theses, 21d for the fast sleeve). Quality of read > volume — a thin read
     is a SKIP, never a take to hit a number. The hypothesis under test is that the READ adds
     value; diluting it to fill the cap tests a worse version of us.
   - **HARD tag ceiling — ≤3 bets with the same `pattern_tag` per run [2026-08-04].** A 4th+
     same-tag bet in one run must carry one line in its thesis naming why it is NOT the same
     trade again (different mechanism, different regime exposure — not just a different ticker).
     Why: 21 of the first 53 bets were same-season post-earnings-drift LONGS — near-identical
     bets that are partly ONE macro draw, so they shrink the pooled verdict's effective N
     (FINDINGS 2026-08-04 caveat (a)). Generation cadence only — no bar moves; the mover SKIP
     for a redundant read still gets logged (the denominator is untouched by this ceiling).
   - **MIX MIRROR — a mirror, never a quota [ARC 5 #12a].** The per-run ceiling above can't see
     cross-run drift, so: when one `pattern_tag` carries >50% of the LAST 15 catalogue bets
     (count them — `tail -15 research/bets_catalogue.csv`), the step-7 run note must name the
     driver in ONE sentence: environment (e.g. earnings season is genuinely PED-rich) or habit
     (the read reaching for its favorite shape). NEVER force diversity to fix the number —
     taking worse bets to balance a dashboard dilutes the very pool under test, and changing
     the mix mid-flight is what [ARC 5 #10] forbids. Naming it out loud is the whole mechanism.
   - **MILESTONE REVIEW — absorbed, not scheduled [ARC 5 #12a].** When settled LONG bets cross
     n=10/20/30 (the digest banners it from P4; until then notice it in `bets show`), THIS run
     carries the review: reachability arithmetic on every live deadline ([ORDERS #1] N≥20 by
     2026-12-31; kill 2027-06-30 — settled-per-week × weeks left, one line each), the mix
     verdict, and AT MOST one new-hypothesis proposal + one re-arm proposal (SKILL re-arm
     protocol), each as a pre-registration DRAFT for the owner — never self-approved, and only
     if genuinely warranted. Nothing warranted = say so in one line and move on.
5. **SYSTEM TAKE + COUNTERFACTUAL ORDER** — the paper-regime bridge [ARC 5 #12/#12a; this
   section REPLACED the real-money 5a/5b on 2026-08-18 (P6) — the old text, with its broker
   instructions and cash gates, is in git history and summarized in FINDINGS].

   **5a. 🟢 SYSTEM TAKE card (mandatory whenever the run has a take).** For the run's
   highest-conviction take(s) — at most 2, ranked, or none if the batch was genuinely thin —
   include in the step-7 push (plain text — the note is HTML-escaped):

       🟢 SYSTEM TAKE — <TICKER> long · <H>d vs <BENCH>
       ref <price> = <YYYY-MM-DD> close, NOT a live quote
       WHY: <one line — the catalyst + why it is mispriced>
       conviction: <high|medium> · risk: <the one thing that kills it>

   INFORMATIONAL by design: no broker instruction, no "place the LIMIT" text, never a DO-NOW —
   there is no broker leg. The bet is logged and scored either way, so the verdict N can never
   be cherry-picked by execution. If the batch produced no take worth a card, say so in one
   line: that is a scored-skip-style claim, not a free pass.

   **5b. ONE counterfactual order per take-carrying run [#12a cadence].** If this run logged
   ≥1 take, log exactly ONE counterfactual working order for its highest-conviction take —
   bet first (the scored twin), then the order:
     `python3 -m research.bets add TICKER long H BENCH "thesis" --tag=<scenario>`
     `python3 -m research.orders place TICKER long STOP H BENCH`
   `orders place` does ALL the arithmetic — it reads the last COMPLETE bar as the reference and
   computes the limit + expiry (band and session count live in `config.py`, never restated
   here); shares stay BLANK — no cash, no sizing, nothing to execute. Do not hand it a price
   you worked out yourself; `--ref=P` exists only to reproduce a past run. Settle's
   `orders check` resolves it against real bars and scores fill AND no-fill forward — the
   [ORDERS #1] band DIAGNOSTIC, never an edge verdict, and model-vs-model until real money
   returns [#12a]. A zero-take run logs NO order (say so in one line). **Never re-issue an
   expired order at a new price** — it expired because the name re-rated away from us, and
   chasing it is the exact behaviour the band exists to stop.

   *(Why a limit and not a point entry [2026-08-03, unchanged]: measured across the 40 taken
   movers, a point entry decayed 1.07% by the next open / 2.42% by the next close with a −23.4%
   tail; a limit is age-invariant, which is why the daily run may re-show it.)*

   **Expiry is STATE, and the daily run DOES re-push — both reversed 2026-08-03.** This used to
   read "expiry = supersession (no timers, no stored state)" and "the daily settle run never
   re-pushes a suggestion — a days-old entry price presented as actionable is worse than
   silence." That was correct *for a point price*, which is only true at the instant it is
   written. A LIMIT is age-invariant: re-showing it on day 3 is the same instruction it was on
   day 1. So `orders check` (in `daily.sh`) resolves each order against real bars and the
   digest re-pushes anything still pending, with today's spot beside the limit. The human
   sleeps through the pre-market alert — that is the normal case, not the failure case, and
   supersession-only silence is what made it expensive.
   The order dies on its own after `config.ORDER_EXPIRY_D` sessions; **do not re-issue an
   expired order at a new price just because the thesis still reads well.** It expired because
   the name re-rated away from us, and chasing it is the exact behaviour the band exists to stop.
6. **COMMIT + PUSH** — `git commit` the updated `bets_catalogue.csv` /
   `movers_ledger.csv` / `orders.csv` + `research/data/_feed_status.json` and `git push origin HEAD:master` (cloud runs are ephemeral — unpushed
   work is lost). `orders.csv` was missing from this list while `digest.LEDGERS` checked it, so a
   run that placed an order raised a spurious "ledgers are uncommitted" DO-NOW [2026-08-04]. **This step is now CHECKED, not trusted:** `digest._git_section` inspects the
   ledgers and, if they are uncommitted or unpushed, puts "any bet in this message is NOT scored
   yet" at the top of the very push you are about to send. On 2026-07-27 this step was skipped
   while step 5a still alerted INTC as "pre-registered and scored either way" — the row did not
   exist and the call went unscored. Commit BEFORE step 7, always.
7. **TELEGRAM the run report** (decided 2026-07-03: every run pushes, silence = broken) —
   ONE message, fail-soft, never blocks the run. Push the **actionable digest** [W4] with the
   run note passed in (what you did + the 5a 🟢 SYSTEM TAKE card(s) + the 5b counterfactual
   order line or the zero-take line):
   `python3 -m research.digest --notify --slim "📖 read run YYYY-MM-DD: N bets (TICKERS) · movers X take/Y skip
   <5a card(s)> <5b line>"`.
   **`--slim` (digest v2 [ARC 5 #12a], P4): this push is the 📖 MORNING BRIEF; settle's 📋 is
   the day's one FULL state photo.** Both legs LEAD with the 🎯 POOL SCOREBOARD; the 📖 keeps
   DO-NOW + the run note + the 🟢 system take and DROPS what settle owns (Δ-since-HEAD, the
   bets/movers state blocks, the 📋 banner — the headline is this message's identity). The 💰
   band and the live-book blocks retired with the book [#12/#12a]. DO-NOW items are never
   collapsed.
   **Write the summary as the note's FIRST line and the alert blocks below it** — `digest` splits
   there: line 1 becomes the message headline (and the Telegram preview), the rest lands in a
   RUN NOTE block at the BOTTOM. Stacking the whole note on top buried the DO-NOW list
   [2026-08-04]. Do not format the note yourself; the layout is the digest's job.
   **The note is a CARD, not a memo [2026-08-07, user call]: ≤6 short lines after the headline.**
   The reader is not a sector SME and investigates the chart himself — the note's job is
   *what + how to act*, never the full case. Per take: ticker/direction/horizon/tag, conviction,
   and ONE short WHY clause (the hook); the full case already lives verbatim in the bet's thesis
   row — do not restate it in the push. Skips are NEVER enumerated or justified in the note:
   their count is in the headline and their reasons live in `movers_ledger.csv`. The violation
   this rule is named for: the 2026-08-07 DVA note ran five dense sentences plus a five-name
   skip taxonomy, and the human asked for the wall of text to stop.
   Keep it ONE message — the alert rides IN the digest push, never as a second send (duplicate
   messages are the failure mode we fixed 2026-07-24, not a feature). **NEVER push a ✅
   success/heartbeat/confirmation message: `research/heartbeat.py` exists for FAILURES only,
   and on a clean run the 📋 digest IS the confirmation. A second message of any kind is a
   contract violation — one arrived 2026-08-05 and this sentence is its tombstone.**
   **The digest PRINTS a delivery verdict and that line is the ONLY truth about delivery
   [2026-08-06]: `PUSH DELIVERED` = done, stop. `PUSH REJECTED (nothing sent)` = re-run the SAME
   digest command ONCE. `PUSH UNCONFIRMED` (or a bare exit 1) = STOP — the message may already
   be delivered and a re-send double-posts (the 2026-07-24 bug; a "delivery check" copy and a
   bare "Probe" arrived 2026-08-06 exactly this way). NEVER send a probe/test/verification
   message; `python3 -m research.notify` is a HUMAN-only tool — a routine never invokes it.**
   AFTER the push, commit the delivery stamp the digest just wrote, so the next run can see a
   stranded message (`git add research/data/push_log.csv && git commit -m "chore: push-log
   stamp (read)" && git push`) — best-effort, skip if unchanged; never re-push the digest over
   a failed stamp commit.
   **If the verdict was NOT `PUSH DELIVERED`, fire the 🚨 fallback once — `python3 -m
   research.heartbeat digest-read` — after the stamp commit [2026-08-11].** This is PARITY with
   the settle leg, not a new policy: `daily.sh` has routed a failed digest push into
   `heartbeat.py` all along and the read leg never had the equivalent, so on 2026-08-10 the
   brief died UNCONFIRMED and produced total silence — no 📖, no 🚨, and Tuesday's message
   still said "DO NOW: nothing". It does not violate the no-second-message rule above: the
   heartbeat is an ALARM on a failed run, and the rule bans a ✅ on a CLEAN one. It is not a
   re-send either — never re-push the digest on UNCONFIRMED; the 🚨 says the brief may be lost
   without risking the 2026-07-24 double-post.
   The digest itself carries the 🎯 POOL SCOREBOARD (v2 [ARC 5 #12a]), the ⚠️ DO-NOW list,
   and the run note. Done.

## What to expect (honest)
Most bets will lose to their benchmark — that's fine; the scoreboard decides the VERDICT at
N≥30 settled in ONE pooled general silo (Arc 5 #7: median excess **>+1%** AND beat-rate >55%,
Wilcoxon, α≈.017). Core bets mature in 63–126d (first real read months out); 21d fast bets
return settled numbers in ~weeks (faster, noisier — pooled in, split out only as a diagnostic). The
**LLM stays OUT of the settle path** — settlement is deterministic price math (`bets.settle`,
`movers.settle`). If free-data reads can't clear the bar, that fires the PAID-DATA
trigger (Arc 5 #2) — buy better data; do NOT lower the bar.
