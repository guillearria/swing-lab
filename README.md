# swing-lab

A trade-signal **research** project, run in public. An LLM reads live market situations and
pre-registers falsifiable calls — ticker, direction, horizon, benchmark, pass/fail bar —
BEFORE the outcome; a deterministic pipeline settles and scores every one against its
benchmark, wins AND losses, takes AND skips, so the record cannot be cherry-picked. Having
rigorously shown the free mechanical edges aren't there (see `research/FINDINGS.md`), the
project runs a **falsification engine** that kills bad ideas cheaply and surfaces the rare
lead. The ledger is the product. Live scoreboard: the GitHub Pages site of this repo.

> **Not investment advice.** This is an educational research log, not a recommendation
> service. Most results are paper/counterfactual; the experiment's premise is that no signal
> here is proven until its pre-registered bar passes. Do not risk money you cannot afford to
> lose. Past performance does not indicate future results. The author may at times hold
> positions in securities mentioned. Use at your own risk; the author assumes no
> responsibility for your trading results.

**Edge graduation (standing rule).** If a probe ever passes its pre-registered bar, its live
signal generation graduates to a private repo BEFORE real capital is sized on it; the
framework, the method, and this ledger stay public. (The freqtrade seam: engine public,
alpha private.) Until that day, everything is here.

License: MIT. This is the one place to see every command.

## See everything (start here)
```bash
python3 -m research            # live status: scoreboard + forward bets + signal
python3 -m research help       # this command index
```

## Live commands
| Command | What it does |
|---|---|
| `python3 -m research` | Live status panel (the dashboard) |
| `python3 -m research.engine` | Falsification **scoreboard** — every probe + verdict + multiple-testing check |
| `python3 -m research.bets show` | Forward-bet **catalogue** (Claude's pre-registered future calls) |
| `python3 -m research.bets add TICKER long 63 SPY "thesis" --tag=scenario` | Log a forward bet (tag = scenario type). **Admission is LONG-ONLY above a $5M median-dollar-volume floor, fail-closed, code-enforced [ARC 5 #12a]** — a REFUSED add is the rule working; shorts return only via the SKILL re-arm protocol |
| `python3 -m research.bets settle` | Score matured bets vs their benchmark |
| `python3 -m research.movers` | Daily mover scan, TWO cohorts (S&P 500 + the 400/600 **tail** [ARC 5 #11]) = the general candidate **denominator** (`scan` / `decide` / `settle` / `show`); `settle` scores take+skip fwd vs SPY = the "too conservative?" diagnostic [ARC 5 #9] |
| `python3 -m research.dualmom current` | Dual-momentum core — what to hold this month |
| `python3 -m research.book` | **The RETIRED real-money book [ARC 5 #12] — TERMINAL since 2026-08-18** (liquidated 08-17; closure FINDINGS [ARC 5 #13]/#13a — the account number is the owner's inherited book, not the system's verdict, which lives solely in the bets ledger): every command prints one BOOK CLOSED line; `book.csv`/`book_equity.csv` stay tracked as frozen evidence. Long-realm personal assets live in the private long-term repo, never here |
| `python3 -m research.orders show` | **COUNTERFACTUAL working orders [ARC 5 #12a]** — `place TICKER long\|short STOP H BENCH` computes the LIMIT off the last complete bar (no sizing — there is no cash; blank shares); `check` resolves pending orders against real bars (filled/expired) and scores both forward at 21d ([ORDERS #1] band diagnostic, N≥20 by 2026-12-31); `cancel TICKER "why"` kills a still-PENDING one. `placed`/`pulled` retired with the broker leg. A limit, not a quoted price — the point price it replaced decayed 1.07%/2.42% by the open/close [FINDINGS 2026-08-03]. **Every fill is a counterfactual by construction; the fill model is unverifiable against broker truth until real money returns** |
| `python3 -m research.tools.slippage_audit` | Reproduce the numbers behind the band + expiry (slippage medians, fill rate per band, sessions-to-fill) |
| `python3 -m research.notify "msg"` | **Manual Telegram test send — HUMANS ONLY, a routine never invokes this** (routines push via `digest --notify`; config status with no arg) — needs `TELEGRAM_BOT_TOKEN`+`TELEGRAM_CHAT_ID` in env, fail-soft when unset; HTML mode + newline-safe truncation + plain retry on rejected HTML |
| `python3 -m research.digest` | **THE per-run Telegram message** (HTML), **digest v3 [MSG 2026-08-18]** — a PULSE + ALARM channel: the plain-English scoreboard leads BOTH legs (**v3.1 2026-08-19: Scored / So far / To pass rows, every row counting the SAME bets so they add up; the bar is a COUNT — "17 of 30 beating" — and the median is words — "8.0% behind"**; 🏁 milestones + the ahead-of-bar flag ride it), then ⚠️ DO-NOW **only when nonempty** (paste-ready commands), the read's 🟢 NEW BET card(s) as one `<blockquote>` each, and the 📈 next-scoring line. Stats vocabulary (Σ/p/α), shorts, orders/band, movers denominators: CLI-side only. `--slim` = the read leg's push-log stamp (composition no longer branches on it). `--notify` prints a delivery VERDICT (`PUSH DELIVERED` / `REJECTED` / `UNCONFIRMED` — re-send ONLY on REJECTED), exits 1 on a non-delivered send, and stamps `research/data/push_log.csv` so a stranded push is flagged by the next delivered message |
| `python3 -m research.site` | **The PUBLIC DASHBOARD page [P7a]** — regenerates `docs/index.html` from the catalogue (stdlib, deterministic, no clock). **Audience contract (owner, 2026-08-15): end users get predictions + a performance summary, zero method prose** — tiles, cumulative-excess curve, per-prediction bars, FULL sortable/filterable catalogue (filters are views, never removals; no-jargon-leak + no-book/no-dollars both test-enforced). Regenerated + committed by the settle run |
| `python3 -m research.pulse` | **The X social pulse [P7b] — DETERMINISTIC AUTOPOST by policy** (BACKLOG P7b, 2026-08-15): code renders a post from the committed ledgers (newly scored verdict rows + 🏁 milestones, pool tally vs bar — verdict-grade numbers ONLY, never raw scan output) and daily.sh `--post`s it unconditionally; a per-post human approve would be publication-layer selection bias. ≤1 POSTED/UTC-day cap, tri-state delivery verdict stamped in `research/data/pulse_log.csv` (never re-post on UNCONFIRMED), "Not investment advice." standing. INERT until the owner sets `X_API_KEY`/`X_API_SECRET`/`X_ACCESS_TOKEN`/`X_ACCESS_SECRET` (local .env + settle trigger cloud env); bare invocation = dry-run print. LLM-authored prose stays out by construction (redlist + human gate lane) |
| `python3 -m research.heartbeat` | **Fallback 🚨 proof-of-life** — daily.sh fires it ONLY when a step or the digest push failed; on a clean day the digest IS the message |
| `python3 -m research.watchdog` | **External dead-man's switch** — 🚨 if no ledger commit in 36h. Runs from its OWN routine: every other alarm is emitted BY the daily run, so none can fire when the daily run is what died |
| `/loop run one iteration of research/READ_LOOP.md` | **Generate** a batch of pre-registered forward bets (the active frontier) |
| `/loop run one iteration of research/LOOP.md` | Run the **autonomous loop** (Claude generates → tests → red-teams → logs) |

## Automation (cloud routines — laptop-off-safe, the PRIMARY path)
Three scheduled cloud `/schedule` routines run the forward engine unattended:
- **settle** (DAILY): runs `scripts/daily.sh` → scores matured bets + movers (take/skip fwd vs SPY), commits the ledgers (free, deterministic, idempotent); pushes the 📋 digest (+ 📊 per scored settlement — 🚨 has meant FAILURE ONLY since v3); the 🚨 heartbeat fires only if a step or the digest push failed (NEVER a ✅ success ping).
- **read** (pre-market, Mon–Fri): runs one `research/READ_LOOP.md` iteration → reads live situations, pre-registers a batch (≤~10–15, a ceiling not a quota) of LONG-ONLY forward bets above the liquidity floor; every take-carrying run logs exactly ONE 🟢 COUNTERFACTUAL working order (`orders place` — a LIMIT with an expiry, unsized, nothing to execute [ARC 5 #12a]); commits; pushes the 📖 slim morning brief (`digest --slim`: run-note headline + 🎯 scoreboard + DO-NOW + book + 🟢 system take). A pending order is re-shown daily by **settle** until it fills or expires against real bars.

**Notification contract (2026-07-03; v2 2026-08-14; v3 2026-08-18 [MSG] — Telegram is a PULSE + ALARM channel): every scheduled run pushes ONE message — SILENCE = BROKEN; a clean weekday = exactly ONE 📋 SETTLE + ONE 📖 READ, plus ONE 📊 SCORED on days bets mature.** 📋/📖 = the scoreboard rows + ⚠️ DO-NOW (only when nonempty) + 🟢 NEW BET card(s) (read) + the 📈 line; 📊 = a scored settlement the moment it lands (`notified`-column delivery guarantee); 🚨 = FAILURE ONLY (a broken step or dead push → check `cron.log`); 📣 = the X mirror once P7b activates (locked requirement). ESCALATION beyond the daily two: only 🚨 failures · verdict events (🏁 milestones, PASS-CANDIDATE flip, pass/kill) · spend-gate proposals · anything genuinely needing a human.

- **watchdog** (daily, own hour, fresh session): runs `python3 -m research.watchdog --notify` → 🚨 only if no ledger commit has landed in 36h. It is deliberately NOT part of daily.sh: a check that runs inside the thing it watches cannot report that thing dying. **Honest limit: it narrows the blind spot, it does not close it** — if the scheduling platform itself dies, both routines go with it and nothing reports that.

Manage with `/schedule` (list / run / edit). Generation = `read`; scoring = `settle`; liveness = `watchdog`. They never overlap.
Bets pool into ONE general verdict (`python3 -m research.engine`); horizon (a **fast 21d sleeve** vs the 63/126d **core**) is a diagnostic label for faster feedback, not a separate bar [Arc 5 #7].

## The docs (what's where)
- **`research/ARCHITECTURE.md`** — the layer map: how bets / cases / book / findings communicate.
- **`research/cases/`** — case studies: why a notable move happened → a reusable pattern (each
  births a scored bet; listed in the status panel). First pair: ILLR + SPCX.
- **`research/FINDINGS.md`** — the research audit trail: every test, its number, its verdict. Read first.
  Closed-arc entries archived verbatim in `research/FINDINGS_ARCHIVE.md`.
- **`research/BACKLOG.md`** — engineering changelog + backlog + stale map (cold-session refresh).
- **`research/SKILL.md`** — the method + the rules earned from losses (the reusable asset).
- **`research/LOOP.md`** — how the autonomous research loop runs.
- **`CLAUDE.md`** — the operating contract (how the agent works on this repo).
- **`FINANCES.md`** — private baseline + experimental read (gitignored).
- **`research/book.csv`** — the live book's positions/cash/P&L (tracked in git — the experiment's evidence ledger, public by owner decision [P8]).

## The system in one breath
**Mechanical track (closed):** fixed rules backtested on history *instantly* → the engine
scoreboard (**zero confirmed** to beat buy-and-hold SPY risk-adjusted — proved where money
*isn't*, cheaply; the free mine is exhausted; live probe count: `python3 -m research.engine`). **Forward track (the active frontier, now AUTOMATED):**
Claude reads live situations and logs pre-registered bets vs a benchmark — generated in batch
by the scheduled `read` routine, scored later by the scheduled `settle` routine (weeks for the
21d fast sleeve, a quarter for the 63/126d core). The
one safeguard kept while scaling: pre-register every bet, log every candidate, never drop a
loser (that honesty is the only thing dividing this from a false-positive machine). Verdict
accrues to the bar in `FINDINGS.md` (Arc 5); if free-data reads can't clear it, that fires a
pre-registered paid-data spend trigger.

## Evidence (dormant — kept for reproducibility, not run day-to-day)
- **Arc-1/2 probes** (cited by `FINDINGS.md` `Reproduce:` lines): `dip_index`, `robust`,
  `decorrelate`, `sleeves`, `crypto_trend`, `vix_gate`, `vix_fear`, `fng_crypto`, `regime`,
  `portfolio`, `disaster`, `disaster_port`, `index_deletion`, `lockup`.
- **v1 capture→settle→paper pipeline** — **DELETED 2026-08-02** (`capture`, `news`, `db`,
  `backtest`, `paper`, `reference/`, `db/research.db`). Nothing imported them and no `Reproduce:`
  line cited them; git history has them. `momentum` and `universe` were wrongly listed with them
  until 2026-08-02 — both are **LIVE** (imported by `movers.py` on every scan), and `outcome` is
  imported by the archive-cited `dip_index`. All three stay.
