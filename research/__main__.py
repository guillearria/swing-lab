"""swing_lab — research control panel.

  python3 -m research          live status: scoreboard + forward bets + signal
  python3 -m research help     the command index

Full index in README.md · audit trail in FINDINGS.md · method in SKILL.md ·
autonomous loop in LOOP.md.
"""
import sys

LIVE_COMMANDS = """\
LIVE commands:
  python3 -m research                   this status panel
  python3 -m research.engine            falsification scoreboard (all probes + verdicts)
  python3 -m research.bets show         forward-bet catalogue
  python3 -m research.bets add ...      log a pre-registered forward bet
  python3 -m research.bets settle       score matured bets vs benchmark
  python3 -m research.dualmom current   dual-momentum core: what to hold now
  python3 -m research.movers            daily mover scan, 2 cohorts: S&P 500 + 400/600 tail [ARC 5 #11] = general candidate DENOMINATOR (show/scan/decide/settle)
  python3 -m research.book              TERMINAL evidence ledger [ARC 5 #12] — prints the one BOOK CLOSED line
  python3 -m research.orders            COUNTERFACTUAL orders [ARC 5 #12a]: a LIMIT + an expiry, band diagnostic (place/check/cancel/show)
  python3 -m research.digest            THE Telegram push (v3.1): scoreboard + ⚠️ DO-NOW (when nonempty) + 🟢 cards + 📈
  python3 -m research.site              regenerate docs/index.html — the public dashboard page [P7a]
  python3 -m research.pulse             X pulse dry-run print (--post = the routine's autopost path [P7b])
  python3 -m research.watchdog          external dead-man's switch (own cloud routine; --notify)
  python3 -m research.heartbeat         🚨/✅ fallback, fires only when a daily step failed
  python3 -m research.notify "text"     Telegram transport (no args = config status only)
  /loop run one iteration of research/READ_LOOP.md   GENERATE a batch of forward bets (frontier)
  /loop run one iteration of research/LOOP.md    run the autonomous research loop

`scan`/`settle`/`decide` WRITE ledgers; bare invocation is always the read-only `show`.
Cloud routines (/schedule): read (generate, pre-market weekdays) · settle (score, daily) · watchdog (daily)
Docs: README.md (index) · ARCHITECTURE.md (layer map) · FINDINGS.md (audit) · SKILL.md (method) · LOOP/READ_LOOP.md
(The snapshot/settle/paper/backtest v1 pipeline is dormant — see README.)"""


def _list_cases() -> None:
    """The reasoning layer: list research/cases/*.md (each links to its scored bet)."""
    import glob
    import os
    files = sorted(f for f in glob.glob("research/cases/*.md")
                   if not os.path.basename(f).startswith("_"))
    if not files:
        return
    print("\nCASE STUDIES (research/cases/) — why a move happened → a reusable pattern:")
    for f in files:
        with open(f) as fh:
            head = fh.readline().lstrip("# ").removeprefix("Case study: ").strip()
        print(f"  {os.path.basename(f)[:-3]:<6} {head[:70]}")


def status() -> None:
    from research import engine, bets, dualmom, book, movers
    engine.main()
    bets.show(bets._load())
    movers.summary(movers._load())
    try:
        book.mark(book._load())
    except Exception as e:
        print(f"\n(live book mark unavailable — network? {e})")
    try:
        dualmom.current()
    except Exception as e:
        print(f"\n(dual-momentum signal unavailable — network? {e})")
    _list_cases()
    print("\n" + LIVE_COMMANDS)


def main(argv: list[str] | None = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else "status"
    if cmd == "status":
        status()
    elif cmd in ("help", "-h", "--help"):
        print(__doc__)
        print(LIVE_COMMANDS)
    else:
        print(f"'{cmd}' is not a live command (the old v1 pipeline is dormant).\n")
        print(LIVE_COMMANDS)


if __name__ == "__main__":
    main()
