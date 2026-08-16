# claude_trader — operating contract

## What this is
A trade-signal research project. GOAL: find real, durable edges and trade them —
and learn to build well in the process. STATUS: hypothesis stage. No signal here
has been shown to make money. The v1 scaffolding from that unvalidated build was DELETED
2026-08-02 — it is in git history if a part is ever wanted, not on disk to be mistaken for live.

## Prime directive
Goal is WEALTH. Rigor serves money, not the other way round. Validate edge before
building. The unit of work is a falsifiable question with a yes/no answer from
data — not a feature. If a task can't end in a number or a passing check, it
isn't ready to start. Run a SMALL PORTFOLIO of cheap falsifiable tests in
PARALLEL, not one at a time. Rigor lives in how each is judged, not in queuing
them. Don't inflate one threat into a blocker — measure it, then move.

## The Socratic layer (why this project is shaped the way it is)
Neither the human nor the model is presumed correct. Every claim — a signal, a
threshold, a "this works" — must survive a test against real data. We encode that
humility into the system itself: capture first, judge later, let outcomes decide.
(This discipline may one day be worth extracting as its own project. Not yet.)

## The loop (every change)
1. Propose in plain language.  2. Wait for approval.  3. Make the smallest diff
that answers ONE question.  4. Verify — show the number or the passing test.
5. Commit. If you can't show the number, it isn't done. Never claim success
without the evidence in hand.
**Lanes [reconciled 2026-08-08, owner-delegated — resolves the propose-first vs
drive-autonomously contradiction]:** RUNNING the system (reads, settles, scoring, logging,
ledger/doc upkeep, committing evidence) = autonomous, report after. CHANGING the system
(code, rules, bars, contracts) or MOVING real money = propose first; the broker step is
human-gated by construction. Steps 1–2 above govern the second lane, not the first.

## Anti-over-engineering (hard rules)
- No building for the future. No feature without a present, validated need.
- Delete, don't defer-with-plumbing. No enums/abstractions/config for the unused.
- Cap output at what one busy human can review in the time he has.
- Prefer removing code to adding it. The best change is often a smaller system.
- Reuse free, proven data/tools before building your own (e.g. yfinance).

## Verification & honesty
- Every quantitative claim is backed by a reproducible number.
- Backtests: out-of-sample / walk-forward, realistic costs (commission + slippage),
  FEW parameters. Guard against lookahead and survivorship bias. A backtest you
  can't explain in five lines is suspect.
- Report failures plainly. Flag untestable assumptions (e.g., signals with no
  cheap history). No plausible-completeness.

## Accountability — both of us are watched
Neither the human nor the model is presumed right; the data decides. We build the
check into the process so neither can quietly drift:
- **Pre-register** the hypothesis AND the pass/fail threshold BEFORE running. No
  moving the goalposts to fit the result. No p-hacking by trying variants until one
  "works" (those need fresh OOS data to survive).
- **Red-team every result** with a separate pass (/code-review, Explore agent, or a
  deliberate adversarial reread) before it's trusted — ESPECIALLY backtests. State
  the residual risks plainly; a finding with no stated weakness is not done.
- **Log it or it didn't happen.** Every test — win OR loss — gets one short entry in
  `research/FINDINGS.md` with its number and its caveat. That file is the audit
  trail and the digest for cold future sessions; keep it short and current.
- The human's claims get the same test as the model's. "I know this works" is a
  hypothesis, not a result, until the number is in the log.

## Signals are building blocks (trade-as-a-story)
One mechanical signal is a part, not the system. Real edge lives in the trade's
story — WHY it moved (market-wide vs name-specific), the catalyst, the regime.
Context is what cuts the fat tail (the rare big losses that the average hides).
Earn each added filter: keep it only if it shrinks the tail or lifts edge OUT OF
SAMPLE. Simple stays the baseline; complexity pays rent.

## Cost discipline (discipline, not fear)
- Cheap is a discipline, not a fear. Don't spend or build before the math is
  straight — that's how you fool yourself. But paid data/spend IS allowed when
  evidence shows it buys edge: name the trigger that unlocks it. Refusing a
  justified spend is as wrong as a premature one.
- One agent by default. Multi-agent only for genuinely parallel work (4–220x tokens) —
  reviews qualify: blind micro-independent runs + one cross-model control (the amended
  independence rule, 2026-08-07; see SKILL).
- Local-first, free data first. Keep LLM calls out of the DETERMINISTIC path (triggers,
  settles, scoring, money math) — the READ layer is an LLM by design; it is the hypothesis
  under test, scored deterministically.

## Communication
Least words possible. Lead with the answer. Short sentences. No preamble, recap,
hedging, or niceties. Be direct. Caveman = brevity, not stupid.

## Where things are
- `README.md` (top level) — the single control panel: every live command + what's where.
- `python3 -m research` — live status: scoreboard + forward bets + dual-momentum signal.
- `research/FINDINGS.md` — READ FIRST. The digest: every test, its number, its verdict
  (closed-arc log entries live verbatim in `research/FINDINGS_ARCHIVE.md` — reach back only when
  re-examining old evidence).
- `research/engine.py` — `python3 -m research.engine`: the falsification scoreboard (every
  probe + verdict + multiple-testing reality check). The project's honest state at a glance.
- `research/SKILL.md` — the reusable METHOD (the asset): the loop + rules earned from losses.
- `research/LOOP.md` — the autonomous research loop (run via `/loop`). `research/READ_LOOP.md`
  — the FORWARD generation loop: reads live situations, pre-registers a BATCH of bets (the
  active frontier now that the mechanical mine is closed).
- `research/bets.py` (+ `bets_catalogue.csv`) — forward-bet catalogue (Claude's pre-registered
  future calls, scored vs benchmark). ONE pooled general verdict (FINDINGS Arc 5 #7, supersedes
  #1/#5); horizon (`horizon_d ≤ 30` = the **fast 21d sleeve**, else the 63/126d **core**) AND
  `pattern_tag` (the SCENARIO TYPE) are DIAGNOSTIC decompositions of that one verdict, NEVER
  separate per-tag/per-horizon bars [Arc 5 #8]. `research/movers.py` (+ `movers_ledger.csv`) — the
  daily mover scan, TWO cohorts since [ARC 5 #11]: S&P 500 (unchanged) + an S&P 400/600 TAIL cohort
  (committed caches; `universe` column = a DIAGNOSTIC lens, never a per-universe bar) = the general
  catalogue's candidate DENOMINATOR (`scan`/`decide`/`settle`/`show`):
  logs every big mover take/skip so a pass can't be selection-cherry-picked (the [Arc 5 #7] fix —
  bounds selection, doesn't eliminate it). `settle` scores take AND skip forward vs SPY at 21/63d
  [ARC 5 #9] — a DIAGNOSTIC calibration of the skip filter ("is the read too conservative?"), NOT an
  EDGE verdict silo; prior UNCHANGED, pre-registered threshold locked. Early read logged in
  FINDINGS 2026-08-01(d) (adverse sign at tiny n); bar is skips-63d at N≥30 — watch, do NOT act;
  live state → `python3 -m research.movers show`.
  `research/dualmom.py` — the one banked result (risk SHAPE, not alpha — it tied its own
  Sharpe bar; status in SKILL, re-validate before sizing up).
- **Arc 3 (the insider silo) is CLOSED — the project runs on ONE verdict silo, and that is now
  the honest, stated design rather than an unnoticed degradation [2026-08-02].** It logged NULL on
  its OWN kill-criterion: a 126d verdict horizon against a 2026-12-31 deadline meant the N=20
  branch became unreachable after ~2026-07-08, and only 2 takes were ever logged. The candidate
  stream itself audited CLEAN ([ARC 3 #1d]: 0–2 entity-stack artifacts of 18 against a ≥7
  threshold) — it ran out of calendar, not credibility. All `insider*.py`, the ledger, and the
  EDGAR/SEC caches were DELETED; the evidence lives in `FINDINGS.md` and the code in git history.
  **Do not rebuild it without a fresh pre-registration** — and if you do, two findings are already
  paid for: the 3-distinct-insider trigger is holed by entity stacking (one investor's GP + LP trip
  it on a single Form 4 — real, but it never fired through openinsider), and **IPO-allocation
  filings are the larger false-positive mode** (5 of 18 candidates; exclude filings priced at an
  offer price near an IPO date). FINDINGS [ARC 3 #1b]–[ARC 3 #1d].
- **SCOPE — TWO REALMS, and this repo is only one of them [2026-08-02].** claude-trader is the
  **SHORT-SWING** realm: days-to-weeks reads, benchmark-scored, accruing toward a verdict.
  **LONG-TERM WEALTH lives in its own FULLY-PRIVATE repo** — its pre-registered policy, its
  holdings, and all personal-finance context stay there and are NEVER restated in this repo
  (this repo is being prepared for public release; long-realm facts here are a leak, not a
  convenience). Separate research, separate actions, **markdown pointers only — neither side
  imports the other.** The book holds capital that is tradeable AND chosen; if a holding's next
  decision point is measured in YEARS it is not ours. Do NOT research long-realm holdings,
  personal comp-plan mechanics, or multi-year tax milestones in this repo — that is how a session
  got spent on a position that did not exist (FINDINGS 2026-08-02). Marginal-dollar ranking
  recorded there, not here. **Standing conflict-of-interest exclusion: SPCX is NEVER a scored,
  held, or recommended leg in this repo** (owner rule 2026-08-02; the reason is recorded in the
  private realm) — this line is the guard the cloud read routine relies on.
- `research/orders.py` (+ `orders.csv`, tracked) — the WORKING-ORDER bridge from a read to real
  money: `place/placed/check/cancel/pulled/show`. A real-money entry is a **LIMIT with an expiry**, computed by
  code from the last COMPLETE bar, sized by a per-trade RISK UNIT capped by free cash [ORDERS #2]
  (band + sessions + risk unit live in `config.py`, the one place they do).
  Replaces the point entry price, which decayed 1.07% by the next open and 2.42% by the next close
  on the median taken mover, with a −23.4% tail [FINDINGS 2026-08-03]. `check` resolves against
  real bars and the digest **re-pushes a pending order daily** — a limit is age-invariant, which
  the quoted price was not. Logs fills AND no-fills so the band itself is scorable: **DIAGNOSTIC
  only, never an edge verdict** ([ORDERS #1] pre-registration, N≥20, +3pp bar; reachability
  deadline pre-registered 2026-08-08 after audit #1: if N<20 by 2026-12-31, declare the bar
  UNREACHABLE and re-scope openly — declare, don't decorate, the Arc-3 lesson). An expired order
  is NOT re-issued at a new price. **`placed_at` separates a real order from a counterfactual:**
  unstamped, a fill only says what the market did; stamped, it is money that moved and needs a
  `book open`. **Our expiry is a MODEL; his GTC limit is REAL** — an order that expires (or that we
  cancel) while carrying `placed_at` may still be working at the broker and can fill into a position
  no ledger expects, so the digest nags until `pulled TICKER` records that the human took it off
  [2026-08-04]. Holding that ticker does NOT silence it: that is the case where a stale limit doubles
  a position.
- `research/book.py` (+ `book.csv`, **tracked in git — evidence ledger, public by owner decision [P8, 2026-08-15]**) — the
  REAL-MONEY LIVE BOOK: the small experimental account (both brokers; **TRADEABLE swing capital
  ONLY** — long-realm personal assets are out of scope, see above; size → `book show`, never
  restated here), REAL capital — external inflows FROZEN [2026-08-05, FINDINGS; "no more
  paper/roleplay" (2026-07-06) stands] — sized positions, stops, cash, $ P&L marked vs same-$-in-SPY AND dual-mom [ARC 5 #7].
  SEPARATE from `bets.py` so real-money churn never pollutes the skill verdict (MORE important now, not less).
  Real-money stance [reconciled 2026-08-08, owner-delegated — resolves don't-lose-it vs
  size-aggressively]: ruin-bounded at the POOL level (−40% stop, inflows frozen),
  conviction-sized at the POSITION level per the owner's loosened harness [ARC 5 #6] —
  bounded-loss aggressive exploration maximizes information per dollar while the prior stays
  LOW and the ledgers accrue. Supersedes the pre-#6 "don't-lose-it + cheap beta + capped
  experiments" phrasing. Rules: FINDINGS [ARC 5 #4]; sizing cap LIFTED, integrity guards kept [ARC 5 #6];
  `seed/open/close/stop/target/mark/snapshot/show` (`target` = the structured exit-into-strength
  level; the digest nags when spot crosses it [2026-08-04]). `book_equity.csv` (tracked) = the daily equity CURVE written by
  `snapshot`; `book.equity_marks()` is the ONE computation behind both `mark` and `snapshot` so the printed
  and logged numbers can't diverge.
- `research/cases/*.md` — the CASE-STUDY reasoning layer: WHY/HOW a notable move happened → a
  reusable pattern, each birthing one scored `bets.py` call (single source of truth — cases
  narrate, numbers stay in their silo). `research/ARCHITECTURE.md` — the layer map (how bets/
  cases/book/findings communicate). `research/BACKLOG.md` — engineering changelog + backlog +
  stale map (cold-session refresh, distinct from the FINDINGS science log).
- `scripts/daily.sh` — SETTLE script (scores matured bets + movers, commits the ledgers).
  Run by the cloud `/schedule` **settle** routine (PRIMARY — laptop often off, runs DAILY) and
  locally. Generation runs in the separate cloud **read** routine (`READ_LOOP.md`, PRE-MARKET
  weekdays — alerts must land before the open, never after the close).
  **Telegram contract: every scheduled run pushes ONE message — SILENCE = BROKEN; a clean weekday =
  exactly ONE 📋 (settle, the day's full state photo) + ONE 📖 (read, the MORNING BRIEF)
  [slim reshaped 2026-08-06 on user utility — FINDINGS [MSG]].**
  Both come from `research/digest.py` (HTML: fail-soft per silo, DO-NOW list with paste-ready
  commands). Settle's 📋 = everything: 💰 SINCE-LAST band (what CHANGED vs git HEAD — no state
  file, no `settled_at` column [2026-08-04]) + full book + orders + bets/movers state. Read's 📖
  (`--slim`) = DO-NOW + the FULL book (every position with $ P&L and stop/target distance —
  "where do I stand?" must be answerable from the one message the human reads) + the run note +
  🟢 WORKING ORDER for idle cash; it drops what settle owns (band, 🎯/📡 one-liners, ORDERS
  block, 📋 banner). READ_LOOP step 5: human places the LIMIT at broker + confirms the real fill
  via `book open`; settle re-pushes a pending order daily, `orders check` resolves it — and a
  fill the human books FIRST flips the nag to a one-line FYI (`orders.booked`, 2026-08-06), and
  a booked-then-CLOSED round trip stays cleared — a closed lot counts as booked [2026-08-09]. Plus
  🚨 per scored settlement; the 🚨 heartbeat (`research/heartbeat.py`) fires ONLY when a step or
  the digest push failed — NEVER as a ✅ success ping (one arrived 2026-08-05; it is a contract
  violation). Transport: `research/notify.py` (fail-soft, HTML + truncation + plain retry,
  TELEGRAM_* env). **The digest prints a delivery VERDICT and that line is the only truth about
  delivery [2026-08-06]: exit 1 ≠ undelivered — a routine re-sends ONLY on `PUSH REJECTED
  (nothing sent)`, never on `PUSH UNCONFIRMED` (re-sending a maybe-delivered message is the
  2026-07-24 double-post; a "delivery check" copy + a bare "Probe" arrived 2026-08-06 that way);
  every push stamps `research/data/push_log.csv` (committed), and the next delivered message
  raises a DO-NOW when EITHER leg's last due push was never confirmed — settle daily, read on
  weekdays, each held against its own calendar [both legs since 2026-08-11; settle-only until
  then, which is why the 08-10 read died UNCONFIRMED — bet committed, alert never seen — behind
  a message that said "DO NOW: nothing"]. This is the transport failure the commit-watching
  watchdog cannot see, observed 08-05, 08-06 AND 08-10. A read whose push fails also fires the
  🚨 heartbeat, the parity with `daily.sh` the read leg lacked.**
  **Delivery is no longer ASSUMED [2026-07-27]:** a settlement's 🚨 is stamped in a `notified` column
  only after Telegram confirms, so a lost message is RE-SENT next run instead of vanishing with the
  row's open status; settle exits nonzero on a lost push. The digest fails LOUD — a dead silo, a
  stale feed (`research/feedstatus.py`), uncommitted/unpushed ledgers, or a stuck settlement each
  become a DO-NOW rather than prose. `research/watchdog.py` (its OWN routine, 36h) is the EXTERNAL
  dead-man's switch: every other alarm is emitted BY the daily run and so cannot fire when the daily
  run is what died — it NARROWS that blind spot, it does not close it (a dead platform kills both).
- Dormant (evidence, kept for reproducibility): the Arc-1/2 probes (`dip_index`, `vix_fear`,
  `disaster`, …). Every one is cited by a `Reproduce:` line in `FINDINGS_ARCHIVE.md` — that is
  WHY they stay. **DELETED 2026-08-02:** the v1 capture→settle→paper pipeline and `reference/`
  (nothing imported them, nothing cited them). Do not confuse the two sets: `momentum.py` and
  `universe.py` sat in the old "dormant" list and are LIVE (`movers.py` imports both).
- `FINANCES.md` — private baseline + experimental read (gitignored). API keys in `.env`
  (gitignored). Never commit or paste secrets/finances.

**Single source of truth (anti-drift convention):** live numbers live in ONE runnable silo and
docs reference the COMMAND, never restate the figure. Portfolio shares/cash/P&L → `python3 -m
research.book`; probe count + verdicts → `python3 -m research.engine`; forward bets → `python3 -m
research.bets show`. In committed `.md`, write the SHAPE/decision generically and point to the silo;
dated log entries in `FINDINGS.md` keep their then-true numbers (append-only evidence), everything
else stays generic. If you catch a hardcoded count/holding drifting, genericize it — don't re-sync it.
