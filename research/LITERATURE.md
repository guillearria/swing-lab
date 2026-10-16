# LITERATURE — what published research says about the edges this project hunts

Built 2026-10-16 (BACKLOG head item, Phase 2) after Arc 5's forward test failed [ARC 5 #18] and
the mover-ledger leads were withdrawn [ARC 5 #20]. **Rule: official sources only** — the journal's
own page, the authors' hosted copy, SSRN, NBER, a university-hosted copy, or a regulator's own site;
never blogs, encyclopedias or summaries. Every number below came from a page opened while building
this file; where only an abstract or a working-paper version was reachable, the block says so, and
working-paper numbers may differ slightly from the published tables. Takeaways here feed the NEXT
pre-registration; they never retrofit a bar already written.

## The short version

1. **Published edges shrink.** Long-short returns run about 26% lower out of sample and 58% lower
   after publication (McLean & Pontiff 2016) — before costs, and mostly in illiquid names.
2. **Most anomalies do not replicate the way a real portfolio would trade them.** With NYSE
   breakpoints and value weights, 65% of 452 anomalies fail at |t|≥1.96 and 82% at 2.78; 102 of
   106 "trading-frictions" anomalies fail; microcaps are 3.2% of market value but 60.7% of stocks
   (Hou, Xue & Zhang 2020). The bar for a new signal is t>3, higher once your own trials are
   counted (Harvey, Liu & Zhu 2016).
3. **Short-term reversal is real gross, and a liquidity taker loses it net.** Value-weighted
   one-month reversal: 0.37%/mo gross, 1.65%/mo cost, −1.28%/mo net; in small stocks (20th–50th
   NYSE percentile) 0.41 gross vs −0.84 net (Novy-Marx & Velikov 2016). The gross effect is
   front-loaded in the first week, concentrated in illiquid losers and largely bid-ask bounce
   (Lehmann 1990; Avramov, Chordia & Goyal 2006; Nagel 2012). The one reversal variant that
   survived costs was industry-relative reversal among low-volatility stocks (+0.28%/mo net, to
   2012).
4. **Why a stock moved decides the sign.** Moves that came with news, especially bad news, keep
   drifting; no-news moves partly reverse, mostly in low-priced stocks (Chan 2003). Low-coverage
   losers keep falling for months (Hong, Lim & Stein 2000). Stocks with a lottery-like one-day spike
   underperform the next month (Bali, Cakici & Whitelaw 2011).
5. **Post-earnings drift is gone where it can be traded.** No drift in stocks above the NYSE 20th
   size percentile since 2006, and gone in microcaps by 2016 (Martineau 2022). That was Arc 5's
   most-used pattern.
6. **Overlapping bets are not independent.** Overlapping event windows can make test statistics up
   to four times too large (Mitchell & Stafford 2000); calendar-time portfolios fix it (Fama 1998).
7. **What survives careful testing is slow and diversified.** Twelve-month trend across 58 futures
   (Sharpe above 1, gross) and value plus momentum across eight markets (Sharpe 1.59 combined, gross;
   about 0.3 for a single US leg) (Moskowitz, Ooi & Pedersen 2012; Asness, Moskowitz & Pedersen 2013).
8. **Retail outcomes, per regulators.** Most retail traders lose in leveraged, short-dated products:
   74–89% of CFD accounts (ESMA), 82% (FCA), two-thirds of US retail forex customers per year
   (CFTC), 87.7–93% of Indian equity-derivatives traders (SEBI). The share earning a meaningful
   income is about 1% or less wherever it was measured (SEBI, Taiwan, Brazil). No official source
   measures retail swing-trading outcomes.

## What it means for this project

- **Arc 5's FAIL fits the literature.** The reader leaned on large-cap post-earnings drift (dead
  since 2006 per Martineau) and "overreaction" dips that the news-versus-no-news evidence says keep
  falling when the drop came with news. The Arc 5 bar also treated overlapping bets as independent;
  correcting that can only widen the error bars, so it cannot turn the FAIL into a pass.
- **The one surviving lead [ARC 5 #20] was short-term reversal**, the effect most consistently
  reported as eaten by costs. It got exactly one official-data gate, [GATE R1] in FINDINGS, and
  FAILED on every condition: in NYSE size quintiles 2–4 the spread averaged +1.05%/mo (t=7.50) over
  1926–2014 and +0.04%/mo (t=0.14) over 2015-01..2026-05 — gone before costs. The lead is closed.
- **Where a small account plausibly has room** (inference, not a source claim): low-turnover,
  multi-week holding periods in liquid instruments, diversified across markets, with costs and
  behaviour controlled — not speed, not short-dated leverage, and not edges that live only in tiny
  stocks, which is where model artifacts concentrate (Fama 1998).
- **Method upgrades for every future test:** NYSE breakpoints and value weights for any portfolio
  claim; calendar-time portfolios for event tests; t>3 counting our own trials; charge the
  effective spread on entry and exit; skip day one after a move; separate news from no-news moves
  where possible.

## Short-list (written after [GATE R1], 2026-10-16)

The rule: survived independent replication · plausible net of costs at small size · preferably
long-only · testable on free data · not a rerun of a probe this repo already killed unless the
re-arm protocol is met.

1. **Lottery-stock avoidance — the one untested, eligible candidate.** Stocks with an extreme
   one-day gain last month underperform the next month: value-weighted high-minus-low MAX decile
   −1.03%/mo, four-factor alpha −1.18% (Bali, Cakici & Whitelaw 2011, 1962–2005). The long-only use
   is a negative screen — do not buy right after an extreme spike — the same family as the
   small-cap spike fade that started Arc 6. Free official data: Chen & Zimmermann's Open Source
   Asset Pricing carries the predictor; everything after publication is out of sample. Expect decay
   (McLean & Pontiff) and possibly disappearance (as [GATE R1] found). **Next step: its own
   pre-registration and blind review before anything runs** (BACKLOG).
2. **Price momentum — the literature's strongest survivor, blocked here by our own rule.**
   Value-weighted 6/6 and 11/1 momentum clear t>3 over 1967–2016 (Hou, Xue & Zhang). This repo
   already failed single-name momentum and graded the momentum ETF "NEAR" over 2013–2026, so the
   re-arm protocol allows only data after those verdicts — a forward-only test, years from power.
3. **Diversified trend across asset classes — the north-star answer, already banked as risk
   shape.** Time-series momentum across futures and value-plus-momentum across markets are the most
   robust premia found, with Sharpe ratios at or above 1, gross of costs, and only when diversified.
   This repo's dual-momentum result is the small-account version: SPY-like return, half the
   drawdown, no alpha. It stays the default-allocation lane, not a new test.

**The next-market question.** Official retail data shows no market type where small traders succeed
broadly. The measured share earning a meaningful income is about 1% or less wherever it was
measured (SEBI, Taiwan, Brazil), and losses grow with turnover, leverage and short horizons. The
landscape doc's 5–15% "success" rates are unsupported and should not be used to choose a market.
The evidence-backed room for a small operator is low-turnover, liquid, diversified exposure with
costs controlled — which this engine already measures as a better risk shape, not alpha.

---

## Sources: reversal, trading costs, news versus no-news

### Jegadeesh (1990) — Evidence of Predictable Behavior of Security Returns
- **Source read:** https://www.jstor.org/stable/2328797 (abstract only; JSTOR is the journal's DOI-registered archive; Wiley behind a human check; no author/SSRN/NBER copy found)
- **Claim:** Monthly individual-stock returns have a highly significant negative first-order serial correlation; longer lags positive, strongest at 12 months.
- **Sample:** 1934–1987.
- **Effect size:** abstract: extreme-decile spread 2.49%/month (deciles on model forecasts, not raw last-month return).
- **Survived replication / costs?** Avramov, Chordia & Goyal's 2004 draft sets the 2.49% beside a 2.45% institutional round-trip cost for illiquid, high-turnover stocks; Novy-Marx & Velikov's value-weighted one-month reversal: 0.37%/mo gross, −1.28% net.
- **For a small account:** gross long–short with full monthly turnover — nothing supports a net long-only edge.
- **Testable with free data?** The raw-reversal leg: French "10 Portfolios Formed on Short-Term Reversal", "Short-Term Reversal Factor".

### Lehmann (1990) — Fads, Martingales, and Market Efficiency
- **Source read:** https://www.nber.org/papers/w2533.pdf (NBER WP 2533, full text) + https://academic.oup.com/qje/article-abstract/105/1/1/1928416 (published abstract)
- **Claim:** A week's winners and losers reverse the following week; the abstract blames inefficient markets for liquidity around large price changes.
- **Sample:** all NYSE/AMEX stocks, CRSP daily, July 1962–December 1986.
- **Effect size:** 1.79%/week (t=41.07), positive in 93.4% of 1,276 weeks (Table 1A); four-day-return weights (a bid-ask-bounce guard) 1.21%/wk; lags 2/3/4 earn 0.50/0.18/0.11%/wk — the effect is front-loaded in week one.
- **Survived replication / costs?** 26-week totals (Table 5A): 0.466 gross, 0.388 at 0.10% one-way, 0.154 at 0.40%; the four-day version ≈ zero at 0.40%; turnover ≈ $3/week per $1 long.
- **For a small account:** a week-one effect needing ~$3 of trading per $1 long every week; 0.40% one-way is his own retail-broker figure.
- **Testable with free data?** Needs daily stock-level prices (no weekly French series).

### Avramov, Chordia & Goyal (2006) — Liquidity and Autocorrelations in Individual Stock Returns
- **Source read:** published JF article, author-hosted via https://sites.google.com/view/agoyal145 (full text) + https://users.nber.org/~confer/2004/mmsu04/goyal.pdf (2004 draft)
- **Claim:** Reversals sit mainly in losers and in high-turnover, illiquid stocks — exactly where trading costs exceed the gross profit.
- **Sample:** CRSP NYSE–AMEX 1962–2002; TAQ spreads 1988–2002.
- **Effect size:** extreme high-turnover illiquid losers +1.16%/wk; loser−winner 1.33%/wk (Table VII); relative-strength weights 2.69%/wk (Table VIII).
- **Survived replication / costs?** Mostly no: 1.33% nets −5.26%/wk after Keim–Madhavan costs and −1.09% after price impact; only basis points survive in the liquid, low-turnover cell.
- **For a small account:** even a ~$60,000 book loses the illiquid long–short profit to price impact.
- **Testable with free data?** Amihud illiquidity needs only daily price and volume; French "25 Portfolios Formed on Size and Short-Term Reversal" covers size.

### Nagel (2012) — Evaporating Liquidity
- **Source read:** https://www.nber.org/papers/w17653.pdf (NBER WP, full text) + https://academic.oup.com/rfs/article-abstract/25/7/2005/1602153 (published abstract)
- **Claim:** Short-term reversal returns proxy the return to providing liquidity; time-varying and predictable with the VIX.
- **Sample:** CRSP daily, January 1998–December 2010; days t−1…t−5 reversal, market-hedged.
- **Effect size:** 0.30%/day on closing prices vs 0.18%/day on quote midpoints (much is bid-ask bounce, Table 1); +1pp daily-normalised VIX adds 0.22pp/day (Table 2); fell below 0.2%/day by 2007, spiked in the crisis; large liquid stocks earn ≈ zero.
- **Survived replication / costs?** Not tested — returns are "before costs of carrying out the trades": what liquidity PROVIDERS earn; liquidity takers pay it.
- **For a small account:** a market-order buyer pays exactly the spread this harvests; the horizon is days, not 21 trading days.
- **Testable with free data?** French "10 Portfolios Formed on Short-Term Reversal [Daily]" + VIX history.

### Novy-Marx & Velikov (2016) — A Taxonomy of Anomalies and Their Trading Costs
- **Source read:** https://mysimon.rochester.edu/novy-marx/research/ToAatTC.pdf (author-hosted, Aug 2015, full text) + https://www.nber.org/papers/w20721.pdf (NBER WP, Dec 2014, full text) + https://academic.oup.com/rfs/article-abstract/29/1/104/1844518 (published abstract)
- **Claim:** Anomalies turning over more than 50% a month rarely survive trading costs; short-run reversal is among the worst.
- **Sample:** CRSP NYSE/AMEX/Nasdaq, 07/1963–12/2012; value-weighted deciles, NYSE breakpoints; small-trader effective-spread costs, no price impact.
- **Effect size (short-run reversal, Table 3 Panel C):** gross 0.37%/mo (t=1.71); four-factor alpha 0.45% (t=2.22); turnover 90.9%/mo; trading cost 1.65%/mo; **net −1.28%/mo (t=−6.02)**.
- **Survived replication / costs?** No. With a 10%/50% buy/hold band: cost 1.00%, net −0.72%. With all three cost-cutting techniques: net −0.17% (t=−1.29). **By size (NBER Table 13C), gross/net: micro 1.05/−1.90; small (20th–50th NYSE percentile) 0.41/−0.84; large 0.18/−0.51.** The one reversal variant that survives: industry-relative reversal among low-volatility stocks, net +0.28%/mo (t=2.41).
- **For a small account:** these are already small-trader costs and the net is still negative.
- **Testable with free data?** Gross via French "Short-Term Reversal Factor"; net needs per-stock spread estimates.

### Chan (2003) — Stock price reaction to news and no-news
- **Source read:** https://users.nber.org/~confer/2001/bfs01/chan.pdf (NBER conference draft, May 2001, full text)
- **Claim:** After big monthly moves, stocks with public news (especially bad news) keep drifting; extreme no-news moves partly reverse next month, mostly in small stocks.
- **Sample:** random ~1/10 of CRSP stocks, 1980–1999, Dow Jones headlines.
- **Effect size:** no-news losers +0.7% next month after −13.7%; no-news winners −0.6% after +16.3% (Table 6); news losers do not rebound, −3.3% by month 12. Removing stocks ≤$5 makes the no-news reversal weak and insignificant; the news-loser drift holds (−3.9%, t=−3.8).
- **For a small account:** buying losers whose drop came with news bets against the drift; the no-news rebound is ≈0.7% gross, mostly in low-priced names.
- **Testable with free data?** Needs a dated headline source to split news from no-news.

### Bali, Cakici & Whitelaw (2011) — Maxing Out: Stocks as Lotteries
- **Source read:** https://www.nber.org/papers/w14804.pdf (NBER WP, March 2009, full text; JFE page refused access)
- **Claim:** Stocks with an extreme one-day gain last month earn low returns next month — a preference for lottery-like stocks.
- **Sample:** CRSP, July 1962–December 2005.
- **Effect size:** value-weighted high−low MAX decile −1.03%/mo (t=−2.83), four-factor alpha −1.18% (t=−4.71); controlling for prior-month return −0.81 raw / −0.98 alpha (value-weighted). MAX and MIN correlate 0.55.
- **For a small account:** mostly a list of stocks to AVOID buying.
- **Testable with free data?** Yes, daily returns only; no French series.

### Hong, Lim & Stein (2000) — Bad News Travels Slowly
- **Source read:** https://www.nber.org/papers/w6553.pdf (NBER WP, May 1998, image scan read page by page)
- **Claim:** Six-month momentum is strongest where news spreads slowly — small (not the tiniest) stocks and low analyst coverage — and mostly on the loser side.
- **Sample:** CRSP with I/B/E/S coverage, 1980–1996.
- **Effect size:** 0.53%/mo overall (t=2.61); peaks at 1.43%/mo in the third NYSE/AMEX size decile, 1.05% of it from losers; low-coverage stocks 1.13%/mo vs 0.72% high coverage (difference 0.42%, t=3.50).
- **For a small account:** low-coverage losers tend to keep falling for months — the opposite of a reversal bet.
- **Testable with free data?** Size side via French "25 Portfolios Formed on Size and Momentum"; coverage needs I/B/E/S.

**Cluster takeaway (reversal, costs, news):**
1. The gross reversal is real but front-loaded and narrow: week one carries most of it; it concentrates in illiquid losers; much is bid-ask bounce; Chan's no-news rebound fades above $5.
2. Net of costs a liquidity TAKER loses almost everywhere: Novy-Marx & Velikov's one-month reversal nets −1.28%/mo (−0.84% in the 20th–50th NYSE-percentile bin); the one survivor is industry-relative reversal in low-volatility stocks (+0.28%/mo net, pre-publication).
3. Why the stock moved decides the sign: drops that came with news keep drifting; only no-news drops rebound; big up-movers carry a lottery (MAX) drag.
4. Regime matters: reversal returns rise with the VIX.
5. For S&P 400/600 big movers held ~21 trading days, long-only, small account: prior ≈ zero to negative net. A test should skip day 1, charge the effective spread on entry and exit, split news from no-news, and log the VIX at entry.

---

## Sources: drift, momentum, decay, replication

### Ball & Brown (1968) — An Empirical Evaluation of Accounting Income Numbers
- **Source read:** https://www.jstor.org/stable/2490232 (first page only) + the authors' 2019 retrospective slides hosted by Wharton: https://jacobslevycenter.wharton.upenn.edu/wp-content/uploads/2019/09/Ball-and-Brown-Presentation.pdf (full slides, not the paper)
- **Claim:** Earnings news matters to prices, but prices mostly anticipate it; the announcement reaction is small and prices keep drifting toward the surprise afterwards — "the first reported anomaly" (slide 12).
- **Sample:** 2,340 firm-years, 1957–65 (slide 9).
- **Effect size:** Fig. 1 (slide 11): good-news abnormal performance index ~1.06–1.08 and bad-news ~0.89–0.91 by month 0, small further drift to month +6 (read off the chart).
- **Survived replication / costs?** Authors' replication (slide 16, US, to 2017): long ΔEPS>0 / short ΔEPS<0 earns 27.88% over days −360…−1, 1.20% on day 0, 2.16% over days +1…+180; drift significant in 15 of 16 other countries (slide 15). Pooled decades, before costs — Martineau (2022) shows pooling hides the decay.
- **For a small account:** ~2% over 180 days, long+short, before costs, is thin once costs are paid.
- **Testable with free data?** Proxies only: global-q `sue_1`/`sue_6`, OSAP `EarningsSurprise`.

### Bernard & Thomas (1989) — Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?
- **Source read:** https://www.jstor.org/stable/2491062 (first page only; no author-hosted copy found)
- **Claim:** Tests whether post-earnings-announcement drift is a delayed price response or a risk premium; Martineau's Table A.1 classifies it as "delayed price response to earnings news".
- **Sample:** 1974–1986 (per Martineau Table A.1).
- **Effect size:** Own estimates not accessible. Page 1 quotes Foster, Olsen & Shevlin (1984): long top / short bottom unexpected-earnings decile for 60 trading days ≈ 25% annualized, before costs.
- **Survived replication / costs?** Hou, Xue & Zhang Table 3A (NYSE breakpoints, value-weighted, 1967–2016), SUE high-minus-low: 1-month hold 0.46%/mo (t=3.48), 6-month 0.16% (t=1.44), 12-month 0.08% (t=0.73); equal-weighted all-stock breakpoints 1.34/0.64/0.24% — the multi-month drift lives in microcaps. Martineau: no drift for non-microcaps since 2006.
- **For a small account:** Little left in liquid names; what remains sits where costs are highest.
- **Testable with free data?** Approximately: global-q `sue_1`/`sue_6`; OSAP `EarningsSurprise`.

### Jegadeesh & Titman (1993) — Returns to Buying Winners and Selling Losers
- **Source read:** https://afajof.org/issue/volume-48-issue-1/ + https://www.jstor.org/stable/2328882 (abstract only)
- **Claim:** Buying past winners and selling past losers earns significant returns over 3–12-month holding periods, not explained by systematic risk; part of the first-year return dissipates over the next two years (abstract).
- **Sample:** US stocks, 1964–1989.
- **Effect size (as cited by Hou, Xue & Zhang):** 6-month formation / 6-month hold 1.1%/mo (t=3.61).
- **Survived replication / costs?** Yes, smaller: Hou, Xue & Zhang Table 3A (value-weighted, NYSE breakpoints, 1967–2016) 6/6 momentum 0.82%/mo (t=3.50); 11/1 momentum 1.16% (t=3.99). Clears every Harvey, Liu & Zhu adjustment. No cost test in these sources.
- **For a small account:** Long-only winners are implementable, but Stambaugh, Yu & Yuan Table 1C puts most of momentum's alpha in the short leg (long 0.63 vs short −1.14%/mo).
- **Testable with free data?** Yes: French "10 Portfolios Formed on Momentum" and "Momentum Factor"; OSAP `Mom6m`/`Mom12m`; global-q `r6_*`, `r11_*`.

### Martineau (2022) — Rest in Peace Post-Earnings Announcement Drift
- **Source read:** https://cfr.ivo-welch.org/published/papers/martineau2021rest.pdf (full text, CFR-hosted April 2021 draft)
- **Claim:** Prices now absorb earnings surprises on the announcement day: no drift in large stocks (above the NYSE 20th size percentile) since 2006; in microcaps it disappeared in 2016 (analyst surprises).
- **Sample:** US stocks, price >$1, cap >$5M; I/B/E/S 1984–2019 (312,462 announcements) and Compustat 1973–2019 (593,654).
- **Effect size:** Table 3B, days 2–60 drift slope on surprise decile: non-microcaps 0.003*** in 1984–90, then −0.001, 0.000, −0.002** across 2006–19; microcaps 0.003–0.004*** through 2011–15, then 0.002 (n.s.) in 2016–19. Announcement-day reaction 6× stronger for large stocks in 2016–19 than in 1984–90.
- **Survived replication / costs?** Consistent with Hou, Xue & Zhang (value-weighted 6/12-month SUE sorts fail). No cost test.
- **For a small account:** No multi-week earnings drift left to harvest in liquid stocks.
- **Testable with free data?** Partly; analyst surprises need paid I/B/E/S.

### McLean & Pontiff (2016) — Does Academic Research Destroy Stock Return Predictability?
- **Source read:** https://afajof.org/issue/volume-71-issue-1/ (published abstract) + https://ivey.uwo.ca/media/3775549/pontiff.pdf (May 2013 working paper, full text)
- **Claim:** Predictability decays out of sample and more after publication; investors learn from the papers.
- **Sample:** 97 published cross-sectional predictors, US stocks, long-short extreme quintiles, mostly equal-weighted.
- **Effect size (published abstract):** returns **26% lower out of sample** and **58% lower after publication**; ~32 points attributed to publication-informed trading; bigger declines for predictors with higher in-sample returns; returns higher in high-idiosyncratic-risk, low-liquidity stocks.
- **For a small account:** Budget about 42% of a paper's in-sample spread after publication — and that is equal-weighted, before costs, concentrated in illiquid names.
- **Testable with free data?** Yes, via OSAP returns and its signal documentation (sample and publication years).

### Hou, Xue & Zhang (2020) — Replicating Anomalies
- **Source read:** https://global-q.org/uploads/1/2/2/6/122679606/houxuezhang2020rfs.pdf (published RFS version, authors' site) + https://www.nber.org/papers/w23394.pdf (2017 working paper)
- **Claim:** Most anomalies fail once microcaps are controlled with NYSE breakpoints and value weights; survivors are much smaller than originally reported.
- **Sample:** 452 anomalies; NYSE/Amex/NASDAQ, January 1967–December 2016.
- **Effect size:** **65% fail |t|≥1.96; 82% fail the 2.78 hurdle** (abstract). **Trading-frictions anomalies: 102 of 106 fail** (introduction). **Microcaps are 3.2% of market cap but 60.7% of stocks.**
- **Survived replication / costs?** This is the replication; microcap anomalies called "difficult to exploit" because of costs (§2.2).
- **For a small account:** Trust only evidence built with NYSE breakpoints and value weights.
- **Testable with free data?** Yes: global-q testing portfolios (201 anomalies, value-weighted, NYSE breakpoints, 1967–2025).

### Harvey, Liu & Zhu (2016) — …and the Cross-Section of Expected Returns
- **Source read:** https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF (published RFS version, author-hosted)
- **Claim:** After hundreds of factor tests, t>2 is far too low; "a new factor needs to clear … a t-statistic greater than 3.0"; most claimed findings are likely false.
- **Sample:** 316 factors from 313 papers.
- **Effect size:** Bonferroni hurdle 3.78 (2012) rising to 4.00 by 2032; false-discovery hurdle 2.78 at 5%; 3.18 once unpublished trials are allowed for; of 296 significant factors, 80–158 are false discoveries.
- **For a small account:** Every variant you try raises your own bar; demand t≥3 and count your trials.
- **Testable with free data?** A rule, not a signal.

### Stambaugh, Yu & Yuan (2012) — The Short of It: Investor Sentiment and Anomalies
- **Source read:** https://www.nber.org/papers/w16898.pdf (2011 working paper, full text) + https://experts.umn.edu/en/publications/the-short-of-it-investor-sentiment-and-anomalies/ (published abstract)
- **Claim:** Anomalies reflect overpricing that short-sale limits keep alive; every anomaly is stronger after high sentiment, through the short leg.
- **Sample:** 11 anomalies, value-weighted deciles, 1965–2008, Baker-Wurgler sentiment.
- **Effect size:** Combined FF3 alpha 0.87%/mo: long leg 0.28, short leg −0.60 (Table 1C); 78% of short-leg profit comes after high sentiment.
- **For a small account:** Long-only gets the smaller leg (0.28 of 0.87%/mo).
- **Testable with free data?** Yes: Baker-Wurgler sentiment on Wurgler's NYU page; OSAP has most legs.

**Cluster takeaway (drift, momentum, decay, replication):**
1. Decay: published long-short returns run 26% lower out of sample and 58% lower after publication — and those are equal-weighted, before costs.
2. Replication: with NYSE breakpoints and value weights, 65% of 452 anomalies fail at |t|≥1.96 and 82% at 2.78; microcaps carry much of what papers report.
3. Hurdle: require t>3 for any new signal, and count your own trials.
4. Post-earnings drift is the warning case: gone in non-microcaps since 2006.
5. Short leg: most anomaly profit is on the short side; a long-only small account gets the weaker leg. Value-weighted, only price momentum and 1-month SUE clear t=3 in 1967–2016, before costs.

---

## Sources: method and multi-market premia; retail outcomes (regulators and academic)

### Fama (1998) — Market efficiency, long-term returns, and behavioral finance
- **Source read:** Shandong University copy of the published JFE 49:283–306: https://www.econ.sdu.edu.cn/__local/C/49/1B/348A9A139B45B4C6EB103B73C11_2BD6154A_21916.pdf (full text; ScienceDirect returned 403)
- **Claim:** Long-horizon anomalies split about evenly between over- and under-reaction, and most disappear under reasonable changes of method — what chance plus model error would produce.
- **Sample:** a survey of event studies (IPOs, SEOs, mergers, splits, repurchases, listings, dividend changes, spinoffs, proxy fights).
- **Method point:** model error compounds with horizon; prescribes calendar-time portfolios (each month, average the abnormal returns of every firm in its event window, so the time-series variance absorbs cross-firm correlation). Value-weighting shrinks anomalies: acquirers −0.25%/mo (t=−3.49) equal-weighted vs −0.11% (t=−1.55) value-weighted. The survivors he names — post-earnings drift and short-term momentum — are both stronger in small stocks.
- **For a small account:** count independent calendar periods, not trades; run a value-weighted check; distrust edges that live only in tiny stocks.
- **Testable with free data?** Yes — event dates, returns, a benchmark.

### Mitchell & Stafford (2000) — Managerial decisions and long-term stock price performance
- **Source read:** https://www.jstor.org/stable/10.1086/209645 (abstract, pp. 287–294, 325–326)
- **Claim:** Multi-year buy-and-hold abnormal returns with bootstrap inference assume independent events; overlapping events are positively cross-correlated, "producing test statistics that are up to four times too large". After the correction almost no reliable abnormal performance remains.
- **Sample:** 4,911 SEOs, 2,421 repurchases, 2,193 acquisitions, CRSP, 1958–93.
- **Method point:** t-statistics commonly fall from above 6 to below 1.5 once cross-correlation is handled; calendar-time portfolios have more power than corrected BHARs; for SEOs the 3-year abnormal return is −7.9% equal-weighted vs 0.0% value-weighted.
- **For a small account:** bets with overlapping horizons are not independent — aggregate to one portfolio return per period before testing.
- **Testable with free data?** Yes.

### Moskowitz, Ooi & Pedersen (2012) — Time series momentum
- **Source read:** https://pages.stern.nyu.edu/~lpederse/papers/TimeSeriesMomentum.pdf (author-hosted published JFE 104:228–250, full text)
- **Claim:** A futures contract's own past 12-month excess return predicts its next month; the effect lasts about a year then partly reverses; a diversified version earns abnormal returns with little exposure to standard factors and does best in extreme markets.
- **Sample:** 58 futures/forwards (24 commodities, 12 currency pairs, 9 equity indexes, 13 bond futures), 1965–2009.
- **Effect size:** all 58 positive, 52 significant at 5%; alpha ≈ 1.58%/mo vs MSCI World, SMB, HML, UMD; Sharpe above 1 (≈2.5× equities), 1.1 on the 1966–85 out-of-sample period. Gross of costs.
- **For a small account:** monthly, low turnover — but the Sharpe comes from diversifying across 58 instruments; a handful of ETFs captures less.
- **Testable with free data?** Partially, via ETF/index proxies.

### Asness, Moskowitz & Pedersen (2013) — Value and momentum everywhere
- **Source read:** https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf (author-hosted published JF 68:929–985, full text)
- **Claim:** Value and momentum premia appear in all eight markets studied, co-move across them, and are negatively correlated with each other.
- **Sample:** liquid stocks in the US, UK, Europe, Japan (1972/74–2011); country index futures, currencies, government bonds, commodities.
- **Effect size:** across all asset classes, Sharpes 0.72 (value), 0.74 (momentum), 1.59 (50/50 combination), correlation −0.60; US stocks alone 0.29 / 0.33 / 0.63. Gross — the authors say gross returns overstate practical profits.
- **For a small account:** single-market legs ≈0.3 Sharpe before costs; the strength is breadth plus the negative correlation, which a small long-only account can only approximate.
- **Testable with free data?** Partially (US and ETF proxies).

## Official evidence on retail outcomes
- **ESMA (EU), 27 Mar 2018:** 74–89% of retail CFD accounts typically lose money; average losses €1,600–€29,000 per investor (figures from national regulators' studies). https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors · ESMA35-43-1000.
- **AMF (France):** >89% of retail CFD investors lost money over 2009–2013; average loss €10,887; the most active lost most; no learning curve. AMF decision of 1 Aug 2019.
- **FCA (UK), CP16/40 (Dec 2016):** 82% of sampled clients at 8 CFD/spread-bet/FX firms lost money over one year; average −£2,200; clients with 100+ trades lost £3,500 on average vs £400 for fewer. https://www.fca.org.uk/publication/consultation/cp16-40.pdf
- **CFTC (US):** "Over the past year, about one-third of customers at registered OTC forex dealers made a profit, while two-thirds lost money" (Q2 2021–Q1 2022; break-even counted as not profitable). https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/CustomerAdvisory_MustKnowForex.html
- **SEC (US), 2000 day-trading study:** "The Staff did not determine whether day trading was generally profitable or unprofitable." No SEC or FINRA retail options/day-trading outcome rates found.
- **SEBI (India):** (a) 23 Sep 2024: 93% of >10 million individual F&O traders lost over FY22–FY24 (≈₹2 lakh each incl. costs); only 1% made more than ₹1 lakh after costs; prop traders and FPIs profited, 96–97% of it via algorithms. https://www.sebi.gov.in/sebi_data/attachdocs/sep-2024/1727086965496.pdf (b) Jul 2024 intraday cash: 71% of 6.9 million intraday traders lost in FY23; 80% among 500+ trades/yr; costs added 57% to losers' losses. (c) Aug 2026 FY25–FY26: loss-makers 90.9% (FY25), 87.7% (FY26); options 87.7% vs futures 66.0%; algorithms earned 99% of FPI/prop profits. https://www.sebi.gov.in/sebi_data/attachdocs/aug-2026/1787233506209.pdf
- **BIS Bulletin 69 (Feb 2023):** a model, not account data — a majority of crypto-app investors in nearly all economies probably lost money on bitcoin (2015–22).
- **Barber, Lee, Liu, Odean & Zhang (Taiwan, 1992–2006):** profitable day traders ≈5% by headcount; >75% quit within two years; aggregate −7 bp/day before costs, −23.9 bp/day after; predictably profitable under 3% on an average day. https://faculty.haas.berkeley.edu/odean/papers/day%20traders/day%20trading%20and%20learning%20110217.pdf
- **Barber, Lee, Liu & Odean, "The Cross-Section of Speculator Skill":** ≈13% profitable net of fees in a typical year; under 1% predictably outperform.
- **Chague, De-Losso & Giovannetti, "Day trading for a living?" (Brazil, abstract only):** of those who day traded index futures for 300+ days, 97% lost money and 0.4% earned more than a bank teller's wage. https://repositorio.fgv.br/items/e87d04fc-4b4c-4a56-ab5a-1c84c1afde1b/full

**Landscape doc vs official sources:** "most retail traders lose" is supported for leveraged, short-dated products (CFDs 74–89%, India F&O 87.7–93%, Brazil 97%), lower for others (CFTC forex two-thirds, India futures 66%, India intraday 71%). The doc's 5–15% "success = $50K+/yr consistently" rates have NO support: the nearest measured thresholds are ~1% or less (SEBI 1% over three years; Brazil 0.4%; Taiwan <1% predictably profitable). No official source measures retail swing-trading outcomes. No official global participant counts exist.

**Where a small operator plausibly has room (sources vs inference):** sources state losses grow with turnover, leverage and short horizons, and that the winners in those markets are institutions and algorithms; the premia that survive careful testing are slow, diversified, in liquid instruments (trend and value+momentum reach Sharpe 1.1–1.6 only diversified across asset classes; a single US leg ≈0.3, gross). Inference: no source shows room in intraday trading, short-dated options, CFDs or retail forex; any room is in low-turnover, multi-week horizons in liquid instruments, with cost and behaviour discipline and calendar-time, value-weighted, out-of-sample testing — not speed or information.

**Note on this repo's Arc 5 verdict:** its pooled bar treated bets with overlapping horizons as independent; Mitchell & Stafford show overlap inflates significance. A correction could only widen the error bars — it cannot turn the FAIL into a pass.

---

## Access notes

- Read as abstract only: Jegadeesh (1990), via JSTOR's archive of the journal — whether that counts
  as official is the owner's call; Ball & Brown (1968) and Bernard & Thomas (1989) first pages only.
- Numbers from working-paper versions (NBER, SSRN-equivalent, author drafts): Lehmann, Nagel,
  Novy-Marx & Velikov, Chan, Bali et al., Hong et al., McLean & Pontiff, Stambaugh et al.
- Blocked and not bypassed: Wiley and SSRN human checks, ScienceDirect, one MIT repository.
- Chague, De-Losso & Giovannetti read as an abstract on the university repository.
