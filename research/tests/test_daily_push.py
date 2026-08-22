"""Guard scripts/push_ledgers.sh — the leg that lost a whole settle run on 2026-07-31.

The commit/push logic used to live inline in scripts/daily.sh, where it was never tested, and
it failed in the one way that cost real evidence: it pushed, the push failed, the ephemeral
cloud checkout was destroyed, and the commit (six Telegram delivery stamps + a day of the
equity curve + 25 scored movers rows) went with it. These tests run the real script against a
real bare remote, because the failure modes ARE git's behaviour — a mock would have agreed
with the broken version.
"""
import subprocess

import pytest

SCRIPT = "scripts/push_ledgers.sh"
LEDGER = "research/bets_catalogue.csv"          # a real path from $LEDGERS


def _git(cwd, *args, check=True):
    return subprocess.run(("git",) + args, cwd=cwd, capture_output=True, text=True,
                          check=check, timeout=30).stdout.strip()


def _push(clone, *ledgers):
    """Run the script under test; returns (exit_code, stdout).

    stdout is asserted WHOLE, not last-line: daily.sh does `FAILS="$FAILS $OUT"` and passes
    $FAILS to heartbeat.py as argv, so any git chatter leaking onto stdout would become fake
    step names inside a 🚨 alert. The script must say exactly one word, or nothing.
    """
    r = subprocess.run(["bash", str(clone / SCRIPT), *(ledgers or (LEDGER,))],
                       cwd=clone, capture_output=True, text=True, timeout=90)
    return r.returncode, r.stdout.strip()


@pytest.fixture
def repo(tmp_path, request):
    """A bare origin + a clone carrying the real script and one committed ledger."""
    origin, clone = tmp_path / "origin.git", tmp_path / "clone"
    subprocess.run(["git", "init", "--bare", "-b", "master", str(origin)],
                   check=True, capture_output=True)
    subprocess.run(["git", "clone", str(origin), str(clone)], check=True, capture_output=True)
    _git(clone, "config", "user.email", "t@t"), _git(clone, "config", "user.name", "t")

    src = request.config.rootpath / SCRIPT
    (clone / "scripts").mkdir()
    (clone / "scripts" / "push_ledgers.sh").write_text(src.read_text())
    (clone / "research").mkdir()
    (clone / LEDGER).write_text("ticker,status\nAAA,open\n")
    _git(clone, "add", "-A")
    _git(clone, "commit", "-m", "base")
    _git(clone, "push", "origin", "HEAD:master")
    _git(clone, "branch", "--set-upstream-to=origin/master", "master")
    return origin, clone


def test_push_lands_on_master(repo):
    origin, clone = repo
    (clone / LEDGER).write_text("ticker,status\nAAA,closed\n")
    code, out = _push(clone)
    assert (code, out) == (0, "")
    _git(clone, "fetch", "origin")
    _git(clone, "merge-base", "--is-ancestor", "HEAD", "origin/master")   # raises if not
    assert "settle-backup" not in _git(origin, "branch", "--list")


def test_no_commit_when_ledgers_unchanged(repo):
    """A quiet day must not manufacture an empty commit — guards the --cached change."""
    _, clone = repo
    before = _git(clone, "rev-parse", "HEAD")
    assert _push(clone) == (0, "")
    assert _git(clone, "rev-parse", "HEAD") == before


def test_new_untracked_ledger_file_is_committed(repo):
    """`git diff --quiet` only sees TRACKED files, so a first-of-its-kind ledger looked like
    'nothing to do' and was never committed at all. Staging first is what fixes it."""
    _, clone = repo
    (clone / "research" / "data").mkdir(parents=True)
    (clone / "research/data/_feed_status.json").write_text("{}")
    code, out = _push(clone, LEDGER, "research/data/_feed_status.json")
    assert (code, out) == (0, "")
    _git(clone, "fetch", "origin")
    assert "_feed_status.json" in _git(clone, "ls-tree", "-r", "--name-only", "origin/master")


def test_push_race_recovers_on_retry(repo):
    """master moves under us (the read routine commits on its own schedule). A non-fast-forward
    is a race, not a conflict — one fetch+rebase clears it and no human should be involved."""
    origin, clone = repo
    other = clone.parent / "other"
    subprocess.run(["git", "clone", str(origin), str(other)], check=True, capture_output=True)
    _git(other, "config", "user.email", "o@o"), _git(other, "config", "user.name", "o")
    (other / "unrelated.txt").write_text("moved master under us\n")
    _git(other, "add", "-A"), _git(other, "commit", "-m", "race")
    _git(other, "push", "origin", "HEAD:master")

    (clone / LEDGER).write_text("ticker,status\nAAA,closed\n")
    assert _push(clone) == (0, "")
    _git(clone, "fetch", "origin")
    _git(clone, "merge-base", "--is-ancestor", "HEAD", "origin/master")
    assert "settle-backup" not in _git(origin, "branch", "--list")


def test_rebase_conflict_strands_to_backup_ref_with_the_rows_intact(repo):
    """THE 2026-07-31 CASE. An unattended auto-merge of an append-only evidence file is worse
    than a stranded commit, so the script must refuse to merge — but the work has to survive
    the container, and it must still contain the rows."""
    origin, clone = repo
    other = clone.parent / "other"
    subprocess.run(["git", "clone", str(origin), str(other)], check=True, capture_output=True)
    _git(other, "config", "user.email", "o@o"), _git(other, "config", "user.name", "o")
    (other / LEDGER).write_text("ticker,status\nAAA,stopped\n")     # same line, different value
    _git(other, "add", "-A"), _git(other, "commit", "-m", "conflicting edit")
    _git(other, "push", "origin", "HEAD:master")

    (clone / LEDGER).write_text("ticker,status\nAAA,closed\n")
    code, out = _push(clone)
    assert (code, out) == (1, "push-stranded")
    refs = _git(origin, "branch", "--list", "settle-backup/*")
    assert refs, "the commit must survive the container on a backup ref"
    ref = refs.split()[-1]
    assert "AAA,closed" in _git(origin, "show", f"{ref}:{LEDGER}")   # the ROWS, not just a ref
    assert _git(clone, "status", "--porcelain") == ""                # no rebase left in progress


def test_unreachable_remote_reports_push_lost(repo):
    """If even the backup push fails the work exists ONLY here — that must be reported as a
    distinct, louder word than a recoverable strand, and the script must not hang."""
    origin, clone = repo
    (clone / LEDGER).write_text("ticker,status\nAAA,closed\n")
    _git(clone, "remote", "set-url", "origin", str(origin.parent / "gone.git"))
    assert _push(clone) == (1, "push-LOST")


def test_missing_ledger_path_says_add_instead_of_reporting_success(repo):
    """A LEDGERS path that does not exist must ABORT the run, not silently discard it.

    `git add -A -- <paths>` exits 128 when any pathspec matches nothing. Unchecked, control fell
    straight through to `git diff --cached --quiet` — which also matched nothing, reported "no
    changes", and `exit 0`. So a run whose real ledger changes were never staged ended as a
    CLEAN settle: no commit, no backup ref, no 🚨, and daily.sh went on to push a digest whose
    numbers were not in git. That is the 2026-07-31 failure shape (work destroyed with the
    container) reached through the one unguarded step left in the script written to prevent it.
    """
    _, clone = repo
    (clone / LEDGER).write_text("ticker,status\nAAA,closed\n")     # a REAL, changed ledger
    before = _git(clone, "rev-parse", "HEAD")
    code, out = _push(clone, LEDGER, "research/does_not_exist.csv")
    assert (code, out) == (1, "add")                    # one word, for $FAILS -> 🚨
    assert _git(clone, "rev-parse", "HEAD") == before   # nothing was committed
