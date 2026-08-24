# LOOP — the autonomous research heartbeat

Run one research iteration unattended. The brain is **Claude** (paid for via Max) — the
maker that generates ideas and the checker that red-teams them. No human data-feeding
required; the loop decides what to test next from what it has already learned.

## Run it continuously (no constant input)
    /loop run one iteration of research/LOOP.md       # Claude self-paces; stop anytime
Or schedule it: a cron / routine that runs `claude -p "run one iteration of
research/LOOP.md"`. Start by running it WITH you watching a few times; automate once you
trust it. The stop conditions are numbers, never "the agent says it's done."

## One iteration  (maker → checker → log)
1. **ORIENT** — read `research/SKILL.md` (rules + dead-ends) and the `PROBES` list in
   `research/engine.py` (what's been tried). NEVER re-test a dead end.
2. **GENERATE (maker)** — propose ONE new falsifiable hypothesis with a numeric pass/fail
   BAR. Pick the track that fits the idea (run BOTH tracks over time, alternate):
   - **MECHANICAL** (a fixed rule, pure math): backtest on HISTORY — answer is instant.
     Claude knowing past outcomes does NOT contaminate a mechanical rule; just don't
     hindsight-pick the period (test across ALL history). **There is no known untested family
     left** — vol-premium, carry, factors and seasonality are all CLOSED (see `PROBES` in
     `research/engine.py`; Arc 4 #4–6). This line listed them as "still untested" for weeks
     while rule 1 above said NEVER re-test a dead end. Check `PROBES` before proposing, always.
   - **FORWARD** (Claude's judgment/reading): CANNOT be backtested — Claude already knows
     how the past turned out, so the only clean test is the FUTURE. Log it as a bet in the
     catalogue: `python3 -m research.bets add TICKER long HORIZON_d BENCH "thesis" --tag=<scenario> --conviction=<high|medium>`
     (LONG only + liquidity floor, code-enforced [ARC 5 #12a] — shorts need the re-arm protocol).
3. **PRE-REGISTER** — write hypothesis + bar to `FINDINGS.md`, knobs fixed. Commit (the
   timestamp is the anchor: no moving goalposts).
4. **TEST** — write the smallest probe (`research/<name>.py`), run it, get the number.
   Out-of-sample, realistic costs, few parameters, de-overlapped, survivorship-aware.
5. **JUDGE (checker)** — adversarially: did it clear the bar? Red-team it. A marginal pass
   after many tests is NOISE until confirmed on fresh OOS data. Different lens than the maker.
6. **LOG** — append the verdict to `FINDINGS.md` and one row to `engine.PROBES`. If a loss
   taught a rule, add it to `SKILL.md` (this is how the system gets smarter). Commit.

## What to expect (honest)
Most iterations end in **FAIL** — that is the system working, killing bad ideas cheaply.
It compounds knowledge because `SKILL.md` and `PROBES` grow, so it stops repeating itself
and narrows toward the few live levers: **risk-shaping** (sizing/trend), untested mechanical
**risk premia**, and **Claude's forward reading** (the bet catalogue). It will not "print
alpha while you sleep." It will tell you, cheaply and continuously, what works and what
doesn't — and surface the rare lead (e.g. Arc 4 #2 vol-targeting) for a real confirmation
pass. Two tracks always run: instant mechanical backtests + the slow forward bet catalogue.
The honesty is the product.
