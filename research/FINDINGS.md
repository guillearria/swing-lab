# FINDINGS — the research ledger

Curated, append-only record of every falsifiable test and its verdict. The point:
a future session (or a forgetful human) can reach back and understand the whole
project in two minutes, without re-deriving it. Keep entries SHORT — one block per
test: question → number → verdict. New results go at the bottom of the log.

Rule: nothing is "true" here until it has a reproducible number AND a red-team note.

---

## Mindset check (standing rule, 2026-06-22)
Before each push ask not only "is our ANSWER right?" but **"are we answering the RIGHT
QUESTION?"** We may be throwing compute at the wrong one. The framing itself is a hypothesis
under test — re-examine it whenever results keep TYING the benchmark (that's the tell).

## Where we are — FREE-DATA HUNT CONCLUDED across 4 arcs → PATH A: bank the result + the ENGINE is the asset (2026-06-23)
> Cold-start: run `python3 -m research.engine` for the scoreboard; read `research/SKILL.md` for the method.

**The honest conclusion (5 arcs; live probe + settled counts: `python3 -m research.engine`, never
restated here): there is NO free mechanical risk-adjusted alpha for us.** ZERO of the settled probes
beat buy-hold SPY risk-adjusted. (Arc 3 joined the settled set 2026-08-02 as a NULL — it hit its own
kill-criterion deadline; Arc 5, the forward reading track, is the one still accruing.) The "real" ones
(dip-fade, VIX-buy, crypto-trend, disaster-entry, dual-momentum) are CORRELATED risk-reducers — consistent
with chance after multiple testing. This is a real, money-SAVING result, not a failure.
- **PATH A (chosen w/ user 2026-06-23):** stop hunting the empty free mine. (1) BANK the one usable result —
  dual momentum (SPY return, HALF the drawdown; `python3 -m research.dualmom current`). (2) Make the rigor
  **ENGINE the asset** (`research/engine.py` scoreboard + `research/SKILL.md` method) — the confluence of the
  quant-loop pattern with honesty the hype skips.
- **Remaining alpha levers (deferred, gated):** PAID survivorship-clean data ($), or TIME (the forward
  insider-read ledger, still accruing). Pre-register + gate the spend before reopening the hunt.
- Arc detail below stands as the reproducible audit trail.

**Arc 1 verdict (settled): the mechanical fear/timing edges are REAL but they are
RISK-REDUCERS, not GROWTH-capturers — none beats buy-hold SPY.**
- Validated & real: index dip-fade (+0.42%/trade, 60% win, 20y/5 mkts), extreme-VIX-buy
  (beats buy-any-day, 3 of 4 decades), crypto trend-following (risk-reducer), disaster-buy
  (−20%-off-high bounces in **13/14** global markets incl. corpses).
- All the SAME KIND of thing: each cuts drawdown or harvests a bounce. Stacked / diversified
  / globally rotated they at best TIE SPY via beta and usually LOSE on CAGR (idle capital).
  The global disaster portfolio lifted utilization **13%→53%** and STILL lost (CAGR 1–4% vs
  11%, Sharpe 0.28 vs 0.65). Utilization was never the crack.
- **The lesson:** you can't out-compound buy-and-hold by timing fear and rotating risk.
  Beating SPY needs a DIFFERENT KIND of edge.

**Arc 2 question (the pivot): where is an edge a SMALL, UNCONSTRAINED operator can reach that
the $-trillions that already make SPY efficient CANNOT?** Beating SPY = finding INEFFICIENCY,
and inefficiency only survives where big money can't/won't go:
  - **convexity/asymmetry** — small cost, large skewed upside;
  - **illiquidity & size** — micro-caps, niches too small for funds;
  - **forced flows** — spinoffs, index add/delete, distress, expiries;
  - **novel data** the crowd doesn't process — where agent-as-researcher is a real advantage.
  NOT large-cap US selection — crowded, ~90% of active pros LOSE to SPY there (the wrong-question
  trap). Pre-register the first falsifiable inefficiency-probe before building anything.

**Arc 2 backlog (candidate probes, not yet run):**
- **Index-deletion bounce** — forced index-fund selling on S&P 500 removals → overshoot → rebound. *(FAILED — the positive mean is an outlier/survivor lottery; median negative at 3–6mo, ~coin-flip hit rate, decaying post-2020. See log.)*
- **Post-IPO behaviors** — lockup-expiry forced selling (~180d) and post-IPO drift. *(FAILED — the lockup dip has DECAYED (2020s event +0.7%) and post-expiry is continued underperformance/beta, not a buyable rebound. See log.)*
- **Russell 2000 reconstitution** — forced index-fund buying of June additions → run-up/reversal. *(DATA-BLOCKED — no clean free historical add/delete list; reconstructing it needs the survivorship-clean market-cap universe = paid data. The data moat IS the moat.)*

---

## ARC 3 — the CUSTOM reading-agent edge (CLOSED 2026-08-02 · NULL on its own deadline branch)

**Why this:** Arc 2 proved the free forced-flow corner is exhausted (deletion + lockup DECAYED, Russell DATA-BLOCKED). And commodity data (~$50/mo Sharadar) is NOT a moat — cheap+popular = the same arbitraged trap. The bet that survives is NOT a new mechanism but: known effects that PERSIST in the **under-covered tail** (where arbitrage doesn't reach) + the **agent's READING-AT-SCALE** as the exploitation tool (our strongest, already-paid-for axis — the $120/mo compute). Patience = the user's separate passive long-horizon accounts ([[holistic view]] later). **Method = FORWARD, pre-registered, scored prediction log** (revive the dormant paper infra) — qualitative reading can't be clean-backtested, so we forward-test it honestly. **Honest prior: NO established edge that LLM reading beats markets — this may find nothing; the point is to know cheaply.**

**Candidate catalogue** (each must: require READING not a screen · live in UNDER-COVERED names so breadth=moat · be scored FORWARD vs IWM/sector):
1. **Filing-language CHANGE** ("Lazy Prices") in the tail — diff each new 10-K/Q vs the prior, flag material shifts.
2. **Buried 8-K catalysts** in no-coverage names — material-positive 8-Ks no analyst will write up (fastest N).
3. **Special-situation orphans** — spin-off stubs / post-bankruptcy emergences (force-sold, complex; rare, low-capacity).
4. **Insider / "whale" CLUSTERS + corroborating read** ← **USER'S FAVORITE (the inside scoop)** — a cluster of open-market insider buys (structured trigger) filtered by the agent reading whether the context backs real conviction.

**THE BUILD (user's stated goal): AUTOMATE it.** An overnight autonomous loop that GENERATES new candidate edges AND TESTS them, growing a **tested catalogue** to dig for winners — agent-as-researcher running while he sleeps. **GUARDRAIL (non-negotiable or it becomes a p-hacking machine):** every auto-generated candidate must be PRE-REGISTERED and judged on FORWARD / OOS data; the catalogue must clearly separate in-sample hits from forward-validated ones, with multiple-testing honesty. LLM stays OUT of the live trade trigger (see [[project-experimental-event-edges]]).

**DECISION (2026-06-23, locked w/ user):** do candidate **#4 (insider/whale clusters)** BY HAND
first — prove the pattern yields clean pre-registered FORWARD verdicts before building any
automation. The overnight loop (six-piece maker/checker pattern from `raw_input/` quant-loop
notes) is the DEFERRED target; building it now is motion, not progress. Confluence framing:
the loop *pattern* (new data) carries the *rigor content* (this project) → a falsification
engine, NOT an "alpha printer." Trigger to build the loop: the manual candidate produces clean
forward verdicts. See pre-registration entry [ARC 3 #1] at the bottom of the log.

**Deprecated / dormant (not live for Arc 2):** the v1 capture→settle→paper cron pipeline
(`capture` `paper` `db` `news` `outcome` `universe` `momentum`) — forward plumbing, paper book
empty, superseded by backtests; don't run for Arc 2, retire if the cron is removed. The Arc-1
probe scripts (`dip_index` `robust` `decorrelate` `sleeves` `crypto_trend` `vix_gate` `vix_fear`
`fng_crypto` `regime` `portfolio` `disaster` `disaster_port`) remain as REPRODUCIBLE EVIDENCE
only — Arc 1 is closed; don't re-mine them.

**Dead ends (do NOT re-mine):** raw momentum, trend-filtered momentum, FMP social (free tier
dead), VIX>30 gate on the fade, crypto dip-fade (crypto trends, doesn't revert), 200d-slope gate
on the fade, crypto F&G sentiment-fade (crypto reverts on neither price nor sentiment), and
**utilization-via-rotation** — the global disaster portfolio lost to SPY despite 53% time-in-market
(risk-rotation ≠ growth; the whole Arc-1 family are risk-reducers, not compounders).

---

## Log

_(Closed-arc entries — Arc 1-2 fear/timing + forced-flow, Arc 4 trend/risk-premia — are
archived verbatim in `FINDINGS_ARCHIVE.md` (2026-07-02; every entry keeps its numbers +
`Reproduce:` line). Conclusions: header above + `python3 -m research.engine`. Live entries
below: Arc 3 (insider forward track) and Arc 5 (the automated reading engine).)_

---

## ARC 3 — the custom reading-agent edge (CLOSED 2026-08-02 — see the [ARC 3 #1d] entries at the end)

**2026-06-23 · [ARC 3 #1] PRE-REGISTRATION (no data peeked) — insider-cluster buys in the under-covered
tail.** Written BEFORE any outcome is observed; knobs fixed here, NOT to be tuned to fit results (p-hacking).
- **Hypothesis:** a cluster of open-market insider PURCHASES in an under-covered small-cap, when the agent's
  read of the surrounding context corroborates genuine conviction, earns positive excess vs IWM over 3–6mo.
- **Structured trigger (deterministic, free — openinsider cluster-buys screen):** trade type `P - Purchase`
  only (no option-exercise/award/10b5-1 where flagged); **≥3 distinct insiders** (openinsider `Ins`≥3) buying
  within openinsider's cluster window (~30d); market cap **$100M–$2B** at signal (tail proxy: exclude <$100M
  illiquid-spread trap and >$2B covered/arbitraged); aggregate cluster value **≥ $250k** (drop token buys).
- **Agent read (the value-add UNDER TEST):** binary take/skip — TAKE if context (recent 8-Ks, the filings,
  who is buying, the business/valuation) backs genuine conviction (real-size C-suite/independent-director
  buying after an identifiable positive change or at a washed-out valuation); SKIP if routine/comp/forced.
- **Benchmark / entry / horizon:** excess vs **IWM**; entry = first close on/after the openinsider **Filing
  Date** (no lookahead); horizons **63d & 126d** (≈3mo/6mo), adjusted closes.
- **PASS bar (must clear ALL, FORWARD/OOS):** (1) agent-corroborated set positive MEAN *and* MEDIAN excess vs
  IWM @126d; (2) >50% of corroborated predictions beat IWM @126d; (3) corroborated set beats the BARE
  (un-read) cluster set on mean excess (the READ must add value, not just the trigger). Multiple-testing
  honesty: log EVERY candidate (take AND skip), track N, Bonferroni/BH-adjust the significance bar.
- **Kill-criterion:** after **N=20** forward-settled corroborated predictions OR **2026-12-31** (whichever
  first), if the bar isn't cleared → log NULL, stop expanding this candidate.
- **Honest prior:** insider-cluster buying is among the more durable documented anomalies (opportunistic-
  insider / cluster-buy literature) but well-known and partly arbitraged in LIQUID names — hence the bet is
  the UNDER-COVERED tail. May still find nothing; the point is to know cheaply.
- *Next: a cheap HISTORICAL sanity screen of the BARE trigger vs IWM (survivorship-caveated — NOT the
  verdict), then the forward ledger.*

**2026-06-23 · [ARC 3 #1] HISTORICAL SANITY screen of the BARE trigger → WEAK/NEGATIVE (raises the bar
for the read).** openinsider cluster buys 2021-2025, my own ≥3-distinct-insider/30d grouping, $100M–$2B
(current-shares proxy), ≥$250k, de-overlapped; excess vs IWM, entry = first close after the 3rd insider's
filing (no lookahead). 1502 cluster events, 724 priceable, **778 (52%) CENSORED** (delisted/no-data →
survivorship UP-bias). Result: 63d mean +1.60% / **median −2.54%** / beat **44%**; 126d mean **−0.77%** /
**median −6.53%** / beat **42%** (n=724). The positive 63d MEAN is the SAME outlier-lottery as index-deletion
(a few winners drag it up); the TYPICAL name LAGS its own small-cap benchmark, worse at 6mo, <50% beat — and
this is WITH the up-bias, so the truth is worse. *Verdict: the BARE insider-cluster trigger in this cap band
is NOT an edge (negative median vs IWM) — the famous cluster-buy anomaly is arbitraged/absent here too, same
fate as deletion & lockup. This does NOT settle Arc 3 #1 (the pre-registered verdict is the FORWARD
agent-read), but it sets a hard baseline: the READ must turn a −2.5%/−6.5%-median, sub-coin-flip lottery into
positive-median selection — a steep bar. Did NOT tune knobs to chase a better bare number (p-hacking).
Reproduce: `python3 -m research.insider screen 2021 2025` (cache: research/data/insider_clusters.csv).*

**2026-06-23 · [ARC 3 #1] FORWARD ledger stood up (manual, pre-registered).** `research/insider_ledger.py`
(scan→decide→settle→show) reuses the openinsider ingest + a no-lookahead, multiple-testing-honest CSV
(`research/insider_ledger.csv`). scan logs every live cap-eligible cluster as a SEEN candidate (the
multiple-testing count); I read each in-session and `decide take|skip "why"` (timestamped pre-registration);
entry = first close AFTER that stamp; settle scores TAKES vs IWM at 63/126d. Gate unit-tested
(`tests/test_insider_ledger.py`, 3/3): refuses to score any entry not strictly after pre-registration.
*STATUS: ready; verdict accrues over 3–6mo (kill-criterion N=20 forward-settled TAKES or 2026-12-31). Given
the weak bare baseline, the honest expectation is LOW — but the read is the untested lever; this tells us
cheaply.* See [[project-experimental-event-edges]].

---

**MECHANICAL TRACK ~MAPPED (2026-06-23):** with factors/seasonality/carry done, the cheap free-data
mechanical families — reversion, fear/timing, forced-flows, trend, vol-premium, factors, seasonality, carry —
are all tested: ~21 pre-registered probes, **0 CONFIRMED to beat buy-hold SPY risk-adjusted.** The
momentum/trend family is the consistent near-miss (regime-flattered, never confirmed). Live levers unchanged:
the forward READING catalogue (accruing) and paid/gated data. The loop's mechanical queue is essentially
empty — don't re-grind it.

---

## ARC 5 — AUTOMATE & SCALE the forward-reading track (LIVE)

**2026-06-24 · DECISION (with user): the mechanical free mine is closed; point throughput at the
UNEXHAUSTED forward-reading edge and AUTOMATE it.** Diagnosis (full review): rigor never throttled bet COUNT
(23 pre-reg probes in ~3mo). Two REAL throttles did — (a) throughput was aimed at the exhausted mechanical
mine while the forward track was capped at "manual, 3 bets, prove-first"; (b) nothing was scheduled — the
cloud settle path CLAUDE.md calls PRIMARY did not exist, `/loop` was never scheduled, `daily.sh` was in no
cron. Fix: keep the ONE safeguard that matters (pre-registration + log-every-candidate + multiple-testing
count — the only thing separating this from `reference/`'s false-positive machine); drop the
human-approval/throughput throttle. Budget unlocked: spend when the trigger below fires.

**2026-06-24 · [ARC 5 #1] PRE-REGISTRATION (no data peeked) — the GENERAL forward-bet catalogue verdict
bar.** The `bets.py` catalogue (Claude's reading-driven directional calls vs a per-bet benchmark) graduates
from 3 hand-typed bets to a scheduled, batch-generated, auto-settled engine. Bar fixed BEFORE scaling, NOT to
be tuned to fit results:
- **PASS bar (must clear ALL, FORWARD/OOS):** at **N≥30 settled bets**, the catalogue shows (1) MEDIAN excess
  vs benchmark **>0**, AND (2) **beat-rate >55%** vs benchmark, AND (3) the result survives a multiple-testing
  adjustment (BH/Bonferroni over N) — i.e. not a chance run.
- **Honesty (non-negotiable):** every bet the agent takes is logged with an immovable timestamp
  (= pre-registration; lookahead-guarded at `research/bets.py:67`) and scored; NONE dropped retroactively. For
  any bet drawn from a BOUNDED candidate universe (e.g. insider clusters), every candidate is logged take/skip
  (the SEEN count, `insider_ledger.py`) so beat-rate can't be cherry-picked by volume. N counts toward the
  project multiple-testing tally.
- **Kill-criterion:** **N=30 settled OR 2027-06-30** (reading bets take 63–126d to mature, so the window
  extends past the insider ledger's 2026-12-31) — whichever first; if the bar isn't cleared → log NULL, the
  reading edge is noise on free data, stop expanding.
- **Honest prior: LOW.** The bare insider trigger already had a negative median (Arc 3 sanity screen); the
  whole hypothesis is that the READ beats the bare trigger / a naive benchmark. Free-data reads may find
  nothing — the point is to know cheaply, then let the trigger below decide the spend.

**2026-06-24 · [ARC 5 #2] PRE-REGISTRATION — the PAID-DATA spend trigger (budget = "spend when the math
justifies").** Do NOT spend pre-emptively. Trigger (pre-registered): **if the forward reading track (general
catalogue OR insider ledger) shows MEDIAN excess >0 AND beat-rate >55% vs benchmark at N≥20 settled**, buy a
real news/fundamentals + survivorship-clean price feed (Sharadar/Norgate-class, ~$50–100/mo) and (a) re-test
the data-blocked mechanical corners (Russell recon, cleaner deletion), (b) widen the reading agent's candidate
sources. Rigor on the math, not the wallet: refusing this spend once the trigger fires is as wrong as spending
before it.

*STATUS (2026-06-25, engine LIVE): two weekly cloud routines run unattended — **read** (Opus, Fri:
generate a batch of pre-registered bets via `research/READ_LOOP.md`) and **settle** (Sonnet, Mon: score
matured bets, commit). First batches in: **6 general bets** (NOW/META/NFLX/ACN/FDS/CMPS) + **2 insider takes**
(NVRI new-CEO-post-spin, LOGC Abrams-Capital NOL shell) + **17 insider candidates SEEN** (15 honest skips
logged). First general settlements ~**2026-09-21/22** (63 trading days), insider takes ~**2026-12-18** (126).
Verdict accrues toward N≥30 settled / 2027-06-30. Bug caught + fixed during red-team: the insider cap-gate
silently dropped 100% of clusters (`fast_info.get("market_cap")` → None; key is camelCase) — the whole
insider track was dark; now lit (0→17). Reproduce live state: `python3 -m research`.*

**2026-06-25 · [ARC 5 #3] PRE-REGISTRATION (no data peeked) — CATALYST CONTAGION in the psychedelics
complex.** Origin: user holds CMPS+HELP; on 2026-06-25 HELP (Helus/ex-Cybin) +24% on an idiosyncratic
catalyst (APPROACH Ph3 enrollment >86% + a $50M raise at $4.85 closing same day, removing the
run-out-of-cash overhang into Q4-2026 data), and CMPS +8% on NO own-news — pure sympathy. User's
hypothesis: "the complex moves on specific events." That's a TRUISM as stated (stocks move on news);
the falsifiable, TRADEABLE form:
- **Hypothesis:** when one psychedelics name posts a big *idiosyncratic* up-day (own catalyst), the PEERS
  (no own-news) earn *predictable* excess vs biotech (XBI) over the next 1–5 trading days. Sign unknown:
  continuation (buy peers) OR reversion (fade the sympathy pop).
- **Event def (fixed):** basket = liquid US psychedelics survivors {CMPS, ATAI, MNMD, GHRS} (+ HELP/CYBN
  where data exists); an "event" = a name's daily return ≥ +10% AND idiosyncratic (name return − basket-mean
  ≥ +7pp, so it's a NAME catalyst not a sector day). Peer reaction = equal-weight next-1/3/5d return of the
  OTHER names, entry at the close of the event day (no lookahead), excess vs XBI.
- **PASS bar (must clear ALL):** peers' next-1-to-5d excess vs XBI shows consistent-sign mean AND median,
  >55% hit-rate, AND era-consistent (not one cluster) — at a usable N.
- **Honest prior + caveats stated UP FRONT (this is a SANITY SCREEN, not a verdict):** (1) SURVIVORSHIP is
  fatal here — the basket is the survivor set; the 2021-vintage psychedelics SPACs/microcaps that went to
  ~0 are excluded, biasing any result UP (same trap as index-deletion/insider screens). (2) N is tiny — a
  handful of liquid names × a few catalysts/yr = low power, easy to fool yourself. (3) the names are highly
  correlated = one thematic bet; "contagion" may just be shared sector beta (hence the XBI benchmark). The
  CLEAN test is therefore FORWARD: pre-register the NEXT catalyst's peer reaction. Backtest = a lead only.
- **Kill-criterion:** if the cheap screen is null/sign-flipping/era-inconsistent → log NULL, do NOT build a
  module; if it shows a consistent sign, pre-register ONE forward bet (the OOS confirm) and stop.

**2026-06-25 · [ARC 5 #4] DECISION + PRE-REGISTRATION (with user) — the experimental account becomes a
PAPER LIVE BOOK, played as real.** Reframe: the user's long-term compounding lives in a SEPARATE,
already-compounding account (out of scope); this ~$6–8k is declared RISK/PLAY capital. We run it as
`research/book.py` (+`book.csv`) — a paper portfolio with sized positions, stops, cash, realized $ P&L,
SEPARATE from `bets.py` so sized roleplay churn never pollutes the [ARC 5 #1] skill-verdict N. The user
executes (or paper-executes — line deliberately blurred for fidelity) on Robinhood/E*Trade and reports
fills; I weigh each as a real financial decision and act as an unrestrained-but-pre-registering trading
partner. Goal = real GROWTH; cadence = short swing (days–2wk).
- **HARNESSES (fixed in advance, light — no goalpost-moving):** (1) whole-pool hard stop **−40%** from the
  seed baseline (equity at seed) → halt + log verdict; (2) max single play **~35%** of equity; (3) every
  play logs a **stop + target at entry** (no open-ended "see where it goes"); (4) **no PDT-triggering
  intraday round-trips** (<$25k ⇒ ≤3 day-trades/5d — we swing, don't day-trade); (5) CMPS+HELP sized as ONE
  bet (same theme).
- **SUCCESS BAR (growth-first):** over the run, **beat same-$-in-SPY** (the `book mark` yardstick), net of
  assumed costs/slippage. **Honest prior: NEGATIVE-EV.** Active retail churn underperforms (Barber–Odean) and
  our own 4 arcs found zero free edge — the open question this book answers is whether discretionary
  short-swing reads DEFY that, on a tiny scored sample. It may simply bleed to the −40% stop; that is itself
  a logged result. The book = the FULL experimental portfolio across **both brokers** (Robinhood + E*TRADE +
  a locked SPCX slug [redacted: long-realm]), seeded 2026-06-25 (CMPS/HELP/NIO/XRP + two SPCX lots + blended cash).
  First trade: trimmed the HELP position into its +24% catalyst spike (loss harvested; weakest binary horse).
  **Balances/sizes live in `book.csv`, never restated in this log.** Reproduce:
  `python3 -m research.book mark`.

**2026-06-25 · [ARC 5 #3] SANITY SCREEN → peer-contagion NULL; name-level REVERSION the only signal (weak,
no module).** 3y, survivor basket (MNMD returned no data — survivorship made literal), XBI bench, 38
idiosyncratic +10% single-name events. PEER reaction: +1d mean +0.58%/median +0.47%/hit 55% but DECAYS to
+3d median −0.39% / +5d mean −0.71% median −1.24% hit 42% — sign FLIPS across horizons → fails the
consistent-sign bar. The CATALYST NAME itself fades: +1d mean **−2.39%** median −2.51% hit 37%, negative all
horizons (spike-reversion / "sell-the-news"). *Verdict: the stated peer-contagion hypothesis is NULL — the
sympathy pop is a same-day/+1d blip that's gone by day 3 (consistent with the project's standing lesson:
small-cap event anomalies are arbitraged + survivorship inflates + tiny-N). The only consistent-sign reading
is name-level REVERSION after a +10% idiosyncratic spike, but it's n=38 survivor-biased, a SHORT in
hard-to-borrow microcaps (not cheaply tradeable), so NO module and NO forced forward bet. Practical
take-home (not an edge, a discipline): a one-day +24% spike like HELP's is statistically a better EXIT than
entry — trim into strength, don't chase. The READ_LOOP may opt to forward-test the spike-fade as one short
bet if a clean setup appears; not forced here. Reproduce: `python3 -m research.contagion` (one-off evidence, not wired into the engine).*

**2026-06-25 · [ARC 5 #4] BOOK MOVE + LESSON — XRP cut (spent-catalyst tell); NIO held to a dated trigger.**
Consolidation call (user leans on the model to decide timing; he executes + keeps his own observer ledger).
XRP $1.03 = a fresh 12-month low printed *today*, −55% 12m / −28% 3m, 0% of its range — and BTC −44% & ETH
−59% are ALSO at 0% of range while SPY is +22% at 91% → a synchronized crypto bear / risk-off rotation, NOT
an XRP-specific story. Its bull catalysts are REAL but SPENT: 7 US spot ETFs live (~$1.4B AUM, 7-wk inflow
streak), SEC case settled, EU CASP license 6/23 — and price made a NEW LOW into all of it. **Tell: when
public good news can't lift price, that's distribution, not accumulation — the catalyst is already in the
tape.** Our one validated edge (dual-mom, currently HOLD EEM) is negative on EVERY XRP horizon → avoid; so
"double down + be simple" inverts the only discipline we've banked. Verdict: SELL XRP (dead thesis) — exit
on the DECISION, not on a hoped-for bounce ($-timing immaterial at a $50 satellite; the bounce-wait is the
loser's anchor). NIO ($4.78, +38% 12m but −17% 1m) is NOT a peer of XRP: positive long-term trend, May
deliveries +62% YoY, first Q1 2026 adj operating profit, June delivery print due ~early-July → HELD on a
dated trigger (cut if the print misses / it can't reclaim). Take-home discipline (not an edge): cut what
violates the one signal we trust; don't average a downtrend; park a live name on its NEXT catalyst date,
never open-ended. Reproduce: `python3 -m research.book mark`.

**2026-06-25 · [ARC 5 #5] DECISION + PRE-REGISTRATION (with user) — CRANK THROUGHPUT + a FAST 21d
SLEEVE.** Diagnosis (live numbers): the book is ~deployed ($838 idle is correct — nothing clears the bar,
NOT a bug); the "stale" feeling is three throttles, two of them obsolete. (a) the `≤5 bets/run` + weekly
read cap was a *human-review* throttle from before the engine was automated — nothing reviews it now, so
it's lifted; (b) settle ran weekly though it's free, deterministic, idempotent — moved to **daily**; (c)
the real one: 63–126d horizons mean feedback is a quarter out. **Fix:** read cadence → **Mon/Wed/Fri
(3×/week)**, batch ceiling → **~10–15** (a CEILING not a quota — thin reads still SKIP), and a **21d FAST
SLEEVE** (`horizon_d ≤ 30`) that returns settled numbers in ~weeks. Throughput serves **discovery** (learn
sooner if the read edge is real), NOT P&L; the honesty guards are UNCHANGED — pre-registration +
log-every-candidate + multiple-testing. Mandate locked: **prove-edge-then-scale** — the book stays
small-sized, NO leverage / NO forced cash deployment, until the read track clears its bar.
- **Fast-sleeve hypothesis (pre-registered, no data peeked):** short-horizon (21d) catalyst reads beat
  their benchmark. Scored on its OWN N/bar, SEPARATE from the core 63/126d test so the (noisier) short
  reads can't contaminate the clean core verdict (`bets.is_fast`, threshold 30d).
- **PASS bar (must clear ALL):** **N≥30 settled, median excess >0, beat-rate >55%** vs benchmark — same
  shape as [ARC 5 #1], understood to be a NOISIER track (21d = more variance per bet, so treat a marginal
  pass with extra suspicion).
- **Kill-criterion:** bar not cleared by **N=30 settled OR 2027-06-30** → short-horizon reading is noise;
  retire the sleeve, keep core. Honest prior: LOW (same as the core read edge — unproven).
- Verdicts (both tracks + insider) live in ONE silo: `python3 -m research.engine`. Generation contract:
  `research/READ_LOOP.md`. Cadence is set on the cloud `/schedule` routines (settle=daily, read=Mon/Wed/Fri).

**2026-06-25 · [ARC 3 #1 / ARC 5 #5 follow-on] EDGAR bulk = durable 2nd insider source + cloud egress
fix.** The first crank-hard read run flagged the cloud insider scan ran DARK — egress policy 403'd
openinsider + yahoo (both work LOCALLY → pure cloud-egress block, not the source). Two-part fix:
(1) **allowlist** `openinsider.com` + `query1/query2/fc.finance.yahoo.com` + `finance.yahoo.com` in the
cloud env so the live scan + cap gate run unattended (user action — egress is an env setting, no repo file);
(2) **added `research/insider_edgar.py`** — SEC's quarterly Form345 structured datasets joined
(SUBMISSION + REPORTINGOWNER + NONDERIV_TRANS on ACCESSION_NUMBER) into the SAME
`[filing,trade,ticker,insider,value]` frame `insider._group()` already consumes, so the SAME
pre-registered trigger runs on authoritative ground truth (no scraper, no 1000-row page cap).
**Validation (number): EDGAR 2021-2025 = 2,266 clusters vs openinsider 1,502 → +51% completeness at the
same bar (2025 slice: 438 vs 330, +33%).**
Raw EDGAR carries occasional footnoted/garbage price rows (a "$325T buy") — bounded to plausible equity
txns (price ≤$1M, value/txn ≤$1B). EDGAR is QUARTERLY + lagged, so it is NOT the live feed (openinsider
stays live): it is the durable HISTORY (`edgar history START END`) + a forward completeness CROSS-CHECK
(`edgar audit`, clean once a published EDGAR quarter overlaps the live ledger's window; today it surfaces
out-of-window clusters — a diagnostic, not fresh takes). Pre-registered trigger UNCHANGED — no goalpost
moving (we widened SIGHT, not the gate). Reproduce: `python3 -m research.insider_edgar history 2025 2025`.

**2026-06-26 · [ARC 5 #6] DECISION (with user) — LOOSEN harnesses for an experimental phase +
add the CASE-STUDY reasoning layer.** The user moved the system toward faster, more aggressive
experimentation (trade/structure calls delegated to the model; his feedback after, not before).
- **Sizing cap LIFTED:** dropped the 35% max-single-play warning in `book.py` — size
  aggressively / concentrate on conviction, and idle cash MAY be deployed (the "prove-first /
  no-forced-deployment" mandate from [ARC 5 #4/#5] is retired).
- **KEPT (non-negotiable):** the integrity guards — pre-registration (immovable timestamp) +
  log-every-candidate (take AND skip) + multiple-testing N — the only thing dividing this from a
  false-positive machine; and the −40% whole-pool `POOL_STOP` (the money circuit breaker). The
  verdict BARS ([ARC 5 #1/#5]) are UNTOUCHED — loosening is on sizing/throughput, NOT the goalposts.
- **New layer — CASE STUDIES (`research/cases/*.md`):** the REASONING layer between a live move
  and a bet — document WHY/HOW a move happened → a reusable pattern, which births a scored
  `bets.py` call. Single source of truth: cases NARRATE, every number stays in its silo. Added
  `research/ARCHITECTURE.md` (the layer map + data flow) and `research/BACKLOG.md` (engineering
  changelog + open work + stale map — distinct from this science log).
- **First case bet (the worked example):** ILLR short 21d vs IWM (fast sleeve) — a
  borrowed-narrative "SpaceX-treasury-asset" pump on a 1:10-reverse-split, negative-equity,
  delist-deadline shell; spike-fade per [ARC 5 #3], XRP spent-catalyst tell per [ARC 5 #4].
  Paired with SPCX (the REAL SpaceX vehicle we hold) as the `real-vehicle-vs-meme` pattern.
  See `cases/ILLR.md` + `cases/SPCX.md`. Reproduce: `python3 -m research.bets show`.

**2026-06-26 · [ARC 5 #7] DECISION + PRE-REGISTRATION (with user, multi-model review) — SHARPEN the
reading verdict (one general silo, dollar-meaningful bar) + the book↔bets CONVERGENCE doctrine.**
Three independent reviews (Opus/Sonnet/Haiku, cold, read-only) + a user reframe. Legitimate as
pre-registration, NOT goalpost-moving: **0 bets have settled** (no data peeked) — this window closes
at first settlement (fast ~late-Jul, core ~Sep). Refines [ARC 5 #1/#5]; the kill date is unchanged.
- **MERGE the fast (≤30d) sleeve INTO the core → ONE pooled "general catalogue" verdict.** The
  question is "does the read add value", not "at 21 vs 63d". `is_fast`/horizon stays a DIAGNOSTIC
  label (post-hoc decomposition), never a separate goalpost. Two parallel N≥30 bars ~doubled
  time-to-verdict for no scientific gain. Multiple-testing silo count drops 3→**2** (general + insider).
  Caveat carried: pooling mixes horizons (a 126d bet has more room than a 21d) — the diagnostic split
  keeps that visible.
- **PASS bar (pooled general, must clear ALL, FORWARD/OOS):** at **N≥30 settled**, (1) **median excess
  > +1%** vs benchmark — an effect-size FLOOR; `>0` can confirm a 0.1% economically-meaningless ghost,
  (2) **beat-rate > 55%**, (3) survives multiple-testing: one-sided **Wilcoxon signed-rank** on
  excess_pct, **α = 0.05/2 ≈ 0.017** (Bonferroni over the 2 silos). Wilcoxon (not the bare sign test)
  buys ~25–30% power → a verdict near N≈22. The significance test is applied at settlement (no data to
  compute on yet; the engine shows PASS-CANDIDATE until then). Insider bar unchanged (N=20, median>0,
  beat>50% vs IWM).
- **STATED LIMITATION (not cheaply fixable — must accompany any pass):** the general catalogue draws
  from an UNBOUNDED news scan with NO candidate denominator (unlike the insider ledger, which logs every
  SEEN cluster). Selection alone could lift the chosen set's beat-rate to ~58–62% with zero skill. A
  general-catalogue pass is therefore CONDITIONAL: "the read may be selection, not skill, at N=30." The
  insider ledger is the clean-denominator control.
- **CONVERGENCE doctrine (what we DO — the missing "pass→action"):** the live book IS real money (no
  paper/real split); it was seeded from PRE-SYSTEM human positions, so book ≠ edge today. The book's
  standing job is to **converge onto the edge** — redirect legacy/underwater holdings into edge-driven
  high-conviction reads as catalysts/conviction allow: HOLD on conviction, recycle when a thesis/catalyst
  breaks or a higher-conviction read needs the capital; never dump merely to dump. Every legacy holding
  carries a **hold / redirect-on-catalyst** verdict (e.g. NIO→Jul delivery print, HELP→limit+backstop).
  `bets.py` (skill silo) and `book.py` (money silo) stay SEPARATE [ARC 5 #4] so sized churn never
  pollutes the verdict N; the existing case→bet→book bridge (`ARCHITECTURE.md`) is the channel. The book
  is judged in DOLLARS vs the real opportunity cost — **same-$-in-SPY AND same-$-in-dual-mom (the current
  EEM hold)** — floored by the −40% pool stop. "Scared money don't make money" is itself under test:
  aggressive sizing stays (no caps, [ARC 5 #6]); the stop bounds the experiment's downside.
- **Honest prior UNCHANGED: LOW.** This sharpens HOW we judge + WHAT we do; it does not raise the odds
  the free-data read has edge. Reproduce: `python3 -m research.engine` (one general silo + computed
  first-maturity dates), `python3 -m research.book mark` (vs SPY AND dual-mom).

**2026-06-28 · [ARC 5 #8] DECISION + PRE-REGISTRATION (with user, evidence-verified) — STRUCTURE the
read by SCENARIO TYPE (`pattern_tag`) + give the general catalogue a candidate DENOMINATOR.** Origin:
user hypothesis that edge is PER-SCENARIO, not one universal rule — consistent with our own 21-probe
null AND the "trade-as-a-story" doctrine. Two minimal, evidence-backed changes; written BEFORE any
settled data (0 bets closed → legitimate pre-registration, not goalpost-moving). Refines [ARC 5 #7];
bars + kill-dates UNCHANGED.
- **`pattern_tag` (the scenario type) becomes a STRUCTURED column** on `bets.py` / `insider_ledger.py`.
  The `cases/*.md` layer already names a tag, but the scored silo couldn't see it — so we could not
  decompose the verdict by scenario to TEST the per-scenario hypothesis. The engine now breaks the
  pooled general verdict down BY tag — a **DIAGNOSTIC lens ONLY** (exactly like the fast/core horizon
  split), **NEVER a per-tag goalpost**: N independent per-type bars = N× the multiple-testing false
  positives. A scenario type earns its own verdict only at a Bonferroni-clearing N.
- **Mover-scan = the candidate DENOMINATOR.** A deterministic daily top-movers scan over
  `universe.sp500()` (free, via `momentum.compute`) logs every mover as a SEEN candidate with a
  take/skip — mirroring the insider ledger's clean-denominator discipline. This **PARTIALLY** addresses
  the [ARC 5 #7] unbounded-selection caveat: selection is now bounded by the scan universe + logged →
  **reduced, NOT eliminated** (the scan universe ≠ all conceivable reads; that residual is stated
  with any pass).
- **UNCHANGED:** the pooled general bar (N≥30, median excess >+1%, beat>55%, Wilcoxon α≈.017), the
  insider bar (N=20), the integrity guards ([ARC 5 #6]), and the **honest prior: LOW.** This sharpens
  HOW we test + WHAT we log; it does NOT raise the odds the free-data read has edge.
- **DEFERRED (evidence-based, not assumed):** a bespoke multi-year NARRATIVE monitor. The mechanical
  narrative-arc form already FAILED twice — index-deletion [Arc 2 #1], lockup-expiry [Arc 2 #2]; the
  validation horizon is YEARS vs 0 settled bets today; survivorship/hindsight is severe (the loud
  narratives that DIED are invisible). Narrative stage is captured instead as the
  `narrative-stage-transition` tag; the monitor is built only if that tag accumulates instances with
  signal. Reproduce: `python3 -m research.engine` (per-tag diagnostic), `python3 -m research.movers`
  (the denominator scan).

**2026-07-06 · [ARC 5 #9] PRE-REGISTRATION — score SKIPS, not just takes: make "are we too
conservative?" a measurable question.** Origin: user asked whether the read's skip-heavy discipline
(the 2026-07-06 record-rally read took 1/25 movers — a contrarian IRM short — and skipped 24 up-movers
as "market-wide beta") is protecting edge or leaving money on the table. Found the system COULDN'T
answer it: `movers_ledger` scored only takes; a skip's forward return was never measured. Added
`movers settle` — scores BOTH takes AND skips forward vs SPY at 21d/63d (direction-aware, reuses
`bets._score`), assuming a momentum-continuation entry. Written BEFORE any matured data → legitimate
pre-registration, not goalpost-moving.
- **Number today: 100 decided movers logged (denominator), 0 matured at 21d/63d** (earliest decision
  8 calendar days old — 21d needs ~30 cal, 63d ~90); 0 fetch errors across all 100 names. Instrument
  built + running; N accrues (first 21d reads ~late-Jul, 63d ~late-Sep).
- **PRE-REGISTERED THRESHOLD (locked):** at skips 63d N≥30, if median excess >+1% AND beat-rate >55%
  vs SPY ⇒ the skip filter is TOO TIGHT — loosen the "thin read = SKIP" doctrine WITH evidence; else the
  discipline is vindicated. Takes are scored on the SAME 21/63d-vs-SPY ruler for contrast.
- **Red-team / residual risk:** (1) momentum-continuation assumption — a skip we'd have shorted
  (reversal) is mis-signed; `direction_hint` = the move's direction, which matched the actual take on
  the one taken short (IRM). (2) fixed 21/63d windows ≠ each idea's natural horizon (a coarse ruler,
  deliberately, for comparability). (3) still bounded by the S&P-500 scan universe [ARC 5 #7], not all
  conceivable reads.
- **Honest prior UNCHANGED: LOW.** This measures the DISCIPLINE; it does not add edge. Reproduce:
  `python3 -m research.movers settle` then `python3 -m research.movers show` (pooled take-vs-skip outcome).

**2026-07-06 · REAL-MONEY BOOK (operating decision w/ user).** Dropped the "paper/roleplay" framing:
the live book is the user's REAL-money account (~$6-8k, capital being added). This does NOT change the
honest prior — it RAISES the stakes on it. Real-money stance: grow it UNDER the null (LOW edge) —
don't-lose-it + capture cheap beta (SPY / dual-mom, the one banked result) + run CAPPED discretionary
experiments while the forward ledgers accrue; earn the right to size up WITH evidence, never on hope.
`bets.py` (skill verdict) stays SEPARATE from `book.py` (money) — more important now, so real-money
churn can't pollute the verdict N. Allocation policy + risk/concentration visibility backlogged; open
concerns logged in `BACKLOG.md` (NIO, cloud digest first-run; two items [redacted: long-realm]).

**2026-07-10 · BOOK RECONCILIATION + ALL-IN SUGGESTION POLICY (operating decision w/ user).**
(a) **Phantom position found and removed:** the 2026-07-06 SGOV park (11 sh @ 100.44 = $1,104.84)
was booked in `book.csv` but the order was NEVER placed at the broker (user-confirmed; CMPS/NIO/SPCX
are real). Fix = direct CSV edit, the exact inverse of the phantom `open`: row deleted, cash
68.64 → 1,173.48; realized P&L verified unchanged before AND after (sum −525.31); equity unchanged
(SGOV ≈ cash). The commit is the audit trail — no `book cancel` plumbing for a one-time event.
LESSON: the book only records reality when the human confirms the fill — which is exactly the
contract the new suggestion loop hardcodes (a `<fill>` placeholder that won't parse until replaced).
(b) **Deployment policy (user call, supersedes the 7/06 "capped experiments" default):** ALL free
cash is available to the read-run's sized suggestions — READ_LOOP step 5 DEPLOY: when cash idle
> $500, each Mon/Wed/Fri read MUST emit ONE sized order (pre-registered FIRST as a scored bet
carrying a `SIZED SUGGESTION` marker; the human executes at the broker and confirms with the real
fill via `book open`) or state in one line why cash stays idle. Expiry = supersession at the next
run. Integrity guards UNCHANGED [ARC5#6]: pre-registration, log-every-candidate, multiple-testing N,
the −40% pool stop. Verdict bars UNTOUCHED.
- **Red-team / residual risk:** (1) all-in single-name sizing can concentrate the book hard — the
  recommended core-beta-plus-capped-sleeve shape was declined; user chose max-learning/max-exposure
  knowingly; concentration-visibility stays an open BACKLOG watch. (2) The mandate pressures the read
  toward action — the (b) escape hatch (one honest idle line) plus skip-scoring [ARC5#9] keep
  "disciplined 0-take" measurable rather than forbidden. (3) Suggestions quoted at read time can be
  stale by execution — mitigated by supersession + confirming with the REAL fill, never the quote.
- **Honest prior UNCHANGED: LOW.** The book converges on edge only if the ledgers ever show one;
  this policy buys faster learning with real dollars, not edge. Reproduce: `python3 -m research.book
  show` (cash/positions) · `git log research/book.csv` (the reconciliation commit).

**2026-07-24 · EMA trend-break for ALPHA → NULL (user hypothesis tested, confirms the trend family).**
Origin: user asked whether simple EMA trend-breaks would out-earn the project. Tested, didn't argue.
EMA fast/slow crossover, long when fast>slow else flat, prior-day signal (no lookahead), 10bps/switch,
basket of 12 liquid high-beta names (SPY QQQ TSLA NVDA AMD META AAPL AMZN COIN NFLX MU PLTR), ~5y.
- **Number:** across 3 param sets, buy-hold beaten risk-adjusted (Sharpe) on at most **3/12** names,
  on CAGR at most **3/12** — worse than a coin flip. 20/50 and 10/30: **0/12** on CAGR. The seatbelt
  signature is intact: strat DD < buy-hold DD in ~8/10 (first single-name run), but return is given up.
- **The tell (regime, not edge):** split each series in halves → Sharpe-beats **0/12 in the 1st half**
  (the bull run: flat-in-cash cost you) vs 4–6/12 in the 2nd (which held the drawdowns to dodge). The
  "help" is entirely regime-dependent + unstable across time → not a durable edge.
- **Verdict: EMA trend-break is a regime-dependent DRAWDOWN-REDUCER, not alpha** — the SAME finding as
  single-name momentum [engine FAIL], 200d-trend-filtered momentum [engine FAIL], crypto trend [REAL*
  risk-reducer]. NOT logged as a new engine probe (would double-count the trend family already there);
  the durable USE is as a de-risk/exit overlay on beta, never an entry edge. Red-team: single split not
  full walk-forward, 12 names, 3 params (all reported — no cherry-pick), ~5y one era; a fuller
  walk-forward could only lower the prior further given 0/12 first-half. Chasing more params = p-hacking
  a mapped dead end. Reproduce: `PYTHONPATH=. python3 scratchpad/ema_test2.py` (one-off evidence).

**2026-07-24 · GO-ACTIVE book decision (with user) — kill the passivity tax, honor the stops, own beta.**
Origin: user frustrated the real-money book is stagnant (−16.4% vs baseline while same-$-in-SPY is +0.4%
— a ~$1.1k opportunity-cost gap) and chose "go active now". Diagnosis on live marks (`book mark`): the
loss is NOT SPCX (the locked 17-lot is +$143) — it's realized −$525 (HELP/XRP) + NIO −47%, and **$1,173
idle cash earning zero through a rally**. The stance was "cautious under the null" but was implemented as
sit-in-cash-and-underwater-names — the worst of both worlds (took the caution tax AND the passivity tax).
- **Decision:** (1) **honor the stops** — NIO 4.52 is THROUGH its 4.60 stop and was never cut; cut it.
  (2) **deploy idle cash into BETA** (fractional SPY / SPLG) — the one thing that has beaten our own
  picks (−16% vs +0.4%); stop-picking-and-own-the-index is the highest-EV active move the data supports.
  (3) **EMA20/50 break as the de-risk EXIT overlay** on that beta — the user's idea used where the number
  above says it pays (cutting DD), never as an entry-alpha signal.
- **UNCHANGED (non-negotiable):** integrity guards [ARC5#6] — pre-registration (immovable timestamp),
  log-every-candidate, multiple-testing N — and the −40% pool stop. "Active" changed our aggression, NOT
  the honesty machine or the verdict bars. `bets.py` (skill verdict) stays SEPARATE from `book.py` (money).
- **Honest prior UNCHANGED: LOW.** This stops a self-inflicted opportunity-cost bleed and adds an exit
  discipline; it does not create edge. Edge still only comes if the forward ledgers show one (settlements
  land this week). Reproduce: `python3 -m research.book mark`.

**2026-07-24 · EXIT-TIMING AUDIT (user hypothesis "we sell at lows") → yellow flag; adopt exit-into-strength.**
Origin: user flagged NIO would be our 3rd sale near a low + "don't sell the low" instinct. Tested our two
realized forced-low cuts vs holding, exit date → 2026-07-24.
- **Number:** HELP sold ~$6.50 (6/25) → now **$7.52 (+16%)**, peaked $8.10 (+25%). XRP sold $1.03 (6/25) →
  now **$1.09 (+6%)**, peaked $1.16 (+12%). **2/2 bottom-ticked — holding beat cutting on both.** The user's
  read of our behavior beat the model's (I'd invoked the disposition effect = hold-losers-too-long; our
  actual leak is the OPPOSITE, capitulation into recovering lows).
- **Rigor / why it's a flag not a verdict:** n=2 is an anecdote, and effectively **n≈1** — both sold the SAME
  day (6/25), i.e. one decision to liquidate the book into a late-June dip that broadly recovered. Proves
  nothing statistically; the sharper lesson is "don't liquidate into a down day."
- **RULE ADOPTED (cheap + robust regardless of N):** book exits use **limit orders into strength, never
  market orders into lows**; no same-day multi-name liquidation into weakness. This is process, not edge —
  honest prior UNCHANGED: LOW.
- **NIO application:** switched from the badly-placed 4.60 market-stop (it sat right on the 52wk low) to a
  limit-sell-into-strength exit at 4.85–5.15 (dead delivery thesis), downside fallback = close below the
  durable $3.14 floor (never breached in 3.5y). Reproduce: `PYTHONPATH=. python3 -c "from research import
  prices; ..."` (post-exit paths) · `python3 -m research.book show` (NIO exit rule).

**2026-07-24 · STANDING MANDATE (user) — bias to ACTIONABLE, fast-to-judge trades.** The user's
throughline this session: be more aggressive and learn from REAL decisions we can SCORE, not just
slow 63/126d reads. This is the ethos already behind the 21d fast sleeve [ARC5#5], go-active book
[this date], and skip-scoring [ARC5#9] — now stated as the standing preference: prefer trades with a
clear, near-term, gradeable outcome; grade every real book decision (entries AND exits) like a probe;
aggression is the default, the −40% pool stop + integrity guards are the only brakes. Does NOT change
the verdict bars or the honest prior (LOW) — it changes what we PRIORITIZE generating, not how we judge.
- **Cash plan:** ~$428 idle held DRY on purpose — reserved for post-settlement experimental plays
  (first fast-sleeve settlements land ~this week; deploy into the highest-conviction actionable read
  once we see them). SPY beta anchor already absorbs the bulk of former idle cash. Reproduce:
  `python3 -m research.book show`.

**2026-07-27 · ALERT AUDIT (INTC) — the read run's stated WHY was factually wrong, and its bet never
persisted. Book DECLINED to fund; the bet is registered LONG anyway.** User asked whether to buy the
alerted INTC long with the $428 idle cash. Checked the alert's premise against bars before answering.
- **The alert's claim is false (number):** it framed a "+9% rally into a −2.2% Nasdaq/semis-down tape =
  relative strength." The pop was **7/21, +8.6%, and SOXX was +5.4% that day** — an UP tape. True
  relative strength +3.2%, not strength-against-a-decline. The one sentence carrying the conviction
  didn't survive a two-minute check.
- **The setup had already inverted (number):** 105.45 (7/21) → **89.98 (7/27) = −14.7% in 4 sessions**,
  putting INTC **−7.3% below its pre-earnings 7/20 close of 97.06**. The gap fully round-tripped. That is
  the opposite of post-earnings drift, and it matches two things we already banked: spike-fade [ARC 5 #3]
  and the XRP spent-catalyst tell [ARC 5 #4] — *when good news can't hold price, that's distribution.*
  Context: −32% in a month (132.87 6/25 → 89.98), and higher-beta DOWN (7/24: −7.9% vs SOXX −4.4%).
- **We had skipped INTC 4× this month** (`movers_ledger` 7/08, 7/10, 7/13, 7/17), each time naming "18A
  yield delay + AMD DC-rev lead" as real thesis-breakers. The print retired neither. A long here is a
  silent reversal of four logged skips — exactly the drift the denominator ledger exists to catch.
- **PROCESS BUG (the important find):** the run pushed the alert to Telegram claiming it was
  "pre-registered and scored either way," but **`bets_catalogue.csv` had no INTC row and no read-run
  commit landed for 7/27** (catalogue 37 rows vs the digest's 38 open — the bet existed only in the
  run's container). A push without a commit is an unscored call. **This breaks the core integrity
  guarantee** — that the verdict N can't be cherry-picked by which alerts we act on. Alert-push and
  ledger-commit must be atomic, or the audit trail is decorative. *Backlogged as a real bug, not a
  one-off.*
- **Registered it LONG as alerted anyway** (`bets.py`, 7/27, entry 89.98 vs alerted 92.32) — filtering
  out calls I disagree with is itself cherry-picking. Stated caveat on the row: entering 2.5% better
  than alerted **flatters** this bet; discount any pass accordingly.
- **BOOK DECISION: NO BUY** — cash stays dry. Rationale is not "INTC is bad" but sequencing: the first
  fast-sleeve settlements land THIS WEEK (MU matured, ON/ILLR/AYI/BB mature today). Spending the reserve
  on a discretionary read the day before the first-ever evidence on whether this read has edge is
  backwards. Honest prior UNCHANGED: LOW. Reproduce: `python3 -m research.bets show` · `python3 -m
  research.movers show`.

**2026-07-27 · BOOK STRUCTURE — retired the stale SPCX stop (a nag is not a signal); user's "wait for
the bounce" reasoning rejected while reaching the same action.** The digest had repeated a DO-NOW
"SPCX THROUGH stop 150.00" for weeks; the user wanted to hold because "it dipped so low."
- **The user's stated reason is the error we already named** — "the bounce-wait is the loser's anchor"
  [ARC 5 #4, XRP]. Right action, wrong reason; logged as such so the reasoning doesn't get banked as
  validated. (The 7/24 audit's lesson is *how* to exit — limit into strength — not *whether*.)
- **The real reason to hold: [redacted — long-realm detail].** Selling the 1 liquid share managed
  no meaningful risk — churn on a ~$111 stub, 2% of the book. This is what distinguishes it from NIO, where the through-stop lot was fully liquid and
  the passivity genuinely cost money [7/24 go-active].
- **Stop retired, not moved:** the 150 stop was set under the then-6wk floor of 153; that floor broke
  ~7/17 and the stop has been un-actionable since. Spot 110.69 is an **all-time low on 30 bars** — there
  is no floor below it to anchor a replacement, so inventing one would be false precision. Logged as a
  deliberate, timestamped exception to the [ARC 5 #4] harness-3 stop-at-entry rule, scoped to an
  un-hedgeable stub — **not silent drift**. Exposure decision deferred [redacted: long-realm]; revisit on
  SpaceX-SPECIFIC news (today's −3.8% is tape: SOXX −3.5%, AMD −7.0%, NVDA −4.2%).
- **Generalizable lesson:** a recurring DO-NOW that no one acts on is usually a **stale rule**, not a
  disobeyed one. Fix the rule or honor it; leaving it to nag trains us to ignore the alert channel — the
  one channel whose silence is supposed to mean "broken." Reproduce: `python3 -m research.book show`.

**2026-07-27 · FIRST SETTLED BET — MU long 21d vs SOXX: excess −8.65%. n=1, decides nothing.**
**⚠️ [CORRECTED 2026-07-30 — the −8.65% below is WRONG: it was scored against a still-open
intraday bar. The true figure vs the completed close is −7.99%. See the 2026-07-30 entry.]**
The forward catalogue's first scored result, and the fast sleeve's whole purpose (a settled number
in weeks rather than a quarter) delivering its first one.
- **Number:** entry 1132.16 on 2026-06-26 (the bar strictly after the 6/25 pre-registration — the
  no-lookahead gate held), 21 trading bars, **−8.65% vs SOXX**. Pooled general silo now n=1,
  median −8.65%, beat 0%.
- **What it decides: NOTHING.** The bar is N≥30 & median >+1% & beat >55% [ARC 5 #7]. One
  observation is noise; quoting it as a verdict in either direction would be the exact
  goalpost-drift the pre-registration exists to prevent. It is logged because the rule is log
  every test, win OR loss.
- **Worth noting anyway (not a conclusion):** it was a *mod-HIGH* conviction call — the thesis
  named a structural guide-beat, $100B SCA supply contract, HBM sold out, PTs doubled — and it
  still lost 8.65% to its own sector. The stated risk ("already gapped +15%, crowded AI-memory")
  is what happened. If the pooled median lands negative at N≥30, this is the shape it will have.
- **Discovered by accident, which is itself the finding:** MU matured on 7/24 and had not settled,
  because the settle path had never run to completion. See the process entry below. Reproduce:
  `python3 -m research.bets show`.

**2026-07-27 · PROCESS AUDIT (user asked for gaps in the daily loop) — the evidence path was
lossy in nine places; fixed. No science claim.**
Full audit of the settle/read/Telegram loop. Two defects had already fired for real, and both
were SILENT — they lose evidence or lose the message while reporting success.
- **The settlement announcement could be lost forever.** `bets`/`insider_ledger` saved the closed
  row, then called `notify.send()` and discarded the result; `send` is fail-soft, so a dropped
  message exited 0, `daily.sh` recorded no failure, no heartbeat fired — and because the retry set
  was "rows that were open when settle started", a closed row could never be re-announced. That is
  how MU's −8.65% was announced by nothing. Fixed with a `notified` column stamped only on
  confirmed delivery; the retry set now comes from the ledger, so a lost 🚨 is re-sent next run.
- **`python-dotenv` was never declared in `requirements.txt`** though `config.py` imports it and
  `notify.py` imports `config` — a fresh container has NO working Telegram at all. Root cause of
  the above. The cheapest fix in the batch and the most consequential.
- **A 🟢 TRADE ALERT was pushed for a bet that was never committed** (the 7/27 INTC alert claimed
  "pre-registered and scored either way"; catalogue had 37 rows, digest said 38). READ_LOOP step 6
  already required commit-before-push and was simply not followed — so the check moved into
  `digest._git_section`, where it can be verified rather than requested. **Lesson worth keeping: a
  process rule that only exists in a document is not a control.**
- Also fixed: one poisoned row aborted the whole settle; a dead silo degraded to a quiet trailing
  line; a dead FEED did not even raise (a `scan` returning nothing looks identical to a quiet day
  → `feedstatus.py`); `daily.sh` pushed to a moved master with no rebase; the digest hardcoded a
  read cadence that had been stale for three days; a genuinely stuck settlement was
  indistinguishable from ordinary holiday drift.
- **Liveness:** "SILENCE = BROKEN" delegated outage detection to a human noticing an absence.
  Added a daily equity snapshot (`book_equity.csv`) whose newest date is a clock the digest reads,
  plus `research/watchdog.py` on a SEPARATE routine. **Honest limit, stated because it matters:**
  the watchdog only helps because it fails independently — if the scheduling platform dies, both
  die and nothing reports it. Narrowed, not closed.
- **This creates no edge and changes no bar, threshold or horizon. Honest prior UNCHANGED: LOW.**
  It only makes the ledgers trustworthy enough that the verdict, when it lands, means something.
  Reproduce: `python3 -m pytest research/tests/ -q` (82 passed) · `python3 -m research.watchdog`.

**2026-07-30 · CORRECTION + FIRST REAL READ — the fast sleeve returns 6 settled bets:
n=6, median −7.08%, beat 33%. Decides nothing. And MU's −8.65% was an artifact (true: −7.99%).**

**(a) The correction, first, because a wrong number in this log is worse than no number.**
The 2026-07-27 entry recorded MU at −8.65%. That settle ran MID-SESSION, and yfinance reports the
in-progress bar as the latest "close" — so the exit leg was priced off a still-moving quote (SOXX
508.49 intraday vs a **516.23** final close). Scored against completed bars, **MU is −7.99%**. The
row had already flipped to `closed`, so nothing would ever have re-scored it: a silently permanent
wrong number in the audit trail. Fixed at the source — `_score` now carries TWO symmetric gates
(entry bar strictly after pre-registration; exit bar a COMPLETED session), and the scheduled settle
at 05:08 UTC was never exposed. *Lesson, and it is the same one as the whole 7/27 audit: the
dangerous failures are the ones that write a plausible value and move on.*

**(b) The first real read of the general catalogue (all 21d fast sleeve, settled 7/28):**
| bet | excess vs bench |
|---|---|
| **short ILLR** | **+69.74%** |
| long ON | +15.28% |
| long AYI | −6.17% |
| long MU | −7.99% |
| long CIEN | −19.09% |
| long BB | −33.30% |

**n=6 · median −7.08% · mean +3.08% · beat 33%.** Bar is N≥30 & median >+1% & beat >55% [ARC 5 #7].
- **This decides NOTHING.** n=6 against a 30-bet bar is noise; quoting it either way would be the
  goalpost-drift pre-registration exists to prevent. Logged because the rule is log every test.
- **The one number worth staring at:** the mean is POSITIVE only because of ILLR. Strip that single
  short and the remaining five average −10.3% with a 1-in-5 beat rate. A mean carried by one
  observation is exactly the fat-tail shape CLAUDE.md warns about — read the MEDIAN here.
- **ILLR was the case-study short** (`cases/ILLR.md`, `real-vehicle-vs-meme`, [ARC 5 #6]): a
  borrowed-narrative pump on a negative-equity delist-deadline shell. n=1 proves nothing, but it is
  the one bet whose thesis named a mechanism rather than a direction.
- **The longs are the concern:** 5 of 6 bets were post-earnings-drift-style longs, and 4 lost to
  their benchmark, two of them badly (BB −33%, CIEN −19%). If that shape holds to N=30 the pooled
  verdict fails, and the honest prior (LOW) will have been right.

**(c) A silo has been dead for five weeks and nothing said so.** The insider ledger has not grown
since **2026-06-25**: still 18 rows, 2 open takes, 16 skips, zero new candidates. openinsider has
been returning nothing (the 7/30 read note says "insider fetch down"), so the silo that exists to
be the CLEAN-DENOMINATOR CONTROL on the general catalogue's selection caveat has contributed no
evidence for over a month, and its N=20 bar is going nowhere. This is precisely the failure mode
`feedstatus.py` was written for — it just wasn't merged yet. **Honest reading: we have been running
on ONE verdict silo, not two, without noticing.** Options are to repair the scrape or promote
`insider_edgar.py` (the durable SEC source, already built, quarterly/lagged) — a decision, not a
patch, and it is the user's to make.
- **Honest prior UNCHANGED: LOW.** n=6 is not evidence against it; it is not evidence yet at all.
  Reproduce: `python3 -m research.bets show` · `python3 -m research.insider_ledger show`.

**2026-08-01 · DIAGNOSIS + OPERATING DECISIONS (with user) — "trading feels stuck" is measurable,
and it was three things, none of them a missing feature. Plus the first [ARC 5 #9] skip numbers.**

**(a) Why the money never moved.** The user's read ("we improved messaging but trading is stuck")
is correct and the ledgers say why:
1. **Horizon mismatch.** Since 2026-06-28, **33 of 34** new bets are 63d+; exactly ONE 21d bet is
   open. The stated cadence is weekly swings; the machine generates quarter-long calls. There was
   nothing to *do* week-to-week by construction.
2. **The bridge has never carried money.** Two `SIZED SUGGESTION` bets have ever been issued
   (CTAS 7/17, DHR 7/22); **neither was executed** — a 0% conversion rate. And free cash of
   $427.81 sat **below the `cash > 500` gate**, so the system had stopped asking.
3. **The book never converged.** 4 of 5 positions are pre-system legacy names and account for the
   whole −17%. `ARCHITECTURE.md`'s standing job for the book — converge onto the edge — has not
   advanced since the 7/24 SPY anchor.
- **The part that must not be spun:** the ~$1,236 gap to same-$-in-SPY was NOT caused by too little
  trading. It was caused by legacy conviction positions. And the sleeve we would execute has n=6,
  median −7.08%, beat 33%. **More trading is not more edge.** What the fixes below buy is CADENCE
  and N — the pooled N≥30 bar is the bottleneck on ever reaching a verdict — not alpha.

**(b) DECISION — the $500 idle-cash gate is deleted; threshold now `digest.IDLE_CASH_MIN` = $150.**
Not a goalpost move, and the distinction matters: $500 was a **2026-07-10 operating convention**,
never a pre-registered bar. The protected commitments — the −40% pool stop, the three integrity
guards, the [ARC 5 #7/#8] verdict bars — are UNTOUCHED. Its sibling (the ">$500" *alert* gate) was
already deleted 2026-07-24 for the identical failure of swallowing actionable reads. The number now
lives in exactly ONE place and READ_LOOP points at it rather than restating it.

**(c) DECISION — the fast sleeve becomes MANDATORY when the catalyst is fast.** As a soft "ALSO
consider 21d" it produced one bet in five weeks. Now: any run that takes a weeks-resolving catalyst
must pre-register ≥1 bet at `HORIZON_d=21`, or say in one line why none qualified. **Generation
cadence only — no bar, threshold or horizon definition moves.** Horizon stays a DIAGNOSTIC
decomposition of the single pooled verdict [Arc 5 #8]; this just stops the catalogue back-loading
onto one quarter-end maturity wall.

**(d) FIRST [ARC 5 #9] SKIP-CALIBRATION NUMBERS — and they do not flatter the read.**
`takes 21d n=2 median −17.70% beat 0%` · `skips 21d n=23 median +4.70% beat 83%`.
- **Decides NOTHING**: the pre-registered bar is **skips-63d at N≥30**, and n=2 on the take side is
  not a sample. Logged because the rule is log every test, win or loss.
- **But the sign is the wrong one.** On the 2026-06-26 cohort the candidates we PASSED ON
  outperformed the ones we TOOK. If that survives to the 63d bar at N≥30 it says the read is not
  merely too conservative — it is anti-selective. Watch it; do not act on it at n=2.
- These numbers existed on 7/31 and were **lost**: the settle run committed them, the push failed,
  and the ephemeral checkout was destroyed (`1b014cc`). Master carried 0 of 400 movers rows scored
  for two days and nothing said so. Recovered 2026-08-01 by re-deriving from completed bars; the
  two non-recomputable artifacts (the six Telegram `notified` stamps, the 7/31 equity mark) were
  restored from the stranded commit. **Lesson: a failed push was a silent, permanent data loss
  path — "commit incrementally" is worthless if the commit dies with the container.**
- **Honest prior UNCHANGED: LOW.** Reproduce: `python3 -m research.movers show` ·
  `python3 -m research.digest`.

**2026-08-01 · [ARC 3 #1b] PRE-REGISTRATION (written BEFORE the test was run) — replacing the
live insider feed with SEC daily-index, and the parity bar that decides whether it counts.**

**The situation.** openinsider has produced nothing since 2026-06-25. It is NOT blocked upstream —
it returns 25 clusters from the laptop today, 8 of them new and cap-eligible. It is the only
plain-HTTP dependency in the system (the host serves no TLS at all; :443 times out) and cloud
egress refuses it. Decision with the user: repair the diagnostics AND replace the source.

**The claim under test:** `research/insider_sec.py` (SEC EDGAR daily-index → Form 4 XML) is a
LIKE-FOR-LIKE replacement for the openinsider scrape, not a change to what the insider bar means.
- It builds only the `[filing,trade,ticker,insider,value]` frame and calls `insider._group()`
  **unchanged**. MIN_INSIDERS=3, WINDOW_DAYS=30, MIN_AGG_VALUE=$250k, DEOVERLAP_DAYS=180, the
  $100M–$2B cap band, HORIZONS=[63,126], BENCH=IWM and the **N=20 bar are all untouched**.
- Latency is unchanged: openinsider is itself a Form-4 scraper and Form 4 is due 2 business days
  after the trade, so trade→signal lag is identical. (The QUARTERLY bulk `insider_edgar.py` is
  NOT a live feed — 2026q2 was still 404 a month after quarter end — and is not being promoted.)

**PRE-REGISTERED PASS BAR — locked here, before the number exists:**
> Over **2026-02-16 .. 2026-03-13** (20 business days inside the published 2026q1), comparing
> clusters from the daily feed against clusters from the quarterly bulk, both frames padded 35
> days so WINDOW_DAYS/DEOVERLAP see identical history, match = same ticker with signal dates
> within 5 days: **recall ≥ 0.95 in BOTH directions**, AND every unmatched cluster in either
> direction named and explained individually. At n≈30 that permits at most ~1 unexplained miss
> per direction. **Fail ⇒ the feed is not flipped**, whatever the failure looks like.

**Why the bulk and not openinsider as the comparator.** The obvious control — old feed vs new
feed — is unavailable: the comparator is dead, and gating a replacement on a dead comparator means
either never shipping or quietly weakening the bar afterwards, which is precisely what
pre-registration exists to stop. The bulk is also a *stronger* control: the SAME filings through a
completely different SEC pipeline, so any disagreement isolates a parser bug rather than a source
coverage difference. If openinsider ever returns, its overlap becomes a report-only sanity read
(20-day window so its 1000-row truncation does not bind, ≥0.90) — **never the gate**.

**Residual risks, stated in advance so they cannot be discovered conveniently later:**
- n≈30 detects SYSTEMATIC breakage (a wrong path, a dropped transaction code, an off-by-one
  window). It **cannot** detect a 2–3% sporadic defect rate. Do not claim it does.
- The bulk includes **4/A amendments**; the daily feed excludes them by exact form-type match.
  That divergence will show up as `bulk → daily` misses and is the EXPECTED residual, not a pass.
- Both sides share `insider._group()`, so a bug INSIDE the frozen trigger is invisible to this
  test by construction. It tests the frame, not the trigger.
- **This creates no edge and changes no bar. Honest prior UNCHANGED: LOW.** It only restores the
  second verdict silo so the general catalogue's selection caveat has a control again.
Reproduce: `python3 -m research.insider_sec verify 2026-02-16 2026-03-13`.

**2026-08-01 · [ARC 3 #1b] RESULT — the SEC daily feed FAILED its pre-registered parity bar.
recall(bulk→daily) = 0.946 vs a bar of 0.95. The feed is NOT flipped. openinsider stays the
(dead) live source until this is resolved.**

**The number, both runs, first one kept.**
| run | recall(bulk→daily) | recall(daily→bulk) | verdict |
|---|---|---|---|
| 1 — as first written | **0.898** (6 misses / 59) | 1.000 | FAIL |
| 2 — after a HARNESS defect was fixed | **0.946** (3 misses / 56) | 1.000 | **FAIL** |

**Run 1's harness was confounded, and that was my defect, disclosed rather than discovered
later.** `insider_edgar.clusters()` groups over whole QUARTERS, so the bulk arm saw ~90 days of
history while the daily arm saw 61 — `_group`'s 30-day window and 180-day de-overlap therefore ran
on unequal data. Three of the six misses (TRIN, COFS, TLPH) had **byte-identical frames on both
sides** — same trades, same insiders, same values, verified row by row — and differed only because
the two arms were handed different history. A comparison whose arms see different data does not
measure what it claims, so run 1 is not a clean fail; it is an invalid measurement. Both frames are
now clipped to the identical filing-date window. **Run 2 is the real result, and it still FAILS.**

**0.946 < 0.95 is a FAIL.** It is 0.004 short and the temptation to call it "essentially passing"
is exactly what the bar was written in advance to defeat. No third variant was run: tuning until
one clears is p-hacking with extra steps.

**All three residual misses have ONE cause: jointly-filed Form 4s with multiple reporting owners.**
- `BH` 2026-03-13 — bulk sees `BIGLARI, SARDAR` + `BIGLARI CAPITAL CORP.` + `LION FUND, L.P.`
  across four filings; the daily feed sees one insider on the same four filings, same dollar values.
- `SONO` 2026-03-11 — `Coliseum Capital Management, LLC` + `Coliseum Capital Co-Invest IV, L.P.` +
  `Shackelton Christopher S`, same pattern.
- `EMPD` 2026-02-20 — `ATG Capital Management GP LLC` + `ATG Capital Opportunities Fund LP` +
  `Gliksberg Gabriel`, plus one filing the daily window did not carry.
The mechanism: `_rows_from_xml` takes the FIRST `<reportingOwner>`; the bulk's
`.drop_duplicates("ACCESSION_NUMBER")` keeps an ARBITRARY one per accession, and across accessions
the arbitrary picks differ — so the bulk counts three distinct "insiders" where the daily feed
counts one.

**The honest complication, stated because it cuts against my own build rather than for it:** in all
three cases the "three insiders" are ONE economic actor filing through entities he controls. Read
plainly, the bulk is generating a FALSE cluster and the daily feed is the more correct of the two.
That does not rescue the result. The comparator was pre-registered as the bulk, the bar was
pre-registered at 0.95, and discovering after a failure that you prefer your own arm's semantics is
precisely the reasoning pre-registration exists to disallow. **The verdict stands: FAIL.**

**What it means — a question about the BAR, not a patch, and not mine to settle.** Whether related
filing entities count as one insider or three changes what a 3-insider cluster IS, and therefore
what the N=20 insider bar has been measuring all along [ARC 3 #1]. openinsider, the source being
replaced, lists each reporting owner separately — i.e. it sided with "three". Changing the daily
feed to match would be a goalpost move dressed as a bug fix, and must be pre-registered explicitly
with the user before any re-run.

**Status: openinsider remains the configured live feed and remains dead in cloud. The insider silo
is still not accruing.** `insider_sec.py` is built, tested (127 green) and NOT wired in. Two real
defects it caught in itself before any of this — a 400 KB cap silently truncating the daily index
into plausible-looking partial data, and a single TLS timeout killing a multi-hour run — are fixed.
**Honest prior UNCHANGED: LOW.** Reproduce: `python3 -m research.insider_sec verify 2026-02-16 2026-03-13`.

**2026-08-02 · [ARC 3 #1c] PRE-REGISTRATION #2 (written BEFORE the re-run) — multi-owner Form 4s
count as MULTIPLE insiders; same 0.95 bar, same window, one re-run.**

**The decision (user's call, taken explicitly because it defines the bar rather than patching it).**
A Form 4 filed jointly by several reporting owners now emits ONE ROW PER OWNER, so every owner
counts toward `_group()`'s 3-distinct-insider trigger. **Reason: openinsider — the source being
replaced — counted them separately, and the entire existing insider ledger (18 candidates, 2 open
takes) accrued under those semantics.** Choosing "one insider" would have left a single
pre-registered N=20 bar accruing future rows under a different definition than its past rows: a
silently mixed sample, which is worse than either definition on its own.

**Explicitly noted and NOT acted on:** "one economic actor" is arguably the more correct reading —
Biglari buying through Biglari Capital Corp and Lion Fund LP is one person, and by that reading the
3-insider trigger has a real false-positive mode for related filing entities. That is a genuine
weakness in the trigger, it predates this work, and fixing it mid-experiment would be a goalpost
move. It is logged here as a known flaw to test SEPARATELY, with its own pre-registration, later.

**One disclosed divergence from openinsider:** the DOLLARS are split evenly across owners, not
repeated. A joint filing is several filers reporting ONE transaction; repeating the full value
would let a 3-entity filing clear the $250k aggregate floor on $84k of real buying. Aggregate
value is therefore preserved exactly while the insider COUNT rises. This is the one place the new
feed knowingly differs from the old one, and it makes the trigger stricter, never looser.

**BAR — UNCHANGED, deliberately.** Same window (2026-02-16 .. 2026-03-13), same comparator (the
quarterly bulk), same match rule (same ticker, signal within 5 days), same threshold: **recall
≥ 0.95 in BOTH directions**, every miss named. The bar is not being relaxed to fit a feed that
already failed once at 0.946 — only the pre-registered SEMANTICS changed, and they changed toward
the source being replaced, not toward whatever makes the number pass.

**ONE re-run.** If it fails again the feed is not flipped and the SEC replacement is abandoned or
rethought from scratch — not tuned. Trying variants until one clears is p-hacking with extra steps.

**Cache invalidated on purpose.** The day cache stores PARSED rows, so this parser change makes
every cached day stale; reusing them would serve v1-semantics data under a v2 definition with no
error anywhere — the same "plausible wrong number" failure class as the truncation bug. The cache
path is now versioned (`sec_cache/v2/`) so the invalidation is structural rather than remembered.
Cost: a full ~44-day re-fetch.

**Prediction, recorded so it can be wrong:** the three residual misses (BH, SONO, EMPD) were all
multi-owner filings, so recall(bulk→daily) should reach 1.000. The risk now runs the OTHER way —
counting more insiders can manufacture clusters the bulk does not have, which would show up as
`recall(daily→bulk)` falling below 0.95 and would fail just as hard.
Reproduce: `python3 -m research.insider_sec verify 2026-02-16 2026-03-13`.

**2026-08-02 · [ARC 3 #1c] RESULT — FAILED again, WORSE, and my recorded prediction was wrong in
both halves. The SEC feed is ABANDONED as specified. But the run found something bigger: the
3-insider trigger itself has a structural false-positive hole, and openinsider fed it the same way.**

**The number.** Bar was recall ≥0.95 both ways. Result: **recall(bulk→daily) = 0.929,
recall(daily→bulk) = 0.743.** daily n=70 vs bulk n=56 — the feed manufactured 18 clusters the
bulk does not have.

| run | semantics | bulk→daily | daily→bulk | verdict |
|---|---|---|---|---|
| 1 | first owner only (harness confounded) | 0.898 | 1.000 | invalid |
| 2 | first owner only | 0.946 | 1.000 | FAIL |
| 3 | ALL owners [ARC 3 #1c] | **0.929** | **0.743** | **FAIL** |

**My pre-registered prediction was: "recall(bulk→daily) should reach 1.000; the risk runs the other
way." Both halves were wrong.** bulk→daily got WORSE (0.946→0.929), and daily→bulk did not merely
slip, it collapsed. Recording it because a prediction that only gets quoted when it lands is not a
prediction. Per the pre-registration — **ONE re-run, no tuning — the SEC daily feed is not flipped
and is not being adjusted further.** `insider_ledger.scan` still points at openinsider.

**WHY it failed — and this is the finding worth more than the feed was.**
A single Form 4 filed jointly by one investor's entity stack satisfies the 3-DISTINCT-INSIDER
trigger BY ITSELF:
| filing | "distinct insiders" | who they actually are |
|---|---|---|
| CVI 2026-02-24 | 3 | `ICAHN CARL C` + `ICAHN ENTERPRISES G.P. INC.` + `ICAHN ENTERPRISES HOLDINGS L.P.` |
| RXO 2026-02-17 | 6 | one person + five `MFN Partners` entities |
| FLYW 2026-02-18 | 5 | one person + four `Voss Capital` entities |
| BH ×4 filings | 3 each | `BIGLARI, SARDAR` + `BIGLARI CAPITAL CORP.` + `LION FUND, L.P.` |
That is **one buyer**, not a cluster. The whole premise of [ARC 3 #1] is that several INDEPENDENT
insiders buying at once carries information; one fund filing through its own GP/LP chain carries
exactly as much information as one buy.

**This is not a defect in the new feed. It is a defect in the BAR, and it is years old.**
openinsider — the configured live source, which produced every one of the ledger's 18 candidates —
also lists each reporting owner separately. So the existing insider silo has been exposed to this
same false-positive mode the entire time. The new feed did not introduce the hole; it made it
visible by being measured against an independent pipeline.

**NEXT — an audit, not a patch, and pre-registered before it runs:** re-derive the 18 existing
insider-ledger candidates and ask how many were single-filing entity-stack artifacts rather than
genuine multi-insider clusters. If a material share were, then the N=20 bar has been accumulating
toward a verdict on a trigger that does not mean what [ARC 3 #1] said it meant, and the honest move
is to reset the silo, not to keep counting. **Do not fix the trigger before that number exists** —
changing it now would destroy the ability to measure how much it mattered.

**Status: unchanged and stated plainly. The insider silo is still dead, still not accruing, and the
project is still running on ONE verdict silo.** `insider_sec.py` stays built, tested (128 green)
and unwired. Three days of parity work produced no working feed — and one real discovery about a
bar we have been trusting since Arc 3. **Honest prior UNCHANGED: LOW.**
Reproduce: `python3 -m research.insider_sec verify 2026-02-16 2026-03-13`.

**2026-08-02 · [ARC 3 #1d] PRE-REGISTRATION (written BEFORE the audit is run) — is the insider
ledger's evidence real, or entity-stack artifacts? The answer decides whether the silo RESETS.**

**Why.** [ARC 3 #1c] established that a single Form 4 filed jointly by one investor's entity stack
satisfies the 3-DISTINCT-INSIDER trigger by itself (`ICAHN CARL C` + `ICAHN ENTERPRISES G.P. INC.`
+ `ICAHN ENTERPRISES HOLDINGS L.P.`; MFN Partners ×6 on one RXO filing; Voss ×5 on one FLYW
filing). openinsider — which produced **every** candidate in `insider_ledger.csv` — lists each
reporting owner separately, so this ledger has been exposed to that mode since [ARC 3 #1].

**Composition, stated now because it is an input, not a result:** 18 candidates — 16 skip, 2 open,
0 settled. `n_insiders` is **3 for ten of them** (the bare minimum to trigger), 4 for four, 5 for
three, and **15 for one**. The ten 3-insider rows are exactly the ones a single entity stack can
manufacture.

**QUESTION (one, falsifiable):** of the 18, how many were **single-filing entity-stack artifacts** —
i.e. the 3+ "distinct insiders" that fired the trigger were reporting owners on ONE Form 4 and
belong to one beneficial owner — rather than genuinely independent insiders buying separately?

**METHOD.** For each candidate, pull the underlying Form 4s from EDGAR around its `signal_date` and
record two counts: distinct **reporting-owner strings** (what the trigger sees) and distinct
**beneficial owners** (what the hypothesis is about). Reuse `insider_sec._rows_from_xml` and
`insider_edgar._frame_one`; **the trigger stays untouched.** Classify a candidate as an artifact
when collapsing related filing entities drops it below MIN_INSIDERS=3. **Publish the per-candidate
call — all 18 — in the log entry.**

**THRESHOLD, LOCKED NOW: > 1/3 (i.e. ≥ 7 of 18) artifacts ⇒ the insider silo RESETS to N=0** under
a corrected trigger, because the N=20 bar would then be accumulating toward a verdict on something
that does not mean what [ARC 3 #1] said it meant. At ≤ 6, record the contamination rate as a stated
caveat on the bar and continue accruing. Either way the number goes in the log.

**Do NOT fix the trigger before this number exists.** Correcting it first destroys the ability to
measure how much it mattered — and "how much did it matter" is the only thing that justifies either
resetting or continuing.

**Residual risks, stated in advance:**
- **n=18 is small**, and 0 are settled — so this audits the CANDIDATE STREAM, not the edge. It
  cannot say whether insider clusters predict returns; only whether we have been counting the right
  events. Do not let a clean result be reported as support for the hypothesis.
- **"Beneficial owner" is a judgment call per filing, made by me, knowing the hypothesis.** That is
  the weakest link. Mitigation: every call is listed individually so it can be checked or overturned,
  and the rule is fixed in advance — same natural person or same fund family named in the filing's
  reporting-owner block counts as ONE.
- Reporting-owner strings are inconsistent across filings (`BIGLARI, SARDAR` vs `Biglari Sardar`);
  string-matching alone will under-count relatedness, biasing the result toward "not an artifact" —
  i.e. **toward continuing**, the more conservative direction for an already-suspect silo.
- The two OPEN takes (first settlement ~2026-12-18) are included; if either is an artifact its
  forward score is meaningless regardless of what the audit concludes about the rest.

**2026-08-02 · [ARC 3 #1] KILL-CRITERION ARITHMETIC — the deadline branch fired ~2026-07-08 and
nobody noticed. This is an ACCOUNTING entry, written BEFORE the [ARC 3 #1d] audit is run.**

**What the pre-registration says.** [ARC 3 #1] (2026-06-23, above): *"Kill-criterion: after **N=20**
forward-settled corroborated predictions **OR 2026-12-31** (whichever first), if the bar isn't
cleared → **log NULL, stop expanding this candidate**."* Horizon for the verdict: **126d**.

**The arithmetic** (computed with the project's own `engine._add_trading_days`, not by hand):

| Quantity | Value |
|---|---|
| Last date a 126d take could be logged and still settle by 2026-12-31 | **2026-07-08** |
| A take pre-registered TODAY settles | **2027-01-25** — after the deadline |
| Takes logged, ever | **2** (NVRI, LOGC, both 2026-06-25, both settling 2026-12-18) |
| **Max achievable N by the pre-registered deadline** | **2**, and it has been 2 since 2026-07-08 |

**So the N=20 branch has been unreachable for ~4 weeks, and the 2026-12-31 branch is what decides
this arc.** Note what this does NOT depend on: not the dead openinsider feed, not the three failed
SEC parity runs, not the entity-stack hole. A perfectly working feed delivering candidates every day
since 2026-06-25 could not have reached N=20 either. **The arc reached its own NULL branch on the
calendar, independent of every failure we have been busy diagnosing.** We spent 2026-08-01/02
building a replacement feed for a silo whose verdict window had already closed — that is the finding,
and it is a process failure, not a data failure: *no one was computing the deadline against the
horizon.* `engine.py` prints `first settles ~2026-12-18` and the bar `N=20 126d` side by side and
neither of us subtracted one from the other.

**Consequence, stated now BECAUSE it must not be stated later.** [ARC 3 #1d]'s two pre-registered
branches are **both moot**: you cannot "RESET the silo to N=0 and continue accruing" (≥7 artifacts)
toward a deadline that has lapsed, and you cannot "record the contamination rate and continue
accruing" (≤6) either. Declaring that *after* seeing the audit's number would be goalpost drift of
exactly the kind [ARC 3 #1c] refused. Declaring it now — on arithmetic wholly independent of what
the audit finds — is clean. **The audit still runs, unchanged, at its locked threshold**; what
changes is only what it is FOR: evidence on whether a rebuilt insider arc would ever be worth
building, and whether the historical bare-trigger FAIL is contaminated. Its number goes in the log
either way.

**Method honesty.** `_add_trading_days` steps weekdays and ignores holidays, so it reports maturity
EARLIER than reality — which makes 2026-07-08 the **latest possible** last-registrable date. The
real one is earlier. The approximation biases toward the silo still being alive, i.e. against this
finding, which is the conservative direction.

**Residual risk / what this does NOT say.** This says nothing about whether insider clusters predict
returns. It says the pre-registered instrument we built to answer that question can no longer answer
it. The two open takes still settle 2026-12-18 and will be scored — n=2 is not a verdict and must
never be reported as one, and both carry `n_insiders=3`, the bare minimum and precisely the class a
single entity stack can manufacture. **Honest prior on the hypothesis: UNCHANGED. Honest prior on
this silo's ability to test it: it cannot.**

Reproduce: `python3 -c "from datetime import date; from research.engine import _add_trading_days;
print(_add_trading_days(date(2026,7,8),126), _add_trading_days(date(2026,8,2),126))"`

**2026-08-02 · [ARC 5 #10] PRE-REGISTRATION (written BEFORE any new bet is generated under it) —
does the read's SHORT side carry the edge its LONG side doesn't?**

**Why now.** The shape was already logged on 2026-07-30 ("the longs are the concern: 5 of 6 bets
were post-earnings-drift-style longs, and 4 lost"). This entry does not discover it — it **locks a
bar for it before the next batch is generated**, which is the only thing that separates a
pre-registration from a post-hoc slice of an n=6 sample. Landing it tonight, before Monday's
pre-market `read` run, is the point.

**The observation, stated as an input:**

| Direction | n settled | excess vs benchmark |
|---|---|---|
| long | 5 | −7.99, +15.28, −6.17, −33.30, −19.09 → **1 win of 5**, mean −10.3% |
| short | 1 | **+69.74** (ILLR) |

Open catalogue for contrast: **32 long / 9 short.**

**QUESTION (one, falsifiable):** in the pooled forward catalogue, do SHORT bets earn positive median
excess vs their benchmark where longs do not?

**BAR, LOCKED NOW:** at **n ≥ 12 settled shorts**, median excess **> +1%** AND beat rate **> 55%**,
with the long sleeve reported alongside as the contrast. Below n=12 this decides nothing and must not
be quoted as if it did.

**What this is NOT.** It is a **DIAGNOSTIC decomposition** of the single pooled [ARC 5 #7] verdict —
the same class as `horizon_d` and `pattern_tag`, and governed by the same rule: **no separate
per-slice edge bar** [Arc 5 #8]. It cannot pass the project. It can only tell us where inside a
pooled result the variance lives.

**Explicitly forbidden, so it can be checked later:** do NOT tilt generation toward shorts to reach
n=12 sooner. That would be acting on an n=1 short before its bar — the exact p-hacking [Arc 5 #8]
exists to stop. The `read` loop's candidate selection is UNCHANGED by this entry.

**Residual risks, stated in advance:**
- **n=1 on the short side.** The entire "short looks better" impression rests on one observation,
  and stripping it flips the pooled mean from +3.08% to −10.3%. This is the fat-tail shape
  `CLAUDE.md` warns about, pointing the flattering way for once — which makes it more seductive, not
  less.
- **The one short came from a different pipeline.** ILLR was the *case-study* short
  (`cases/ILLR.md`, `real-vehicle-vs-meme`) — the one bet whose thesis named a mechanism rather than
  a direction. So "shorts win" and "case-study-generated bets win" are **confounded at n=1**, and
  this bar cannot separate them. If the short sleeve passes, that confound must be resolved before
  anything is concluded about direction.
- **Asymmetric survivorship:** short candidates that ran away are still open, longs that collapsed
  settled fast. At n=6 the settled set is not a random draw from the catalogue.
- **9 open shorts vs a 12 bar** means the earliest this can resolve is after the current short book
  matures — no new generation required, and none should be added for this reason.
- Also recorded, not acted on: **15 of the 41 open bets carry the `post-earnings-drift` tag**, the
  same tag on 5 of the 6 settled bets of which 4 lost. That is a stated **concentration risk on the
  pooled verdict**, not grounds to change the tag mix mid-flight.

Reproduce: `python3 -m research.bets show`

**2026-08-02 · BOOK DECISIONS (with user) — the NIO cut is REVERSED, and the book's −17% is
inadmissible as evidence about the read. Two facts I had wrong, corrected here.**

**(a) The book's drawdown says NOTHING about the system.** I framed the gap ("beta didn't fail, our
picks did") as evidence the read underperforms. It is not. `book.csv` shows **every open position
was opened 2026-06-25 at seed** — CMPS, NIO, SPCX ×2, the user's pre-existing inventory —
plus the SPY beta anchor opened 2026-07-24. **Zero read-generated equity positions have ever been
in the book.** The −17.1% vs baseline measures legacy inventory and a deliberate beta hedge. Citing
it as evidence about signal quality inverts the exact silo separation `CLAUDE.md` exists to enforce,
and it would have been wrong in the *pessimistic* direction — the flattering error is the one you
catch, this was the other kind. **The read's only evidence remains the catalogue: n=6.**

**Twin coverage of the live book, measured:** 1 of 5 open positions has a pre-registered bet twin
(CMPS, logged 2026-06-25T15:46, same day as the fill — genuine, not retroactive). NIO and the two
locked SPCX lots are seed inventory; SPY is the beta anchor by design. So the book is currently
~20% covered, which is the concrete thing the new twin rule below is for.

**(b) NIO: the deferred cut is REVERSED — HOLD.** Backlog handoff item 2 said "cut NIO, confirm the
fill." Killed on the user's call, and the reasoning survives inspection: NIO is **$4.88 against a
52-week low of $4.44** — 11% off the bottom, −17.4% over 3mo. Selling here is selling the bottom,
and `SKILL.md`'s **"exit into strength; never market-dump into a low"** rule was earned from exactly
this (HELP and XRP both bounced +16%/+6% after we market-sold near local lows; `book.csv`'s own
bottom-tick audit records it). The booked stop stays **$2.90**; exit into strength only. **The
delivery thesis is still dead** — this is a decision about *execution price*, not a revived thesis,
and it must not be logged as one.

**(c) Cash-allocation policy NOT reopened.** BACKLOG's 2026-07-10 decision (all free cash to the
read-run suggestion sleeve) carries its own revisit condition: *"revisit WITH evidence when the
pooled verdict lands."* That is ~2026-10-19 at N=30. Reopening it now on n=6 would be the
goalpost-drift this project exists to prevent — in the direction of *less* risk, which is still
drift. The user's stance is explicit and recorded: trade for alpha, not beta parking.

**(d) NEW RULE — no real-money position without a pre-registered twin.** Every `book open` gets a
`bets.py` bet (thesis, horizon, benchmark, tag, stop) written BEFORE the fill. `READ_LOOP` 5b
already complies by construction; the rule bites on DISCRETIONARY trades opened between runs.
`book.open_` now prints a warning naming the missing twin. **Deliberately non-blocking** — refusing
to record a real fill to enforce paperwork would corrupt the ledger's one job. Silos stay separate
for SCORING; this is about coverage, not merging them.

**Why this is the change that serves "create alpha through experiments":** the constraint is not on
*how much* we trade or *how aggressively* — the [ARC 5 #6] sizing cap stays lifted and the −40% pool
stop stays the only backstop. It is that a trade with no twin can never reach the verdict. At n=6
against a 30-bet bar, coverage is the binding constraint on learning, not conviction.

**Honest prior UNCHANGED: LOW.** Nothing here is evidence for or against the hypothesis; (a) is a
retraction of evidence I should never have offered.
Reproduce: `python3 -m research.book show` · `python3 -m research.bets show`

**2026-08-02 · [ARC 3 #1d] RESULT — the entity-stack hole is REAL but it is NOT what built this
ledger. 0–2 artifacts of 18, against a locked threshold of ≥7. The silo does NOT reset on this
number — it is already closed by the [ARC 3 #1] deadline arithmetic logged above.**

**THE NUMBER: 0 of 18** under the primary reconstruction; **1** and **2** under two alternative
window reconstructions (below). **Threshold was ≥7 of 18 ⇒ RESET to N=0. Not approached under any
reconstruction.** I expected this to come back dirty. It came back clean, and the reason is
specific and checkable.

**Per-candidate calls — all 18, as pre-registered.** "EDGAR owner strings" = distinct
reporting-owner names on the underlying Form 4s (what the trigger sees). "Beneficial" = after
collapsing related filing entities (what the hypothesis is about).

| ticker | signal | ledger n | EDGAR owner strings | beneficial | artifact? |
|---|---|---|---|---|---|
| LODE | 2026-06-03 | 4 | 4 | 4 | no |
| NVRI | 2026-06-08 | 3 | 3 | 3 | no |
| SSMR | 2026-06-08 | 5 | 5 | 5 | no |
| BWFG | 2026-06-09 | 5 | 5 | 5 | no |
| MBC | 2026-06-09 | 4 | 4 | 3 | no |
| INR | 2026-06-11 | 4 | 4 | 4 | no |
| PICS | 2026-06-12 | 3 | 3 | 3 | no |
| LOGC | 2026-06-15 | 3 | 3 | 3 | no |
| EU | 2026-06-16 | 3 | 4 | 4 | no |
| FLNT | 2026-06-16 | 4 | 8 | 6 | no |
| VIA | 2026-06-16 | 3 | 3 | 3 | no |
| EML | 2026-06-17 | 5 | 7 | 6 | no |
| BORR | 2026-06-22 | 3 | 3 | 3 | no |
| FCBM | 2026-06-22 | 15 | 15 | 10 | no |
| LOVE | 2026-06-23 | 3 | 3 | 3 | no |
| KARD | 2026-06-24 | 3 | 13 | 8 | no |
| LILA | 2026-06-24 | 3 | 5 | 4 | no |
| MOBI | 2026-06-29 | 3 | 27 | 15 | no |

**THE DECISIVE COLUMN is not the artifact flag — it is `ledger n` vs `EDGAR owner strings`.**
Entity-stack inflation, if it were happening, would show as the ledger counting **MORE** insiders
than EDGAR has distinct reporting owners. **It never happens.** 12 of 18 match EXACTLY; the other 6
run the other way (EU +1, EML +2, LILA +2, FLNT +4, KARD +10, MOBI +24 — the ledger UNDER-counts).
There is not one candidate in the ledger where openinsider inflated the insider count.

**So the [ARC 3 #1c] premise was wrong about THIS ledger.** That entry stated openinsider "lists
each reporting owner separately, so this ledger has been exposed to that mode since [ARC 3 #1]."
The exposure was real in principle and was demonstrated on SEC data (RXO/MFN ×6, FLYW/Voss ×5) —
but the openinsider cluster screen that actually fed these 18 candidates evidently collapses
multi-owner filings rather than expanding them. **The hole is in the trigger, as [ARC 3 #1c] said.
It just never fired through this particular feed.** Writing that down because the previous entry's
closing line ("the existing candidates are suspect too") is now measured and false.

**And the 3-insider rows — the ten flagged as most at risk — are clean.** Spot-checked by name:
NVRI = Minan / Purvis / Hochman; PICS = Augusto / Batista Costa / Pruett; LOGC = Stewart / Levy /
Bobbili; VIA = Fain / Ramot / Peres; BORR = Schorn / Morand De Oliveira / Troim; LOVE = Nelson /
Fox / Heyer. Three separate natural persons filing three separate Form 4s in every case. These are
genuine multi-insider clusters, not one investor's filing chain.

**METHOD, and where it deviates from the pre-registration.** The pre-reg named
`insider_sec._rows_from_xml` and `insider_edgar._frame_one`. `_frame_one` proved **unusable**: the
2026q2 bulk is not published yet (verified — `_quarter_path(2026,2)` returns None), and it also
`drop_duplicates()` to one owner per accession, which is the exact count under audit. Purchases are
therefore parsed with the named parser `_rows_from_xml` (identical P/A semantics), fetched per
ISSUER via the EDGAR submissions API rather than the daily index — ~250 requests instead of
~21,000, and it preserves which owners co-reported on the SAME Form 4, which is the entity-stack
signature. **The trigger was not touched.** A first run returned 0 documents for all 18 and looked
like a finding; it was a bug — `primaryDocument` is the XSL *viewer* path, and fetching it returns
HTML that parses to zero owners. Recorded because a broken fetch that resembles a clean result is
the most dangerous failure mode in this project.

**Robustness, honestly.** Three window reconstructions were tried and none is exact, because
`_group` fires on a 30d window running FORWARD from a candidate first-trade while `signal` is the
LATER filing date of the 3rd distinct insider — the window cannot be recovered from the signal date
alone. Wide filing net: **0** artifacts. Trades within 30d BEFORE the signal: **2** (MBC, MOBI).
Re-deriving the cluster via the untouched `_group`: **1** (LILA). Manual inspection shows all three
flags are artifacts of the window recovery, not entity stacks — LILA's window is Malone / Bracken /
Winter / Nair / Paddick, five distinct people. **The threshold is 7. The spread 0–2 does not reach
it, so the window ambiguity does not change the conclusion.**

**The matcher's error direction is stated, and it favours the hypothesis I was testing.** Owner
grouping chains on any shared identifying token, so it **over-merges**: it merged `Banyard R David`
with `PETRATIS DAVID D` (shared "DAVID"), `CRANDELL KEITH` with `Johnson Keith Bryon`, and chained
six separate FCBM directors through shared given names. Every such error **lowers** the beneficial
count and therefore **manufactures** artifacts. The reported counts are an **UPPER BOUND**. A clean
entity resolver would return fewer artifacts, not more — which is why the conclusion survives
without one.

**SECOND CONTAMINATION MODE — recorded separately, NOT folded into the count** (changing what is
counted mid-audit is the drift this pre-registration exists to prevent). **IPO-allocation
artifacts** are present and are materially larger than entity stacking: KARD (ARCH ×3 + HRTG ×3
entity stacks buying their own deal at the $16.00 IPO close, $90M), FCBM (15 buys at the exact
$12.50 offer), MOBI (27 owner strings dominated by pre-IPO vehicles at exactly $15.00), SSMR
(directors at the $13.50 offer), PICS. **Five of 18 candidates — 28%.** These clear a
"3 distinct insiders + $250k" bar mechanically and mean nothing about conviction. Any future
insider trigger must exclude filings priced at an offer price near an IPO date. It needs its own
pre-registration; it does not get retro-fitted here.

**A point FOR the agent read, stated with its caveat.** The read **skipped all five** IPO-allocation
candidates and named the mechanism in each rationale ("IPO artifact - 15 buys all at exact 12.50
offer", "90M is ARCH/Berns buying own deal at 16.00 IPO-close price"). The structured trigger could
not see it; the read could. **Caveat that kills this as evidence: 0 of the 18 are settled**, so this
says the read identified a mechanical false-positive mode correctly — not that skipping them made
money. It is a point about the READ's mechanism-detection, logged as such, and it is NOT support for
the [ARC 3 #1] hypothesis.

**WHAT THIS DOES AND DOES NOT DECIDE.**
- It does NOT resurrect the silo. [ARC 3 #1]'s deadline branch fired ~2026-07-08 (entry above); a
  clean candidate stream cannot revive a verdict window that has closed. **≤6 artifacts would have
  meant "record the caveat and continue accruing" — and there is nothing left to accrue toward.**
- It does NOT say insider clusters predict returns. As pre-registered: this audits the CANDIDATE
  STREAM, not the edge. 0 of 18 are settled. **Do not report a clean result as support for the
  hypothesis** — the pre-registration said that in advance, and it applies now.
- It DOES mean the two open takes (NVRI, LOGC) are real 3-person clusters, so their 2026-12-18
  settlement will measure what it claims to. n=2 remains not a verdict.
- It DOES retire "the existing candidates are suspect" as a live concern. That was the stated
  reason `insider_sec.py` was being kept. It no longer applies.

**Honest prior UNCHANGED: LOW.** Three days of feed work produced no working feed, and this audit
produced a clean bill of health for a ledger that has already run out of calendar.
Reproduce: the audit script is one-shot (scratchpad, not shipped); the decisive column is
reproducible directly — for any candidate, `data.sec.gov/submissions/CIK<issuer>.json` → Form 4s
around `signal_date` → count distinct `rptOwnerName` vs the ledger's `n_insiders`.

**2026-08-02 · [ARC 3 #1c] follow-up CLOSED WITHOUT A NEW TEST — the historical bare-trigger FAIL
cannot be entity-stack contaminated, for structural reasons. `SKILL.md`'s rule stands unamended.**

[ARC 3 #1c] logged the entity-stack hole as "a known flaw to test SEPARATELY, with its own
pre-registration, later." The worry that made it urgent: `insider.py`'s 2021–2025 historical screen
(1502 events, 724 priceable, 126d median **−6.53%**, beat **42%**) ran the SAME `_group()` trigger,
so if entity stacks manufacture clusters then that FAIL is computed on a contaminated population —
and that FAIL is not a dead number. It is `engine.py`'s `insider-cluster bare trigger — FAIL` row
AND one of the four anchors under `SKILL.md`'s **"Free + famous = arbitraged"** rule. A wrong
conclusion promoted to a durable method rule is worse than an unresolved silo, so this was queued
as the next expensive test.

**It does not need one. Both historical sources are structurally incapable of the failure mode:**

- **The screen's actual source is openinsider** (`insider screen 2021 2025`, cache
  `research/data/insider_clusters.csv`) — and [ARC 3 #1d] just measured openinsider against EDGAR
  on 18 candidates: 12 exact matches, 6 where it UNDER-counts, **0 where it over-counts.** It
  collapses multi-owner filings; it does not expand them.
- **The EDGAR-bulk cross-check cannot do it either, by construction.** `insider_edgar._frame_one`
  calls `.drop_duplicates("ACCESSION_NUMBER")` on REPORTINGOWNER, so **every accession contributes
  exactly one insider name**. Verified on 2025q2: 50,861 accessions, 1,379 (2.7%) carry more than
  one reporting owner, max 10 — and after the dedupe, max owners per accession is **1**. A single
  filing mathematically cannot supply 3 distinct insiders.

**The only path that ever produced the failure was `insider_sec.py` run 3**, which deliberately
emitted one row per owner to match what openinsider was *believed* to do. It manufactured 18 false
clusters (daily→bulk recall 0.743) and is abandoned. **The hole is real, it is in the trigger, and
it has never touched a number this project relies on.**

**Consequences:** `engine.py`'s FAIL row stands. `SKILL.md`'s "free + famous = arbitraged" rule
stands — its insider anchor is sound. And the stated reason for keeping `insider_sec.py`
("the [ARC 3 #1d] audit may reset and rebuild the silo") is now void on both halves.

**Residual risk, stated:** the direct evidence for openinsider's collapsing behaviour is n=18
candidates, all from June 2026; the historical screen covers 2021–2025. Same code path, same feed,
but I have not verified openinsider's semantics were identical five years ago and cannot cheaply —
re-deriving 1502 clusters from per-issuer Form 4s is a large fetch against a hypothesis with no
supporting evidence. The EDGAR-bulk half of the argument is structural and carries no such caveat.
**Decision: not worth the spend.** Logged as a bounded assumption rather than a silent one.
Reproduce (the local cache was deleted with the arc — refetch, ~13MB, no auth):
`curl -A "you@example.com" -o /tmp/q.zip https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2025q2_form345.zip`
then read `REPORTINGOWNER.tsv` from it and compare
`groupby("ACCESSION_NUMBER").RPTOWNERNAME.nunique().max()` (observed **10**) against the same after
`drop_duplicates("ACCESSION_NUMBER")` (observed **1** — the collapse that makes the failure mode
structurally impossible).

**2026-08-02 · ARC 3 CLOSED — the insider silo is retired and its code deleted. Logged as its own
decision, on the deadline arithmetic, NOT as an output of the [ARC 3 #1d] audit.**

The audit came back CLEAN, so this retirement cannot be attributed to it — that would be reading a
result to justify a conclusion it does not support. The justification is the entry three above:
**[ARC 3 #1]'s kill-criterion fired on its deadline branch ~2026-07-08**, with max achievable N = 2.
`engine.py`'s probe row moves `PENDING → NULL` (probe count unchanged at 23; the historical bare-
trigger FAIL row is untouched — it is settled evidence and its validity was separately confirmed).

**Deleted:** `insider.py`, `insider_ledger.py`, `insider_sec.py`, `insider_edgar.py`,
`insider_ledger.csv`, `insider_clusters*.csv`, both test files, and the `edgar_cache/` (216MB) +
`sec_cache/` caches. **Rewired in ONE commit** across the six call sites that made this a refactor
rather than a delete: `engine.forward_track`, `__main__.status`, `heartbeat.msg`, `digest.LEDGERS`,
`watchdog.WATCHED`, and `scripts/daily.sh` (settle step + LEDGERS list).

**Three things kept deliberately:**
1. **The `engine` surface still prints an "insider ledger: CLOSED" line.** A silo that silently
   disappears reads as one that never existed; the point of that surface is that a cold session
   sees the honest state first — including that this project runs on ONE verdict silo.
2. **The evidence.** Every number, every per-candidate call, and both contamination modes stay in
   this file. The code is in git history. Deleting a module is not deleting a result.
3. **The two paid-for findings**, recorded in `CLAUDE.md` for whoever rebuilds an insider arc: the
   entity-stack hole in the 3-distinct-insider trigger, and the larger IPO-allocation mode.

**One live degradation fixed by the same diff:** `digest._feed_section` had been emitting
"openinsider has NEVER reported a successful fetch" as a DO-NOW on **every** push, with no possible
resolution. An alarm that cannot be cleared trains the reader to ignore the channel — a real
weakening of the alerting spine, not cosmetics. The `openinsider` key is dropped from
`_feed_status.json` and `feedstatus.py` now carries the rule: **when a feed is retired, delete its
key in the SAME diff.** The digest is back to one clearable DO-NOW.

**What the project looks like now:** ONE verdict silo (the pooled general catalogue, n=6 toward
N≥30, first core settlement ~2026-08-20), ONE candidate denominator (`movers.py`), one real-money
book, one banked usable result (dual momentum). **Honest prior UNCHANGED: LOW.**
Reproduce: `python3 -m research.engine`

**2026-08-02 · BOOK CORRECTION — a third of the book was never a position. $1,785 of CASH was
recorded as 17 shares of stock at seed and marked to SPCX's price for five weeks.**

*[Body redacted for the public record — long-realm personal detail. The full entry is preserved
in the private archive; what the science needs survives below.]*

**What happened.** At seed (2026-06-25) a human-seeded line item was logged as `SPCX 17 @
$105.00`. Reconciliation against the account's own statements showed **0 shares** — the
"position" was a cash balance held outside the brokerage, money that cannot move with the
stock. The book had been marking cash to SPCX's live price for five weeks, manufacturing P&L
(a fictitious +$57 at discovery) and diluting the loss on everything else. **Corrected book
equity is −24.6% vs baseline, not −17.1% — the error was hiding 7.5 points of drawdown.**

**The fix.** The phantom row is REMOVED, not closed — closing books a realized P&L on a trade
that never happened. The `__SEED__` baseline drops by the same $1,785 (6582.74 → 4797.74) so
the vs-SPY comparison stays apples-to-apples. Private git history holds the original rows. The
cash stays OUT of the book by design: it is not a trading decision, and counting it would
corrupt the benchmark the book exists to measure against.

**Consequence for the one real SPCX position.** The 1-share lot's standing rationale ("selling
it disposes of 6% of the exposure and manages nothing") is **void**: it was 100% of the SPCX
held anywhere. The [ARC5#4] stop exception logged on 7/27 was reasoned from a holding that did
not exist.

**The lesson, and it is the expensive one.** We spent this session's second half chasing
documents to pin down the terms on a position that was never held. **The prior question — "do
we actually own this?" — was never asked, because the number was in the ledger and ledgers are
treated as evidence.** A seeded position is NOT a settled fact; it is an unverified human
input, and it was the largest single line in the book. Rule now in `SKILL.md`: reconcile every
book position against a statement before reasoning about it, and re-reconcile anything that
has never produced a confirmable fill.

**Residual risks stated.** The corrected seed is arithmetic (6582.74 − 1785.00), not a
re-derivation from statements — the rest of the seed remains unreconciled human input and could
carry the same class of error. `book_equity.csv` history before today embeds the inflated
equity; it is NOT being rewritten (those were the numbers we actually reported), so the curve
has a step down at this entry.
Reproduce: `python3 -m research.book mark`

**2026-08-02 · HUMAN HYPOTHESIS TESTED — "we're going to pop soon / a market crash of sorts."
DECISION: no action, and the reason is a probe we already ran.**

The user's claims get the same treatment as mine (`CLAUDE.md`), so this is logged as a question
asked, answered, and declined — not as a market call.

**The reading (2026-08-02, all computed, not eyeballed):**

| Measure | Value | Reads as |
|---|---|---|
| SPY vs 2y high | **−1.4%** | at the highs |
| SPY vs 50d / 200d | **+0.4% / +7.1%** | above both |
| 200d slope, 3mo | **+4.7%** | rising |
| VIX | **16.0 — 23rd percentile of 1y** | calm |
| realized vol, 21d ann. | **12.4%** | calm |
| 1m / 3m / 12m | SPY +0.2 / +3.9 / +19.5% · QQQ **−5.1** / +2.2 / +22.4% · IWM −2.7 / +4.5 / +34.1% | one soft month in tech |

**There is no distress in the tape.** QQQ's −5.1% month is the only soft spot, and breadth is fine
(IWM +34% on the year). **This is NOT evidence that a crash isn't coming** — calm-near-highs is
also precisely what every pre-crash tape looks like, and saying otherwise would be the same error
in the opposite direction.

**Why we do nothing, and it is not complacency — it is Arc 1.** We already ran this experiment.
Dip-fade, extreme-VIX-buy, disaster-buy and a **200d-slope regime proxy** were all pre-registered
and settled: every one is a REAL effect and every one is a risk-*reducer* that does not beat
buy-and-hold SPY risk-adjusted. `engine.py` carries the row `200d-slope regime proxy — FAIL`.
**"Detect the regime and act on it" is the specific hypothesis this project falsified.** Acting on
it now, on a feeling, with no pre-registration, would discard our own most expensive result.

**What survived is already deployed.** Dual momentum — SPY-like return at HALF the drawdown
(ret/|DD| 2.2×) — is the one banked usable result, and the book's SPY anchor already carries an
EMA20/50 de-risk exit. That IS the crash protocol. It is mechanical, pre-registered, and it does
not require anyone to predict anything. Note dual-mom currently signals **EEM**, not SPY; that
signal is followed on its own schedule, not because of a feeling about a crash.

**Honesty guard, stated in advance because it is the whole point of writing this down:** if the
market crashes in the next months, this entry must NOT be re-read as a missed call, and if it
rallies it must NOT be re-read as a good one. **No prediction is being made here in either
direction.** This records that a regime question was raised, that the project had already tested
the actionable version of it and failed to find an edge, and that we therefore declined to trade
it. The only thing that would change the answer is a pre-registered probe with a locked bar on
fresh out-of-sample data — which nobody has proposed and which Arc 1 says would probably fail too.

**Honest prior UNCHANGED.** Reproduce the reading:
`python3 -c "import yfinance as yf; d=yf.download(['SPY','^VIX'],period='2y',progress=False,auto_adjust=True)['Close'].dropna(how='all'); s=d['SPY'].dropna(); print(s.iloc[-1], s.rolling(200).mean().iloc[-1], d['^VIX'].dropna().iloc[-1])"`

---

**2026-08-03 · EXECUTION SLIPPAGE MEASURED — the read's quoted entry decays faster than the read
is worth, and waiting costs more than the gap.** Origin: the 08-03 read pushed
`SIZED SUGGESTION: 5 sh @ ~83.45` for DXCM; by the time the user saw it DXCM was 86.54 and he
asked whether to still buy. The 83.45 was never a live quote — it is Friday's close, the newest
complete bar a PRE-MARKET run can honestly cite (READ_LOOP "WHEN this runs").
- **Number** (all 40 taken movers with price history, reference close → the alert day's bars):
  median |gap at the open| **1.07%**, median |move by the close| **2.42%**. The intraday half is
  the bigger one — sleeping through the alert costs more than the overnight gap it was blamed on.
  Weekday split Mon 1.09% · Wed 0.63% · Fri 1.43% (N=10/13/7): **no Monday effect, this fires
  every run.** The tail is what matters: PNR gapped **−23.4%** through its alert, SMCI +13.3%,
  DLR +5.9% — on those names a point price is prose, not a level.
- **Number (band calibration):** a limit at ref×(1+band) would have filled **87.5% on session 1
  at every band from 1.0% to 2.0%** — the fill rate is FLAT — while the median entry advantage
  over a blind close-chase decays **+0.52% → +0.35% → +0.12%**. The tight end dominates on both
  axes, so it is taken. Sessions-to-fill at a 1.0% band: 88% by session 1, 90% by 2, 92% by 6;
  sessions 3–10 add exactly ONE name (SMCI, which had already run +19.8% on day 1 — a round-trip,
  not a bargain). Hence expiry = 3 sessions.
- **Rigor / why this is an execution finding and not an edge one:** N=40 over ONE month of ONE
  earnings season. The flat fill rate is the robust part; the +0.4pp entry advantage is not, and
  the 1.0%-vs-1.5% choice is thin at this N. It says nothing about whether the reads are any good
  — `bets.py` was never exposed to this, because it enters at the first complete bar strictly
  after pre-registration and is lookahead-guarded (`bets.py:82`). **Only real money was exposed.**
- **The adverse-selection caveat, stated because it cuts against us:** a 1.5% band would have
  refused SMCI (+19.8% day 1), DLR (+11.0%) and WAB (+10.0%) — the three biggest day-1 movers.
  Only 2 takes in the whole ledger have 21d forward data, so we **cannot yet say** whether
  refusing them was right. That is the question the next entry pre-registers.
- **RULE ADOPTED:** every real-money entry is a LIMIT with an expiry, computed by code
  (`research/orders.py`; band + sessions in `config.py`, the one place they live). The
  `SIZED SUGGESTION:` prose marker is deleted — it was a structured fact hidden in free text that
  no code read, and 2 of 2 issued suggestions went unexecuted with nothing noticing
  (FINDINGS 2026-08-01). An expired order is NOT re-issued at a new price.
- **Honest prior UNCHANGED: LOW.** This buys back execution cost; it does not create edge.
  Reproduce the band + the DXCM case: `python3 -m pytest research/tests/test_orders.py -q`.
  Reproduce the slippage medians + every band row: `python3 -m research.tools.slippage_audit`.

**2026-08-03 · [ORDERS #1] PRE-REGISTRATION (written BEFORE any order has been placed) — is the
entry band too tight?** The band refuses to chase, which by construction forfeits some fills. The
honest worry is adverse selection: the names that run away are exactly the ones with the most
momentum, so a discipline that systematically avoids them could be forfeiting the winners.
- **Hypothesis:** the band costs nothing real — the fills and the no-fills perform the same
  forward, so refusing to chase is free.
- **Instrument:** `orders.csv` scores EVERY resolution — filled AND expired — 21d forward vs the
  order's own benchmark, direction-aware, via `bets._score` (one scoring definition, no
  lookahead). This is `movers.py`'s take/skip logging applied to execution: a no-fill that is
  never scored makes the discipline untestable.
- **THRESHOLD, LOCKED:** at **N≥20 resolved orders**, if EXPIRED orders' median 21d excess beats
  FILLED orders' median by **more than +3pp**, the band is TOO TIGHT → widen it WITH the evidence.
  Otherwise the band is vindicated and stays. No moving this to fit the result.
- **Scope, stated so it cannot drift:** this is **DIAGNOSTIC**, not a verdict silo. It calibrates
  EXECUTION, never EDGE. It does not move the Arc 5 #7 bar (N≥30, median >+1%, beat >55%), it does
  not create a per-band goalpost, and a pass here would mean "we chase slightly better", not
  "the reads work". The project still runs on ONE verdict silo.
- **Prediction on the record:** I expect NO significant difference (band vindicated). Stating it
  so the log can catch me being wrong. Reproduce: `python3 -m research.orders show`.

**2026-08-03 · [ORDERS] LEDGER SEMANTICS — a modelled fill and a real fill are different facts, so
they get different columns.** Raised by the user the same day: he placed the DXCM limit at his
broker. That makes his row categorically different from one we merely logged — and nothing in the
schema could tell them apart.
- **The distinction:** an order row without `placed_at` is a COUNTERFACTUAL (the market traded
  through our limit; nobody was there). With `placed_at`, a fill is money that actually moved and
  needs a `book open` with the real broker fill. Conflating them invites the worst possible ledger
  error — recording a position that never existed, which is exactly the phantom-SPCX failure of
  2026-08-02, arrived at from the opposite direction.
- **Applied:** `placed_at` is its OWN column, not a phrase in `note`. That is this session's own
  rule taken seriously — the whole reason `SIZED SUGGESTION:` failed is that it hid a structured
  fact in free text. The digest now asks the right question per state: "place it at the broker"
  while unplaced, "nothing to do unless it fills" once working, and a `book open` nag ONLY on a
  fill the human actually placed. An unplaced fill degrades to a state line reading
  "would have filled — counterfactual only".
- **Cost of getting this wrong, stated:** the [ORDERS #1] band diagnostic scores fills AND expiries
  regardless of placement — that is deliberate, because the band question is about what the MARKET
  did, not about what the human did. Do not "fix" it later by filtering the diagnostic to placed
  orders only; that would shrink an already-slow N and mix an execution question with a discipline
  question. Reproduce: `python3 -m research.orders show`.
- **Honest prior UNCHANGED: LOW.** This is ledger hygiene, not edge.

**2026-08-04 · [MSG] THE DAILY MESSAGE SAID WHAT *IS*, NEVER WHAT *CHANGED* — measured, then fixed.**
Raised by the user: "how come I got 2 digests today… both having big gaps of space near the bottom".
Two separate faults behind one complaint, and the second was the real one.
- **Fault 1 (layout, shipped first):** `compose()` emitted a blank separator per section
  unconditionally, but four sections (git/stranded/feed/liveness) only ever return DO-NOW actions
  and never display lines — so **every message, every day, ended in five blank lines**. And the
  read run's whole note was prepended, burying the DO-NOW list ~15 lines down. Max consecutive
  blanks **5 → 1**; note line 1 is now the headline, its body a `📖 RUN NOTE` block at the bottom.
- **Fault 2 (the substance).** Two digests a weekday is BY DESIGN (settle 05:00 UTC + read 11:30
  UTC weekdays, one 📋 each). The defect was that they said the same thing: **69% of the two
  messages' lines were byte-identical**, ~85% once refreshed spot prices are discounted. And of
  the last 7 settle runs **only 2 changed a scored row** — the last 4 changed nothing but the
  mechanical equity-snapshot row. Nothing in the repo computed a delta; every check was an
  absolute-staleness test. The 1am message was yesterday's message with a new date.
- **The fix — anchor on git HEAD, the last state this repo PUBLISHED.** `digest._committed()`
  reads each ledger via `git show HEAD:<path>` and diffs the working tree against it. No state
  file: a cloud checkout is ephemeral, so anything the digest wrote would need committing, and the
  read run commits BEFORE it pushes — its own write could never land. The commit state IS the
  window: on settle the run's scoring is still uncommitted (diff = what this run just scored), on
  read it is already committed (diff = ∅, correct — its bets are in its own headline). Same trick
  and reason as `watchdog.last_commit_epoch`.
- **THE NUMBER — and the definition it took two wrong tries to get right.** A period's P&L is
  **`Δunrealized + Δrealized`, never `Δequity`.** Equity moves for reasons that are not
  performance: a deposit, a scope correction, a position opening or closing. Replayed on the real
  curve, 2026-08-02→08-03 (the long-realm scope removal) gives `d_equity −1950.01` but
  `d_perf −30.01` — **the −35.7% "day" that never happened is gone, and the real −$30.01 market
  move is reported instead of nothing**. `unexplained = −1920.00` is named separately as money that
  left by fiat. 08-03→08-04 gives `d_perf −0.65, clean=True, d_gap +66.88` — **ground gained on SPY
  that the message had never carried.** Reproduce: `python3 -m pytest research/tests/test_book.py -q`.
- **TWO FALSE-NUMBER BUGS THE RED-TEAM CAUGHT BEFORE THIS SHIPPED**, both in my first guard, which
  tested `d_equity == d_cash + d_unrealized` (basis untouched) and refused to print a % when it
  failed. It was wrong in **both** directions:
  - **A DEPOSIT SATISFIES THAT IDENTITY EXACTLY** — cash and equity rise together, residual 0 — so
    funding the book would have printed as a **+28.5% day with $1,000 of alpha vs SPY**. The book
    takes real deposits; this would have lied the first time the user funded it.
  - **AN ORDINARY `book open` VIOLATES IT** — cash moves against basis — so a **normal trading day
    rendered as "RESTATED — not P&L"**. That is the *next* thing that happens when the live DXCM
    order fills.
  Both vanish under `Δunrealized + Δrealized`, which is why the definition, not the guard, was the
  bug. **The lesson worth keeping: an "honesty guard" that fires on the wrong axis is not
  conservative, it is just wrong in a direction that looks responsible.**
- **A REAL BUG CAUGHT BY THE BAND'S FIRST LIVE RENDER.** It announced "1 scored (BB −33.30%)" on a
  day nothing settled. Rows were keyed by `logged_at` alone, but a batch write stamps every row in
  it with the same second — **11 timestamps in the live catalogue are shared by two bets each**
  (META/NFLX, AVGO/ON, BB/OXM…). The pairs collapsed and the survivor was compared against the
  wrong row. Identity is now `(logged_at, ticker)`, verified unique across both ledgers. A false
  settlement in a money message is exactly the class of error this project exists to not make.
- **Also shipped, each ≤5 lines:** the **−40% pool stop** [ARC5#4] now prints its LEVEL on the BOOK
  line every day and escalates a breach to a DO-NOW — the project's one circuit breaker could
  previously only fire into `cron.log` via a `book.mark` print nobody reads unattended. The BETS
  line carries the **next date the scoreboard can move on its own** (`≥2026-08-20, SMCI`) — under a
  LOW-edge prior "nothing to do" is the honest message most days, and it should come with a date.
  A working order shows its **session countdown** (`sessions_left` existed and nothing called it).
- **An unplugged money hole, now plugged.** The ORDERS section iterated `pending` + `filled` only,
  so an order that EXPIRED on our clock while carrying `placed_at` produced **no message at all** —
  our expiry is a model, the human's GTC limit at the broker is real and can fill days later into a
  position no ledger expects. New `pulled_at` column + `orders pulled` verb so the alarm is
  clearable (`cancel` only accepts `pending`). The live DXCM order is the one that will land in
    this state if it expires without filling — it was still `pending` when this was written.
- **Also fixed from the same review**, each a wrong number or an un-actionable alarm:
  - **A dead price feed was reported as a scope change.** `equity_marks` DROPS a position whose
    `_spot` returns None, so one failed fetch on CMPS produced a −$2,100 headline blamed on the
    market. The band now refuses to report at all when any spot is missing and raises a DO-NOW
    naming the feed — and says the snapshot `daily.sh` wrote minutes earlier is short too.
  - **"nothing scored" was false on mover-settlement days** — `daily.sh:19` settles movers and the
    band diffed only bets/orders/equity. A run that scored 25 mover rows said nothing changed.
  - **`next score ≥` could print a date in the PAST** — a matured-but-open (STUCK) bet was eligible
    to be "next". Now only dates ≥ today qualify.
  - **The pool-stop DO-NOW was unclearable** — a breach is permanent (equity does not climb back
    over the floor after a halt), so it would have nagged forever, which this project forbids
    [FINDINGS 2026-08-02]. It is now gated on risk still being ON: following the instruction
    (flattening to cash) silences it. The LEVEL still shows every day; only the ASK is conditional.
  - **The stale-limit alarm was silenced by any holding in that ticker** — exactly the case where a
    live GTC limit DOUBLES a position. The book no longer suppresses it; only `orders pulled` does.
    `cancelled` rows count too: calling an order off in OUR ledger does nothing at his broker.
- **Red-team / residual risks.** Reviewed by a different model per the standing rule; the delta
  ANCHOR itself survived (fresh checkout, detached HEAD, twice-in-a-day, and a `settle-backup`
  strand all behave — a strand widens the window, which is correct for "since last PUBLISHED").
  The anchor is the last COMMIT, not the last MESSAGE; they coincide because both routines commit
  within minutes of pushing, and a stranded push makes the next band REPEAT a delta rather than
  skip one. `_row_id` is blind to row DELETIONS by construction. `_marks()` is `lru_cache`d for the
  process, which is one CLI invocation. **Not built:** collapsing unchanged sections — the marks
  genuinely move between runs, so "unchanged" is usually false. **PRE-REGISTERED:** re-measure the
  69% overlap on the next weekday's two real pushes; **bar ≤55%**. Miss it and collapse gets built
  with evidence.
- **Honest prior UNCHANGED: LOW.** This is the message layer, not edge. It converts and protects;
  it does not predict. Tests **113 → 147**. Reproduce: `python3 -m research.digest`.

**2026-08-04 · [ARC 5 #7] PRE-SETTLEMENT CAVEATS — logged BEFORE the first core settlements land
(~2026-08-20), while the pooled verdict is unseen. These scope the INTERPRETATION; no bar moves.**
Origin: a full-project review (with user) asked whether our own constraints are choking the goal.
Three caveats on the pooled general verdict, written now so they cannot be discovered conveniently
after the number exists:
- **(a) Correlated N.** 21 of the 53 catalogue bets carry `post-earnings-drift` — **all 21 LONG**,
  logged 2026-06-28→2026-08-03, i.e. one scenario type in ONE earnings season, mostly vs sector
  ETFs. The Wilcoxon at the [ARC 5 #7] bar treats settled bets as independent draws; same-season
  same-mechanism same-direction bets are partly ONE macro draw (a drift-regime shift moves them
  together). **Effective N < row count, in both directions** — a pass could be one season's regime,
  a fail could be one season's unwind. The bar (N≥30, median >+1%, beat >55%, α≈.017) is UNTOUCHED;
  this entry pins how the result must be read, and the per-tag/per-direction diagnostics are the
  instrument for seeing it.
- **(b) Arena scoping.** The candidate denominator is (as of this writing) exclusively S&P 500
  movers — the arena Arc 2's own banked conclusion calls crowded/arbitraged ("~90% of active pros
  LOSE to SPY there"). A FAIL at N≥30 therefore means **"no edge reading large-cap earnings-season
  movers on free data"** — NOT "reading has no edge." Symmetrically, a PASS is a pass in the
  hardest arena and should not be discounted by this caveat. [ARC 5 #11] below is the response.
- **(c) α rationale lapsed, bar retained.** α≈.017 was Bonferroni over TWO verdict silos; Arc 3
  closed 2026-08-02, so the arithmetic behind it is stale. The stricter α is **RETAINED
  deliberately** — a significance bar is never loosened mid-flight, whatever happens to its
  original justification.
- **Honest prior UNCHANGED: LOW.** Reproduce the inputs: `python3 -m research.bets show` (tag and
  direction counts) · `python3 -m research.engine` (diagnostic decompositions).

**2026-08-04 · [ARC 5 #11] PRE-REGISTRATION (no data peeked — written before any tail candidate
exists) — the denominator WIDENS: an S&P MidCap 400 + SmallCap 600 TAIL cohort joins the mover
scan.** Why: caveat (b) above. Arc 2 concluded the reachable inefficiency lives in the
under-covered tail, and Arc 3 — the arm that was aimed there — closed on calendar arithmetic, not
falsification. Since 2026-08-02 the project's ONLY candidate stream has been the arbitraged
arena. This change points part of the scan where our own evidence says edge could survive.
- **What changes:** `movers scan` adds a SECOND cohort — the top `movers.TAIL_TOP_N` daily movers
  (same |5d move| ranking, same PCT_STRONG floor) drawn from committed S&P 400 + S&P 600
  constituent caches (~1,000 names) — beside the UNTOUCHED S&P 500 top-`movers.TOP_N` cohort
  (denominator continuity: the existing stream keeps accruing unmodified). Every ledger row gains
  a `universe` column (`sp500`|`tail`); rows written before this entry are `sp500` by construction.
- **What is DIAGNOSTIC:** `universe` decomposes the pooled [ARC 5 #7] verdict and the [ARC 5 #9]
  take/skip contrast exactly like `pattern_tag` / `horizon_d` / direction — **NEVER a per-universe
  goalpost** [Arc 5 #8]. It cannot pass or fail the project. A tail-vs-sp500 asymmetry at
  diagnostic N motivates a NEW pre-registered probe, never a verdict change.
- **What is FIXED:** the pooled bar, the [ARC 5 #9] skip threshold AND its SPY ruler — the skip
  verdict continues on the POOLED skip set (this entry records, dated, that the population under
  that threshold widened mid-accrual; the universe split keeps it decomposable). The read bar is
  unchanged and HIGHER in practice for tail names: mechanism NAMED or SKIP, and liquidity/spread
  checked before any sized alert (small-cap frictions eat small edges).
- **Explicitly forbidden, so it can be checked later:** tilting generation toward the tail to
  chase the under-covered story. The scan quotas are fixed in `movers.py`; the read decides each
  candidate on its own evidence.
- **Deferred (phase 2, needs evidence this plumbing works):** anything beyond S&P 1500 — the true
  micro-cap tail has no clean free constituent list and a 3× fetch is untested; widen again only
  after the tail cohort has run clean for weeks.
- **Reproduce (cache build):** one-off local fetch of the Wikipedia constituent lists
  (`List_of_S%26P_400_companies`, `List_of_S%26P_600_companies`, first table, `Symbol` column),
  normalized like `universe.sp500()` (strip, `.`→`-`, upper) → `research/data/sp400_current.csv`
  / `sp600_current.csv` (single `Symbol` column, committed; the cloud path reads caches only).
  Verification at build: counts within [395,405]/[595,610], zero duplicates, zero overlap with
  each other or with `sp500_current.csv`.
- **Honest prior UNCHANGED: LOW.** A wider denominator buys the right QUESTION, not edge.

**2026-08-04 · [ops] PARTIAL-BAR GUARD + FEED TRUTH (`last_bar` / coverage) — instrumentation,
never evidence.** The incident: on 2026-08-04 the pre-market read logged **0 new movers** because
the price feed had not advanced past 07-31 — while `_feed_status.json` showed `last_ok:
2026-08-04`. "ok" measured the PIPE (a fetch returned), not the WATER (fresh bars). Consequence,
stated because it is permanent: **the 2026-08-03 session's mover cohort was never logged** — the
scan only reads the newest bar, so that day is a hole in the denominator (partially self-healed
by the 5-day move window; any one-day spike that faded is missed).
- **Fixes (pre-registered here, before any run uses them):** (1) `movers.scan` gains a
  completed-sessions-only filter (the same gate as `bets._score` / `orders._complete`, injectable
  `today`) — the BACKLOG partial-bar item's trigger ("before anyone runs scan by hand") fired
  during this session's verification plan. (2) `feedstatus.record` gains `last_bar` (newest
  completed session actually used) + `n_ok`/`n_total` (fetch coverage), and the digest escalates
  a stale bar or thin coverage to a DO-NOW **even when `last_ok` is fresh**. Thresholds live in
  `digest.py` (`FEED_BAR_STALE_D`, `FEED_COVERAGE_MIN`) — named here once, values never restated
  in docs. Known false positive, accepted and named in the alarm text: the first weekday after a
  market holiday (~9/yr, self-clears next day).
- **Semantics change, disclosed:** feed `ok` becomes "bars were returned", not "movers were
  found" — a genuinely quiet day is no longer indistinguishable from an outage (that conflation
  was itself a latent false-alarm path).
- **This creates no edge and changes no bar. Honest prior UNCHANGED: LOW.**

**2026-08-04 · BOOK + GENERATION DECISIONS (with user) — the NIO claim gets scored, exit plans
get a column, and generation gets a diversity ceiling.**
- **(a) NIO "likely to flip" → USER bet.** The user's stated reason for holding is bottom-avoidance
  (consistent with the banked exit-into-strength rule); his added claim — "likely to flip" — is a
  hypothesis with, in his own words, no clear evidence. Per the standing accountability rule his
  claims get the same test as the model's: pre-registered as a scored bet (long 63d vs SPY,
  `--tag=capitulation-reversal`), SPCX-USER-bet precedent. It also closes NIO's twin-rule gap
  (the book lot had no open bet twin). Scored either way; n=1 will decide nothing.
- **(b) Exit plans become STRUCTURED.** The number that forced it: NIO's exit plan ("limit-sell
  into strength 4.85–5.15") lived in thesis PROSE; **NIO's high since 7/24 was 4.94 — inside the
  band — and nothing noticed**, because the digest reads only `stop`. Third occurrence of the
  structured-fact-in-prose class (after `SIZED SUGGESTION` and the 🔒 flag). Fix: the book's
  dead `target` column goes live (`book target TICKER PRICE`), the digest renders it and
  escalates a touched exit band to a DO-NOW ("verify the sell limit is working at the broker").
  Sell-side ORDER machinery stays deliberately unbuilt (gate unchanged: ~10 realized exits).
- **(c) HARD tag ceiling — ≤3 takes per `pattern_tag` per read run.** Caveat (a) above made
  operational, the same way the fast-sleeve mandate was [2026-08-01(c)]: a 4th+ same-tag bet in
  one run needs one line naming why it is not the same trade again. **Generation cadence only —
  no bar, threshold, or horizon moves.** The soft form was rejected on evidence: the fast sleeve
  produced ONE bet in five weeks as a soft rule.
- **Honest prior UNCHANGED: LOW.** Reproduce: `python3 -m research.book show` ·
  `python3 -m research.bets show` · `python3 -m research.digest`.

**2026-08-04 · [ARC 5 #2b] PRE-REGISTRATION (written while the checkpoint number cannot be
seen — 6 settled vs an N≥20 gate) — the paid-data checkpoint gets a FAIL branch.**
**Why.** [ARC 5 #2] fires only on a PASS. The same-day caveat (b) above establishes that a FAIL
at N≥20 is SCOPED — "no edge reading large-cap earnings movers on free data" — yet as written a
FAIL leads nowhere until the 2027-06-30 kill date: the one decision that could test the
remaining arena (paid survivorship-clean small-cap + filings data, Arc 2's "the data moat IS
the moat") would be made by drift, or never. A trigger that can only fire in one direction is
half an instrument.
- **RULE, LOCKED NOW.** At the FIRST settle run where the pooled general catalogue reaches
  **N≥20 settled** (expected ~late Sep 2026; the settle run's N is the clock, never the
  calendar):
  - **PASS per [ARC 5 #2]** (median excess >0 AND beat >55%): the spend trigger fires exactly
    as registered. Nothing here amends it.
  - **OTHERWISE (fail or inconclusive):** a DECISION POINT goes to the user in the next
    session, carrying the pooled numbers, the universe/tag/direction/horizon diagnostics, and
    the 2026-08-04 caveats — with exactly THREE pre-named options, so the choice set cannot be
    invented after seeing the number: **(a)** a CAPPED exploration spend (~$50–100/mo,
    Sharadar/Norgate-class survivorship-clean prices + a filings-grade feed) — if chosen, it
    gets its OWN fresh pre-registration (scope, bar, kill-criterion) BEFORE any money moves;
    **(b)** ride free data to the [ARC 5 #1] kill date 2027-06-30; **(c)** stop the forward
    track early and log the NULL.
- **What is pre-committed is the WHEN and the INPUTS, not the outcome.** The decision is the
  user's; this entry only guarantees it happens on schedule, with the evidence assembled, and
  from a menu written before anyone knew the number.
- **Guards:** the [ARC 5 #2] PASS trigger, every bar, and the kill date are UNTOUCHED. This
  cannot cause a spend by itself. **Honest prior UNCHANGED: LOW.**
  Reproduce the clock: `python3 -m research.engine` (settled N on the pooled line).

**2026-08-04 · [ORDERS #2] DECISION (with user) — auto-sizing gets a per-trade RISK UNIT.**
`orders place` auto-sizing was `floor(free cash / limit)` — ALL free cash into any name,
regardless of stop distance. Now: **shares = min(cash cap, floor(RISK_PCT × book equity /
per-share stop distance))** — the position is sized so the stop being hit costs a fixed
fraction of equity, then capped by free cash as before. Constant lives in `config.py` (the one
place); docs point at it, never restate it.
- **Why now:** the [ARC 5 #11] tail cohort reaches the order path with gappier, wider-stop
  names, and the one execution number we own (the −23.4% PNR gap tail, FINDINGS 2026-08-03)
  says stop distance is the risk that matters. A wide-stop name now sizes smaller
  automatically; a tight-stop name stays cash-capped, exactly as before.
- **Value choice, stated:** 2% — the aggressive end of the standard 1–2% band, consistent with
  the loosened-harness phase [ARC 5 #6]; the −40% pool stop stays the only other brake. Shorts
  still require explicit `--shares` (collateral is a broker question we do not model).
- **Scope:** EXECUTION, never edge. No bar moves; [ORDERS #1] is unaffected (it scores fills
  and expiries regardless of size). Cash-cap-first ordering means a cash refusal never fetches
  marks. **Honest prior UNCHANGED: LOW.**
  Reproduce: `python3 -m pytest research/tests/test_orders.py -q`.

**2026-08-05 · [MSG] PRE-REGISTERED RE-MEASURE: 56% vs ≤55% — MISS; fail branch fired (read
push went `--slim`).** The 08-04b bar was measured on the day's two REAL pushes with the exact
pre-registered command: **20 of 36 read-message lines byte-identical = 56%** (down from 69%).
The unflattered companion number: **87% of the settle message (20/23 lines) reappeared verbatim
in the read one** — the improvement was mostly denominator inflation (the read message grew a
RUN NOTE), not less echo. As pre-registered, the miss promoted "collapse unchanged sections"
from CUT to BUILD: the read push is now `digest --slim` (📖 band + DO-NOW + book header/cash +
one-liners + run note; no position rows, no ORDERS block, no 📋 banner — settle's 📋 stays the
day's one full photo). Deterministic, not diff-based: the read run cannot change book/orders,
so for it those sections are unchanged BY CONSTRUCTION; the marks-move objection to a vs-HEAD
diff stands. **Caveat, stated:** local same-instant sims of the new pair read 58-62%, inflated
by artifacts a real 6h-apart pair cannot have (identical band/marks/spots) — the FIRST real
full-vs-slim pair is the verdict (expect ~40-50%; if IT misses, next candidate is the shared
blank-line skeleton + contract lines — measure, then decide). Same day, same thread: a
"✅ heartbeat: digest pushed" arrived in violation of the one-message contract (the prompt
already forbade it — the agent improvised); prohibition now explicit on every surface, and
READ_LOOP's title no longer contains the word "heartbeat". OPS, never edge — no bar moves,
prior UNCHANGED: LOW.
  Reproduce: `python3 -m pytest research/tests/test_digest.py -q` (slim tests) + the overlap
  command in BACKLOG's WATCH block on the next real pair.

**2026-08-05 · BOOK DECISION (with user) — external capital FROZEN until two gates pass.**
No new outside cash enters the book until the long-term realm's emergency fund is full AND a
pre-registered PASS exists — the owner's bar, his words: "serious heroic alpha." Supersedes
"user adding more" [2026-07-06]; the 2026-07-10 in-book free-cash allocation rule is UNTOUCHED
(realized cash inside the book stays deployable). Book runs to its existing verdicts unchanged;
book-capital DISPOSITION goes on the [ARC 5 #2b] decision point's agenda — the three-option
menu itself UNTOUCHED, registered while the checkpoint number is still unseen (6 settled vs
N≥20). Context, for the record: the book's realized losses to date are ALL on positions the
owner bought before this system existed (inherited, cleanup called) — the freeze is capital
sequencing, not a verdict on the reads; the reads' verdict is the pooled clock. The staged
future ([EDGE-SYSTEM], BACKLOG) waits on the same two gates. **Honest prior UNCHANGED: LOW.**
  Reproduce: `python3 -m research.book show`.

**2026-08-06 · [MSG] SLIM RESHAPED ON USER UTILITY — the ≤55% overlap bar's shape is SUPERSEDED,
stated openly, and the re-measure is RE-PRE-REGISTERED.** The 08-05 slim shape optimized the
overlap number and failed the reader the next morning: the 📖 nagged a DXCM order while hiding
the DXCM position line — "where do I stand?" had no answer in the one message the human reads
(his words: "didn't help me at all see where I'm standing in that trade"). User chose the fuller
shape: slim KEEPS every position row, upgraded with $ P&L + stop/target distance, and DROPS what
settle's 📋 owns (💰 band, 🎯/📡 one-liners, ORDERS block, 📋 banner). This is a deliberate,
named supersession of the 08-04b bar's object — utility beat the metric; NOT a quiet goalpost
move. **Pre-registered:** measure the FIRST real 📋/📖 pair after this lands with the exact
overlap command in BACKLOG's WATCH block and log the number whatever it is; no target bar this
time — the number is diagnostic context, the shape's verdict is the reader's. OPS, never edge —
no bar moves, prior UNCHANGED: LOW.
  Reproduce: `python3 -m pytest research/tests/test_digest.py -q` (slim tests) +
  `python3 -m research.digest --slim "📖 preview"`.

**2026-08-06 · [OPS] TRIPLE-PUSH + A SECOND STRANDED 📋 + A NAG ON A BOOKED FILL — one morning,
four failures, mechanisms found, fixed.** THREE messages hit the read window (11:41–11:43 UTC)
vs the contracted one: the legit 📖, a near-copy suffixed "(delivery check — see prior full
note)", and a bare "Probe". Neither string exists anywhere in the repo — the cloud read agent
improvised both extra sends. The bait: `digest --notify` exited 1 on an AMBIGUOUS send (message
possibly delivered, response lost), and the routine's out-of-git prompt still named
`research.notify` for the push + carried a "retry once" rule — BOTH pre-registered open as
BACKLOG cloud-runs FINDINGS 2/3. Fix: tri-state delivery verdict printed by the digest
(`PUSH DELIVERED` / `REJECTED, nothing sent` / `UNCONFIRMED — do NOT re-send`); a re-send is
licensed ONLY by REJECTED; `research.notify` documented HUMANS-ONLY everywhere it is named.
Separately, settle's 📋 died in transport the SECOND consecutive night (user confirmed nothing
overnight; the run itself committed at 05:08 UTC = 430dc09) — invisible to the watchdog, which
watches COMMITS. Fix: every push stamps `research/data/push_log.csv` (committed with ledgers);
the next delivered message raises a DO-NOW when the last due settle push lacks a DELIVERED
stamp. Third failure: DXCM's broker fill was booked 08-05 but `orders.csv` stayed `pending` —
the 📖 nagged "WORKING at broker" against a position that EXISTS, and `place()` double-counted
the $421.40 as committed against $6.41 cash, silently blocking ALL long sizing (the 08-06 read
run could not have placed any order). `resolve()` replay says filled @84.28 on 08-05 — the
logic was right; the 08-06 settle failed to APPLY it (root cause open: the silent
`bars_after→[]` feed-flake path, or the settle prompt not running `daily.sh` verbatim — the
prompt read is the next action). Fixes: row resolved + committed; `orders.booked()` flips the
pending nag to a one-line FYI and frees the committed cash when the fill is already in the
book; `orders check` goes LOUD (exit 1 → heartbeat) on zero complete bars where ≥2 weekday
sessions have elapsed. **Decided AGAINST a manual `orders filled` command:** the resolver is
provably correct — the failure was not running/feeding it (now loud); the human-facing gap
closes at `book open` via booked(); and a second hand-writer into ledger status invites
recording modelled fills as real (the exact class `placed_at` exists to prevent). Caveats,
stated: booked() accepts an unrelated same-name/direction lot opened after the order (3-position
book, accepted; the stale-GTC alarm stays deliberately ungated); the empty-bars alarm
false-positives on back-to-back holidays (~9/yr, named in its text, self-clears); the settle
transport root cause is UNPROVEN until the routine prompt/env is read. OPS, never edge — no bar
moves, prior UNCHANGED: LOW.
  Reproduce: `python3 -m pytest research/tests -q` (189) · `python3 -m research.orders show`
  (DXCM FILLED @ 84.28 on 2026-08-05) · the [MSG] entry above for the shape change.

**2026-08-07 · [CASE] SPCX UNLOCK-RELIEF — the telegraphed-supply falsifier fired; pattern
registered with a pre-registered trigger, NO scored bet yet.** First unlock day (08-06, ~911M
shares newly eligible) closed +6.1% on record volume; next session +15.8% to 133.11 (~134 AH) —
two-day +23%, within ~1% of the $135 level the owner's 08-05 long-realm analysis pre-registered
as its "supply absorbed → revise up" falsifier. Read: anticipatory selling (~50% off the high
into the year's most-telegraphed unlock) exhausted the sellers; the unlock-day up-close on
record volume is direct low-sell-through evidence. Confounds, stated: Terafab phase-1 outline +
reported Cursor acquisition + a Morgan Stanley entry note + short-covering (~219M SI) all landed
08-07 — N=1, catalyst-confounded; the Musk-holder-loyalty mechanism is plausible, NOT proven.
Registered as `unlock-relief` in `research/cases/SPCX.md` with the tell-stack pre-registered
BEFORE the next instance: hard-dated unlock ≥10% of float + price ≥30% under its high going in +
unlock session closes flat/up on above-average volume → LONG 21d vs SPY, scored in `bets.py`
the day it fires. SPCX itself is NEVER the scored leg (standing conflict-of-interest exclusion,
2026-08-02 rule) — and a +23%-later entry would be a chase, the exact thing the trigger exists to
prevent. Long-realm consequences recorded in the private long-realm repo, not here. No bar moves,
prior UNCHANGED: LOW.
  Reproduce: `research/cases/SPCX.md` (the tell-stack) · mover scan = the watchlist.

**2026-08-08 · [OPS] CALCIFICATION AUDIT #1 — four blind micro-independent reviewers re-derived
the classification of every standing rule in CLAUDE.md, SKILL.md, and the session-memory layer;
the memory layer failed hardest.** Method (per the owner-amended independence rule 2026-08-07):
3 fresh-context Fable agents (statistical / regime-skeptic / neutral lenses) + 1 Opus cross-model
control, each blind to the generator's conclusions and to each other; disagreement = the signal.
CONSENSUS 4/4: the live-book memory's paper-book frame was wrong on EVERY load-bearing fact
(paper→REAL, stale cash figure, HELP/XRP shown open→long closed, SPCX in book→moved to the
long-term realm, 35% cap→lifted) — memories REWRITTEN same-day to hold only non-derivable facts
and point at `book show` (memories now obey the docs' anti-drift rule). CONSENSUS 3–4/4 —
EMPIRICAL rules wearing law's clothing, no live kill-path: exit-into-strength (n≈2, both
bull-tape bounces, currently steering real money); the EMA-cross permanent ban (one 12-name
bull-window test); free+famous=arbitraged (N=3); utilization-is-not-the-bottleneck (2 correlated
probes, contradicted by the live idle-cash posture); dual momentum as "the one banked usable
result" (static backtest that TIED its own pre-registered Sharpe bar yet was promoted; no
forward re-test while it sits in the live digest path). UNIQUE CATCHES — the cross-model control
earned its seat with items no Fable lens produced: (a) the [ORDERS #1] N≥20 bar may be
UNREACHABLE at the current cash/order rate — the Arc-3 decorative-bar death replaying; (b) the
standing "LLM out of the decision path" rule contradicts READ_LOOP being an LLM read in the
decision path — the rule's real meaning (no LLM in DETERMINISTIC triggers/settles; the read IS
the hypothesis under test) is nowhere stated; (c) the open SPCX 174d bet's thesis text cites the
phantom "17-sh locked lot" (bet STANDS — pre-registered — the annotation is false). OPEN
CONTRADICTION PAIRS for the owner: don't-lose-it stance vs the size-aggressively memory;
"propose, wait for approval" vs drive-autonomously; SKILL.md/ARCHITECTURE.md still carry the
superseded different-model review rule. Anti-drift violations: dated movers snapshot hardcoded
in CLAUDE.md; "n=6" hardcoded in SKILL.md; book.csv's NIO note still narrates the dead June
thesis. Doc fixes NOT applied — smallest-diff list awaits owner approval. OPS, never edge — no
bar moves, prior UNCHANGED: LOW.
  Reproduce: re-run the 4-blind-reviewer protocol on the same files; the disagreement list is
  the output. Cadence: quarterly, or on regime flip, or when a rule starts steering real money.

**2026-08-08 · [OPS] AUDIT #1 FIXES APPLIED + TWO RECONCILIATIONS (owner-delegated) + TWO
INCIDENTAL DISCOVERIES.** Applied, 16 smallest-diffs: the five flagged SKILL lore rules
stamped/demoted — free+famous (N=3; re-test on regime flip or [ARC 5 #2] unlock), risk-reducers
(dated bull-sample summary; re-rank on regime flip), utilization (N=2 hypothesis; live posture
contradicts it, unscored), EMA ban (standing default, not permanent law), exit-into-strength
(DEMOTED to hypothesis with a pre-registered kill-path: repeat the bottom-tick audit at N≥10
realized book exits, limit-into-strength vs market cuts; no advantage → rule dies; never
overrides a stop); dual momentum restated honestly (TIED its own Sharpe bar — least-dead
default; re-validate walk-forward before sizing up); the amended independence rule propagated
to SKILL step 3 + ARCHITECTURE; the LLM rule's real meaning stated (deterministic path stays
model-free; the READ layer IS the hypothesis under test); the movers 08-01 snapshot
genericized; [ORDERS #1] reachability deadline pre-registered (if N<20 by 2026-12-31, declare
the bar UNREACHABLE and re-scope openly — declare, don't decorate); NIO book note now leads
with live status (the dead thesis was the first thing `book show` printed); the SPCX user bet's
phantom "17-sh hedge" corrected (bet STANDS, unhedged, pure pre-registered call).
RECONCILIATION 1 — sizing: ruin-bounded at the POOL (−40% stop, inflows frozen),
conviction-sized at the POSITION [ARC 5 #6]; supersedes the pre-#6 "don't-lose-it + cheap
beta + capped experiments" phrasing — bounded-loss aggressive exploration maximizes
information per dollar, the fastest honest route to the alpha verdict. RECONCILIATION 2 —
approval lanes: RUNNING the system (reads, settles, scoring, logging, upkeep, committing
evidence) = autonomous, report after; CHANGING the system (code, rules, bars, contracts) or
MOVING real money = propose first (the broker step is human-gated by construction).
DISCOVERED while verifying: (a) 4 digest tests fail on the CLEAN tree — test_digest composes
against LIVE push_log/ledger state instead of fixtures, so any real alarm breaks the suite;
fix = test isolation, PROPOSED not applied (CHANGING lane); (b) the alarm leaking into those
tests is REAL — push_log has NO row for the 2026-08-07 SETTLE (ledger commit f2fba61 exists;
read 08-07 DELIVERED; settle stamp ABSENT): the commit-without-push transport class again;
per the 08-06 rule an absent stamp does NOT license a re-send (double-post risk) — the next
delivered digest raises the DO-NOW; human checks the settle routine's cron.log + Telegram env.
OPS, never edge — no bar moves, prior UNCHANGED: LOW.
  Reproduce: `git show` this commit · `python3 -m pytest research/tests -q` (4 pre-existing
  isolation failures) · `tail research/data/push_log.csv`.

**2026-08-08 · [OPS] SETTLE-STRAND POST-MORTEM (08-07 night) — root cause nailed to the
dependency import chain by elimination; test isolation fixed (189 pass).** Signature: trigger
fired 22:35:43Z, ledger commit 22:36:37Z (book_equity ONLY — a healthy settle commit also
carries the push_log stamp), no 📋, no 🚨, no push_log row. The commit message is
push_ledgers.sh-generated → daily.sh ran END TO END → digest --notify died BEFORE its stamp
line AND heartbeat died after it. The one shared component: `from research import notify` →
`config` → `from dotenv import load_dotenv` — the ONLY non-stdlib import on both paths, and
requirements.txt has documented this exact death since 2026-07-27 ("without this every
Telegram push dies on import and the run reports success anyway"). Elimination check: every
step that provably ran (bets settle, book snapshot) avoids that chain; every silent step
(movers/orders — into $FAILS unseen — digest, heartbeat) sits on it. Compose runs clean
locally on the same data; nothing installs deps in daily.sh or the settle/read prompts (only
the watchdog prompt pip-installs). Conclusion: a COLD cloud container without python-dotenv
kills both messengers instantly (54s run time fits import-death, not network death), while
warm containers deliver — matching the strand-some-nights-deliver-others pattern (08-04/05,
08-05/06, now 08-07). CONFIRMATION pending (stated honestly): the container state is
unprovable from here — the settle routine's own run report on claude.ai (prompt requires
quoting the verdict line) will show the traceback; cron.log died with the container. FIX
PROPOSED, not yet applied (awaits owner): (1) daily.sh dependency guard before step 1 —
`python3 -c "import dotenv, requests" || pip install -q -r requirements.txt`; (2) digest run()
wraps the notify block in try/except so an import/transport death still stamps REJECTED
(nothing sent — true for an import death, safe-to-resend semantics hold) and prints the
verdict line instead of a bare traceback. APPLIED (pre-approved): test_digest isolation — the
autouse fixture now stubs `_pushlog_section` like every other environment section (the live
08-07 strand alarm had broken 4 compose tests; the dedicated test uses _REAL_PUSHLOG against
tmp_path). 189/189 pass. OPS, never edge — no bar moves, prior UNCHANGED: LOW.
  Reproduce: `python3 -m pytest research/tests -q` · `git show f2fba61 --stat` vs
  `git show a75901c --stat` (the missing-stamp signature) · grep dotenv requirements.txt.

**2026-08-08 · [OPS] STRAND FIX APPLIED (the two diffs from the post-mortem above, owner "go").**
daily.sh now guards deps before step 1 (probe dotenv/requests/yfinance/pandas → quiet
`pip install -r requirements.txt` on a cold container); digest run() survives a notify death —
import failure stamps REJECTED (nothing sent, safe to re-send), a RAISING send() stamps
UNCONFIRMED (may be post-request, never re-send) — and always prints the verdict line. New
test encodes the incident (a raising send → UNCONFIRMED stamp + exit 1); 190/190 pass.
OUT-OF-SAMPLE TEST, pre-registered: the next settle runs (22:30 UTC nightly) — a DELIVERED
stamp confirms; a third stamp-less strand FALSIFIES the cold-container theory and points at
the environment itself. Residual, stated: the READ routine does not run daily.sh, so a cold
container still kills its pipeline steps early — its digest now at least stamps + prints, and
the run report shows the death; adding the same guard to READ_LOOP step 0 is proposed,
unapplied. OPS, never edge — prior UNCHANGED: LOW.
  Reproduce: `python3 -m pytest research/tests -q` (190) · `bash -n scripts/daily.sh` ·
  next settle's push_log row.

**2026-08-08 · [OPS] STRAND ROOT CAUSE CONFIRMED BY THE RUN REPORT — and the window hypothesis's
pre-registered falsifier FIRED.** The settle routine's own report (owner-retrieved): verbatim
`ModuleNotFoundError: No module named 'dotenv'` at notify.py:22; killed movers settle, orders
check, digest --notify, heartbeat; bets settle + book mark/snapshot ran; git push succeeded;
"DELIVERY VERDICT: none printed"; "ZERO messages sent" — the exact elimination pattern the
post-mortem predicted. Sha reconciliation makes it stronger: the report's `750fcde` is the
08-07 05:09Z OLD-schedule settle; `f2fba61` (22:35Z, NEW schedule) left the identical
stamp-less signature — BOTH 08-07 settles died the same death, cold-container lottery twice in
one day. Consequence: the 2026-08-07 schedule move (05:00→22:30, "third stranded push") treated
the WRONG variable — the pre-registered falsifier ("a 22:30 strand kills the window
hypothesis") fired on its first trial; dependency presence, not time-of-day, was the real
variable. The routine report's "Action required: install python-dotenv" is satisfied by the
already-shipped daily.sh guard (self-healing per run — no manual env mutation to keep in sync).
The report also notes the sanctioned retry was correctly NOT taken ("sanctioned by letter but
pointless by fact" — the agent reasoned right). OOS test unchanged: tonight's 22:30 stamp.
READ_LOOP step-0 guard still proposed, unapplied. OPS, never edge — prior UNCHANGED: LOW.
  Reproduce: the settle routine's 08-07 run reports (claude.ai) · `git show 750fcde f2fba61
  --stat` · push_log.csv (no 08-07 settle row).

**2026-08-09 · [OPS] STRAND FIX OOS: PASSED 2/2.** The pre-registered test (08-08 entry: "the
next settle's push_log stamp") resolved: the 08-08 AND 08-09 settles both stamped DELIVERED —
the first two cold-container-exposed settles after the daily.sh deps guard shipped. Friday's
read (08-07) also DELIVERED, and READ_LOOP step 0 now carries the same guard (applied later
that same day in the handoff commit e6176da, superseding "proposed, unapplied" above). Cold-container theory stands; the window
hypothesis stays falsified. Residual, stated: the guard runs per-run, so the failure mode
shifts from missing deps to a pip install failing inside a run — that death would still stamp
REJECTED and be visible. OPS, never edge — prior UNCHANGED: LOW.
  Reproduce: `tail -4 research/data/push_log.csv` (08-08 + 08-09 settle DELIVERED).

**2026-08-09 · [OPS] MOVERS "STALE FEED" DO-NOWS (08-08 + 08-09, both cohorts) = WEEKEND FALSE
POSITIVE, not a dead feed.** Feed is healthy: last_ok 08-07, coverage 503/503 (sp500) and
1002/1003 (tail). The bar-lag check (digest.py `_feed_section`) computes
`_busdays(last_bar, today)` vs FEED_BAR_STALE_D=1 — but the scan runs pre-market weekdays, so
on Sat/Sun the newest possible bar is Thursday's and `busday_count(Thu→Sat/Sun)=2` fires EVERY
weekend by construction (first live weekend: `last_bar` field shipped 08-04). Self-clears
Monday when the read advances bars to Friday. Fix PROPOSED, unapplied: measure lag against
last_ok (bars the last SUCCESSFUL scan should have seen) instead of today — steady state = 1
every day incl. weekends; a live-scan/frozen-bars outage still grows; a dead scan is already
FEED_STALE_D's alarm; a holiday still fires once with the existing caveat. OPS, never edge —
prior UNCHANGED: LOW.
  Reproduce: `python3 -c "import numpy as np; print(np.busday_count('2026-08-06','2026-08-09'))"`
  → 2 · research/data/_feed_status.json · digest.py FEED_BAR_STALE_D.

**2026-08-09 · [OPS] THE DXCM NAG WAS THE DIGEST'S BUG, NOT A LEDGER GAP — both digest fixes
APPLIED (owner "go").** The "DXCM order FILLED @ 84.28 … but no book position" DO-NOW (every
settle since 08-07; the owner corrected it three times, finally with the broker screenshot:
sold 5 @ 82.575 on 08-07 to fund DVA, plus the 1-sh SPCX @ 119.74 whose proceeds stay OUTSIDE
the book per the inflow freeze) was a false alarm against a ledger that was ALREADY RIGHT:
book.csv holds the full round trip (open 08-05 @ 84.28 → closed 08-07 @ 82.575, −$8.52) and
cash reconciles to the penny ($6.41 → +$412.88 → −$356.00 → $63.29). Root cause: the fills
matcher checked OPEN lots only, and a `filled` order row is terminal (`pulled` matches
expired/cancelled only) — so the moment the position CLOSED, the nag became PERMANENT: the
unclearable-alarm class this repo forbids. An earlier session then compounded it by trusting
the alarm over the ledger ("likely never filled"). Fix: a settled lot, open OR closed, matching
the order's fill signature (`orders.booked()`) now clears it; old unrelated lots still nag.
Weekend feed fix applied exactly as pre-registered above (lag vs `last_ok`, threshold
unchanged). Tests encode both incidents (frozen-Sunday date + closed-round-trip w/ old-lot
negative + 2-weekday threshold case); 193/193 pass. Live compose 08-09 post-fix: DO-NOW EMPTY,
DVA "filled + BOOKED" FYI intact. OPS, never edge — prior UNCHANGED: LOW.
  Reproduce: `python3 -m pytest research/tests -q` · `python3 -m research.digest` (DO-NOW
  empty) · `git show 0f81228` + BACKLOG 08-07 rotation entry (the fill was always booked).

**2026-08-09 · [OPS] RED-TEAM OF THE DAY'S FIXES (two blind micro-reviews + one cross-model
control, per the independence rule) — the reviews CONVERGED on two real regressions; both
addressed.** (1) Lag-vs-last_ok is structurally BLIND to a dead scan: last_ok and last_bar
freeze together, so the bar alarm can never fire and detection fell to FEED_STALE_D=3 — up to
4 weekdays of all-clear DO-NOWs while the read leg is dead, and NOTHING else watches that leg
(push_log alarms are settle-only; the watchdog watches settle's commits). FIX: FEED_STALE_D
3→1 — escalation on the 2nd missed weekday, weekends verified silent (busdays Fri→Sat/Sun =
1), zero new code; the old today-based check saw a dead scan a day sooner but was inseparable
from the every-weekend false positive. (2) The closed-lot suppression's mirror image: an
unrelated same-name lot opened after the order now suppresses a genuinely UNBOOKED fill
permanently (pre-fix the false-suppress self-cleared when the lot closed). ACCEPTED, not
fixed, and documented in-code: tightening on date/shares equality re-creates the permanent
NAG for late-booked (book open stamps _now(), no date arg) or partially-closed fills — the
very bug just killed; on this book the miss is booked()'s stated known-miss made cheaper than
the alternative. Also unified booked() across both order paths (the pending FYI matched open
lots only — a booked-then-closed SAME-DAY round trip would have reverted to the WORKING nag)
and deleted the redundant status filter (meta rows can't match booked()'s ticker+side test).
Stated side effect: unplaced counterfactual state lines are also suppressed by a post-order
round trip (info-only; the name was traded anyway, muddying the counterfactual regardless).
194/194 pass; live compose unchanged (DO-NOW empty, DVA FYI intact). OPS, never edge — prior
UNCHANGED: LOW.
  Reproduce: `python3 -m pytest research/tests -q` (194, incl. the new dead-scan-at-2-weekdays
  pin) · digest.py FEED_STALE_D comment + the fills-loop residual comment.

**2026-08-11 · [OPS] FIRST LIVE WEEK AFTER THE SWEEP — the read leg died in transport and
NOTHING alarmed. Four defects behind two delivered messages; all four fixed.** User review of
Mon 08-10 (settle only) + Tue 08-11 (read only). (1) **The 08-10 read RAN** — commits `5836273`
+ `eb2e72a` at 11:43 UTC pre-registered a TTD short (bets_catalogue line 60, still accruing) —
and `push_log` stamped it `UNCONFIRMED`, so per contract it was never re-sent. The human never
saw the alert and NOTHING alarmed, because `_pushlog_section` filtered `kind == "settle"`.
**This falsifies the 08-09 red-team's coverage claim one day after it shipped:** FEED_STALE_D
3→1 was adopted as the read leg's watcher, but it only sees a read that DOESN'T RUN — this one
ran, on a healthy feed, and only the PUSH died. Read-leg muteness ≠ read-leg death.
(2) Settle pushed REJECTED 22:36 then DELIVERED 22:48; the retry's own first commit had already
moved the band's baseline, so the ONE message that got through called a −$67.63 day (−$66.17 vs
SPY, per `book_equity` 08-09→08-10) "book flat · vs SPY +$0". The band's whole job, defeated by
the retry that existed to save it. (3) That message's single DO-NOW was FALSE: it accused
2026-08-09, which `push_log` shows DELIVERED. The check held the LAST row — its own superseded
attempt — and printed `due` rather than the failing row's date, sending the human to debug a
failure that had self-healed one line above. (4) DVA sat `pending` since 08-07 under an FYI
promising "resolves at the next orders check": `resolve()` sees only sessions strictly AFTER
`scan_from`, and the human's own limit filled IN the anchor session (logged 13:53, filled
13:58). At 3 complete bars (08-10/11/12) the **08-13 settle would have stamped a live, green,
BOOKED position `expired — did NOT chase`** — a false row on the wrong side of [ORDERS #1]'s
filled-vs-expired comparison, as 1 of only 2 resolved rows against a bar with a 2026-12-31
reachability deadline. FIXES: `check` yields to `booked_lot()` (a real broker fill outranks a
model of one); push_log watches BOTH legs on their own due calendars (read = weekdays, rolls
back over weekends), fires on "no DELIVERED row on/after due" instead of "the LAST row is
DELIVERED", and names the failing row's own date; the band baseline skips any committed row
dated today; READ_LOOP gains `daily.sh`'s 🚨 heartbeat parity on a non-DELIVERED verdict.
**The never-re-send-on-UNCONFIRMED rule STANDS** — 08-10 is its first observed GENUINE loss
(n=1), and flipping it on one observation re-opens the 07-24 double-post; the new read-leg
alarm makes the loss visible on the next run instead, which is the safe half of the trade.
204/204 pass. Live after the fix: DVA resolved FILLED @178.00 on 08-07 (orders 0 working / 2
filled), the 4-day-old FYI cleared, DO-NOW clean. OPS, never edge — prior UNCHANGED: LOW.
  Reproduce: `python3 -m pytest research/tests -q` (204, incl. the 08-10 push_log replay and
  the DVA anchor-session case) · `git log --format='%h %ci %s' 68abae6..1b82685` ·
  `git show 1b82685:research/data/push_log.csv` · `python3 -m research.orders show`.

**2026-08-14 · [ARC 5 #12] DECISION + PRE-REGISTRATION (owner, cloud session) — THE PAPER-VERDICT
REFACTOR: live book RETIRED, capital exits; the system becomes a pure forward-falsification engine.**
Owner call, approved in-session: liquidate the live book (positions + cash per `book show`; broker =
human) and move the proceeds OUT of the project entirely (handled in the private
long-realm repo — pointer only, per the two-realms rule). The 2026-08-05 inflows-freeze becomes an
ALL-flows exit. Rationale (argued both ways, model recommended, owner ratified): the verdict engine is
`bets.py`, the book contributes ZERO to it by design [ARC 5 #4]; the execution lessons real money bought
are harvested and encoded (limit-band [2026-08-03], GTC nag, wash-sale/ADR fees, booked-fill flow); at
current size even a passing edge pays noise-level dollars while the DO-NOW loop is the system's largest
human-time cost.
- **AMENDS "no more paper/roleplay" (2026-07-06) — owner call, logged openly:** what ends is the
  SIZED-BOOK layer; `bets.py` was never roleplay (pre-registered, deterministically scored, benchmark-
  relative). The falsification instrument continues unchanged.
- **RE-FUND PRE-REGISTRATION (locked NOW, against ourselves — pool is ADVERSE at writing: n=6 settled,
  median −7.08%, beat 33%):** real money returns ONLY on the existing [ARC 5 #7] pooled pass (N≥30
  settled · median excess >+1% · beat-rate >55% · one-sided Wilcoxon α≈0.017) → then a staged LIVE
  re-validation tranche (~$5–10k, 10–15 trades: confirms paper excess isn't a fill artifact — fills at
  size cannot be simulated) → then scale. No funding on hot streaks before N; no new bar invented later.
- **KILL branch unchanged and accepted:** N=30 settled OR 2027-06-30 [ARC 5 #1/#7]; null/adverse at the
  bar → "the read has no edge — stop," logged as the verdict. Reachability (Arc-3 lesson): 60 open bets,
  fast sleeve matures in 21d — N≥30 lands well inside the window.
- **Income math logged (owner memory "≥$60k" NOT found in this ledger → treated as hypothesis,
  re-derived):** at pass-bar-sized edge (~+3–8pp/yr portfolio excess), $60k ≈ $2–5k/yr — real, not
  income; income-like ($1k+/mo) needs $150k+ or a bigger edge than the bar demands. Recorded so
  scale-up expectations are pre-set, not improvised at the pass.
- **First act of the new regime:** the TPR working order (logged 2026-08-14) is deliberately NOT placed —
  it expires as the first counterfactual; the TPR bet scores from ref regardless (the book↔bets
  separation doing exactly its job).
- **NOTHING implemented in code yet** — this entry is the decision + pre-registration; the execution
  checklist lives in BACKLOG (owner executes locally). Book's CLOSING VERDICT (final vs-SPY/dual-mom
  from `book mark`) gets its own entry at liquidation; the [ARC 5 #4] experiment closes against its own
  bar and the number is logged plainly, win or lose.
  Reproduce: `python3 -m research.bets show` · `python3 -m research.book show` · this session's transcript.

**2026-08-14 · [ARC 5 #12a] IMPLEMENTATION ADDENDUM (owner session, local) — the #12 design
amended and LOCKED before any code changes the verdict computation. Six decisions, pre-registered
against ourselves while the pool is ADVERSE.**

- **1 · LONG-ONLY pooled verdict — an amendment to [ARC 5 #7]'s POPULATION, not a new bar.**
  `bets.stats()` (the one pooled computation) filters to `direction=long`; the bar itself (N≥30 ·
  median >+1% · beat >55% · one-sided Wilcoxon α≈0.017) is untouched. WHY: the re-fund meaning of a
  pass is "edge real money can buy" — paper shorts carry unearnable alpha (borrow fees, borrow
  availability, buy-ins all unmodeled) and thin names fill at fantasy prices. The catalogue's only
  settled winner is exactly the archetype: ILLR short +69.74%, a micro-cap almost certainly
  unborrowable at size. **Locked at ADVERSE numbers (verified live 2026-08-14): pooled n=6 median
  −7.08% beat 33.3% → long-only n=5 median −7.99% beat 20.0%** — the rule change strips our one
  flattering row, so it cannot be read as tally-shopping. Shorts keep scoring forever as a BELOW-BAR
  diagnostic contrast (reported beside every verdict, both numbers at the final verdict);
  multiple-testing N keeps counting ALL rows (66 at writing). Governed by [Arc 5 #8]: no per-slice
  bar is being created — the one verdict's population is being defined, openly, before it exists.
- **1b · [ARC 5 #10] (short-sleeve n≥12 diagnostic bar) is declared UNREACHABLE-BY-DESIGN.**
  Max possible settled shorts = 11 (1 closed + 10 open; admission is long-only forward). The Arc-3
  lesson applied proactively: declare, don't decorate. The short sleeve remains the descriptive
  contrast #10 itself scoped below n=12 ("decides nothing and must not be quoted as if it did").
- **1c · Admission rule (code-enforced from P2): LONG ONLY + LIQUIDITY FLOOR.** `bets.add` refuses
  `direction != long` and requires median(close×volume) ≥ $5M over the last 20 COMPLETED sessions,
  FAIL-CLOSED (a fetch failure also refuses — if prices are down, the pre-market run is degraded
  anyway). The 66 existing rows are GRANDFATHERED (disclosed; the settled five longs are all
  large/mid-cap — retro-fitting an exclusion at n=6 would be its own p-hack). Re-arming shorts later
  requires a fresh pre-registration per the re-arm protocol (#5 below) — the refusal in code is that
  protocol's tripwire, not a value judgment on shorting.
- **2 · Re-fund: ONE sentence replaces the #12 gate machinery (owner call — "just focus on finding
  alpha").** No real money returns before the pooled pass; amount, source, and staging are decided
  AT the pass, in the private long-realm repo, not here. The #12 tranche/source/staging text is superseded as
  premature planning; the only standing commitment is the necessary condition itself.
- **3 · Counterfactual-orders regime (dated at this entry; code lands P3).** The broker leg is
  retired with the book: `orders placed`/`pulled` and every broker nag go; the place→check cycle
  (limit from the last complete bar, fills resolved against real bars) continues unchanged, so
  [ORDERS #1] keeps accruing on the SAME fill model — bar and reachability clause (N≥20 by
  2026-12-31, else declare) untouched. Cadence: each read run with ≥1 take logs exactly ONE
  counterfactual order for its highest-conviction take (replaces the cash-idle gate — there is no
  cash). At writing the diagnostic is n=0 on both arms; one order per weekday run reaches N≥20
  ~mid-September. **Stated caveat: with no broker, the fill model is unverifiable against broker
  truth until real money returns — a band verdict at N≥20 is a model-vs-model result and must be
  read that way; the re-validation happens live at re-fund, not before.** First counterfactual =
  the TPR order (logged 2026-08-14, deliberately unplaced, expires ~2026-08-18).
- **4 · Digest v2 contract (code lands P4).** The 💰 SINCE-LAST band retires with the book; the 🎯
  POOL SCOREBOARD leads BOTH daily legs: n settled (long-only) · median · beat · distance to bar ·
  Wilcoxon p when computable · Σ settled excess (equal-weight percentage points, each bet vs its
  OWN benchmark — never restated as "vs SPY") · the short contrast one-liner. 🏁 milestone banners
  when settled-long n crosses 10/20/30 (stateless: working tree vs git-HEAD catalogue, the
  since-last mechanism reused); a PASS-CANDIDATE line may appear from n≥10 (median>+1% AND
  beat>55%) and is ALWAYS labeled below-bar — it can never pass anything. ESCALATION CONTRACT:
  beyond the daily 📋+📖, a push happens ONLY for 🚨 failures, verdict events (milestones,
  PASS-CANDIDATE flip, pass/kill), spend-gate proposals, or something genuinely needing a human.
  ONE-message-per-leg, push-log confirmation, failure-only heartbeat: unchanged.
- **5 · Freshness protocol (near-zero owner cost).** (a) MIX MIRROR, never a quota: the digest
  prints the last-15-bets tag mix; when one tag is >50%, the next read's run note names the driver
  in one sentence — environment or habit. **Disclosed: the mirror fires on day one — 8 of the last
  15 bets are post-earnings-drift** (earnings season is the likely driver; the mirror exists to
  keep saying so out loud). Respects #10: naming the mix is not changing it mid-flight. (b) RE-ARM
  PROTOCOL (rule, lands in SKILL.md): retesting any closed probe requires a fresh pre-registration,
  ONLY data accrued since the original verdict, and the original bar or stricter — never softened.
  (c) MILESTONE REVIEW, absorbed not scheduled: the 🏁 banner day's NEXT read run carries the
  review (pool recompute, mix verdict, reachability arithmetic on every live deadline) and may
  propose at most ONE new hypothesis and ONE re-arm — as pre-registration drafts, never
  self-approved.
- **6 · Data quality, found during planning (code lands P2).** (a) The BACKLOG item-7 diagnosis
  was WRONG and is corrected: movers `pct_change` is a 5-SESSION close-to-close BY DESIGN
  (`config.TREND_DAYS=5`); TPR's −20.7% reproduces exactly (162.00 on 08-06 → 128.39 on 08-13);
  the −16.5% "close-to-close" hypothesis was the 1-session gap. Fix = LABELING the surfaces "5d",
  nothing else. (b) The REAL bug: `prices.py` split adjustment no-ops when Yahoo ships
  adjclose==close across a split — confirmed live on MNST's 2:1 (ledger −50.6% is an ARTIFACT;
  rows stay, append-only, hereby recorded as such). It poisons movers ranking AND `bets._score`
  AND order scoring for any window straddling a split → fixed via the chart response's
  `events.splits` + a regression test. (c) The [ARC 5 #7] Wilcoxon EXISTS ONLY AS PRINTED TEXT —
  nothing computes it; at N≥30 the bar could not have been evaluated. A decorative-bar gap of
  exactly the Arc-3 class, caught before it mattered: a stdlib one-sided signed-rank
  (zeros dropped, average ranks on ties, exact null distribution to n=50) lands in P2.
- **Execution shape:** pieces P0(logs, this entry)→P2(pool rule+data)→P3(orders)→P1(book
  retirement, owner-gated on broker fills, slots in any time)→P4+P5(digest v2+freshness
  texts)→P6(docs+cloud-prompt sync); P7 (the PUBLIC DASHBOARD) is backlogged with its strategy
  notes — publish the ledger BEFORE the verdict, full catalogue always, repo stays private. One
  commit per piece, tests green + the piece's own number before each. Roadmap: BACKLOG "PICK UP
  HERE". Book's terminal state: a `__RETIRED__` meta row (the `__CASH__`/`__SEED__` pattern); the
  pool-stop alarm retires WITH the pool (on a swept book it would fire forever); the liveness
  clock moves from the frozen equity curve to the push-log + watchdog pair.
  Reproduce: `python3 -m research.bets show` (both tallies) · `git log --oneline f6d575b..HEAD` ·
  the locked long-only vector: −7.99, +15.28, −6.17, −33.30, −19.09.

**2026-08-18 · [ARC 5 #13] BOOK CLOSING VERDICT — liquidated at the broker 2026-08-17, book retired;
the [ARC 5 #4] experiment FAILS its own bar.** Owner executed the P1b liquidation (all four positions,
market, ~10:30 ET Mon 08-17): CMPS 50.136664 @ 13.48 · SPY 1.009934 @ 775.41 · CACI 1 @ 662.00 ·
DVA 3 @ 177.49. Final mark (08-18, all-cash): equity **$3,970.42** vs seed baseline $4,662.74 =
**−14.8% over 53 days**; same-$-in-SPY $4,878.43 (**+4.6%**) → ~19pp behind; same-$-in-dual-mom
$4,539.56 (−2.6%) → ~12pp behind. The pre-registered bar was beat-same-$-in-SPY [ARC 5 #4]:
**FAIL — the honest prior (negative-EV retail churn, Barber–Odean) held.**
- **Diagnostic decomposition (one pool verdict stands; this is context, not re-scoring):** realized
  −$425.89 total = legacy June seed book −$641.03 (HELP −$486.60, NIO −$115.72, XRP −$38.71) +
  CMPS theme +$199.75 + SPY beta anchor +$37.44 + the read-era order-bridge trades −$22.05
  (DXCM −$8.52, DVA −$1.53, CACI −$12.00). The reads the verdict engine actually scores were
  near-flat in dollars; the drawdown was overwhelmingly the inherited seed positions.
- **Realized −$426 ≠ equity delta −$692:** the seed baseline was marked at seed-day MARKET prices
  while lots carry COST basis (HELP/NIO were already underwater at seed); plus the $3.86 ADR fee.
  Both numbers are true; they answer different questions.
- **One last book-vs-broker divergence, the GTC class [2026-08-04]:** E*Trade sold **3** DVA vs
  book 2 — trued with a 1-share row, entry ASSUMED 178.00 (the GTC limit price; order ledger shows
  2), realized −$0.51. Cash trued to $3,970.42.
- Proceeds exit the project per #12 (recorded in the private long-realm repo — pointer only).
  `book.csv` / `book_equity.csv` are frozen evidence; every book command now prints the one
  BOOK CLOSED line. Re-fund ONLY on the [ARC 5 #7] pooled pass — no new bar, no hot-streak funding.
- Residual risks, stated: the extra DVA share's entry is assumed, not confirmed (±$ trivial);
  the equity endpoint is marked 08-18 against 08-17 fills (all-cash, so price-invariant).
  Reproduce: `python3 -m research.book show` (prints BOOK CLOSED) · final rows of
  `research/book.csv` + `research/book_equity.csv` · broker confirmations in owner records.
