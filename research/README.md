# research/

The live research code. **For the command index and live status, see the top-level
[`README.md`](../README.md)** — or just run:

```bash
python3 -m research          # live status: scoreboard + forward bets + signal
python3 -m research help     # command index
```

- **Audit trail:** [`FINDINGS.md`](FINDINGS.md) — every test, its number, its verdict.
- **Method / rules:** [`SKILL.md`](SKILL.md) — how a probe is run + lessons from losses.
- **Autonomous loop:** [`LOOP.md`](LOOP.md).

Live modules: `engine.py`, `bets.py`, `movers.py`, `paths.py`, `book.py`, `dualmom.py`, `digest.py`,
`notify.py`, `heartbeat.py`, `watchdog.py`, `feedstatus.py`
(shared: `config.py`, `prices.py`, `universe.py`, `momentum.py`).
DORMANT — do not run as live: `voltarget.py`, `volrp.py`, `outcome.py`, and the Arc-1/2 probes.
These stay on disk because `FINDINGS_ARCHIVE.md` cites them in `Reproduce:` lines — see the
top-level README's "Evidence" section.
**DELETED 2026-08-02:** the insider modules (Arc 3 closed on its own deadline branch) and the v1
capture→settle→paper pipeline (`capture`/`news`/`db`/`backtest`/`paper`, `reference/`). Evidence
lives in `FINDINGS.md`; the code lives in git history.
