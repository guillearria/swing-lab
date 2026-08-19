# BACKLOG — engineering changelog · open work · stale map

The ENGINEERING/structure log, distinct from `FINDINGS.md` (the RESEARCH/science audit) and
from `python3 -m research` (live numbers). Purpose: a cold session can refresh on what changed,
what's queued, and what NOT to touch — in one screen. Newest first. Holds no live numbers.

## ▶ PICK UP HERE (2026-08-18, post-liquidation — book TERMINAL; cutover to swing-lab COMPLETE)

**State:** The book is CLOSED — owner liquidated at both brokers 08-17, ledger closed + retired
08-18; closure FINDINGS **[ARC 5 #13] + the #13a scope correction** (the account number −14.8%
vs SPY +4.6% is the OWNER's inherited book; the SYSTEM's verdict = the pooled bets ledger only;
system-originated trades +$15, n=4). Proceeds exited to the long realm (its §4 emergency fund).
The system is PURE PAPER until the [ARC 5 #7] pass. Cutover verified live 08-18: all three
routines commit to swing-lab (settle 08-17, read 08-18), Pages serves
**https://guillearria.github.io/swing-lab/** (HTTP 200), HQ board repointed, claude-trader frozen
with zero post-freeze commits. P7b pulse code landed, INERT (no X keys). The 08-15 queue's
deploy-key task is OBSOLETE (it served the retired mirror; Pages here needs no key) and its
Telegram-review item was overtaken by daily use. The 08-18 read ran DEGRADED (Yahoo nulled the
08-17 closes) — expect self-heal at the next settle; if the 08-19 read is also degraded,
investigate the feed.

**OWNER QUEUE (2026-08-18):**
1. ~~**Archive `claude-trader` on GitHub**~~ **DONE 2026-08-18** (owner-retried; verified
   `isArchived=true`). The old repo is now read-only — the permanent private evidence chain.
2. ~~**Delete `forward-ledger`**~~ **DONE 2026-08-18** (owner ran it after a `delete_repo`
   scope grant; repo 404s, old Pages URL 404s — pre-08-16 shared links dead as accepted).
   The two-repo era is fully closed: swing-lab is the one public home.
3. **X activation (P7b)** ("working on it"): developer app Read+Write → 4 keys in local .env +
   settle trigger cloud env → set PULSE_URL to the Pages URL → dry-run `python3 -m research.pulse`
   together before the first autopost.
4. **P9 README voice pass** (item below) + decide the public page `<title>` — "Forward Ledger"
   vs "swing-lab" is a site.py display string; rides P9 either way.
5. **Together-edit of public page wording** (owner offer stands) — thesis text is append-only
   ledger evidence; any public cleanup is a display rule in site.py, never a ledger rewrite.

(The 08-15b handoff this block replaces — P7 hosting detail, the P1b runbook — is preserved in
the P7/P1 records below and in git history.)

**P7 BUILDS: DONE 2026-08-15 (same day as the owner's pull) — P7a live at the URL above, P7b
inert-complete. Full record + what superseded what (audience contract, hosting mechanics,
autopost policy): the P7 section below.**

**Read FIRST: FINDINGS [ARC 5 #12] (the decision) + [ARC 5 #12a] (the locked amendments — long-only
population, floor, counterfactual regime, digest-v2 contract, freshness protocol, data-quality
findings).** This roadmap supersedes the 08-14 cloud-session checklist (git 0acff03 — its item 7
diagnosis was WRONG, corrected in #12a: pct_change is 5-session by design; the real bug is the
prices.py split adjustment). The owner-approved plan is cut into PIECES — one commit each, `python3 -m pytest research/tests -q` green + the piece's own
verification before committing, pull/rebase first (cloud routines commit to master daily), push
promptly after. Tick a piece here when it lands.

**Standing:** WATCH next read (08-19): first live v3 📖 — if its card still says "SYSTEM TAKE"
instead of "NEW BET #n", the cloud read trigger's prompt drifted from READ_LOOP; refresh the
trigger line. First live v3 📋 = 08-19 settle; first 📊 = SMCI (~Thu 08-20).
digest v3 SHIPPED 2026-08-18 (owner GO on the same-day proposal): Telegram =
PULSE + ALARM — 🧪 plain-English scoreboard leads both legs, 🟢 NEW BET cards (3 lines, bet #),
📈 open/next-settle line, ⚠️ only when real, 📊 SCORED replaces the settlement 🚨 (🚨 = failure
only), jargon/diagnostics CLI-side; FINDINGS [MSG] v3 entry = the full record + the locked 📣
X-mirror requirement for P7b. Delivery machinery untouched.
08-18 settle RUN FAILURE (orders) diagnosed + repaired 08-18: the #13a hand-edit
left an UNQUOTED COMMA in DVA's note → a 19-field row → `orders._save` (truncate-then-write)
crashed mid-write and the cloud run committed `orders.csv` with 4 of 5 rows DESTROYED (068dd81).
Ledger restored from cf0afcc with the note properly quoted; CAVA resolved through the normal
`check` path (filled, 08-17). Lesson: never hand-edit a ledger CSV — go through the module, or
quote. FIXED same day (owner green-lit): atomic write-then-replace in the orders/bets/movers
savers + a loud BY-NAME refusal of overflow rows at load; guard tests in all three. book.py
untouched (frozen). All tracked CSVs field-count audited clean.
TPR RESOLVED (filled 127.95, 08-15 settle — the band diagnostic's first row; the
P3 tolerances cleared when P3 landed 2026-08-14; `orders placed`/`pulled` no longer exist).
BSX CEO-buy read (08-14): STALE — dropped, no backfilling. NIO wash-sale window to
2026-09-12 (moot unless rebought). Liquidation DONE 2026-08-17 (recorded 08-18); the book is
TERMINAL — closure FINDINGS [ARC 5 #13] + #13a (account number ≠ system verdict). daily.sh
needs no edit (mark/snapshot early-return post-retire; step removal stays optional P6 cleanup).

- [ ] **P8 — GO PUBLIC (owner-approved 2026-08-15; fresh-repo path; name LOCKED: swing-lab).**
  The project opens to the public: site + code converge in ONE public repo and the two-repo split
  (private code + `forward-ledger` Pages mirror) dies — the split existed only because Pages on a
  private repo needs a paid plan. **Path decision: FRESH PUBLIC REPO seeded from a redacted
  snapshot, NOT an in-place visibility flip.** Why: the 2026-08-15 audit found the owner's
  private long-realm personal details woven through ~218 historical revisions of the
  evidence files; an in-place flip publishes all of it irreversibly, and a filter-repo rewrite of
  292 commits is riskier than a clean seed. Public trustlessness starts at flip time either way
  (outsiders can't verify pre-flip private history wasn't rewritten); this repo stays ARCHIVED
  PRIVATE as the internal evidence chain — never deleted, never rewritten.
  **Audit results (2026-08-15):** gitleaks over full history CLEAN — the only 3 hits are X's
  public OAuth documentation test vectors in `test_pulse.py` (false positives). `.env` /
  `FINANCES.md`: never committed in any revision. No Telegram chat IDs or token-shaped strings in
  tracked files; `push_log.csv` carries only date/kind/verdict. Operating docs genericized in HEAD
  this session (CLAUDE.md two-realms + book bullets, README, ARCHITECTURE, SKILL ×2, digest.py
  comment, book.py docstring, test_book.py docstring): private-realm specifics → "long-realm
  personal assets", private-repo name/paths dropped, SPCX restated as a standing
  conflict-of-interest exclusion (reason recorded in the private realm).
  **SNAPSHOT REDACTION LIST (apply to the SNAPSHOT at seed time — never to this repo's evidence
  files, which stay append-only):** FINDINGS.md (the 2026-08-02 book-correction entry's plan
  mechanics + balances; the lockup-shares sentence; the one-real-position paragraph; the 08-13
  phrasing — grep the private redlist), BACKLOG.md
  (2026-08-02 entries, the MOVED-OUT block, scattered mentions — same grep), cases/SPCX.md (front
  matter + private-realm framing; SpaceX-as-MARKET-SUBJECT stays — the leak is the private context, not
  the ticker), bets_catalogue.csv SPCX row thesis prose (the ROW and its score STAY — dropping a
  scored row is cherry-picking; redact prose, note the redaction inline). Residual-inference call
  (OWNER): ACCEPTED 2026-08-15 — redaction bounds detail, not deduction; zero private figures
  survive in the public tree.
  **OWNER GATES — state 2026-08-16:** (1) name LOCKED: swing-lab (owner call). (2) DONE — LICENSE
  (MIT) + README public preamble landed: disclaimer + the EDGE-GRADUATION rule (a probe that
  passes its pre-registered bar graduates to a private repo BEFORE real sizing; the framework and
  its ledgers stay public — the freqtrade seam: engine public, alpha private). (3) SEED BUILT +
  PUSHED: `scripts/build_public_seed.py` (private-only tool, EXCLUDED from its own output) copies
  the tracked tree, applies exact-match redaction rules (aborts unless each matches exactly once)
  then a zero-tolerance redlist verifier; the seed is ONE "history begins here" commit at
  github.com/guillearria/swing-lab — suite 219 green inside the seed tree. (4) **DONE 2026-08-16 —
  the owner reviewed the seed and flipped swing-lab PUBLIC. This repo IS that seed; work continues
  here, and the old private repo is the frozen evidence archive.**
  **CUTOVER SEQUENCE after seed:** enable Pages on the new repo (`docs/` on the default branch —
  public repo = free Pages); repoint the 3 cloud routines (list + patch in the SAME session, per
  SKILL); delete `publish-ledger.yml` + the `LEDGER_DEPLOY_KEY` secret + the mirror repo (the
  Pages URL changes UNLESS the new repo takes the mirror's name); update HQ's observation +
  schedule boards (hq repo) and any profile links; local dir: fresh-history path ⇒ CLONE
  swing-lab to ~/code/swing-lab, COPY the gitignored privates over from the old checkout (.env,
  FINANCES.md — enumerate with `git status --ignored`), keep ~/code/claude-trader as the archived
  private evidence clone, then migrate the Claude project-memory dir (keyed to the folder path)
  and update git remotes. [Supersedes the 08-15 mv-guidance — mv would carry the OLD history; the
  seed is a new root.] Protection facts: strangers can never
  push to a public repo (PR-only, owner merges); Actions keeps the first-time-contributor approval
  default; issues can be disabled if unwanted.
  **CUTOVER STATUS 2026-08-16 (all agent-side steps DONE):** Pages ENABLED —
  https://guillearria.github.io/swing-lab/ serves `docs/` from master; all 3 cloud routines
  REPOINTED via RemoteTrigger with full-body echoes verified (settle tonight 22:34Z is the first
  run against this repo; read Monday pre-market; watchdog 19:13Z — its 36h ledger-commit window
  carries over cleanly since the seed commit is dated today), and the read prompt's scope line now
  uses the cleansed phrasing; local working clone at `~/code/swing-lab` with the gitignored
  privates copied over; the old mirror page now redirects here; HQ boards updated. REMAINING
  (owner, after tonight's first green settle here): archive the old private repo on GitHub
  (Settings → Archive), and optionally delete the retired mirror repo once the redirect has
  outlived any shared links.
  **X layer (P7b) legal frame (researched 2026-08-15; public-source research, NOT legal advice):**
  the publisher's exclusion (Lowe v. SEC 1985) keeps impersonal + bona fide + REGULAR-cadence
  publication outside "investment adviser" status — paid or free. Every modern enforcement case is
  SCALPING: recommending while concealing/misstating one's own position and selling into the
  induced move, near-always in microcaps a post can move. Pulse's locked policy (deterministic
  verdict-grade numbers only, ≤1/day, no entry alerts, standing disclaimer) already matches the
  conservative lane; ADD a position-disclosure line whenever a post names a ticker the book holds,
  and never trade into a post's own reaction. After-settlement ledger reporting is the safest
  posture; pre-registration + take/skip denominators actively SUPPORT bona-fide status.
  Disclaimers help framing; honesty + completeness (wins AND losses, no cherry-picks) are the
  actual defense. One-hour securities-lawyer consult before ever monetizing. **Owner decision
  2026-08-15c: NO per-position disclosure on the pulse — posts carry system performance only**
  (clean while the regime is counterfactual: there are no positions; the README "author may at
  times hold positions" line covers the general case). REVISIT the moment a funded private book
  overlaps a posted ticker — that overlap is the scalping fact-pattern's front door.
  **2026-08-16 addendum:** the 08-08 correction annotation in `bets_catalogue.csv` named the plan
  type of the misbooked cash and RENDERED INTO THE LIVE PUBLIC DASHBOARD via the thesis expander —
  rephrased in the real file to "a cash balance misbooked as shares" (meaning identical, zero
  numbers touched; the ONE deliberate evidence-text edit of this cleanse, logged here), the page
  regenerated, and the mirror updated directly. Residuals kept in the seed BY DESIGN: sell-side
  "Morgan Stanley note" mentions (market prose), the generic employee-stock-plan lesson in SKILL,
  and the SPCX conflict-of-interest exclusion — the accepted weak inference, zero figures.

- [ ] **P9 — README voice pass (owner request, 2026-08-16).** The public preamble was written
  owner-facing and reads as the agent narrating the project's inner workings. Rewrite the top of
  `README.md` for a public reader: neutral voice, state what the project is and shows, drop the
  process narration. KEEP: the disclaimer block, the edge-graduation rule, the license line.
  Display/voice only — no rule or contract changes ride along.

- [x] **P0 — log layer (2026-08-14b):** branch merged to master; [ARC 5 #12a] appended; this
  roadmap; READ_LOOP transition banner; read-trigger prompt verified delegating to the repo doc.
- [x] **P2 — pool rule + data integrity (DONE 2026-08-14, commit 810f33b):** `bets.stats()` →
  long-only via a raw `_agg` split (engine `_grp` MUST switch to `_agg` or tag/universe diagnostics
  silently lose shorts); bar constants single-homed (`BAR_N/BAR_MEDIAN/BAR_BEAT/WILCOXON_ALPHA`);
  stdlib `wilcoxon_p` (one-sided vs 0, zeros dropped, tie-averaged ranks, exact DP n≤50) wired into
  engine's PASS gate + `show`; `bets.add` → refuse shorts + liquidity floor (`config.LIQ_FLOOR_USD=
  5_000_000` / `LIQ_WINDOW_D=20`, median close×volume over 20 COMPLETED bars, fail-CLOSED, returns
  bool, run() saves only on True); `prices.py` split-adjustment fix via `events.splits` (MNST 2:1
  regression test); "5d" labeling on 📡 header + movers FIELDS comment. Tests: floor/short
  refusals, long-only vs `_agg`, wilcoxon vectors (n=5 all-pos p=0.03125; live vector
  [−7.99,15.28,−6.17,−33.30,−19.09] → p≈0.906), split fixture. Verify: `bets show` prints "pooled
  LONG-ONLY … n=5 median −7.99% beat 20%" + short subline n=1 +69.74 intact.
- [x] **P3 — orders counterfactual (DONE 2026-08-14):** delete `place` sizing block (all `book.*` coupling; shares
  optional → blank) + `check` booked-lot precedence + `placed`/`pulled` + their dispatch;
  `config.RISK_PCT` deleted; KEEP `booked`/`booked_lot` (digest uses until P4), `limit_price`,
  `resolve`, `_complete` (movers.scan imports it!), `sessions_left`, `score`, `stats`, `summary`
  ('—' for blank shares), `cancel`, the [ORDERS #1] footer. MUST ride along: digest
  `_orders_section` → 🟢 "system take (counterfactual)" display lines, NEVER actions (else the
  nightly 📋 instructs a deleted command); `_book_section` idle-cash nag + `IDLE_CASH_MIN` deleted;
  READ_LOOP banner updated (fallback obsolete). Verify: digest has zero orders DO-NOWs; scratch
  `place` prints counterfactual voice (then `git checkout research/orders.csv`).
- [x] **P1 — book retirement — DONE 2026-08-18 (P1a code 2026-08-14 · P1b liquidation session
  2026-08-18 on the owner's 08-17 broker fills; closure FINDINGS [ARC 5 #13] + #13a scope
  correction: account −14.8% vs same-$-SPY +4.6% / dual-mom −2.6% = the owner's inherited book,
  not the system's verdict — system-originated trades +$15 n=4; DVA trued 3-vs-2, owner
  confirmed).** Original P1b spec: with real fills run `book close` each → final
  `mark` + `snapshot` → FINDINGS CLOSING VERDICT entry (final vs-SPY/dual-mom from mark) →
  `book retire` → one commit → tick this box. daily.sh needs NO edit (mark/snapshot early-return
  one line post-retire; step removal is optional P6 cleanup). Original spec: code first
  (`RETIRED_T`/`is_retired`/`retire` — refuse with open positions, sweep cash→0 into the meta row,
  `__CASH__`/`__SEED__` pattern; `mark|show|snapshot` one-line early-return, NO network so the
  perpetual POOL-STOP print and `__main__`'s network-misattribution are unreachable; mutating cmds
  refused when retired) → then with real fills: `book close` each → final `mark`+`snapshot` →
  FINDINGS CLOSING VERDICT (final vs-SPY/dual-mom) → `book retire` → one commit. Digest: retired
  guard in `_book_section` BEFORE `_marks()` + in `_delta_band` (if P4 not yet landed); DELETE
  `_liveness_section` (frozen curve = unclearable alarm; push-log DO-NOW + watchdog cover it;
  daily commit survives via the push-log stamp). daily.sh: drop `book mark` + `book snapshot`
  steps → **re-read/patch the settle trigger prompt SAME session (prompt-drift rule).**
- [x] **P4 — digest v2 (DONE 2026-08-14 — landed BEFORE P1b by keeping the book section dual-path; the live-book rendering becomes dead code at retire → delete in P6):** `_delta_band` → `_pool_scoreboard()` in the
  same `_safe` seam, leading BOTH legs: 🎯 POOL n/median/beat/Σpp(equal-wt, OWN benchmarks)/p/bar
  distance + short-contrast line + PASS-CANDIDATE (n≥10, below-bar label, thresholds from bets
  constants) + 🏁 milestone on settled-long count crossing 10/20/30 vs `_committed(bets.CATALOGUE)`
  (works ONLY because daily.sh runs digest BEFORE push_ledgers — comment-guard that ordering; read
  leg commits first so no false banner). Book section → CLOSED one-liner only; orders section
  final (slim shows 🟢 too; delete `orders.booked/booked_lot` once digest drops them); bets state
  line loses its verdict numbers (scoreboard owns them) + gains the mix line (`tag_mix`, last 15);
  new `bets.cum_excess`. P5: READ_LOOP mix-mirror + milestone-review rules (≤1 new hypothesis +
  ≤1 re-arm, only if warranted); SKILL re-arm bullet (beside the deadline-reachability bullet);
  "If we resume hunting" points at #12a. Verify: full + `--slim x` both lead 🎯 POOL; no 💰
  anywhere; clean-day DO-NOW empty.
- [x] **P6 — doc pass + memory — DONE 2026-08-18 (docs follow code, landed with the P1b
  session): CLAUDE.md status leads (orders → counterfactual, book → TERMINAL #12/#13/#13a,
  digest → v2) + site/pulse added to "Where things are" + single-source book pointer; ARCHITECTURE
  (title, Money layer CLOSED, diagram counterfactual, convergence → SUPERSEDED-historical,
  telegram v2, pool stop retired-with-pool, public-surface layer added); READ_LOOP transition
  banner OUT + step-5 full rewrite (5a SYSTEM TAKE card / 5b one counterfactual order) + step-7
  v2 anatomy; `__main__.py` + `book.py` docstring leads; README was already v2-clean. Verify
  grep: remaining band/broker-verb hits are historical comments, tests, or text under a HISTORY
  lead. 219 green. Memory updated (claude-trader path; swing-lab path blocked by permissions —
  content also lives in FINDINGS #13a). RESIDUE carried, deliberate: digest.py dead live-book
  rendering + daily.sh mark/snapshot steps stay (unreachable post-retire; removal = P6b below,
  not urgent, live paths untouched right before a session clear).** Original spec: CLAUDE.md (book → retired,
  real-money stance ¶ → superseded by #12/#12a, digest → v2, orders → counterfactual, **+ add
  site/pulse to "Where things are" — P7 landed after the last CLAUDE.md sweep**); README rows
  24/25/26/29/38/40 + automation; ARCHITECTURE (Money layer CLOSED, convergence doctrine 60-68 →
  SUPERSEDED-historical, telegram contract v2, pool stop retired, + the P7 public surface layer);
  READ_LOOP step-5 full rewrite
  (banner removed); `__main__.py` LIVE_COMMANDS wording. RemoteTrigger: re-read + patch BOTH
  prompts (<2KB). Assistant memory files updated. Verify: `grep -rn "placed\b|RISK_PCT|SINCE-LAST|
  IDLE_CASH"` over docs/py → only historical FINDINGS/ARCHIVE/BACKLOG hits.

- [ ] **P6b — dead-code sweep (optional, small):** delete digest.py's unreachable live-book
  rendering (dead since `book retire`, P4 note) + drop daily.sh's `book mark`/`book snapshot`
  steps (early-return no-ops post-retire). Pure deletion, tests must stay green; do it in a
  quiet session, not minutes before a routine fires.

**Deferred by decision (owner, 2026-08-14b):** per-run bet-cap raise + slow-bleed probe (both need
their own pre-registration; the freed capacity argument lives in #12a); shorts/illiquid candidates
(admission now refuses them — re-arm path only).

### P7 — PUBLIC DASHBOARD (**trigger FIRED 2026-08-15 — owner pulled: start "before Monday"**)
- [x] **P7a LANDED 2026-08-15, REDESIGNED same day on owner feedback (`research/site.py` →
  `docs/index.html`):** the first cut was verbose and leaked internal reasoning; the owner set
  the AUDIENCE CONTRACT that now governs the page — **the end user gets PREDICTIONS and a
  PERFORMANCE SUMMARY, nothing else; every explanation (method, bars, pre-registration
  language, diagnostics) is owner-side and lives in repo docs.** This supersedes the earlier
  "full take/skip denominator ON the page" strategy note — the movers log stays fully in the
  LEDGER (nothing stopped being recorded), it just doesn't render publicly. Page now: header
  + one-line stamp, performance tiles (open/settled/median/beat/Σ — long-only; shorts render
  in the table with a one-line note), cumulative-excess curve + per-prediction sign-split
  bars (diverging blue/red), FULL sortable+filterable catalogue with theses (filters are
  views, never removals — test-enforced, incl. a no-jargon leak test on the template).
  Still: stdlib, DETERMINISTIC (no clock), never imports book / no account dollars
  (test-enforced), "Not investment advice" standing. Regenerated by daily.sh + committed.
  **PUBLISHING APPROVED by owner 2026-08-15 ("no problem publicizing now, we will edit
  together")** — thesis TEXT is ledger evidence (append-only); public wording touch-ups are
  a together-edit, never a silent rewrite. Same-day table v3: thesis left the grid for a
  click-to-expand detail row (owner: the column "diminishes the quality of the table").
  **HOSTING (LIVE 2026-08-15):** page → public mirror repo `guillearria/forward-ledger`
  (page + one-line README only; created after owner direction — this repo's plan refused
  Pages on private, HTTP 422) → GitHub Pages at **https://guillearria.github.io/forward-ledger/**.
  Freshness: `.github/workflows/publish-ledger.yml` re-publishes on every commit that
  touches docs/index.html (i.e., the nightly settle) via a WRITE deploy key on the mirror.
  **PENDING owner (3 paste commands, in the 2026-08-15 session report): mint the deploy key +
  add it to the mirror + set `LEDGER_DEPLOY_KEY` secret on this repo** — the session's
  permission layer refused credential creation (ssh-keygen/gh secret), correctly a
  human-hands step. Until the secret exists the workflow skips GREEN and the public page
  simply stays at its last published copy. Page safety-scanned before first publish: no
  names/brokers/account dollars (thesis dollar figures = company financials, public data).
  PULSE_URL (the X pulse's link slot) ← set to the Pages URL at P7b activation.
- [x] **P7b CODE LANDED 2026-08-15 (`research/pulse.py`) — INERT until the owner's one-time
  activation.** Implements the autopost policy below exactly: compose() renders verdict-grade
  numbers ONLY (newly-scored verdict rows vs git HEAD + 🏁 milestone crossings take the
  headline; a settling SHORT never posts; nothing from movers can render — the MNST artifact
  class has no path in). Transport = X API v2 `POST /2/tweets`, OAuth 1.0a signed in stdlib
  (HMAC-SHA1 pinned in tests to the documented reference vector), tri-state delivery verdict
  (POSTED w/ tweet id · REJECTED · UNCONFIRMED — never re-post on UNCONFIRMED, the 07-24
  class), every attempt stamped in committed `research/data/pulse_log.csv`. Metered fuel:
  ≤1 POSTED per UTC day in code (structural ≤1/day via settle; free tier 500 writes/mo ≈16×
  margin). daily.sh runs `pulse --post` AFTER site, BEFORE push_ledgers (HEAD-diff ordering
  contract, comment-guarded like the milestone check); failed post ⇒ FAILS ⇒ 🚨 heartbeat.
  **ACTIVATION (owner, one-time): create the X account + developer app (Read AND Write),
  put X_API_KEY / X_API_SECRET / X_ACCESS_TOKEN / X_ACCESS_SECRET in local `.env` AND the
  settle trigger's cloud env; optional PULSE_URL adds the dashboard link once P7a is hosted.
  Until then every run prints "SKIPPED (autopost inert)" and exits clean.** 10 tests.
  **PROMPT-DRIFT STATUS (standing rule): CLEAR.** The settle prompt was re-read + patched
  TWICE this session, both verified echoed in full: (1) the `site` step + regenerated
  docs/index.html as expected shapes; (2) the pulse step — SKIPPED-while-unconfigured is
  normal, never run research.pulse manually, never re-run daily.sh over a pulse failure,
  quote any PULSE verdict line, pulse_log.csv expected in the commit. (The second patch was
  briefly blocked by the session's permission classifier; the owner-directed retry landed
  2026-08-15 ~21:50Z.)
Sequence agreed: **P7a = the visualization first** (ledger + performance rendered from the CSVs —
scoreboard curve of settled excess, pool tally vs bar, take/skip denominator, catalogue table;
LOCAL/private artifact first, publishing is a separate later gate), then **P7b = the social
pulse** under the autopost policy below. Build P7a as a GENERATED static page committed from the
ledgers (stdlib only, global-observatory pattern) so the later publish step is a hosting
decision, not a rebuild.

**P7b AUTOPOST POLICY (decided 2026-08-15 — owner reviewed HQ's rule, model concurred):**
HQ's "never autopost" governs the PERSONAL-BRAND publishing lane (hq/publish, LinkedIn-class
posts under the owner's name); by HQ's own scope rule ("HQ conventions never override a
child's") it never bound this repo. It is REPLACED here by the project's own architecture —
not by nothing:
- **DETERMINISTIC autopost is ALLOWED — and for the pulse it is REQUIRED.** A post rendered by
  CODE from committed ledgers (scoreboard tally, settled excess, 🏁 milestones — verdict-grade,
  test-covered numbers only, NEVER raw scan output: the MNST −50.6% artifact class must have no
  path to a public post) publishes unconditionally. A human approve per post would reintroduce
  selection bias at the publication layer — "posts only when approved" is the survivorship
  theater the public ledger exists to refute; mechanical publication IS the credibility asset.
- **LLM-authored public prose keeps a gate:** narrative content (case threads, commentary)
  passes a deterministic redlist-style check + human approve — the model never self-certifies
  to the public. Same split as the digest: LLM generates hypotheses, code renders + transports.
- **Transport discipline inherited from the digest's paid lessons:** ONE post per trigger with
  a delivery verdict (the 07-24/08-06 double-post class), fail-LOUD, standing "not investment
  advice" framing. Cadence/spend gets its own cap when P7b is built (metered fuel).
- HQ's rule stays untouched for HQ's lane; nothing here ever posts under the personal brand.
The paper-verdict regime makes the ledger publishable (no personal dollars in the paper track).
Strategy notes, locked while cold: (1) **publish BEFORE the verdict** — a pre-registered public
ledger scored vs benchmark with the full take/skip denominator, published while the answer is
unknown, is the credibility asset; revealing only a winning record is survivorship theater. (2)
**Full catalogue always** — "best bets" may be a VIEW, never the page; the honesty is the moat.
(3) Repo stays PRIVATE (`book.csv` = real dollar history); the public thing is a GENERATED static
surface (global-observatory pattern: committed page, GitHub Pages). (4) HQ publishing rules apply
(deterministic redlist gate + human approve; NEVER autopost) — a signals account that autoposts
needs an explicit owner policy decision first. (5) "No financial advice" framing, README already
has the language.

## Handoff 2026-08-13 (superseded by the above — kept for the 08-13 conversion record)

**State:** everything is on `master` and pushed; `python3 -m pytest research/tests -q` green.
Live numbers: `python3 -m research` (never restated here). **Setup gotcha:** `pip install -r
requirements.txt` first — `research/config.py` needs `python-dotenv` or Telegram dies silently.

**WHAT LANDED 2026-08-13 — the legacy conversion: every book position is now system-chosen
(ledger-only session; no code or doc-logic changed, cloud prompts deliberately untouched).**
Owner disclosed NIO + CMPS were PRE-SYSTEM whim buys — attribution at the 08-12 close: system-era
decisions +$32, every drawdown dollar legacy. Executed at the broker and booked same morning
(42a6c23 + ce6b91b): NIO closed in FULL @ 4.48 including a 0.784864-sh fractional remainder the
seed missed (HELP-precedent twin row; broker held 28.784864 vs book 28.0) — **wash sale: no NIO
rebuy before 2026-09-12**; CMPS trimmed 193.136664 → 50.136664 in two tranches (50 @ 14.00 +
93 @ 13.77, count trued to broker) = the 2-risk-unit conviction size into the Q4-26 FDA binary;
first ADR pass-through fee booked as a cash debit (~2¢/sh, recurs while the ADR is held — noted
on the row). CACI 1 sh entered through the FULL orders arc in one morning — `place` (limit
686.88, band off the 08-12 close; the prior evening's in-session 674.25 had anchored on the
08-11 bar: a live demo that a limit is COMPUTED at placement, never quoted from an old session)
→ `placed` → broker fill 674.00 → `book open` → `check` resolved from the booked lot (the
08-11 booked-lot fix's designed path, second live use after DVA). Paper bets untouched — CMPS
126d and the NIO-flip USER bet keep scoring; execution never touches the verdict. **Comms rule
earned (also in assistant memory): broker instructions are "SELL n (keeps m)" — never "193 →
50",** which got executed as "sell 50"; the follow-up working limit then hid 50 shares of sell
availability behind the broker's "available" count (both caught and recovered same morning, no
harm). Backlog gained **[AUTOMATION]** (owner: "eventually this whole system is going to be
automated" — staged as a named trigger, not a build; stops stay digest-watched ledger rules
meanwhile, the bottom-tick evidence standing). **WATCH tonight/tomorrow:** settle's 💰 band must
narrate the day's churn vs HEAD (four closed rows + an open + a fee across two ledger commits);
the CACI order row should render filled+BOOKED as an FYI, never a nag; and tomorrow's read
arrives with free cash above the `IDLE_CASH_MIN` gate for the first time since 08-07 — the 🟢
idle-cash working-order path should actually fire on a take.

**WHAT LANDED 2026-08-11 — the first live week after the sweep, reviewed from the two messages
the user actually received (FINDINGS [OPS] 2026-08-11).** Four defects, all fixed, 204 pass.
(1) **The read leg had no delivery watcher and lost a brief in silence:** the 08-10 read ran and
committed a TTD bet, its push stamped `UNCONFIRMED`, and nothing alarmed — `_pushlog_section`
filtered `kind == "settle"`. The 08-09 FEED_STALE_D 3→1 change had been adopted as that leg's
watcher and does not cover this: it sees a read that doesn't RUN, not one that runs and can't
SPEAK. Now both legs are held against their own due calendars (read = weekdays, rolls back over
weekends). (2) The same check false-alarmed on a REJECTED→retry, naming `due` instead of the
failing row's date — the 08-10 message accused 08-09, which was DELIVERED; it now fires on "no
DELIVERED row on/after due". (3) The retry's own first commit moved the 💰 band's baseline, so a
−$68 day was reported as "book flat"; the baseline now skips any committed row dated today.
(4) `orders check` resolved only against bars strictly after `scan_from`, so DVA — filled by the
human's own limit IN the anchor session — was one session from being stamped `expired, did NOT
chase` while open and green; `check` now yields to `booked_lot()`. Note the 08-09 handoff below
anticipated the DVA expiry and prescribed `orders pulled DVA`; that was the wrong remedy — the
row was never a stale broker order, it was a real fill the resolver structurally could not see.
READ_LOOP also gains `daily.sh`'s 🚨 heartbeat parity on a non-DELIVERED verdict. The
never-re-send-on-UNCONFIRMED rule STANDS (n=1 genuine loss; flipping it re-opens the 07-24
double-post). **WATCH (next scheduled runs):** the 08-11 settle's 💰 band should print a real
delta vs 08-10, not "flat"; and a read that ever fails to deliver should now produce a DO-NOW in
the following message plus a 🚨.

**WHAT LANDED 2026-08-09 — strand fix OOS PASSED 2/2; two digest false-alarm classes closed
(FINDINGS [OPS] 2026-08-09).** The strand watch below resolved: the 08-08 AND 08-09 settles both
stamped `settle,DELIVERED` — cold-container class closed. The weekend then exposed two digest
bugs, both fixed + tested (193 pass): (1) the DXCM "FILLED … but no book position" nag was
PERMANENT by construction — the ledger held the full 08-05→08-07 round trip all along (owner's
broker screenshot confirmed the 82.575 sale; the rotation is recorded below at 08-07), but the
matcher checked OPEN lots only and a `filled` order row is terminal, so closing the position
locked the alarm on forever; now any settled lot (open OR closed) matching the order's fill
signature via `orders.booked()` clears it. (2) The movers bar-lag check measured against TODAY,
so every Sat/Sun it read 2 weekdays and BOTH cohorts false-alarmed all weekend (the first
weekend `last_bar` was live); now measured against `last_ok` (the last successful scan),
threshold unchanged — a frozen bar with a live scan still grows the gap. Same-day red-team
(two blind reviews + cross-model control) caught what the fixes traded away and it was
repaired before it ever ran: FEED_STALE_D 3→1 (a dead scan now escalates on the 2nd missed
weekday — lag-vs-last_ok had left it invisible for up to 4), booked() unified across both
order paths, one residual accepted + documented in-code (unrelated same-name lot can suppress
an unbooked fill; FINDINGS [OPS] 2026-08-09 red-team entry). NEXT (Mon 08-10),
all self-running: the read advances bars to Fri 08-07; `orders check` resolves the DVA
pending row (if it instead EXPIRES midweek untouched, the GTC alarm repeats daily until
`orders pulled DVA` records it's off the broker's book; the real fill is long since
booked); and the overlap
re-measure's first valid full-vs-slim pair = the 08-09 22:30 📋 + Monday's 📖 (command and
≤55% bar in the WATCH block below).

**WHAT LANDED 2026-08-06 — the triple-push morning, dissected and fixed (FINDINGS [OPS] +
[MSG] 2026-08-06).** The read window delivered THREE messages (📖 + a "(delivery check)" copy +
a bare "Probe" — both extras improvised by the cloud agent off an ambiguous exit 1, the exact
FINDING 2/3 shape below), settle's 📋 stranded a SECOND consecutive night, the digest nagged
DXCM's already-booked fill, and that stale pending row silently blocked ALL long sizing
($421.40 double-counted). Shipped: tri-state delivery verdict (re-send ONLY on `PUSH REJECTED`);
`orders.booked()` (booked fill ⇒ FYI not nag, cash freed); loud `orders check` on empty bars;
`research/data/push_log.csv` delivery stamp + a DO-NOW when the last due settle push lacks
DELIVERED; slim reshaped into the MORNING BRIEF (full book with $ P&L + stop/target distance;
band/one-liners dropped — user's call, supersession named in FINDINGS [MSG]). Decided AGAINST a
manual `orders filled` command (reasons in FINDINGS [OPS]).

**THE IMMEDIATE WATCH (next scheduled run): the strand root cause is FOUND and FIXED — verify
tonight [2026-08-08]. → RESOLVED 2026-08-09: PASSED 2/2, see the block above.** The window
hypothesis died on its own pre-registered falsifier: the
FIRST 22:30 settle (08-07 22:35Z → f2fba61) stranded exactly like the 05:0x ones, and the run
reports show why — COLD containers sometimes lack python-dotenv, so the notify→config→dotenv
ImportError killed movers/orders/digest/heartbeat in one shot (zero messages, no stamp, no
alarm) while bets/book survived. BOTH 08-07 settles (05:09 = 750fcde AND 22:35 = f2fba61) died
this way; time-of-day was never the variable. Fix shipped 2026-08-08 (FINDINGS): daily.sh deps
guard (probe → `pip install -r requirements.txt`), digest stamps+prints a verdict even on
import death (incident test, 190 pass), READ_LOOP step 0 carries the same guard. EXPECT from
tonight's 22:30 run: ONE 📋 + a committed `settle,DELIVERED` stamp = class closed. A stamp-less
strand WITH the guard in place falsifies the cold-container theory — then suspect the env image
itself, not the repo. The half-done overlap re-measure (command in the WATCH block below, ≤55%
bar, log the number — FINDINGS [MSG] 2026-08-06) now compares a 22:30 📋 vs next-morning 📖.
2026-08-07 book rotation (user-driven, mid-conversation): DXCM closed @ 82.575 (−$8.52, day 2
of 21 — churn accepted: swapped a chased post-pop entry for the fresher DVA dislocation);
DVA = the USER'S OWN dip-bid GTC limit 178, FILLED same morning and booked (2 sh, stop 169,
21d vs XLV; stop goes live at the broker 08-08 after the funding sale settles — T+1); his
loose 1-sh SPCX lot sold @ 119.74 = −$15.26 REALIZED, proceeds stay OUTSIDE
the book (inflow freeze honored), recorded in the private long-realm repo.
Same session: READ_LOOP step 7 got the note-is-a-CARD rule (≤6 lines — user call), and
`digest._pushlog_section`'s due boundary moved 06:00→23:00 UTC to track the new settle time.

**WHAT LANDED 2026-08-05 — the two daily pushes stopped echoing each other, the ✅ ping was
outlawed, and DXCM is a real position.** The pre-registered overlap re-measure MISSED (56% vs
≤55%; 87% of settle contained in read), so the fail branch fired: the read push is now
`digest --slim` — 📖 band + DO-NOW + book header/cash + one-liners + run note; settle's 📋 is
the day's ONE full state photo. A stray "✅ heartbeat: digest pushed" also arrived (the read
prompt already said "never send a second message" — the agent improvised): prohibition now
explicit in READ_LOOP step 7 + both cloud prompts, and READ_LOOP no longer has "heartbeat" in
its title. DXCM filled at the broker 08-05 @ 84.28 (5 sh) and is in the book; free cash ~$6.
Also: settle fired ONCE on 08-05 but ran daily.sh TWICE (05:08 partial-fail commit, 05:29 clean
retry) — the first pass's digest AND 🚨 both died in transport, the documented blind spot,
observed live; the retry is now a sanctioned one-shot rule in the settle prompt. Detail:
*Recent changes* 2026-08-05 + FINDINGS 2026-08-05 [MSG].

*(The 08-05 WATCH expectations FAILED on both counts — the 08-06 settle did not resolve DXCM
and its 📋 stranded; the first `--slim` read pushed three messages. Post-mortem + fixes: the
2026-08-06 block above and FINDINGS [OPS] 2026-08-06.)* First core settlement lands ~08-20.
Then let the autumn evidence cluster arrive — resist inventing work.

**WHAT LANDED 2026-08-04c — the denominator widened to the tail, and four leaks closed.** A
full-project review (with user) asked whether our own constraints choke the goal; the answer
and its caveats are FINDINGS 2026-08-04 (pre-settlement caveats + [ARC 5 #11]). Shipped, in
pre-registration-first order: (1) `movers scan` now runs TWO cohorts — S&P 500 (untouched) +
an S&P 400/600 TAIL cohort from committed caches — with a `universe` column that is a
DIAGNOSTIC lens only; (2) feed status carries `last_bar` + fetch coverage and the digest
escalates "ok but stale bars" (the 08-04 silent-0-movers shape) to a DO-NOW; (3) `movers scan`
has the completed-session guard (the old partial-bar item below is DONE); (4) the engine's
diagnostic splits show closed AND open counts (post-earnings-drift was rendering "1cl" and
hiding ~20 open); (5) exit plans got a column — `book target` + a touched-band DO-NOW (NIO's
prose band was touched at 4.94 and nothing noticed); (6) READ_LOOP gained the HARD ≤3-per-tag
ceiling + tail reading guidance; (7) NIO's flip claim is a scored USER bet. **WATCH: the first
tail scan belongs to the next scheduled read run — do NOT run `movers scan` interactively.
→ RESOLVED: the tail cohort is live (`tail-movers` in `_feed_status.json`, tail rows in the
ledger; coverage 1002/1003 on 08-07).**
Expect up to `TOP_N+TAIL_TOP_N` SEEN rows, a `tail-movers` key in `_feed_status.json`, and a
longer scan (≈3× names — the coverage field is its own outage canary). **A coverage DO-NOW
with no outage = universe cache rot → rebuild per the [ARC 5 #11] Reproduce line.**

**WHAT LANDED 2026-08-04 — the daily message reports CHANGE, not state.** The user asked why the
settle and read pushes echoed each other. Measured: 69% of their lines byte-identical, and 4 of
the last 7 settle runs had changed nothing but the mechanical equity-snapshot row. The digest now
opens with a 💰 SINCE-LAST band diffing every ledger against **git HEAD** (the last state the repo
published — no state file; the commit state IS the window, and `digest._committed`'s docstring says
why a state file cannot work here). Also landed: the whole-pool stop's LEVEL on the BOOK line every
day (it could previously only fire into `cron.log`), the next date the scoreboard can move on its
own on the BETS line, a session countdown on a working order, and an alarm for an order that
expired while still live at the human's broker. **Three false-number bugs were caught before
shipping** — one by the band's first live render, two by an independent red-team on a different
model. Full detail: FINDINGS 2026-08-04 [MSG] and *Recent changes* below. The durable lessons are
in `SKILL.md` (guard-on-the-wrong-axis · alarms need a clear path · our order ≠ the broker's order).

**SCOPE FIRST — read this before anything else.** This repo is the **SHORT-SWING** realm only.
**Long-term wealth — long-realm personal assets and multi-year tax milestones — lives in a
fully-private repo.** Separate research, separate actions, markdown pointers only; neither side
imports the other. **Do not research long-realm holdings or personal plan mechanics here.** This
boundary had been written down since June and enforced nowhere, and on 2026-08-02 it cost half a
session: SPCX sat in the swing book, we chased its lockup terms through four documents, and **the
position turned out not to exist** — a cash balance misread as 17 shares at seed (FINDINGS
2026-08-02). Full detail in `CLAUDE.md` SCOPE.

**The shape of the project, in one paragraph.** ONE verdict silo: the pooled forward-bet
catalogue (`bets.py`), accruing toward N≥30 with median >+1% and beat >55% [Arc 5 #7]. ONE
candidate denominator: the daily mover scan (`movers.py`). ONE real-money book (`book.py`), whose
job is to converge on the edge — not to prove it. ONE banked result: dual momentum. Arc 3's
insider silo was CLOSED and deleted 2026-08-02, so "two silos" is gone from the docs and the code.
**Everything now waits on maturity, not on work:** first core settlement ~2026-08-20, movers
skips-63d N≥30 ~2026-09-28, the [ARC 5 #2] paid-data checkpoint ~2026-09-29 (its FAIL branch is
now pre-registered too — [ARC 5 #2b], a decision point with three pre-named options, so a
miss cannot resolve by drift), the pooled [Arc 5 #7]
verdict at N=30 ~2026-10-19. That autumn cluster needs ZERO new generation work — the scheduled
`read` and `settle` routines get there on their own. Resist inventing work to fill the wait.

**THE NEAR-MISS OF 2026-08-02, kept here because it is the trap most likely to bite you next: the
cloud routine PROMPTS are a SECOND COPY of the loop docs and live OUTSIDE this repo (`/schedule`,
not git).** After deleting the
insider silo I had every in-repo reference clean and the tests green — and the `read` routine, due to
fire the next morning, still said *"run BOTH denominator scans, **NEVER skip either**:
`python3 -m research.insider_ledger scan`"*, plus an `insider_ledger decide` queue-clear and a commit
of the deleted `insider_ledger.csv`. That is a `ModuleNotFoundError` inside a step the prompt forbids
skipping. `settle` likewise still advertised "scores … + insider-cluster takes". **Both prompts were
patched 2026-08-02** (`read` = `trig_01EsetvEZmVLb56fEmc7YvSi`, `settle` =
`trig_01Uz2fQRMh5UwjnSvFkaSNBY`), each now carrying an explicit "ARC 3 IS CLOSED, do not run any
`insider_*` command, do not treat their absence as a bug" block, and `read` gained "if this summary
and the doc disagree, the DOC WINS — say so in your report". **Patched a second time the same day**
when the two-realm split landed: `read` now also carries a SCOPE block (short-swing only; never
research long-realm personal assets, never pre-register a bet on SPCX (standing exclusion), never
suggest deploying book cash into it).
**The standing rule (this is the second time it has bitten, after 2026-07-02): a repo-only grep is
NOT a complete refactor. Whenever `READ_LOOP.md`, `daily.sh`, or a module name changes, re-read the
routine prompts with `RemoteTrigger {action:"list"}` in the SAME session and patch them.**

**WHAT LANDED 2026-08-03 — real-money entries are now WORKING ORDERS, not a quoted price.** The
user got `5 sh DXCM @ ~83.45` pre-market, saw 86.54, and asked whether to still buy. That price was
Friday's close — the newest COMPLETE bar a pre-market run can honestly cite, and never a live
quote. Measured before changing anything (`python3 -m research.tools.slippage_audit`, N=40 taken
movers): the median name moves **1.07% by the next open and 2.42% by the next close** — waiting
costs MORE than the gap — no weekday effect, tail to −23.4%. So `research/orders.py` + `orders.csv`
now hold a LIMIT + an expiry, computed by code, resolved daily by `daily.sh` against real bars, and
re-pushed by the digest while pending. Band/expiry live in `config.py`; **never restate them.**
Two documented rules were REVERSED on purpose, each with its reason recorded in place in
`READ_LOOP.md`: expiry is STATE not supersession, and the daily run DOES re-push a pending order —
both were right for a point price and wrong for a limit, which does not decay. The
`SIZED SUGGESTION:` prose marker is DELETED (a structured fact in free text that `grep --include=*.py`
found ZERO readers for; 2 issued, 0 executed, nothing noticed). Both cloud prompts were patched the
same session. Full rationale: FINDINGS 2026-08-03 + Recent changes below.

**THE ONE THING TO WATCH on the next scheduled runs — and it is a PRE-REGISTERED number, not a
vibe check.** ~~The 2026-08-04 band shipped against a measured 69% line-overlap between the day's
two pushes. Re-measure on the next weekday's two REAL pushes; the bar is ≤55%.~~ **MEASURED
2026-08-05 on the real pair: 56% — MISS** (20 of 36 read lines shared; the unflattered view: 87%
of the settle message reappeared verbatim in the read one — the drop from 69% was mostly the read
message growing a RUN NOTE, not less echo). The fail branch fired as pre-registered: the read push
went `--slim` the same day (see *Recent changes* 2026-08-05) [slim SHAPE superseded 08-06 —
see the 08-06 block in PICK UP HERE]. **NEW WATCH: re-measure the FIRST
full-vs-slim real pair (settle 22:30 UTC + next-morning read 11:31 UTC — settle moved off 05:00
on 2026-08-07), same command, same ≤55% bar — expect ~40-50%.** Same-instant local sims read 58-62% but are inflated by artifacts a real pair cannot
have (identical band, identical DO-NOW spot, identical marks); the real pair is the verdict, and
if IT still misses, the next candidate is the shared blank-line skeleton + DO-NOW contract lines —
measure, then decide. Measure by saving both messages and counting shared lines:
`python3 -c "import collections,sys;a,b=[open(p).read().splitlines() for p in sys.argv[1:]];s=sum((collections.Counter(a)&collections.Counter(b)).values());print(s,len(b),f'{s/len(b):.0%}')" settle.txt read.txt`

**Also eyeball the first live renders** (a broken band degrades to a loud DO-NOW rather than
silently reverting the message to its old shape, so a silent revert is not a failure mode — but the
CONTENT has never run in the cloud). **Pass = exactly ONE message per run (settle = the 📋 photo, read = the 📖 slim
report [2026-08-05]), no 🚨, no ✅, a 💰 SINCE-LAST line
that reads true, and the read still places a limit rather than quoting an entry price.** A 🚨 naming
`digest` or `orders` ⇒ check `cron.log`. Test count and suite state: `python3 -m pytest
research/tests -q` (never restated here — it drifted to a stale "109" for a day and had to be
genericized).

**STILL UNTESTED IN THE CLOUD: the read routine's `orders place` path.** It landed 2026-08-03; the
08-03 read placed the DXCM order by hand-equivalent path and the 08-04 read was thin (0 takes
cleared the bar), so the automated branch has not fired. Check that a run with a take actually
places a limit.

**LIVE RIGHT NOW [2026-08-09]: one working ledger row — DVA — and its broker fill is ALREADY
booked.** The user placed his own dip-bid GTC limit (`placed_at` 2026-08-07) and it filled the
same morning; the book row exists, so the pending orders row is a formality that resolves at
Monday's `orders check` (the digest shows the "filled + BOOKED" FYI meanwhile). If the MODEL
row instead EXPIRES untouched midweek, the GTC alarm fires once — `orders pulled DVA` clears
it; no live limit remains at the broker. Numbers live in `python3 -m research.orders show`,
never here. (This block's prior occupant, the DXCM order, completed its full arc: placed
08-03, filled 08-05, booked, rotated into DVA 08-07 — and exposed the permanent-nag bug fixed
in the 08-09 block above.)

The paper bet scores vs XLV either way — execution never touches the verdict.

**0. [LIVE, needs nothing but time] [ORDERS #1] — is the entry band too tight?** Pre-registered
   2026-08-03 BEFORE any order existed: at **N≥20 resolved orders**, if EXPIRED orders' median 21d
   excess beats FILLED orders' by **>+3pp**, the band is too tight → widen WITH evidence; else
   vindicated. **DIAGNOSTIC only — it calibrates EXECUTION, never EDGE, and does not move the
   Arc 5 #7 bar.** Do NOT touch `ENTRY_BAND_MAX`/`ORDER_EXPIRY_D` before that N, and never because
   one name got away. `python3 -m research.orders show`. The adverse-selection worry it exists to
   answer, plus the "N=40, one earnings season" caveat, are written out under *Backlog*.

**0b. [DONE 2026-08-02 — the book is now SWING-ONLY and its numbers changed twice]** Two removals,
   both corrections rather than trades: the phantom 17-share SPCX lot ($1,785 of cash
   recorded as stock at seed and marked to SPCX's price for five weeks) and then the real 1-share
   SPCX lot (long-realm holding → the private repo). The seed baseline was cut twice and the
   phantom lot had been hiding ~7.5 points of drawdown; current seed, equity and % vs baseline are
   rendered every day by `python3 -m research.book mark` and on the digest's BOOK line — never
   restated here. `book_equity.csv` history was deliberately NOT rewritten — those were the numbers we
   actually reported, so the curve carries a step down. Book = CMPS, NIO, SPY anchor. Nothing was
   sold; the SPCX share is still held, just tracked in the other realm.

**1. [DONE 2026-08-02 — Arc 3 is CLOSED, the silo is DELETED]** The [ARC 3 #1d] audit ran:
   **0–2 entity-stack artifacts of 18** against a locked ≥7 threshold — the candidate stream was
   clean. What actually killed the arc was arithmetic, logged first and independently: a 126d
   verdict horizon against a 2026-12-31 kill date made N=20 unreachable after ~2026-07-08. It ran
   out of calendar, not credibility. `insider*.py` + ledger + caches deleted; evidence in
   `FINDINGS.md`, code in git history. **Two findings are paid for if it is ever rebuilt** (needs a
   fresh pre-registration): the 3-insider trigger is holed by entity stacking (real, but it never
   fired through openinsider), and IPO-allocation filings are the LARGER false-positive mode
   (5 of 18 — exclude filings at an offer price near an IPO date).

**2. [RESOLVED 2026-08-02 — the cut is REVERSED] NIO HOLDS.** $4.88 vs a 52-week low of $4.44 is
   11% off the bottom; selling there is the capitulation leak `SKILL.md` already booked from
   HELP/XRP. Stop stays $2.90, exit into strength only. The delivery thesis is still dead — this
   is an execution-price call, not a revived thesis. FINDINGS 2026-08-02 (book decisions).

**3. [WATCH, do not act] The mover skip-calibration's first numbers came back with the WRONG
   SIGN** — the candidates we passed on beat the ones we took (FINDINGS 2026-08-01(d)). The
   pre-registered bar is skips-63d at N≥30 and we are far below it, so this decides nothing
   yet. If it holds, the read is not merely conservative, it is anti-selective.
   **The sample grows on its own and needs no intervention** — roughly one 25-row cohort matures
   per session and the daily settle routine picks each up automatically. Current scored counts:
   `python3 -m research.movers show`. Note the
   maturity clock runs from `logged_at` (the DECISION date), **not** the `date` column (the bar
   date) — they differ by a session and reading the wrong one overstates what is ready to score.

**4. [PARTIALLY TESTED] The mandatory 21d fast sleeve** landed 2026-08-01 (`READ_LOOP.md` step 4).
   Read runs have since fired 08-03 (+6 bets, incl. 21d) and 08-04 (thin — 0 takes cleared the bar,
   which is the rule working, not a miss). Keep checking that each run either registers a 21d bet
   or states in one line why no take qualified — that line is a claim, not a free pass.

**5. [NO ACTION — documented on purpose] `book_equity.csv` has no 7/28–7/29 rows** (`snapshot`
   did not exist on master then) and carries weekend rows with duplicate marks. The 7/31 hole
   WAS real and was backfilled from a stranded commit because it had been measured. Do NOT
   backfill 7/28–7/29 — those were never measured.

**6. [MOOT 2026-08-02] `insider_ledger scan` also settles** — resolved by deletion, not by a
   fix. Kept as a one-line note because the CLASS of bug (a read-shaped command that writes) has
   bitten this repo twice; `movers.run` still carries the guard and its regression tests.

## Recent changes
- **2026-08-05b (edge-system staged · external capital frozen)**
  - **[EDGE-SYSTEM]** added to the backlog as a NAMED TRIGGER, not a build; the 8-K bullet's
    swallowed headerless fragment absorbed there.
  - **External capital FROZEN** (user decision, two gates) — FINDINGS 2026-08-05; the
    CLAUDE.md book line amended to match. Docs-only session: no module/READ_LOOP/daily.sh
    change → cloud prompts untouched, deliberately.
- **2026-08-05 (the read push goes slim · the ✅ ping is outlawed · the double-settle decoded)**
  - **Trigger, from the user:** three Telegram messages on 08-05, "still all repetitive" after
    the 08-04 band work. Decomposed into three separate defects, each with its own fix:
  - **(1) Overlap: the pre-registered re-measure MISSED — 56% vs ≤55%** (exact command from the
    WATCH block, on the real pair). Unflattered view: **87% of the settle message (20/23 lines)
    reappeared verbatim in the read one**; the 69%→56% "improvement" was mostly the read message
    growing a RUN NOTE (denominator inflation), not less echo. Fail branch fired as
    pre-registered → `digest.compose(slim=)` + `--slim` flag, wired into READ_LOOP step 7 and
    the read cloud prompt. Slim = 📖 report: band + DO-NOW + book header/cash + bets/movers
    one-liners + run note; drops position rows, the ENTIRE orders block (every pending order
    already rides in DO-NOW with a live spot; the rest was counts + static config reference),
    and the 📋 banner (settle's photo owns it — the banner split also ends "which message do I
    read?"). Chose the DETERMINISTIC variant over the vs-HEAD diff the deferred item sketched:
    read cannot change book/orders, so for it they are unchanged BY CONSTRUCTION; a vs-HEAD
    diff still lies when only marks move (the original objection) and would hide a freshly
    opened position forever once committed. DO-NOW is NEVER slimmed. 4 new tests; stubs of the
    two sections now take `*a, **k`. Local same-instant sims read 58-62% — inflated by
    artifacts a real 6h-apart pair cannot have (identical band/marks/spots); the real pair
    tomorrow is the pre-registered verdict.
  - **(2) The stray "✅ read-loop heartbeat: digest pushed" is a CONTRACT VIOLATION, not drift:**
    the read prompt already said "Never send a second message" — the cloud agent (Opus 4.8)
    improvised a success ping anyway. Plausible confusion source: READ_LOOP.md's own title said
    "generation heartbeat". Fixed on every surface: title reworded, explicit NEVER-✅ line in
    READ_LOOP step 7 + read prompt + CLAUDE.md contract line (heartbeat = failures only; the
    one push IS the confirmation).
  - **(3) The settle trigger fired ONCE (05:07:25 UTC) but committed TWICE** (25d5ce0 05:08 =
    book_equity only; 8799328 05:29 = movers scoring + both self-heal header migrations):
    the routine agent re-ran daily.sh after the first pass's feed-dependent steps failed. The
    first pass's digest AND its 🚨 heartbeat both died in transport — the user received
    NOTHING from it (the documented transport-down blind spot, observed live for the first
    time; watchdog still narrows only total-death). The improvised retry was CORRECT and is now
    a sanctioned ONE-SHOT rule in the settle prompt (re-run only if the digest did NOT push).
    No code built for this — cloud session report is where the exact step failure lives.
  - **Also:** DXCM broker fill (5 @ 84.28, GTC limit) recorded via `book open` — free cash ~$6;
    `orders check` resolves the ledger row against the 08-05 bar at the next settle. Phantom
    `origin/main` pruned locally (the remote branch lived 2 min on 08-02, created+deleted same
    session — GitHub activity log). CLAUDE.md Telegram-contract paragraph rewritten (📋+📖).
  - **[ARC 5 #2b]** pre-registered: at N≥20 settled, a miss of the paid-data trigger now
    produces a scheduled DECISION POINT (three pre-named options) instead of drifting to the
    kill date. Pre-commits the WHEN and the INPUTS, never the outcome.
  - **[ORDERS #2]** shipped (user's explicit call): `orders place` auto-sizing =
    min(cash cap, floor(`config.RISK_PCT` × equity / stop distance)). Cash-cap-first so a cash
    refusal never fetches marks; shorts unchanged (`--shares` required). Read-routine prompt
    re-read and its sizing sentence patched the same session (the standing rule).
  - **8-K orphan arc** added to the backlog as a NAMED TRIGGER, not a build.
- **2026-08-04c (the denominator widens to the S&P 400/600 tail + four leaks close)**
  - **Trigger, from the user:** a step-outside-the-limits review — "we need this system to be
    more alive and eating signals to generate real alpha; find what's blocking us, but don't
    be too sure." The diagnosis and its uncertainty are pre-registered, not asserted:
    FINDINGS 2026-08-04 (caveats a–c + [ARC 5 #11]).
  - **The strategic finding:** since Arc 3 closed, the ONLY candidate stream was S&P 500
    movers — the arena Arc 2's own conclusion calls arbitraged — and 21 of 53 bets were
    same-season post-earnings-drift longs. The pooled verdict was quietly becoming "can the
    read beat the market where our own evidence says nobody can, with one trade shape."
  - **Shipped:** two-cohort scan (`universe` column, per-cohort feed keys, committed 400/600
    caches, cache-only `universe.tail()`), completed-session guard on scan, `last_bar` +
    coverage feed truth with digest escalation, engine split render fix (closed AND open,
    every branch) + per-universe diagnostic, `book target` + touched-band DO-NOW, READ_LOOP
    ≤3-per-tag ceiling + tail guidance, NIO USER bet + structured 4.85 target.
  - Suite state: `python3 -m pytest research/tests -q` (never restated here). Caches: local
    one-off build (Wikipedia constituent lists), committed, read-only in cloud, rebuild
    procedure in the [ARC 5 #11] Reproduce line.
  - **Both cloud prompts re-read and patched the SAME session (2026-08-04, the standing
    rule):** `read` (`trig_01EsetvEZmVLb56fEmc7YvSi`) gained the [ARC 5 #11] block — two-cohort
    scan, tail read bar, hard tag ceiling, feed DO-NOWs are report-only; `settle`
    (`trig_01Uz2fQRMh5UwjnSvFkaSNBY`) gained the 2026-08-04b block — tail rows in `movers
    settle` are normal, per-cohort feed keys, feed/exit-band DO-NOWs are human-only, never
    repaired in-run.
- **2026-08-04b (the message says what CHANGED — 💰 SINCE-LAST band + the circuit breaker becomes visible)**
  - **Trigger, from the user:** "why did we decide to essentially echo the same content for settle
    and read? wouldn't it be more valuable for each to have their own information?"
  - **Measured first:** 69% of the two daily messages' lines byte-identical (~85% discounting
    refreshed spots); only 2 of the last 7 settle runs changed a scored row. Nothing in the repo
    computed a delta.
  - **`digest._committed()` anchors on git HEAD** — the last PUBLISHED state. No state file (an
    ephemeral checkout would need it committed, and the read run commits BEFORE it pushes, so its
    own write could never land). The commit state IS the window; same trick as `watchdog`.
  - **`book.mark_delta()`: a period's P&L is `Δunrealized + Δrealized`, NEVER `Δequity`.** The
    08-02→08-03 scope removal reports its true −$30.01 with the −$1,920 fiat move named separately,
    instead of a −35.7% day that never happened.
  - **Three false-number bugs caught before shipping** — one by the band's first live render, two by
    an independent red-team on a different model:
    (a) rows keyed by `logged_at` alone collided (11 timestamps shared by 2 bets each) and announced
    a settlement that never happened → identity is `(logged_at, ticker)`;
    (b) my first guard (`d_equity == d_cash + d_unrealized`) was satisfied EXACTLY by a deposit, so
    funding the book would print as a +28.5% day;
    (c) the same guard was VIOLATED by an ordinary `book open`, so a normal trading day — the next
    thing that happens when DXCM fills — printed "RESTATED, not P&L".
    All three regression-tested against the real data that produced them.
  - Also from the review: a dead price feed no longer reports as a scope change (the band withholds
    and names the feed), movers settlements now count in the band, `next score ≥` can no longer
    print a past date, the pool-stop DO-NOW is clearable (gated on risk still being ON), and the
    stale-limit alarm is no longer silenced by holding that ticker.
  - Pool-stop LEVEL on the BOOK line + breach → DO-NOW (it could only reach `cron.log` before);
    next-evidence date on BETS (`≥2026-08-20 SMCI`); order session countdown (`sessions_left` was
    dead code); **expired-order-still-live-at-broker DO-NOW** + `pulled_at` column + `orders pulled`.
  - **`digest`'s CLI is unchanged** (a designed property of the HEAD anchor, not luck). `orders`
    DID gain a verb (`pulled`), so the standing rule was honoured — **both prompts re-read the same
    session**, neither was stale (`pulled` is human-only; no routine runs it). Two ASYMMETRIC calls
    worth knowing: **`settle` WAS patched** (2026-08-04) to expect the 💰 band, to quote it verbatim
    in its report so the first cloud render is visible, to treat a `since-last silo DOWN` DO-NOW as
    the band failing loud by design rather than something to fix, and to add "pull" to the list of
    things it must not do to an order. **`read` was deliberately NOT patched:** it points at
    `READ_LOOP.md` and already carries "if this summary and the doc disagree, the DOC WINS", and
    that doc was updated — which is the designed mitigation doing its job. `settle` points at
    `daily.sh`, not at a doc, which is why it needed the words directly.
  - Tests 113 → 147. **PRE-REGISTERED: re-measure the 69% overlap next weekday, bar ≤55%** — a miss
    is the evidence that promotes section-collapse from "cut" to "build".
- **2026-08-04 (digest layout — the message stopped ending in a wall of nothing)**
  - **The trigger, from the user:** both of the day's pushes had "big gaps of space near the
    bottom", and the 7am read push had "a bunch of text stacked on top".
  - **Gap = a real bug.** `compose()` emitted a blank separator per section unconditionally, but
    four sections (git, stranded, feed, liveness) only ever return DO-NOW *actions* and never
    display lines — so every message, every day, ended with **five** blank lines. Now a section
    with nothing to show is skipped. Max consecutive blanks: 5 → 1.
  - **Stacking = the run note's shape.** The read run's note (headline + the multi-line 5a/5b
    alert blocks) was escaped and prepended WHOLE, pushing the ⚠️ DO-NOW list ~15 lines down and
    duplicating the ORDERS section above it. `compose(note)` now splits on the first newline:
    line 1 is the bolded headline on top (it is the Telegram notification preview, and the only
    thing distinguishing a read push from a settle push), the body becomes a `📖 RUN NOTE` block
    at the BOTTOM. Bonus: if a long note ever hits the 3900-char truncation, the *note* is cut
    now, not the actionable digest.
  - Command interface UNCHANGED (`digest --notify "<note>"`), so **no routine prompt needed
    patching** — the drift trap did not apply this time. READ_LOOP step 7 restated to say
    first-line-is-the-headline, so the doc can't drift from the split.
  - **NOT a bug: two digests a day is by design.** settle (05:00 UTC daily) and read (11:30 UTC
    weekdays) each push exactly one 📋. On a weekday that is two.
- **2026-08-03 (working orders — the read→money bridge stops quoting a price that has already moved)**
  - **The trigger, from the user:** the 08-03 read pushed `5 sh DXCM @ ~83.45`; he saw it at 86.54
    and asked whether to still buy. 83.45 was Friday's close — the newest COMPLETE bar a pre-market
    run can honestly cite, and never a live quote.
  - **Measured before deciding anything** (`python3 -m research.tools.slippage_audit`, N=40 taken
    movers): median 1.07% move by the next open, **2.42% by the next close** — waiting costs more
    than the gap — no weekday effect, tail to −23.4% (PNR). Band calibration: fill rate FLAT at
    87.5% across 1.0–2.0%, entry advantage decaying +0.52→+0.12%, so the tight band is free.
    Expiry 3 sessions = 90% of fills; sessions 3–10 add one name that had already run +19.8%.
  - **NEW: `research/orders.py` + `orders.csv`** — a working order (limit + expiry) computed by
    code, resolved daily against real bars by `orders check` in `daily.sh`, re-pushed by the digest
    while pending. Band/expiry in `config.py` (the one place). 18 unit tests + 5 digest tests.
  - **Two documented rules REVERSED, deliberately, with the reason recorded in place**
    (`READ_LOOP.md`): expiry is now STATE not supersession, and the daily run DOES re-push a
    pending order. Both rules were right for a point price and wrong for a limit — a limit is
    age-invariant. The human sleeping through the pre-market alert is the NORMAL case.
  - **`SIZED SUGGESTION:` prose marker DELETED.** It was a structured fact inside a free-text
    thesis that no code read (`grep --include=*.py` → 0 hits); 2 of 2 issued, 0 executed, nothing
    noticed. The digest now nags when an order fills and no book position appears — that specific
    blind spot is closed. Same lesson as the SPCX 🔒-on-prose bug: structured facts get a column.
  - **Scope guard:** `bets.py` scoring is UNTOUCHED and orders is explicitly DIAGNOSTIC, not a
    second verdict silo — [ORDERS #1] pre-registration written before any order existed.
- **2026-08-02b (Arc 3 closed · the repo shrinks · two corrections)**
  - **[ARC 3 #1] had already fired its kill-criterion and nobody had computed it.** 126d verdict
    horizon vs a 2026-12-31 deadline ⇒ N=20 unreachable after ~2026-07-08; 2 takes ever logged.
    We spent 2026-08-01/02 rebuilding a feed for a silo whose verdict window had closed. **A
    kill-criterion of the form "N or DATE" must be checked at WRITE time** — now a `SKILL.md` rule.
  - **[ARC 3 #1d] ran: 0–2 artifacts of 18 vs a ≥7 threshold — CLEAN.** The decisive column was
    ledger `n_insiders` vs EDGAR distinct owner strings: inflation would show as ledger > EDGAR
    and it never happens (12 exact, 6 the other way). [ARC 3 #1c]'s "the existing candidates are
    suspect too" is measured and false. A first run returned 0 docs for all 18 and looked like a
    finding — it was a bug (`primaryDocument` is the XSL viewer path). **A broken fetch that
    resembles a clean result is this project's most dangerous failure mode.**
  - **Arc 3 retired**: `insider*.py` + ledger + 216MB `edgar_cache/` + `sec_cache/` deleted, six
    call sites rewired in ONE commit. The queued de-stacked-trigger test was closed WITHOUT
    running it — structurally impossible (`_frame_one` dedupes to one owner per accession).
  - **A dead alarm fixed**: `digest._feed_section` had emitted an un-clearable "openinsider has
    NEVER succeeded" DO-NOW on every push. An alarm that cannot be cleared trains the reader to
    ignore the channel. Rule now in `feedstatus.py`: a retired feed loses its key in the same diff.
  - **v1 pipeline + `reference/` deleted** (~700 LOC, 142MB). The 20 Arc-1/2 probes were KEPT —
    all archive-cited. The stale map that would have justified deleting them also listed
    `momentum`/`universe`, which `movers.py` imports on every scan. **Verify imports, not maps.**
  - **Two corrections I owed the user**: the book's −17.1% is *not* evidence about the read (every
    position is 2026-06-25 seed inventory plus a beta anchor — zero read-generated), and the "400MB
    of dead data" was mostly the pending audit's own cache. NIO cut REVERSED (11% off its 52w low).
  - **New**: [ARC 5 #10] short-side pre-registration (n≥12 bar, diagnostic only) + the twin rule
    (no `book open` without a pre-registered bet; warns, never blocks).
  - **THE TWO REALMS, enforced (session's second half).** The long-realm holdings moved
    out of this repo; `CLAUDE.md` gained a SCOPE section; ARCHITECTURE's
    Convergence doctrine was scoped to swing capital (as written, it was what justified keeping
    a long-realm holding in the book). **A live landmine was defused on the way:** `digest`'s 🔒 flag
    sniffed the THESIS PROSE for "lock"/"park", so a position's alarm state depended on its
    wording — SPCX was silenced by a thesis saying "NO lockup". Now ticker-keyed, regression-tested
    both directions. **A privacy gap was closed in portfolio-hq:** `hq/finance/` sits inside an
    APPROVED publishing source and was protected only by a net-worth regex — now an explicit
    Hard-never source plus six targeted redlist tokens (NOT "lockup"/"IPO", which would kill our
    own legitimate lockup-expiry research drafts; verified both ways).
    - **Superseded the same day:** that directory became its own fully-private repo, so the
      inside-an-approved-source trap no longer exists. The
      Hard-never entry was kept anyway and repointed — an absence is not a statement, and
      absences get filled in by accident. Every pointer in THIS repo now reads
      "the private long-realm repo"; the two lines above keep their then-true paths as history.
  - **The crash question was asked and declined**, with the reading logged and an explicit guard
    that it is not a prediction either way. Arc 1 already falsified the actionable version.
  - **A memory was wrong for a month:** `wealth-loops` is vertical-foundry's OLD GitHub name, not a
    separate project. Corrected. Verify a repo exists before recording it as one.
- **2026-08-02 (session-clear cleanup: integrity + honest docs)**
  - **A read-only sweep corrupted the denominator.** Bare `python3 -m research.movers` defaulted
    to `scan` — and every UNRECOGNISED command fell through to the write path too — so it
    appended 25 `seen` rows re-scanning an already-decided bar, and `daily.sh`'s `git add -A --
    $LEDGERS` would have committed them at 05:00 UTC. Restored before it landed. Both
    `movers.run` and `insider_ledger.run` now default to `show` and reject unknown commands
    without writing; the insider one could also fire a 🚨 push on a typo. Regression tests
    assert bare/typo invocations leave the CSVs byte-identical. **This is the same LEDGER
    COLLISION class as 2026-07-24, reached by a different route.**
  - **`insider_sec.py`'s stop-condition had inverted into a go-signal** ("do not flip until the
    parity recall is logged" — it is now logged, as three FAILs). Rewritten as DORMANT/FAILED/
    DO-NOT-WIRE-IN and added to the dormant list below.
  - Docs corrected to describe the system that EXISTS: one verdict silo not two; the N=20 bar
    now carries its trigger caveat on the live `engine` surface a cold session sees first;
    `LOOP.md` no longer tells a fresh session to re-test four CLOSED dead ends while rule 1 of
    the same file says never re-test a dead end.
- **2026-08-01/02 (the SEC insider feed arc — built, gated, FAILED, kept dormant)**
  - `research/insider_sec.py`: a live insider feed from the SEC EDGAR daily index, built to
    replace the cloud-dead openinsider scrape. Feeds `insider._group()` unchanged. **Failed its
    pre-registered parity gate three times** (0.946, then 0.929/0.743 against a 0.95 bar) and is
    NOT wired in. Commits `cab1847` `eeb544e` `9559368` `5571f20` `f5af3e4` `095176c`.
  - Two of its own bugs, both caught by running the gate rather than trusting the code: a 400KB
    read cap silently TRUNCATED the daily index (form-4 rows begin part-way in, so busy days
    returned plausible-looking PARTIAL lists that were cached as authoritative), and a single
    TLS timeout killed a multi-hour run. Both fixed; the cache path is now versioned by parser
    (`sec_cache/v2/`) so a semantics change cannot silently reuse stale rows.
  - **The finding that outlived the feed:** the 3-distinct-insider trigger counts one investor's
    entity stack as three insiders on a SINGLE Form 4. openinsider fed it that way for the whole
    life of the ledger. See FINDINGS [ARC 3 #1c] and the pending [ARC 3 #1d] audit.
- **2026-08-01 (recover the lost day · unstick trading · arm the watchdog · push durability)**
  - **The 7/31 settle run was LOST and recovered.** It committed `1b014cc` (six Telegram
    `notified` stamps, the 7/31 equity row, 25 scored movers rows), the push failed, and the
    ephemeral checkout was destroyed; the work survived only by accident on the harness's own
    session branch. Master ran two days without it. Recovered by restoring the two
    non-recomputable artifacts (the delivery stamps, the equity mark) and RE-DERIVING the movers
    scores from completed bars rather than resurrecting them.
  - **`scripts/push_ledgers.sh` (new)** — the commit/rebase/push leg moved out of `daily.sh`
    because inline it was untestable, and untestable is how the above shipped. It now VERIFIES
    with `git merge-base --is-ancestor HEAD origin/master` instead of trusting an exit code, and
    on failure parks the commit at `settle-backup/<date>-<sha>` so it outlives the container.
    `digest._stranded_section` nags every run until a human recovers the ref (a one-shot
    heartbeat was already proven insufficient). Two bugs found by the new tests: `git diff
    --quiet` never sees NEW files (so a first-of-its-kind ledger was silently never committed),
    and git chatter on stdout would have become fake step names inside a 🚨 alert — stdout is now
    a status channel on fd 3, everything else goes to cron.log.
  - **The `$500` idle-cash gate → `digest.IDLE_CASH_MIN`** (the constant is the single source;
    do not restate its value here). It was silencing the bridge at
    a free-cash level the book could not reach. An operating convention, never a pre-registered
    bar. See FINDINGS 2026-08-01(b).
  - **Fast sleeve is now MANDATORY when the catalyst is fast** — generation cadence only, no bar
    moves. It had produced ONE bet in five weeks. FINDINGS 2026-08-01(c).
  - **The watchdog routine is ARMED** (`trig_01Jk65Rg2VQ9WjzjvCdD5SHP`, daily 19:13 UTC, own
    session, repo bound, MCP connectors stripped — it is read-only by design).
    **CORRECTION to the 2026-07-24 FINDING 1:** agent-created routines are NOT repo-less. They
    accept `job_config.ccr.session_context.sources[].git_repository.url`, exactly as the read and
    settle routines already do. The earlier routine must simply have been created without it.
    That wrong note sat in this file for a week and blocked a fix the agent could always have made.
  - `__main__.py` still printed the read cadence as "Mon/Wed/Fri" (stale since 7/24) — last live
    surface carrying it. The settle routine's cloud prompt said it too; both fixed.
- **2026-07-30 (merged the hardening branch to master + partial-bar guard)** — The 7/27 hardening
  work sat unmerged for 3 days while master kept running the old lossy code and six bets settled
  under it. Merged; one conflicting file (`bets_catalogue.csv`) resolved by taking master's rows as
  the base (correct MU −7.99%, the 6 settlements, the 6 bets added 7/28–7/30), adding the
  branch-only INTC row, adding the `notified` column blank on every row. The branch's MU row
  (−8.65%) was DROPPED: it had been scored mid-session against a still-open bar.
  **New guard:** `bets._score` / `insider_ledger._score` now refuse an exit bar dated today —
  two symmetric gates (no-lookahead on entry, completed-session on exit). `today` is injectable for
  tests but defaults to the real UTC date, since a gate that can be skipped by omitting an argument
  is not a gate. The scheduled settle (05:08 UTC) was never exposed; this protects manual runs.
  The six closed rows keep `notified` blank on purpose — they were never announced per-bet (only
  the aggregate BETS line in a read digest), so the next settle run delivers them. 84 tests pass.
  **Still open (user action):** the watchdog Routine must be created in `/schedule` by hand, and
  openinsider has produced nothing since 6/25 — see FINDINGS 2026-07-30(c).
- **2026-07-27 (daily-process hardening — 9 gaps found in an audit of the settle/read/Telegram loop)** —
  Two had already fired for real, both SILENTLY. (a) **Settlement announcements could be lost
  forever**: the silos saved the closed row then called `notify.send()` and discarded the result;
  fail-soft means a dropped message exited 0, `daily.sh` logged no failure, and the retry set was
  "rows open when settle started" so a closed row could never be re-announced. Fixed with a
  `notified` column stamped only on confirmed delivery — the retry set now comes from the ledger.
  `bets.run`/`insider_ledger.run` return exit codes (mirroring `digest.run`). (b) **`python-dotenv`
  was undeclared in requirements.txt** while `config.py` imports it → a fresh container has no
  working Telegram at all; root cause of (a) hitting MU.
  Also: per-row isolation in both `settle()`s (one poisoned row used to abort the whole run);
  `digest._safe` escalates a dead silo to a DO-NOW instead of a quiet trailing line; new
  `research/feedstatus.py` because a dead FEED does not raise (a `scan` returning nothing is
  indistinguishable from a quiet day); `daily.sh` rebases before pushing to master (the collision
  in f57e220 was not a one-off); the digest's hardcoded "Mon/Wed/Fri" read cadence removed
  (3 days stale — the anti-drift rule applied to itself); matured-but-unscored bets past a 3-day
  holiday-drift buffer become a DO-NOW instead of drifting invisibly in the maturity list.
  New: `book.equity_marks()` (one computation behind BOTH `mark` and the new `snapshot`, so the
  printed and logged numbers cannot diverge) → `research/book_equity.csv`, one row/day, tracked;
  `research/watchdog.py` + a SEPARATE cloud routine as the external dead-man's switch.
  82 tests pass. No verdict bar, threshold or horizon touched; honest prior UNCHANGED: LOW.
- **2026-07-24 (read routine → PRE-MARKET daily; smoke-test findings on routine ownership)** —
  The read routine fired 22:09 UTC Mon/Wed/Fri = **18:09 ET, ~2h AFTER the close**: alerts the human
  could not act on for 15+ hours, quoted at prices that no longer existed (the [ARC5 2026-07-10]
  red-team note made operational), and Tue/Thu catalysts read 1–2 days late through peak earnings
  season. **Moved to `30 11 * * 1-5` = 11:30 UTC ≈ 07:30 ET weekdays, ~2h BEFORE the open** (user
  applied the cron in the UI). READ_LOOP.md gains a "WHEN this runs: PRE-MARKET" section — quote
  every level off the **last complete daily bar (yesterday's close)**, labelled indicative; never
  fabricate an intraday print. Cadence de-drifted in README / CLAUDE / ARCHITECTURE (dated FINDINGS
  entries keep their then-true text per the anti-drift convention).
  **FINDING 1 — agent-created routines CANNOT hold a repo source.** An attempt to recreate the read
  routine via `create_trigger` (so the agent could edit its own schedule) produced a routine whose
  fired session lands in an EMPTY directory: a read-only smoke test (prompt temporarily swapped,
  fired, restored) reported `repo: NONE`, no git repo, no research files, deps missing. A second
  probe confirmed sources do NOT inherit from the calling session even with `environment_id` omitted.
  `sources` is a claude.ai-UI-only field; `update_trigger` also rejects `model` changes
  (`model_update_disabled`). Both agent-created routines were deleted; the UI-created routine remains
  the only working one. **Consequence + the workaround that matters:** the UI owns only the SCHEDULE
  and MODEL — the routine prompt delegates authority to `research/READ_LOOP.md` ("the doc is the
  authority"), so the routine's BEHAVIOR is fully editable from this repo. Change behavior in the
  doc; only schedule changes need a human in the UI. **Do not retry the recreate-so-the-agent-can-own-it
  approach** — it is structurally impossible, not a permissions accident.
  **FINDING 2 — the Telegram duplicates are ALSO prompt-level, not just `notify.py`.** The smoke test
  double-sent while having NO repo, i.e. via raw `curl`, never touching `notify.py`. The routine
  PROMPTS across projects instruct "verify `ok:true`; **on failure retry once**" (portfolio-hq
  observer / publisher / job-scout, vertical-foundry digest) — the same ambiguous-retry bug this
  session fixed in code, encoded in English: a timed-out-but-delivered send gets re-sent.
  **CLOSED for THIS repo 2026-08-06** (it fired first: the "delivery check" duplicate + bare
  "Probe" — FINDINGS [OPS] 2026-08-06): both prompts now key any re-send on the digest's printed
  `PUSH REJECTED (nothing sent)` verdict and name `research.notify` HUMAN-ONLY. STILL OPEN for
  the other repos' prompts (deferred by user 2026-07-24, out of this repo's scope).
  **FINDING 3 — prompt/doc drift in the live read routine.** The UI prompt still
  numbered its steps 1–6 and named `research.notify` for the push, while READ_LOOP.md moved on.
  **CLOSED 2026-08-06:** both prompts REWRITTEN COMPACT via `RemoteTrigger update` (which works —
  see the [OPS] item) — they delegate to the repo docs by construction, so this drift class now
  has almost no surface. The "doc wins" line stays in both.
- **2026-07-24 (LEDGER COLLISION — interactive session vs the scheduled read run)** — An
  interactive session scanned/decided movers and added bets at ~23:35 UTC while the scheduled
  **read** routine had already done the same work at 22:11–22:16 UTC the same evening (the session
  branched from the pre-run commit and never saw it). Result before reconciliation: **DLR
  pre-registered TWICE** (once by each) and **50 mover rows for 25 candidates** — an inflated
  multiple-testing N and a corrupted denominator, i.e. exactly what the integrity guards exist to
  prevent. **Resolution (first timestamp wins):** `movers_ledger.csv` taken verbatim from the
  scheduled run (its 22:11 decisions are the earlier pre-registration — never rewritten); the
  session's duplicate DLR bet dropped; the session's **MSCI** bet KEPT (a genuinely independent
  later read of a candidate the scheduled run skipped — both records stand, both timestamped, so
  the audit trail shows the disagreement rather than hiding it). Net: 37 bets, 300 movers seen,
  0 unread. Divergences worth noting: the scheduled run took **ROL short** and **LMT long** where
  the session skipped both as ambiguous/sector-beta; the session took **MSCI** where the run
  skipped it. **LESSON:** an interactive session must `git fetch` and check for a same-day read-run
  commit BEFORE running `movers scan` or `bets add` — the scheduled run owns the daily denominator.
- **2026-07-24 (Telegram duplicate-message fix + trade alerts ungated, with user)** — Off a "my
  Telegram is a mess, routines repeat messages" report. THREE real bugs found, all shipped:
  (1) **`notify.py` double-post** — the HTML fallback retried after ANY exception, including a
  timeout. A timeout is AMBIGUOUS (telegram may have delivered and only the response was lost), so
  the retry sent a SECOND copy — the duplicate-message bug. Now retries ONLY on a definitive answer
  (`ok:false` or an `HTTPError` status = nothing delivered); an ambiguous failure returns False and
  sends nothing more. Prefer one lost message over two sent. New regression test pins exactly-one-post
  on timeout; the existing HTML-fallback test now simulates a real telegram 400 (`HTTPError`) rather
  than a bare `OSError`, which conflated the two cases. (2) **`daily.sh` was DEAD in the cloud** —
  it opened with `cd /home/guillermo/code/claude_trader || exit 1`, a laptop-only path, so every
  cloud settle run exited immediately (the PRIMARY settle path did nothing and the routine improvised
  its own messages). Now resolves the repo root from the script's own location; `/usr/bin/python3` →
  `python3` from PATH. (3) **`digest.py` maturity display lied** — `days_left` counted CALENDAR days
  while `bets.settle` scores on TRADING bars, so live bets rendered as ~8 days OVERDUE and made
  settlement look broken. Now counts weekdays (stdlib `_busdays`, no numpy — digest stays
  dependency-light). Post-fix the same bets read MU(0d)/ON(1d)/CIEN(2d) = due now, matching settle.
  (4) **TRADE ALERTS UNGATED (with user)** — READ_LOOP step 5 split into 5a/5b: the 🟢 alert now
  fires for ANY take (ranked, ≤2), with NO free-cash gate; the old ">$500" gate silently swallowed
  actionable reads whenever the book was low on cash. Sizing (5b) still gated on cash. The alert
  rides INSIDE the one digest push — never a second send. ~~STILL OPEN: a stale one-shot routine `claude_trader catalogue settle`~~ **DELETED by the user;
  verified gone 2026-08-02** (`RemoteTrigger list` shows only `read`, `settle`, `watchdog` for this
  repo). This line stayed marked OPEN after the fact and got read back to the user twice as an
  outstanding action — **a closed item left open in the backlog becomes a recurring false alarm.**
  Close records when they close.
- **2026-07-10 (book reconciliation + Telegram v1.1 + suggestion loop, with user)** — Off a "digest
  is unreadable + free cash never invested" review. (1) **Phantom SGOV park removed** — the 7/06
  11-sh park was booked but never executed at the broker (user-confirmed); cash restored (exact
  inverse of the open), realized P&L verified unchanged; fix = direct `book.csv` edit, the commit
  is the audit trail (no `book cancel` plumbing for a one-time event). (2) **Telegram v1.1 SHIPPED**
  — `notify.py` gains HTML mode + newline-safe >4096 truncation + plain-text retry on rejected HTML;
  `digest.py` rebuilt: DO-NOW list with tap-to-copy `<code>` commands, per-position BOOK block
  (entry→spot, P&L%, stop/⚠️THRU/🔒 flags), dual-mom arrow; lock flag now requires NO stop set
  (fixed the SPCX liquid lot masked by its thesis mentioning the locked sibling — it surfaced as
  THROUGH its stop). `daily.sh`: heartbeat is now the 🚨 FALLBACK (fires only on a failed step or
  failed digest push; digest exits 1 on a lost send) — clean day = exactly ONE 📋. Rejected-for-now
  v1.2: folding the 🚨 settle pushes into the digest (needs a `settled_at` column in two silos for
  a ~weekly, event-worthy message). (3) **Trade-suggestion loop (zero new code)** — READ_LOOP step 5
  DEPLOY: when book cash idle > $500 the read run MUST emit ONE sized order (pre-registered as a
  `SIZED SUGGESTION` bet + paste-ready `book open` confirm command with a `<fill>` placeholder;
  human executes at broker) or state in one line why cash stays idle; expiry = supersession at the
  next run's ORIENT check. Policy decided with user: ALL free cash available to suggestions
  (FINDINGS 2026-07-10). Considered splitting bets vs book into separate projects — NO (shared
  plumbing; the silo wall, not repo boundaries, protects the verdict N; the suggestion bridge now
  spans them). Doc sync: README / CLAUDE / ARCHITECTURE / READ_LOOP.
- **2026-07-06 (legibility + capital + measurement pass, with user)** — Five shipped changes off a
  "system feels clunky / cash idle / too conservative?" review. (1) **Actionable digest** `digest.py`
  [W4] — ONE message: ⚠️ ACTION-NEEDED list (missing/through stops, idle cash, maturing bets) + book/
  bets/movers state, fail-soft per silo; now the PRIMARY Telegram push from settle+read (heartbeat
  kept as proof-of-life backstop). (2) **`movers settle`** [ARC 5 #9] — scores take AND skip fwd vs
  SPY at 21/63d (+`x21_pct`/`x63_pct` cols, reuses `bets._score`); the DIAGNOSTIC for "is the read too
  conservative?", pre-registered threshold locked, NOT a 3rd edge silo. (3) **`book stop TICKER PRICE`**
  subcommand; set CMPS/NIO/SPCX-liquid exit rules. (4) **Idle cash → SGOV** (risk-free park, kills the
  dead-nominal drag). (5) **Local env**: system py3.14 had no pip/pandas/dotenv — restored via apt
  (`python3-pandas python3-pytest python3-dotenv`). Verified: 57 tests green, full status + `movers
  settle` run clean. Doc sync: README/CLAUDE/ARCHITECTURE (digest push + movers `settle`).
- **2026-07-03 (cloud read run — movers scan unblocked; finished the 7/2 egress fix)** — The
  cloud `read` routine's `movers scan` still hung/failed: `movers._fetch` was left on
  `yf.download` (curl_cffi), which the agent-proxy resets (TLS `curl (35)`) — the 7/2 fix moved
  `prices.py` to the urllib chart endpoint but NOT this seam. Repointed `_fetch` at
  `research.prices.daily_history` (threaded, 8 workers; ~503 names in ~30s, 0 rate-limits vs
  yfinance's 429s). Scan then ran clean: 25 new S&P 500 movers logged. Run outcome: 0 general
  takes (cohort-dominated week — AI-software melt-up UP, memory-glut selloff DOWN + 3 no-edge
  discrete events), 25 mover skips, insider queue empty (openinsider fetch still failing — separate
  denominator, non-blocking). `universe.sp500()` still emits a stray yfinance SSLError but falls
  back fine — cosmetic, left as-is.
- **2026-07-03 (notification contract: every run pushes — silence = broken)** — User decided the
  open read-run question (yes) + asked for a daily alive-signal with attention-calling format for
  important events. Shipped: `research/heartbeat.py` (✅ ran clean / 🚨 step failed + ledger
  tallies; PURE builder, tested), `daily.sh` tracks per-step failures and heartbeats LAST+ALWAYS,
  settle msgs now 🚨-prefixed, READ_LOOP step 6 = 📖 run-report push, read trigger prompt
  re-synced same session (the 2026-07-02 drift rule). Emoji key: ✅ heartbeat · 📖 read report ·
  🚨 needs attention. Verified: 50 tests green + real ✅ send received. Closes the "read-run
  Telegram summary" backlog item; v1.1 (book ±5% swing, dated-trigger pings) stays deferred.
- **2026-07-02 (doc hygiene, pre-session-clear)** — Split the closed-arc log entries (Arc 1-2 +
  Arc 4, verbatim, every number + `Reproduce:` line kept) out of `FINDINGS.md` into
  `FINDINGS_ARCHIVE.md` (736→~420 lines; the header digest + live Arc 3/5 stay); compressed this
  file's pre-July entries to one-liners (detail: FINDINGS + git log). Also: Telegram notify v1
  LIVE end-to-end (creds in `.env` + cloud env, test send verified); docs synced (README /
  CLAUDE.md / ARCHITECTURE mention notify + the archive).
- **2026-07-02 (cloud egress block CONFIRMED + RESOLVED same day)** — The Thu 7/2 manual cloud
  `read` run diagnosed from inside the env: `openinsider.com` AND `fc.yahoo.com` (yfinance's
  crumb host) were proxy-denied, while `query1.finance.yahoo.com/v8/finance/chart` returned 200 —
  so neither denominator scan could auto-run, and (latent) the daily settle's price math would
  have failed at first maturity (~Jul 24). The run coped by triaging the locally-seeded 7/1 mover
  queue (25 → 2 takes CRL/APD, 23 skips). BOTH fixes applied: (A) user set the full allowlist
  (incl. `fc.yahoo.com`, `www.openinsider.com`; list in `raw_input/cloud_env_setup.md`,
  local-only); (B) `prices.py` rebuilt on the open chart endpoint via stdlib urllib (adjusted
  OHLC == yfinance auto_adjust; yfinance kept as fallback) — settle no longer touches the crumb
  host. Verified: 49 tests green (+4 `test_prices.py`); old-vs-new ≤0.015% close diff at identical
  row counts (pitfall: `range=max` silently returns MONTHLY bars — use `period1=0`); settle+dualmom
  clean. `movers._fetch`/insider cap-gate stay on yfinance deliberately (allowlist covers them;
  Fri 7/3 verifies — no speculative rewiring).
- **2026-07-02 (routine-drift fix)** — Found + fixed the [ARC 5 #8] denominator going DARK in cloud:
  the Mon 6/29 + Wed 7/1 cloud `read` runs committed bets but ZERO `movers_ledger` rows, and missed a
  new insider cluster (MOBI, filed 6/29) that a local scan caught — the read-trigger PROMPT predated
  the movers wiring (its step summary omitted `movers scan` / mover decides / `--tag=`) and the runs
  followed the summary, not READ_LOOP.md. Fix: rewrote the trigger prompt (RemoteTrigger update) to
  mandate BOTH denominator scans + clearing both unread queues + tags; backfilled locally (25 movers
  SEEN for the 7/1 session; MOBI SEEN, unread — Fri run triages). VERIFY on the Fri 7/3 run: its
  commit must touch `movers_ledger.csv` and decide MOBI. Lesson: a routine's prompt summary is a
  SECOND COPY of the loop doc — re-sync it whenever the loop changes, or it silently wins.
- **2026-06-28 [ARC5#8]** — `pattern_tag` scenario column + engine per-tag diagnostic (Phase A); `movers.py` daily S&P 500 mover scan = the general candidate DENOMINATOR (Phase B); `universe.sp500()` no-egress cache fallback. Detail: FINDINGS [ARC 5 #8] + git log.
- **2026-06-26 [ARC5#6/#7]** — case-study layer (`cases/`, ILLR+SPCX) + ARCHITECTURE/BACKLOG docs; harnesses loosened (sizing cap dropped, integrity guards kept); forward verdict sharpened to ONE pooled general silo + book↔bets convergence doctrine; cloud-routine audit closed (procedure: `RemoteTrigger list`, read's per-run commit = health signal; no local cron exists). Detail: FINDINGS [ARC 5 #6/#7] + git log.
- Earlier engine/automation history → `FINDINGS.md` Arc 5.

## Watch / open concerns (revisit as data matures — raised 2026-07-06)
- **MOVED OUT 2026-08-02 → the private long-realm repo.** The long-realm personal holdings are
  no longer tracked here: [redacted — long-realm detail]. The previous entries in this slot
  described them correctly but in the wrong repo, and the concentration entry beside them
  described a 17-share lot that never existed. **Do not
  re-open long-term wealth work in this repo** — see the SCOPE section of `CLAUDE.md`.
- ~~**New HTML digest + conditional heartbeat untested end-to-end**~~ **CLOSED 2026-08-02.** Both have
  been running in cloud daily since 2026-07-10; the digest's own DO-NOW output is the standing proof.
  The item's verify instructions still named the **Mon/Wed/Fri** read cadence, retired 2026-07-24 —
  the drift class this file exists to catch, found in this file.
- ~~**NIO: cut-vs-hold unresolved**~~ **RESOLVED 2026-08-02 — HOLD** (see the handoff item 2 above;
  FINDINGS 2026-08-02 book decisions). Not restated here.
- ~~**[redacted — long-realm item]**~~ **RESOLVED + RELOCATED 2026-08-02.** The item now lives
  in the private long-realm repo, not here.
- **"Too conservative?" verdict is weeks out.** Skip-scorer needs N≥30 matured (first 21d ~late-Jul,
  63d ~late-Sep) and may not reach it if read cadence is slow [FINDINGS ARC 5 #9]. Don't expect it soon.

## Backlog (open build work)
- **[AUTOMATION, 2026-08-13] DEFERRED PROGRAM — automate execution (broker-side stop/exit
  enforcement first, eventually the full read→order→book loop).** Owner's ask, staged not built,
  raised after the stops clarification: today every stop/target is a LEDGER rule the digest
  watches daily and the human executes by hand — chosen over resting broker stops on the
  bottom-tick evidence (HELP/XRP cut at the lows; NIO's retired 4.60 stop sat ON the 52wk low)
  and because gap-throughs defeat a stop order exactly where it matters most (the CMPS FDA
  binary → sizing is the real defense there). The enforcement-latency cost of the manual path
  is real and acknowledged: an intraday collapse waits for the next digest plus the human.
  **Trigger: the pooled [Arc 5 #7] verdict lands PASS (or the owner explicitly overrides)** —
  automating execution of a system with no demonstrated edge automates noise; until then
  `orders.py`'s computed limit+band+expiry IS the automation layer (its manual half is by
  construction, and its [ORDERS #1] band diagnostic is still accruing toward N≥20). When it
  fires: pre-register the enforcement design (broker API vs native stop-limit orders, gap
  semantics, kill-switch, and which ledger is authoritative when they disagree) BEFORE anything
  is built — and re-read BOTH cloud prompts the same session (the standing rule; automation
  changes what the routines may do to orders).
- **[OPS, 2026-08-05] Verify + record routine config; port the watchdog off-platform.**
  Owner stance today: repo deprioritized ("disproved until real alpha and real capital") but
  the read+settle loop STAYS ON as the background evidence engine — pushes are log lines, not
  trade prompts, until the pooled verdict shows edge.
  **(1) DONE 2026-08-06 — live config VERIFIED via the triggers API and recorded here:**
  read `trig_01EsetvEZmVLb56fEmc7YvSi` = `30 11 * * 1-5` (Opus 4.8) · settle
  `trig_01Uz2fQRMh5UwjnSvFkaSNBY` = `0 5 * * *` (Sonnet 4.6) · watchdog
  `trig_01Jk65Rg2VQ9WjzjvCdD5SHP` = `13 19 * * *` (Haiku 4.5, read-only) — all three in the
  SAME environment (`env_01Cd6kqjVXv6m1DVCmYm9emL`), all repo-bound. Docs were right, the hq
  board was stale (synced same day). **Prompt edits via `RemoteTrigger update` WORK** (the old
  "unproven" note is settled): both read + settle prompts were REWRITTEN COMPACT 2026-08-06 —
  they now delegate to the repo docs (doc wins) and carry only the non-negotiables + the
  delivery-verdict rule (re-send ONLY on `PUSH REJECTED`; `research.notify` HUMAN-ONLY; never
  probe/test). Smaller prompt = less second-copy drift surface. Watchdog prompt untouched.
  (2) **STILL OPEN: port the watchdog schedule to a GitHub Actions staleness workflow in
  THIS repo** (cron + last-commit age on the WATCHED ledgers, red run = email; Telegram via
  repo secrets optional). Kills an LLM routine AND closes the docstring's admitted limit:
  today the watchdog runs on the SAME scheduling platform it watches, so a dead platform
  kills alarm and pipeline together — Actions is a separate platform. `research/watchdog.py`
  stays runnable; the Action replaces only the scheduled wrapper. Note the Action would ALSO
  inherit the push-transport blind spot's fix: `push_log.csv` (2026-08-06) records delivery
  verdicts in-repo, so an Actions job could alarm on a missing DELIVERED stamp, not just on
  commit staleness.
- **[EDGE-SYSTEM, 2026-08-05] DEFERRED PROGRAM — hunt structural/informational/speed edge
  past LLM-routine reads, possibly per-asset (one volatile name).** Owner's ask, staged not
  built. Absorbs the headerless fragment the 8-K bullet below swallowed ("how top modern
  traders actually make money…"); adjacent to the blind-spot analyzer and the North-star
  vision (next-market choice against VERIFIED numbers). The three families map to anchors
  already paid for: **informational** = [ARC 5 #2b] option (a) feeds (survivorship-clean
  prices + filings-grade) · **structural** = the Arc 2 taxonomy corners (convexity/asymmetry,
  illiquidity & size, forced flows, novel data — "the data moat IS the moat") · **speed** at
  retail = reacting-in-minutes to slowly-digested public info, never latency HFT (that race
  is lost at the starting line and is named here so it cannot be romanticized later). Not
  now: [ARC 5 #2b] is unresolved, and the capital gate is closed — the long-term realm's
  priorities come first; its private repo carries the numbers and the two-gate
  rule. SPCX is never a
  candidate asset — standing conflict-of-interest exclusion since 2026-08-02, owner
  confirmed 2026-08-05. **Trigger (BOTH):** the
  [ARC 5 #2b] decision point resolves (either branch) AND the owner declares the capital
  gate open. When it fires: ONE fresh pre-registration per edge family (hypothesis, bar,
  kill-criterion, deadline arithmetic checked at write time — the SKILL.md rule Arc 3 paid
  for) BEFORE anything is built.
- **[CLOSED 2026-08-05 — trigger fired, built as `--slim`] Collapse unchanged digest sections.**
  The re-measure came in at 56% vs the ≤55% bar (and 87% of the settle message contained in the
  read one), so the deferred build fired. Built as the DETERMINISTIC variant, not the vs-HEAD
  diff this item originally sketched: the read push (`digest --slim`) drops what its run cannot
  change — book position rows, the whole ORDERS block, the 📋 banner — because for THAT run they
  are unchanged by construction. The original objection (marks move, so diffed "unchanged" is
  usually false) still stands and is why the diff variant stays dead; a vs-HEAD diff would also
  have hidden a freshly opened position forever once committed. Detail: *Recent changes*
  2026-08-05.
- **[SMALL, 2026-08-04] Three cleanups the red-team named and I did not take**, listed so they are
  not rediscovered as bugs: (a) `digest._orders_section` hardcodes `config.ORDER_EXPIRY_D + 5` for
  its bars fetch, duplicating the same slack inside `orders.check` — wants one shared helper;
  (b) `orders.sessions_left(row, bars)` ignores `row` entirely; (c) `research/orders.csv`'s header
  lags `orders.FIELDS` by the new `pulled_at` column until something next writes the file (runtime
  safe — `_load` backfills and `DictWriter` defaults it — so this self-heals on the next
  `orders check`). Same class, same self-heal [2026-08-04]: `movers_ledger.csv`'s header lags
  `movers.FIELDS` by `universe` until the next `decide`/`settle` write (backfill regression-tested).
  None affects a number; all are papercuts for the next reader.
- **[KNOWN LIMIT, not a bug] The SINCE-LAST band anchors on the last COMMIT, not the last MESSAGE.**
  They coincide because both routines commit within minutes of pushing. A stranded push makes the
  next band REPEAT a delta rather than skip one (benign, and that same message already shouts
  `STRANDED`). `digest._row_id` is likewise blind to row DELETIONS by construction: it asks what a
  row became, not whether one vanished — a truncated append-only ledger is `_git_section`'s problem.
- ~~**[OPEN, cheap] A feed's newest bar date is a structured fact with no column.**~~ **DONE
  2026-08-04** — the trigger ("the next time a stale feed costs a run") had ALREADY fired when
  this was written: the 08-04 read lost the 08-03 session's cohort to it. `last_bar` +
  `n_ok`/`n_total` now live in `_feed_status.json` and the digest escalates a stale bar or thin
  coverage even when `last_ok` is fresh. FINDINGS 2026-08-04 [ops].
- ~~**[BUG, HIGH] Alert-push and ledger-commit are NOT atomic**~~ **FIXED 2026-07-27.**
  The check now lives in `digest._git_section` (uncommitted/unpushed ledgers become a
  DO-NOW in the same message as the alert) rather than in a READ_LOOP instruction that
  could be — and was — skipped. INTC was re-registered by hand [FINDINGS 2026-07-27].
- ~~**Real-money allocation policy**~~ **DECIDED 2026-07-10 (user call):** ALL free cash goes to the
  read-run suggestion sleeve (READ_LOOP step 5), not a passive core — the whole-pool stop (`book.POOL_STOP`) + the
  integrity guards (pre-registration, log-every-candidate, N) are the backstops [FINDINGS 2026-07-10].
  The passive-core-vs-sleeve split was the recommended shape; the user chose max-learning/max-exposure
  knowingly. Revisit WITH evidence when the pooled verdict lands (either direction).
- **Risk / concentration VISIBILITY (measure, don't hard-cap — respect [ARC5#6]).** Surface per-position
  weight, concentration, and correlation clustering in the digest / `book mark`, so
  real-money exposure is legible. The sizing cap stays lifted (that experiment is live); this just makes
  the risk we're carrying a CHOICE, not an accident.
- **Cost / slippage awareness for real money.** ~~Model the frictions swing capital actually pays —
  slippage~~ **ENTRY slippage DONE 2026-08-03** (measured: 1.07%/2.42% by open/close on the median
  taken mover; mitigated by `orders.py`'s limit band — FINDINGS same date). **Still open:** exit-side
  slippage and short-term cap-gains treatment on positions we CHOSE. Build when we're actually acting
  on winners, not before. (Long-realm plan-milestone items moved to the private long-realm repo
  2026-08-02 — that is the long-term realm.)
- ~~**`movers.scan` has no partial-bar guard.**~~ **DONE 2026-08-04** — its trigger ("before
  anyone runs scan by hand") fired during this session's verification planning. `scan` now
  filters to completed sessions via `orders._complete` (one shared definition of "completed",
  injectable `today`), regression-tested for the exact old failure: a mid-session scan defers
  to yesterday's close AND the real close can still be recorded the next day (the old dedup
  blocked it forever). FINDINGS 2026-08-04 [ops].

### Open questions the ORDERS layer raised (2026-08-03) — each needs data, not a decision now

- **[ORDERS #1 is LIVE and unanswered] Is the entry band too tight?** Pre-registered in FINDINGS
  2026-08-03: at **N≥20 resolved orders**, if EXPIRED orders' median 21d excess beats FILLED
  orders' by **>+3pp**, the band is too tight → widen WITH evidence; else vindicated. It accrues on
  its own from the scheduled runs — no build. **Do not touch `config.ENTRY_BAND_MAX` or
  `ORDER_EXPIRY_D` before that N**, and never because one name got away; that is the goalpost-move
  the pre-registration exists to prevent. Read it with `python3 -m research.orders show`.
- **The adverse-selection worry underneath it, stated plainly.** The band systematically refuses
  the names running hardest: at 1.5% it would have passed on SMCI (+19.8% day 1), DLR (+11.0%) and
  WAB (+10.0%) — the three biggest day-1 movers in the sample. Only 2 takes in the whole ledger
  have 21d forward data, so **we genuinely do not know yet whether refusing them was right.** If
  [ORDERS #1] resolves "too tight", this is the mechanism to name in the write-up.
- **The band + expiry rest on N=40, ONE month, ONE earnings season.** The FLAT fill rate across
  1.0–2.0% is the robust part; the +0.4pp entry advantage that picked 1.0% over 1.5% is NOT robust
  at that N, and the choice between them is close to arbitrary on this evidence. Re-run
  `python3 -m research.tools.slippage_audit` once the ledger has spanned a quieter tape — a band
  calibrated only on earnings season may be too tight for the rest of the year.
- **A limit that never fills is a trade not taken.** ~10% of takes go unexecuted by construction.
  Accepted deliberately under the honest prior (LOW edge, 0/22 probes beat SPY risk-adjusted), but
  it is a real cost and it should be named whenever conversion is discussed — not quietly folded
  into "discipline".
- **Nothing models a SHORT's collateral.** `orders place` sizes from free cash and therefore
  refuses to auto-size a short (it demands `--shares=N`). Fine while the book is long-only plus a
  beta anchor; revisit if shorts become real positions rather than paper bets.
- **Exit-side execution is still unmeasured.** `SKILL.md` has the "exit into strength, never
  market-dump" rule from the HELP/XRP capitulation, and now an entry-side limit rule — but only the
  ENTRY side has a number behind it. The same audit on exits (do our limit exits beat a market
  exit?) needs realized exits to score, and the book has 4. **Trigger: ~10 realized exits.**
- **`orders.csv` has no idempotency guard against a double `place` from two sessions.** `place`
  refuses a duplicate *pending* order for the same ticker, which covers the realistic case, but a
  cloud run and a laptop run racing on the same minute are not serialized. Low priority — the read
  routine's ORIENT step already refuses to double-run a day — but it is the same class as the
  2026-07-24 double-scan that corrupted the denominator.
- **THE EXECUTION LAYER — what a "full system" still lacks (opened 2026-08-03, user's framing).**
  `orders.py` closed the first real gap between a read and money: entries are now a limit with an
  expiry, resolved and scored. The layer is deliberately THIN and the remaining pieces are listed
  so the gap is visible, **not so they get built now** — each is gated on a felt need, and the
  honest prior (LOW edge) says an elaborate execution layer on top of an unproven read is the exact
  over-engineering `CLAUDE.md` forbids. In rough dependency order:
  1. **Exit orders.** Entries are modelled; exits are still a manual stop number on a book row that
     nothing enforces (`book.py:188-190` says so outright). The symmetric build is a working SELL
     order with the same limit/expiry treatment. **Gate: ~10 realized exits, so the exit-side audit
     above has something to score.**
  2. **Broker reconciliation.** `placed_at` is a human assertion, and `book open` records a fill the
     human types. Nothing ever reads the actual account. A read-only positions/fills pull would
     make the whole ledger self-checking rather than self-reported. **Gate: a real reconciliation
     error that costs something — `SKILL.md` already carries "reconcile before reasoning" from the
     phantom-SPCX session, which is the warning shot.**
  3. ~~**Position sizing with a risk unit.**~~ **DONE 2026-08-04 [ORDERS #2], on the user's
     explicit call.** `orders place` auto-sizing is now min(cash cap, risk cap) — the stop
     being hit costs ~`config.RISK_PCT` of book equity. Shorts still need `--shares`.
     FINDINGS 2026-08-04 [ORDERS #2].
  4. **Then, and only then, the multi-market question below.** An execution layer that only speaks
     equities is fine until the next-market choice is actually live.
- **North-star vision (decided w/ user 2026-07-02, from `raw_input/trading_landscape_summary.md`,
  local-only)** — what we're building: a trading system that spans as MANY MARKETS as possible
  (equities today; futures / options / crypto / FX as expansion candidates), learning per scenario
  and compounding capital. The doc's rough numbers (success rates by market type, capital floors,
  "30–50%/yr = exceptional") are UNVERIFIED estimates → treat each as a hypothesis: verify before it
  gates a decision. Concrete hook: when the equity read-verdict lands (pass OR fail), the
  next-market choice gets made against VERIFIED versions of those numbers — which market types leave
  structural room for a small operator (the Arc 2 question, asked across asset classes).
- **Telegram notify v1.2 (v1.1 SHIPPED 2026-07-10** — HTML digest, per-position book, suggestion
  block, fallback-only heartbeat; see Recent changes**)**. v1.2 candidates, build only on a felt
  need: book equity swing past ±5% since last notify; dated decision triggers firing (e.g. a
  delivery print); folding the 🚨 settle pushes into the digest (needs `settled_at` in bets/insider
  ledgers — rejected 2026-07-10 as plumbing-for-a-message).
- **[NAMED TRIGGER, 2026-08-04] The 8-K ORPHAN arc — the last untried Arc-3-catalogue
  candidate** ("buried 8-K catalysts in no-coverage names", free EDGAR data, "fastest N"). It is
  the reading-BEFORE-the-move version of what the tail cohort only sees AFTER the move. Do NOT
  build it yet — the tail arm gets first claim on the read runs' attention. **Trigger (either):
  (a) the [ARC 5 #2b] checkpoint lands on the FAIL branch while tail reads look qualitatively
  starved of mechanism, or (b) the tail cohort runs ~2 clean weeks and its takes keep finding
  "the filing was out before the move".** When it fires: a FRESH pre-registration (hypothesis,
  bar, kill-criterion with the deadline arithmetic checked at write time — the SKILL.md rule
  Arc 3 paid for). `insider_sec.py` in git history has the EDGAR daily-index reader bones.
  *(A headerless fragment swallowed here — "cutting-edge research into how top modern traders
  actually make money" — absorbed by [EDGE-SYSTEM, 2026-08-05] at the top of this section.)*
- **Managed OTM put-write (the gentler vol-risk-premium)** — the harsh variance-swap proxy FAILED
  (`volrp`, Sharpe 0.58 < SPY, skew −8.75), but a managed OTM put-write (CBOE PUT/PUTW) historically
  fares better. Deferred: needs options/index data to test cleanly, and it shares the negative-skew
  DNA. **Trigger:** only if we pull paid options data AND want to revisit (low priority).
  *(Migrated from the orphan root `BACKLOG.md` 2026-08-02 before deleting it.)*
- **Visual dashboard** — an HTML view of the scoreboard + catalogue + finances. Deferred: `python3 -m
  research` covers it. **Trigger:** the user asks for a visual. *(Migrated from root `BACKLOG.md`.)*
- **Blind-spot analyzer** (future tool) — a periodic review pass over project / portfolio /
  standings / assumptions that surfaces blind spots and proposes changes / bets / case studies /
  unused trading techniques. Build only on a validated need; if it ever generates bets it MUST
  keep the integrity guards (pre-registration + log-every-candidate + multiple-testing).
- Forward-bet verdict accrues toward N≥30 / 2027-06-30 — no build; let `read`/`settle` run.
- If a clean "real-vehicle-vs-meme" pair recurs, add the case (don't force it).
- Resist building ahead of a validated need (CLAUDE.md anti-over-engineering).

## Stale / dormant (do NOT run as live; kept for reproducibility)
- ~~v1 capture→settle→paper pipeline~~ **DELETED 2026-08-02** (`capture` `news` `db` `backtest`
  `paper` + 4 test files, `reference/`, `paper_book.csv`, `cron.log`, `db/research.db`). Nothing
  imported them; no `Reproduce:` line cited them. **The near-miss worth remembering:** this list
  ALSO named `momentum` and `universe`, which are **LIVE** — `movers.py` imports both on every
  scan — and `outcome`, which `dip_index` (archive-cited) imports. Deleting on the strength of a
  stale map would have broken the daily denominator. **Verify imports, not maps.**
- Arc-1/2 probe modules (cited by FINDINGS `Reproduce:` lines only): `dip_index` `robust`
  `decorrelate` `sleeves` `crypto_trend` `vix_gate` `vix_fear` `fng_crypto` `regime`
  `portfolio` `disaster` `disaster_port` `index_deletion` `lockup` `factors` `seasonality`
  `carry` `volrp` `voltarget` `contagion`.
- ~~`insider_sec.py`~~ — DELETED 2026-08-02 with the rest of Arc 3. It was kept solely because
  "the [ARC 3 #1d] audit may reset and rebuild the silo"; the audit ran, the arc closed, and that
  reason is void. Git history has it if a rebuilt insider arc ever wants a SEC daily-index reader.
- ~~`reference/`~~ + the v1 capture→settle→paper pipeline — **DELETED 2026-08-02.** Nothing
  imported them and no `Reproduce:` line cited them. Git history has them.
