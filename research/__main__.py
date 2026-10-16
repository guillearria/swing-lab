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
  python3 -m research.bets add ...      RETIRED [ARC 5 #19] — Arc 5 generation is closed
  python3 -m research.bets settle       score matured bets vs benchmark
  python3 -m research.dualmom current   dual-momentum core: what to hold now
  python3 -m research.movers            mover ledger [ARC 5 #11]: show/settle (scan/decide RETIRED [ARC 5 #19])
  python3 -m research.paths             settled-bet path diagnostic (peak vs final + noise ref) — DESCRIPTIVE [PATHS #1], read-only
  python3 -m research.book              TERMINAL evidence ledger [ARC 5 #12] — prints the one BOOK CLOSED line
  python3 -m research.orders            COUNTERFACTUAL orders [ARC 5 #12a]: check/show (place RETIRED; [ORDERS #1] closed)
  python3 -m research.digest            THE Telegram push (v4): what the run DID + 📊/🟢 cards + ⚠️ (when nonempty) + 📈
  python3 -m research.site              regenerate docs/index.html — the public dashboard page [P7a]
  python3 -m research.pulse             X pulse dry-run print (--post = the routine's autopost path [P7b])
  python3 -m research.watchdog          external dead-man's switch (GitHub Action; --notify; --issues = 📬 watch)
  python3 -m research.heartbeat         🚨 fallback (failure only); bare = DRY RUN, ✅ needs --notify
  python3 -m research.notify "text"     Telegram transport (no args = config status only)
  /loop run one iteration of research/LOOP.md    run the autonomous research loop

`scan`/`settle`/`decide` WRITE ledgers; bare invocation is always the read-only `show`.
Automation: settle (cloud routine, daily) · watchdog (GitHub Action, twice daily) · read DISABLED [ARC 5 #19]
Docs: README.md (index) · ARCHITECTURE.md (layer map) · FINDINGS.md (audit) · SKILL.md (method) · LOOP.md
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
