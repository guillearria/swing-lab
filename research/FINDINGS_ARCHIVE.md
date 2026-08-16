# FINDINGS ARCHIVE — closed-arc log entries (evidence, append-only)

Moved out of `FINDINGS.md` 2026-07-02 to keep the live digest readable in one sitting.
NOTHING here is deleted or edited: these are the full Arc 1-2 (fear/timing, forced-flow)
and Arc 4 (systematic risk-premia/trend) log entries, each with its then-true numbers and
`Reproduce:` line. The arcs' CONCLUSIONS live in `FINDINGS.md`'s header digest and the
`python3 -m research.engine` scoreboard. Do NOT re-mine these; do NOT append here except
when archiving another closed arc.

---

## Log

_(Arc 1 — fear/timing edges — below, chronological. Arc 2 inefficiency-probe entries append at the bottom.)_

**2026-06-20 · Momentum edge? → NO.** Strong vs weak momentum, broad S&P 500, 5y
(235,948 samples): avgRet5d 0.43% vs 0.35%, win 51.5% vs 53.5%. The exciting
22-winner result was pure survivorship bias. Strong = more volatility, not direction.
*Verdict: no edge.*

**2026-06-20 · 200-day trend filter on momentum? → FAILS OOS.** strong>200d beat
weak in only 2 of 5 years. The 2y +0.89% was overfit. *Verdict: no robust edge.*

**2026-06-20 · Oversold mean-reversion? → SURVIVES OOS (first to pass).** 5-day
drop ≥5% bounces. Broad S&P 500, 5y, 57,319 signals: net5d +0.50% vs baseline +0.08%,
win 55% vs 53%; beats baseline all 6 years incl. 2022. *Verdict: real, but generic —
see refinement below. Caveat: delisting bias inflates this specifically.*

**2026-06-22 · Is oversold "buy any dip" or "buy PANIC"? → PANIC.** Split oversold
by whether SPY also fell ≥2% the same week. S&P 500, 5y, net: market-wide +0.90%
win 59% vs name-only +0.16% win 52% (≈coin flip). Same shape in crypto. *Verdict:
the edge is market-wide selloffs; idiosyncratic drops are flat. Implication: the
tradeable edge needs NO new data (SPY is free); delisting threat shrinks (it lives
in the flat name-only bucket).*

**2026-06-22 · Is "market-wide" just index beta? → MOSTLY YES.** SPY itself bounces
after its own dips: dip≤−2% net +0.43% win 62%; dip≤−5% +1.66% win 77% (5y).
*Verdict: trade the index directly — no stock selection, no delisting bias, deep
liquidity. The stock version is this, amplified by beta.*

**2026-06-22 · Does a 200-day gate help index dip-buying? → YES (confirmed 20y).**
SPY dip≤−2% >200d: net +0.61% win 66% stop 6% (vs <200d +0.26% win 58% stop 24%).
QQQ >200d +0.43% win 63% stop 11% (vs <200d +0.20% stop 26%). Gate ~halves the stop
rate and cuts the tail; positive ~13–14 of ~18–20 years. Generalizes to IWM
(+0.69%), EEM (+0.66%), EFA (+0.38%); DIA fails the gate (dropped). Sits out deep
bears (2008) but not whippy corrections (2011, 2022 lose). *Verdict: the rule above.
Reproduce: `python3 -m research.dip_index 20y SPY QQQ IWM EFA EEM`.*

**2026-06-22 · Is the rule a knife-edge parameter fit? → NO (robust).** Pre-registered:
vary one knob at a time around base (−2% / 200d / 5d), pooled 5 ETFs, 20y; pass =
>200d stays net-positive AND beats <200d with no cliff. Result: dip −1%→−3% gives
>200d net +0.34%→+0.87%; MA 100→250 gives +0.64%→+0.45%; hold 3→10d gives
+0.26%→+0.87%. ALL 12 neighbors net-positive, all ~2–3× the <200d bucket, smooth
(no sign-flips). Base sits mid-range, not on a peak. *Verdict: robust; kept the round
base (did NOT re-optimize to the max — that's p-hacking). Reproduce: `python3 -m
research.robust`.*

**2026-06-22 · Is the dip rule a wealth engine standalone? → NO.** $10k on the SPY rule, 20y → $16k
(2.5% CAGR, 13% time-in-market) vs $74k buy-and-hold (11% CAGR); smaller drawdown (−23% vs −55%). Real
~+21%/yr WHILE deployed, but idle 87% of the time. *Verdict: signal real, bottleneck is utilization.
Wealth needs the idle capital across UNCORRELATED edges (the 5 ETFs co-dip, so they don't count). Now
threat #1. Reproduce: `python3 -m research html`.*

**2026-06-22 · How inflated is the overlapping sample? → ~2.5× (verified).** SPY dip≤−2% & >200d:
305 per-day triggers vs 123 independent one-trade-at-a-time episodes. De-overlapping also shrinks the
edge (+0.61%→+0.42%/trade, win 63%→60%) — the overlapping sample double-counts the best clustered
bounces. Honest count makes SPY's edge only marginally significant (~[51%,69%], 2σ). *Verdict: threat #3
quantified and real; the de-overlapped count (report_html `_strategy`) is canonical.*

**2026-06-22 · Does the dip rule's DEPLOYMENT decorrelate across asset classes? → YES (gate passed).**
Same rule on SPY/TLT/GLD (equity/bonds/gold), 19y common window: per-asset time-in-market ~11–15%, but
UNION (≥1 deployed) = **33.1%** — essentially the statistical-independence ceiling (33.6%). Pairwise
overlap tiny (SPY-TLT **2%**, SPY-GLD 11%, TLT-GLD 10%). Pre-registered pass was union ≥25%. *Verdict:
PASS — uncorrelated assets ~2.6× the utilization; the bottleneck is attackable. Proceed to the portfolio
wealth curve. Caveats: this is a 19y AVERAGE — decorrelation can break in crises (stocks+bonds BOTH fell
in 2022); and utilization only helps if each asset's dip edge is itself net-positive (untested for
TLT/GLD — the wealth curve must check). Reproduce: `python3 -m research.decorrelate`.*

**2026-06-22 · Do the utilization sleeves each have a real dip edge? → SPY/GLD modest, TLT none.**
Standalone one-at-a-time dip rule, independent trades: SPY n=123 +0.42%/trade win 60% (but LUMPY — loses
2010/11/22/23 outright); GLD n=141 +0.25% win 57% (modest, real); TLT n=106 +0.16% win **51% — coin
flip**, no edge, only decorrelation. *Verdict: utilization helps only if idle capital buys WINNING trades
— only SPY+GLD qualify, modestly. The honest core portfolio is SPY+GLD, not five assets; TLT is ballast,
not edge. Every edge is regime-conditional per-year — confirms "history ≠ future." Reproduce: `python3 -m
research.sleeves`.*

**2026-06-22 · Does fade-the-panic survive in crypto (the psychology bridge)? → NO — it's momentum.**
Same dip rule: BTC n=188 +0.59%/trade but win only **52%** and the ENTIRE edge is 2017's mania (+116% cum
of +111% total); 2018/2021 lost −34%/−55% — a fat-tail mirage. ETH n=132 **−0.10%/trade, negative**. *Verdict:
in the purest sentiment markets fear does NOT mean-revert on a 5-day fade — dips keep dipping (reflexive
crashes), rallies keep rallying. The psychological edge in crypto is MOMENTUM/TREND, not reversion. Big
implication: the fade core is an EQUITY-regime edge; crypto needs the opposite temperament. Next falsifiable
candidate: does trend-following (long while >200d, flat below) beat buy-hold in crypto? Reproduce: `sleeves`.*

**2026-06-22 · Does a VIX>30 gate cut the equity fade's losers? → NO (opposite).** Pre-registered: skip
SPY dip-buys when VIX>30 on entry. Result: VIX≤30 bucket net +0.38% (n=116) — LOWER than all-trades +0.42%;
the VIX>30 bucket (n=7) is +1.13%/trade — the BEST trades (2020 crash bounces), not losers. The lumpy
losers (2011/2022) sat at VIX≤30 — moderate-fear whipsaws, not panic. *Verdict: simple VIX gate FAILS —
among >200d dips, high VIX is GOOD (overshoot bounce); the tail is NOT a VIX phenomenon. Did NOT flip the
rule (n=7 = p-hacking). Reproduce: `python3 -m research.vix_gate`.*

**2026-06-22 · Does trend-following beat buy-hold in crypto? → YES (risk-adjusted), thin sample.** Long
while >200d MA else cash, net of switch costs. BTC: CAGR +40.5% (= buy-hold's) but maxDD −64% vs −83%, and
dodged BOTH bears (2018 −45% vs −74%, 2022 0% vs −64%) — a risk reducer, not alpha. ETH: CAGR +25% vs +10%,
maxDD −74% vs −86% — beats buy-hold outright; both bears dodged. *Verdict: PASS the pre-registered bar
(beats risk-adjusted AND sidesteps both bears). The fade-vs-trend split holds — crypto rewards trend,
equities reward fade: temperamentally uncorrelated edges. Caveats: only ~2-3 cycles (suggestive); BTC is
drawdown-reduction at equal return; 2025 whipsaw (BTC trend −18% vs −6%). Reproduce: `research.crypto_trend`.*

**2026-06-22 · Do the two edges compound better TOGETHER? → ladder YES, beat buy-hold NO.** Equal-weight
monthly sleeves, same window (2018-26): Sharpe rose single-SPY-fade 0.54 → CORE(SPY+GLD) 0.72 → FULL(+crypto
trend) 0.91 — uncorrelated edges DO stack (the thesis, confirmed). BUT buy-hold SPY Sharpe = 0.94: FULL only
TIES it, and via crypto BETA (CAGR 3.5%→23% but vol 5%→27%, maxDD −12%→−29%), not alpha. Over full 20y the
fade core is Sharpe 0.45 vs buy-hold 0.74. *Verdict: the framework composes (stacking lifts Sharpe) but our
edges are too modest to BEAT buy-hold risk-adjusted — we match it with beta. Next lever is better/more edges
or the regime (human) layer, NOT more probes on these assets. Equal-weight (unsized), in-sample, crypto
provisional. Reproduce: `python3 -m research.portfolio`.*

**2026-06-22 · Can a cheap regime proxy isolate the equity-fade's tail (mechanize the human edge)? → NO
(2nd proxy fails).** Split SPY fade by 200d-slope sign at entry: RISING n=113 +0.37%, FALLING n=8 +0.83% —
opposite of hypothesis, and the losers (2010/11/22) are ALL in RISING uptrends (the gate already needs
price>200d, so falling-200d trades barely exist). With VIX before it, that's TWO a-priori regime proxies
failed. *Verdict (pre-committed — no 3rd filter, that's p-hacking): the fade's tail is NOT cheaply
mechanizable — the losers are whipsaws inside healthy uptrends at moderate VIX, i.e. the generic 40% tail of
a 60%-win edge, not a separable regime. The human/regime edge (if real) is NOT in micro-filtering equity
dips — it's either regime-level ALLOCATION (which temperament to deploy, fade vs trend — backtestable) or
irreducibly discretionary (forward human-in-the-loop only). Reproduce: `python3 -m research.regime`.*

**2026-06-22 · Does crypto REVERT on sentiment extremes (Crypto F&G)? → NO (decisive).** Buy BTC/ETH at
F&G≤20 (extreme fear; alternative.me free daily 2018→), next-day-close entry, hold 20/40/60d, de-overlapped,
net cost. BTC mean +1.70%/−0.57%/+0.03% vs buy-any-day baseline +2.31%/+5.05%/+8.41% — UNDERperforms at every
horizon; ETH negative throughout (−0.5% to −2.2%). Entries DO land below the 200d (20/30) but there's no edge
to complement; lumpy/sign-flipping by year (2020/21 up, 2018/22/25 down). *Verdict: crypto reverts on NEITHER
price NOR sentiment — it TRENDS; buying fear = catching knives in an up-drifting market, worse than a random
entry. Closes the crypto-sentiment question (the raw_input "social fear = buy" hypothesis fails here). Caveats:
F&G is partly price/volatility-derived (not purely social); ~3 cycles. Reproduce: `python3 -m research.fng_crypto`.*

**2026-06-22 · Does "buy extreme VIX, hold weeks-to-months" beat buy-any-day on SPY? → YES (passes; partly a
NEW regime, partly the fade).** SPY+^VIX 1993→ (8405d), next-day-close, de-overlapped, net cost. VIX≥30: mean
+1.81%/+2.82%/+4.76% at H=20/40/60 vs baseline +0.72%/+1.63%/+2.53% — beats ALL 3, win 66/63/76%, n=61/43/34,
excess GROWS with hold; positive in 3 of 4 decades (1990s/2010s/2020s — NOT 2020 alone; 2000s flat). Vindicates
the n=7 hint from the failed VIX-GATE (high VIX = good bounces) at scale + longer holds. Red-team: only **7–9%
deployment overlap with the dip-fade**, and **85% of VIX≥30 days sit BELOW the 200d** (regime the fade skips) —
largely a DIFFERENT-regime bet, not the fade re-expressed. Split by 200d gate: ABOVE +2.6/+2.6/+5.1% win
**78/62/79%** worst only **−9%** (clean core, n=14–18); BELOW similar mean but worst **−26%** (the fat tail; the
2000s dot-com+GFC washout lives here). *Verdict: real, bigger per-episode than the 5d fade; the 200d gate again
cuts the tail (−26%→−9%) without killing the mean. BUT the genuinely NEW (fade-decorrelated) part is the
BELOW-200d deep-fear buying — exactly the −26%-tail part; the clean ABOVE part ~half-overlaps the fade. Residual:
small N in the clean bucket (14–18); in-sample; "beats buy-any-day" includes up-drift (needs a risk-adjusted
portfolio test); the below-200d mean assumes you hold THROUGH −26% (real liquidation risk). Next pre-registered
test: does the GATED VIX-buy add risk-adjusted return as a 3rd sleeve in `research.portfolio`? Reproduce:
`python3 -m research.vix_fear`.*

**2026-06-22 · Is "disaster = generational buy" real, and does a DYNAMIC exit beat STATIC? → ENTRY half-true;
dynamic-exit claim FAILS (it's insurance, not alpha).** [First test of the experimental event-edge stream — see
[[project-experimental-event-edges]].] Mechanical disaster entry = first close ≥20% below the trailing-1y high,
de-overlapped; from each entry compare STATIC hold vs DYNAMIC (long>200d MA else cash) over 1/2/3y, + Nikkei
honesty check. (1) The ENTRY works broadly — 3y avg multiple SPY ×1.37, QQQ ×1.34, GLD ×1.90, TLT ×1.23, BTC
×8.7, even **Nikkei ×1.21** (+21%, 64% of 3y holds positive): buying −20% drawdowns is a positive entry across
EVERY asset incl. Japan. (2) DYNAMIC does NOT beat STATIC on return (static wins/ties 4 of 6: SPY 1.37>1.27,
GLD 1.90>1.52, TLT 1.23>1.07, Nikkei 1.21>1.12; QQQ/BTC ≈tie) → pre-registered claim FAILS. It IS insurance:
halves drawdown (SPY −25%→−12%, QQQ −46%→−22%, BTC −66%→−52%) and lifts hit-rate (SPY 3y 28/28 vs 23/28 up) at
a return cost. Asset-specific: HELPS trending equities/tech/crypto, HURTS gold/bonds (whipsaw, no clean trend).
(3) Japan myth busted — "30y underwater" is the buy-the-TOP story; buying Japanese DISASTERS and holding 3y
averaged +21%, so the dynamic exit didn't "rescue" Japan (nothing to rescue at 3y). *Verdict (pre-committed
honesty): literal hypothesis FAILS (dynamic≠more return; Japan premise wrong) — but the test banks TWO durable
truths: the disaster entry is broadly positive, and trend-exit is a RISK reducer (~2× return-per-drawdown) not
alpha — same temperament as crypto_trend. RESIDUAL (the real threat): SURVIVORSHIP — SPY/QQQ/BTC/GLD rode
secular bulls and even the Nikkei paid at 3y; we still lack a truly "stays dead" market (delisted/EM) to prove
the thesis CAN fail. Reproduce: `python3 -m research.disaster`.*

**2026-06-22 · Survivorship stress — does disaster-buy survive a GRAVEYARD of dead/stuck markets? → YES (entry
real worldwide); dynamic exit = insurance that PAYS in true collapses.** Same engine on 8 USD corpses
(EWJ/FXI/EWI/GREK/ARGT/TUR/EWZ/RSX). (1) ENTRY is NOT hindsight: STATIC 3y net-positive in **13 of 14** markets
(survivors+graveyard) incl. Argentina ×1.94, Italy ×1.26, Brazil ×1.25, Greece ×1.21, Japan-USD ×1.20, Turkey
×1.18, China ×1.12 — even though their BUY-HOLD was dead (China ×2.6, Japan-USD ×3.3, **Russia ×0.3 = −70%**).
Only RSX (Russia→'22 halt) had STATIC negative (×0.87). Mechanism = harvesting the −20%-dip BOUNCES in choppy
sideways/down markets, NOT secular recovery. (2) DYNAMIC exit: cuts drawdown in ALL 14 (graveyard −31/−56% →
−22/−37%); on RETURN it FAILS to beat static in stuck-but-ALIVE markets (whipsaw: FXI ×0.92, TUR ×0.93) BUT
EARNS ITS KEEP in the true COLLAPSES — RSX ×0.87→**×1.04**, GREK ×1.21→**×1.40** — turning losers into winners
while halving the pain. *Verdict: disaster-ENTRY is a real, GLOBAL, volatility-harvesting edge — survived the
honesty check (only the near-zero corpse beat static, and the dynamic exit rescued even that). The dynamic exit
is INSURANCE: free-or-better in catastrophes, a small premium in stuck markets — vindicates the user's "don't
stay stuck" instinct precisely where it matters. RESIDUALS: brutal intermediate pain the averages hide (2y RSX
×0.81; GREK/Brazil −49/−56% worst; several <50% hit-rate); EM ETF costs/spreads understated (esp. dynamic's
extra switches); RSX data ends at the HALT (~$5, holders got ~0) so even the worst corpse is censored; clustered
episodes overcount (FXI 65, EWZ 92 entries). STILL not shown to beat buy-hold risk-adjusted with sizing.
Reproduce: `python3 -m research.disaster`.*

**2026-06-22 · Can a GLOBAL disaster-buy PORTFOLIO finally beat buy-hold (the utilization thesis)? → NO
(decisive).** 14-asset global basket incl. corpses; arm at −20%-off-1y-high, disarm at new high, dynamic 200d
trend-exit while armed; SPREAD (1/N_eligible) vs CONCENTRATE (1/K_deployed); daily, costed, no leverage, no
lookahead, 1993-2026. vs buy-hold SPY (CAGR **+10.8%**, maxDD −55%, Sharpe **0.65**, ret/|DD| 0.20): SPREAD
+1.3% / −24% / 0.29 / 0.05; CONCENTRATE +3.7% / **−66%** / 0.28 / 0.06. Loses on CAGR, Sharpe AND ret/|DD|;
CONCENTRATE's drawdown is even WORSE than SPY (decorrelation breaks in 2008-style co-crashes). Utilization DID
rise (time-in-market 13%→**53%**, avg 2.7/14 deployed) — the thesis's PREMISE held, its CONCLUSION failed.
*Verdict: utilization thesis REJECTED. Why: the disaster-buy harvests small bounces while structurally SELLING
the one secular winner (US disarms at every new high) and concentrating into the world's weakest markets
(EM/corpses that bounce but go nowhere). You can't out-compound buy-and-hold by selling winners to buy losers'
bounces. DEEP LESSON (consistent across the whole arc): our mechanical edges are RISK-REDUCERS / bounce-
harvesters, NOT growth-capturers — they cut drawdown or win per-trade but don't beat owning the best compounder.
The bottleneck was never utilization; it's the KIND of edge. Beating buy-hold needs leverage on a HIGH-Sharpe
source (these aren't: 0.28 ≪ 0.65) or a fundamentally different edge (selection/growth), NOT timing/rotation of
fear signals. Caveats: cash=0% (T-bills lift SPREAD ~1.5%/yr, verdict unchanged); only 2 sizing designs (risk-
parity/capped untested — but a 0.28→0.65 Sharpe gap is a chasm, not a tuning miss); SPY is a tough US-centric
bogey. Reproduce: `python3 -m research.disaster_port`.*

**2026-06-22 · [ARC 2 #1] Is the S&P 500 index-DELETION bounce a tradeable forced-flow edge? → NO (fails the
bar).** Real removals 1996-2026 (752; tested 356 since 2010) derived from fja05680 membership history — the LIST
includes names that later DIED (no list-survivorship). Buy at first close on/after the deletion effective date,
excess vs SPY at 21/63/126d. Priceable n≈152–164: mean excess +2.1%/+2.9%/+6.4% LOOKS positive, BUT median
+1.1% / **−1.7% / −1.3%** and %-beat-SPY 54% / **46% / 49%** — a right-skewed LOTTERY (a few big winners drag the
mean; the typical deletion LAGS SPY at 3–6mo). Weaker in the 2020s than 2010s (anomaly decay). **52%** of
deletions (184/356) censored — acquired/delisted, no post-deletion data → excluded → biases the bounce UPWARD.
*Verdict: FAILS the pre-registered bar (needed +mean AND +median, >50% beat, era-consistent). Only a faint
≤21d whiff survives — too small/coin-flippy to trade after deleted-microcap spreads. The positive mean is
outlier+survivor-driven, not a reliable forced-flow bounce, and it's decaying. PAID-DATA trigger NOT pulled: a
clean test wants point-in-time delisting-inclusive prices + reason codes (CRSP/Norgate) to include the dead
names and isolate distress-vs-M&A removals — but spending isn't justified to rescue a hypothesis already failing
on free data. Good process result: a real forced-flow idea, tested with survivorship-aware history, rejected
cheaply. Reproduce: `python3 -m research.index_deletion` (data: research/data/sp500_deletions.csv).*

**2026-06-22 · [ARC 2 #2] Post-IPO LOCKUP-EXPIRY forced selling — a tradeable dip→rebound? → NO (decayed +
just-beta).** 1876 operating-company IPOs 2014-23 (NASDAQ calendar, SPACs/units filtered; list records ticker
AT IPO → dead names included). Expiry ≈ IPO+180d (modal proxy; real lockups vary → dilutes). Excess vs SPY;
priceable 1048, censored 828 (44%). Into-expiry [−10,0]: mean −1.43%, median −1.90%, 59% neg (both eras) —
real anticipatory drift down. Event [−3,+7]: mean −0.06% (flat), median −1.27%, but **2010s −1.12% vs 2020s
+0.73%** — the classic −1–3% lockup drop has DECAYED. Post [+7,+37]: mean −3.43%, median −4.10%, 60% neg — NO
rebound; weakness CONTINUES (2020s −5.0% = 2021-vintage bust in '22). *Verdict: FAILS the bar (needed neg-event
+ POSITIVE rebound; got a decayed/flat event and NEGATIVE post = no overshoot to buy). The lone persistent
signal is broad post-IPO UNDERPERFORMANCE vs SPY — but that's the known IPO-underperformance anomaly + unadjusted
high-beta in the '22 bear, a crowded SHORT (hard-to-borrow, squeeze risk from the moon-shot outliers), NOT a
small-operator long edge. Exact lockup dates need S-1 parsing (paid/hard) but not worth it on a decayed effect.
**MINDSET FLAG: two famous forced-flow anomalies (index-deletion, IPO-lockup) now BOTH decayed/crowded —
published edges die; the cheap-free-data textbook corner looks FISHED OUT. The honest next move is NOT a 3rd
textbook anomaly — it's either better/unique DATA (the agent-as-researcher's real lever; name a paid trigger) or
a structurally less-crowded niche.** Reproduce: `python3 -m research.lockup` (data: research/data/ipos.csv).*

**2026-06-22 · [ARC 2 #3] Russell 2000 reconstitution (free route)? → DATA-BLOCKED (not run).** The most-cited
free-ish forced-flow left. Checked: no clean free historical Russell add/delete list exists — ikoniaris/Russell2000
is an UNDATED snapshot (Ticker,Name only); alemicheli/pyndex ships NO data (it reconstructs membership from a
market-cap universe you supply). Getting recon additions requires a survivorship-clean point-in-time universe =
the paid data we were avoiding. *Verdict: the FREE route is EXHAUSTED — and Arc 2's wall is DATA ACCESS, not
edge. The real lesson: cheap+famous anomalies are arbitraged (deletion, lockup BOTH decayed), and the less-
crowded niches sit behind a DATA MOAT — which is exactly why an edge could persist there, and why it costs money.
The barrier is the moat. DECISION POINT: ~$50/mo survivorship-clean fundamentals+prices (Sharadar/Nasdaq Data
Link) to enter the data-gated space, or stop. No code (data unavailable for free).*


---

## ARC 4 — systematic risk-premia / TREND (the cheap mine we skipped)

**2026-06-23 · [ARC 4 #1] PRE-REGISTRATION (no data peeked) — asset-class DUAL MOMENTUM.** Why now: we
tested SINGLE-NAME momentum (junk/survivorship) but NEVER cross-asset time-series/relative momentum — the
most OOS-robust anomaly in finance (trend-following: 100+yr, 50+ markets) and how many profitable SYSTEMATIC
retail traders actually operate; our own crypto_trend PASS already hinted trend works. **Rule (fixed, NO
tuning):** monthly rebalance; among equities {SPY, EFA, EEM} hold the single highest trailing-12-month total
return; **absolute gate** — if that best equity's 12m return ≤ 0 (T-bill≈0 proxy), hold AGG (bonds) instead;
0.1% per-switch cost; common window (~2003-2026, limited by EEM/AGG history). **PASS bar (must clear ALL,
OOS):** beat buy-hold SPY on CAGR **AND** Sharpe **AND** max-drawdown, net of cost, positive in a majority of
decades. **Honest prior:** trend has the best evidence of anything we've tried — BUT every prior "win" still
TIED SPY; if this also merely ties, the free systematic corner is exhausted and the engine / paid-data /
reading become the only remaining levers. **Caveats pre-stated:** ~23y window, T-bill≈0 simplification,
monthly close-to-close, rf=0 in Sharpe (applied equally to both, so the COMPARISON is fair). Reproduce:
`python3 -m research.dualmom`. *Status: pre-registered, awaiting the number.*

**2026-06-23 · [ARC 4 #1] Asset-class DUAL MOMENTUM → FAIL (strict) / BEST-OF-FAMILY near-miss.**
2004-09→2026-06 (261 months), net 0.1%/switch. dual-mom CAGR **+11.4%** Sharpe **0.78** maxDD **−24%** (×10.4)
vs buy-hold SPY CAGR +11.1% Sharpe **0.79** maxDD −51% (×9.8). Pre-registered bar (beat on CAGR AND Sharpe
AND maxDD) = **FAIL** — beat CAGR and HALVED drawdown but TIED Sharpe (0.78 vs 0.79, lost by 0.01); no
goalpost move. Per-decade (OOS): 2000s **+20.4% vs +2.0% (win — rotated to bonds through 2008)**, 2010s +6.7%
vs +13.4% (lose), 2020s +11.7% vs +15.1% (lose — diversified into intl/EM that lagged US tech). *Verdict:
the STRONGEST result in the project and a refinement of the core lesson — Arc-1 edges LOST CAGR (idle
capital); trend KEEPS CAGR while halving drawdown (**ret/|DD| 0.48 vs 0.22 = 2.2×**). But Sharpe TIES SPY, so
it is a better risk SHAPE, NOT alpha: levering it to SPY-vol just rides the same Sharpe line to ~SPY's
risk-adjusted return. Real, robust, usable (drawdown-averse / leverage-tolerant capital), survivorship-clean
(index ETFs). This was the last big CHEAP mine — reversion, events, insider, AND trend now all TIE-or-LOSE
SPY risk-adjusted. CONCLUSION (4 arcs): there is no free mechanical RISK-ADJUSTED alpha for us; the honest
levers left cost MONEY (paid-data moat) or TIME (the slow reading test, accruing) — or we deploy the one
usable risk-shape result and make the rigor ENGINE the asset. Caveats: ~23y, T-bill≈0 gate, monthly,
US-centric bogey. Reproduce: `python3 -m research.dualmom`.*

**2026-06-23 · [ARC 4 #2 · LOOP iteration #1, AUTO-GENERATED] VOL-TARGETING SPY → PASS (first to clear the
bar) — caveated, needs OOS.** First idea produced by the autonomous loop (see research/LOOP.md). Hold SPY
sized to a constant 15% vol (trailing-21d), ≤2x leverage at 5% borrow, monthly rebalance, net 0.1%/turnover;
knobs fixed pre-run, one shot (no tuning). 1993-2026 (33y): vol-target CAGR **+10.8%** / Sharpe **0.68** /
maxDD **−41%** vs buy-hold +10.7% / 0.64 / −55% → PASS the pre-registered bar (beat SPY on CAGR AND Sharpe,
net). *Red-team (why NOT trusted yet): the Sharpe edge is SMALL (0.64→0.68) and vol-targeting lifting Sharpe
is a KNOWN effect (vol clusters), not novel alpha; CAGR is a tie (+0.1%); the return-match leans on CHEAP
leverage (5% borrow — retail margin is dearer; futures/box-spread ~SOFR makes it plausible); FULL-SAMPLE not
OOS-split; still beta-with-sizing; and after ~19 tests a small bump can be chance. Per SKILL ("a marginal
positive is noise until fresh OOS"), verdict = **PASS\*** (promising LEAD, unconfirmed). NEXT loop iteration =
the confirm pass: OOS decade-split + borrow-rate + rebalance-frequency sensitivity. This is the loop working:
idea generated → tested → passed → checker flags the confirm step. Reproduce: `python3 -m research.voltarget`.*

**2026-06-23 · [ARC 4 #2 · LOOP iteration #2, THE CONFIRM] Vol-targeting OOS/robustness → NOT CONFIRMED
(demote PASS\* → REAL\*).** Per-decade Sharpe vs SPY: 1990s 1.28<1.32, 2000s 0.13>0.07 (win), 2010s
0.81<0.93, 2020s 0.69<0.80 — wins only **1 of 4 decades** (the 2008-crash decade). Borrow sensitivity: beats
at 3/5/7% but LOSES at 9% (and 7% is a razor tie). Lookback 21/42/63d: no cliff (that part is robust).
*Verdict: the full-sample "beat" was crash-insurance from ONE decade (de-risking into 2008) plus cheap
leverage; in normal/bull decades it LAGS SPY. NOT a robust risk-adjusted edge → demoted to REAL\* (another
risk-reducer/crash-hedge, not alpha). The LOOP working exactly as designed: the maker found a PASS, the
checker's OOS/robustness pass correctly killed it — a false lead caught cheaply, in one session, no human
judgment needed. Confirmed-beats-SPY back to 0/17. Reproduce: `python3 -m research.voltarget confirm`.*

**2026-06-23 · [ARC 4 #3 · LOOP iteration #3, mechanical] VOLATILITY RISK PREMIUM ("sell insurance") →
FAIL.** Clean variance-swap proxy (free data): each month short a 1-month variance swap struck at the prior
month-end VIX, pay realized variance; 1993-2026 (400 months). short-vol Sharpe **0.58** vs SPY **0.77**; **84%
of months positive** but skew **−8.75**, and the worst month (2008-10) erases **~71 months** of average
premium. *Verdict: FAIL — the premium is REAL (you win 84% of months) but it does NOT beat SPY risk-adjusted
and carries a catastrophic left tail. The textbook "consistent income" mirage: steady small wins, rare ruin;
the 84%-positive is the seductive lie and Sharpe itself UNDERSTATES the danger. Caveat: this is the HARSH pure
variance-swap version; a managed OTM put-write (CBOE PUT/PUTW) historically fares better (~SPY Sharpe, lower
DD) but shares the negative-skew DNA and needs options data — not chased (still paid for crash risk, not free
alpha). Reproduce: `python3 -m research.volrp`.*

**2026-06-23 · [ARC 4 #4 · LOOP, mechanical] Cross-sectional FACTOR ETFs vs SPY → no CONFIRMED edge
(momentum marginally beats in-sample, but regime-artifact).** MTUM/QUAL/VLUE/USMV/SIZE vs SPY,
2013-08→2026-06 (155 months = ETF inception). SPY CAGR +14.0% / Sharpe 0.98 / maxDD −24%. Only **MTUM** beat
on BOTH: +16.3% / **1.02** (razor +0.04) — but maxDD WORSE (−30%). QUAL/VLUE/USMV/SIZE all lose on Sharpe or
CAGR. *Verdict: NOT a confirmed edge. (1) 5 factors tested → multiple comparisons; a +0.04-Sharpe winner is
chance. (2) REGIME ARTIFACT — MTUM launched 2013, AFTER the catastrophic 2009 momentum crash, so its worst
tail is excluded by construction. (3) one bull-ish regime. The MOMENTUM/TREND family keeps coming closest
(cf. dual-mom NEAR, crypto-trend REAL*) but every instance is regime-flattered. Logged NEAR, not a beat.
Reproduce: `python3 -m research.factors`.*

**2026-06-23 · [ARC 4 #5 · LOOP, mechanical] SEASONALITY (Halloween, turn-of-month) on SPY → FAIL (clean).**
SPY 1993-2026. Halloween (Nov-Apr in, else cash): +6.8% / Sharpe 0.56 — worse than buy-hold +10.8% / 0.64 on
BOTH. Turn-of-month (last day + first 3): +3.4% / 0.46 — worse on both (lower DD −18%, but that's just low
time-in-market). *Verdict: FAIL — both calendar rules underperform buy-hold on CAGR AND Sharpe; being out of
the market sacrifices more than the seasonal tilt earns (and cash=0% here FLATTERS them). Reproduce:
`python3 -m research.seasonality`.*

**2026-06-23 · [ARC 4 #6 · LOOP, mechanical] Bond CURVE CARRY (TLT when curve positive else SHY) → FAIL vs
SPY.** 2002-2026 (287 months). curve-carry +4.0% / Sharpe 0.39 / maxDD −42% vs SPY +11.1% / 0.79 / −51%.
*Verdict: FAIL the wealth bar — a bond strategy, ≪ stocks long-run. It DOES beat TLT buy-hold on Sharpe (0.39
vs 0.33 — dodges some inverted-curve pain), a mild within-bonds improvement, not an SPY competitor. Closes the
cross-asset 'carry' family. Reproduce: `python3 -m research.carry`.*

