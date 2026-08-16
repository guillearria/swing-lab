"""P7b — the SOCIAL PULSE: a deterministic, ledger-rendered post to X, autoposted by policy.

THE AUTOPOST POLICY [BACKLOG P7b, decided 2026-08-15 — owner-reviewed]: a post rendered by
CODE from committed ledgers publishes UNCONDITIONALLY. A human approve per post would
reintroduce selection bias at the publication layer — "posts only when approved" is the
survivorship theater the public ledger exists to refute; mechanical publication IS the
credibility asset. The other half of the same policy: LLM-authored public prose (case
threads, commentary) keeps a redlist + human gate — this module can never carry it, because
compose() renders ONLY verdict-grade, test-covered numbers (bets.stats / cum_excess /
wilcoxon_p and the newly-scored rows' own excess). NEVER raw scan output — the MNST −50.6%
artifact class must have no path to a public post, so nothing from movers ever renders here.

WHEN IT FIRES (deterministic gate, no discretion): only when the settle run changed the
VERDICT surface vs git HEAD — a newly-scored verdict row (closed LONG; a settling short is
diagnostic and never posts) — with 🏁 milestone crossings (n=10/20/30) taking the headline.
Runs in daily.sh AFTER the ledgers settle and BEFORE push_ledgers commits (REORDER daily.sh
AND THE GATE GOES SILENT — same HEAD-diff contract as the digest's milestone check).

TRANSPORT DISCIPLINE (inherited from the digest's paid lessons): ONE post per trigger with a
tri-state delivery verdict — POSTED (X confirmed, id stamped) · REJECTED (definitive, nothing
published) · UNCONFIRMED (ambiguous — NEVER re-post: the 2026-07-24 double-post class).
Every attempt stamps research/data/pulse_log.csv (committed with the ledgers). Metered fuel:
a hard code cap of ≤1 POSTED per UTC day (structural cadence is already ≤1/day via settle;
X free tier is 500 writes/month — ~16× margin). Standing "Not investment advice." on every
post. Fail-soft when unconfigured: without the X_* env vars the step is a quiet no-op, so
the code can land before the owner creates the X app.

ACTIVATION (owner steps, one-time): create an X account + developer app with Read AND Write
permission, then set X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET in local .env
AND in the settle trigger's cloud environment. Optional PULSE_URL appends the dashboard link
once the page is hosted (the P7a publish gate).

  python3 -m research.pulse           # compose + print what WOULD post (writes nothing)
  python3 -m research.pulse --post    # the routine path: gate → cap → post → stamp
"""
import base64
import csv
import hashlib
import hmac
import json
import logging
import os
import secrets
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import quote

from research import config  # noqa: F401  — loads .env (same seam as notify)

log = logging.getLogger(__name__)
PULSE_LOG = "research/data/pulse_log.csv"
X_API = "https://api.x.com/2/tweets"   # canonical post-rebrand host (api.twitter.com = alias);
                                       # the OAuth signature BINDS this URL — change both together
TIMEOUT_S = 15
MAX_X = 270                            # X hard cap 280 weighted chars; margin for the URL slot
ENV_KEYS = ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET")


def configured() -> bool:
    return all(os.getenv(k) for k in ENV_KEYS)


def _x_len(text: str) -> int:
    """X's weighted length, approximated CONSERVATIVELY: anything past Latin-1 counts 2
    (X counts most Latin as 1, CJK/emoji as 2) — overcounting can only keep us shorter."""
    return sum(2 if ord(c) > 0xFF else 1 for c in text)


# ---------- compose (pure — the only content that can ever reach the public) ----------

def _tally(rows: list[dict]) -> str:
    """The pool line, verdict-grade numbers only — same sources as the digest scoreboard."""
    from research import bets
    s = bets.stats(rows)
    if not s:
        return f"Pool: 0/{bets.BAR_N} settled longs."
    n, _, md, beat = s
    sig = bets.cum_excess(rows)
    line = f"Pool: {n}/{bets.BAR_N} settled longs, median {md:+.2f}%, beat {beat:.0f}%"
    if sig is not None:
        line += f", cum {sig:+.1f}pp"
    if n >= bets.BAR_N:
        p = bets.wilcoxon_p(bets.excess_values(bets.verdict_rows(rows)))
        ok = (md > bets.BAR_MEDIAN and beat > bets.BAR_BEAT
              and p is not None and p < bets.WILCOXON_ALPHA)
        line += f". AT BAR: {'PASS' if ok else 'FAIL'} per the pre-registered thresholds"
    return line + "."


def compose(rows: list[dict], head_rows: list[dict]) -> str | None:
    """The pulse text, or None when nothing verdict-grade changed vs HEAD. PURE (testable).

    Newly-scored = closed LONG now that was absent-or-open at HEAD (the digest's row-identity
    lesson [2026-08-04] reused verbatim via digest._row_id — batch timestamps collide).
    """
    from research import bets, digest
    was = digest._by_id(head_rows)
    scored = []
    for r in bets.verdict_rows(rows):
        if r["status"] != "closed" or not r["excess_pct"]:
            continue
        old = was.get(digest._row_id(r))
        if old is None or old["status"] != "closed":
            scored.append(r)
    if not scored:
        return None
    n_now = len(bets.excess_values(bets.verdict_rows(rows)))
    n_prev = len(bets.excess_values(bets.verdict_rows(head_rows)))
    crossed = [m for m in (10, 20, 30) if n_prev < m <= n_now]
    if crossed:
        head = f"Milestone: {crossed[-1]} settled longs on the paper ledger."
    elif len(scored) == 1:
        r = scored[0]
        head = (f"Paper ledger settle: {r['ticker']} {float(r['excess_pct']):+.2f}% vs "
                f"{r['benchmark']} ({r['horizon_d']}d).")
    else:
        names = ", ".join(f"{r['ticker']} {float(r['excess_pct']):+.2f}%" for r in scored)
        head = f"Paper ledger settle: {len(scored)} bets scored ({names})."
    bar = (f"Bar, fixed in advance: n>={bets.BAR_N}, median>+{bets.BAR_MEDIAN:.0f}%, "
           f"beat>{bets.BAR_BEAT:.0f}% — publishes pass OR fail.")
    tail = "Not investment advice."
    url = os.getenv("PULSE_URL", "").strip()
    def build(h: str) -> str:
        parts = [h, _tally(rows), bar, tail]
        if url:
            parts.append(url)
        return "\n".join(parts)
    text = build(head)
    if _x_len(text) > MAX_X and not crossed:   # graceful degrade: count-only headline
        text = build(f"Paper ledger settle: {len(scored)} bets scored.")
    if _x_len(text) > MAX_X:                   # still long (odd env) → drop the bar line last
        text = "\n".join([head if crossed else f"Paper ledger settle: {len(scored)} scored.",
                          _tally(rows), tail] + ([url] if url else []))
    return text


# ---------- transport (OAuth 1.0a user context, stdlib only) ----------

def _pct(s: str) -> str:
    """RFC-3986 percent-encode (OAuth flavor): unreserved = A-Za-z0-9 -._~ only."""
    return quote(s, safe="~")   # quote() already leaves -._ and alphanumerics bare


def signature(method: str, url: str, params: dict[str, str],
              consumer_secret: str, token_secret: str) -> str:
    """HMAC-SHA1 OAuth 1.0a signature over ALL given params. PURE — pinned in the tests to
    the documented reference vector, because a signing bug fails as an opaque 401."""
    enc = sorted((_pct(k), _pct(v)) for k, v in params.items())
    param_str = "&".join(f"{k}={v}" for k, v in enc)
    base = "&".join((method.upper(), _pct(url), _pct(param_str)))
    key = f"{_pct(consumer_secret)}&{_pct(token_secret)}"
    return base64.b64encode(
        hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()).decode()


def _auth_header(url: str) -> str:
    """The Authorization header for one POST. The JSON body is NOT part of an OAuth 1.0a
    signature (only oauth_* + query params are — v2 endpoints take JSON, not form data)."""
    oauth = {"oauth_consumer_key": os.environ["X_API_KEY"],
             "oauth_nonce": secrets.token_hex(16),
             "oauth_signature_method": "HMAC-SHA1",
             "oauth_timestamp": str(int(time.time())),
             "oauth_token": os.environ["X_ACCESS_TOKEN"],
             "oauth_version": "1.0"}
    oauth["oauth_signature"] = signature("POST", url, oauth,
                                         os.environ["X_API_SECRET"],
                                         os.environ["X_ACCESS_SECRET"])
    return "OAuth " + ", ".join(f'{_pct(k)}="{_pct(v)}"' for k, v in sorted(oauth.items()))


def post_tweet(text: str) -> tuple[bool | None, str]:
    """(verdict, tweet_id). True = X confirmed (HTTP 201) · False = definitive rejection,
    nothing published · None = AMBIGUOUS (may be live) — the caller must NEVER retry on None."""
    req = urllib.request.Request(
        X_API, data=json.dumps({"text": text}).encode(),
        headers={"Authorization": _auth_header(X_API), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            body = json.load(resp)
            tid = str(body.get("data", {}).get("id", ""))
            if resp.status == 201 and tid:
                return True, tid
            log.info("pulse: unexpected %s response (%s)", resp.status, body)
            return None, ""                      # 2xx but not the documented shape → ambiguous
    except urllib.error.HTTPError as e:          # 4xx/5xx = a definitive answer, nothing posted
        log.info("pulse: X returned HTTP %s (%s)", e.code, e.read()[:200])
        return False, ""
    except Exception as e:                       # timeout / conn reset — the post MAY be live
        log.info("pulse: send failed, delivery ambiguous (%s)", e)
        return None, ""


# ---------- the cap + the stamp (committed — the delivery record travels in git) ----------

def _load_log() -> list[dict]:
    if not os.path.exists(PULSE_LOG):
        return []
    with open(PULSE_LOG, newline="") as f:
        return list(csv.DictReader(f))


def posted_today(log_rows: list[dict], today: str) -> bool:
    """The metered-fuel cap: at most one POSTED pulse per UTC day. PURE (testable)."""
    return any(r["date_utc"] == today and r["verdict"] == "POSTED" for r in log_rows)


def _stamp(verdict: str, tweet_id: str, text: str) -> None:
    new = not os.path.exists(PULSE_LOG)
    with open(PULSE_LOG, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date_utc", "verdict", "tweet_id", "chars"])
        w.writerow([datetime.now(timezone.utc).date().isoformat(), verdict, tweet_id,
                    _x_len(text)])


def run(argv: list[str]) -> int:
    """Exit 1 only on a FAILED post attempt (REJECTED/UNCONFIRMED) so daily.sh's FAILS fires
    the 🚨 heartbeat; every no-post outcome (gate quiet, unconfigured, capped) is a clean 0."""
    from research import bets, digest
    rows = bets._load()
    try:
        head_rows = digest._committed(bets.CATALOGUE)
    except Exception as e:      # no git/HEAD (fresh clone mid-history?) — gate fails CLOSED:
        log.warning("pulse: no HEAD baseline (%s) — nothing posts", e)
        return 0                # better a missed pulse than an unverified one
    text = compose(rows, head_rows)
    if text is None:
        print("pulse: nothing verdict-grade changed vs HEAD — no post")
        return 0
    print(text)
    if "--post" not in argv:
        print("(dry run — pass --post to publish)")
        return 0
    if not configured():
        print("pulse: X_* env unset — SKIPPED (autopost inert until the app keys exist)")
        return 0
    today = datetime.now(timezone.utc).date().isoformat()
    if posted_today(_load_log(), today):
        print("pulse: already POSTED today — cap is ≤1/day (metered fuel)")
        return 0
    ok, tid = post_tweet(text)
    verdict = "POSTED" if ok else ("UNCONFIRMED" if ok is None else "REJECTED")
    try:
        _stamp(verdict, tid, text)
    except Exception as e:      # the stamp must never cost the post path (digest's rule)
        log.warning("pulse: stamp failed (%s) — delivery verdict unrecorded", e)
    if ok:
        print(f"PULSE POSTED (id {tid})")
        return 0
    if ok is None:
        print("PULSE UNCONFIRMED — may be live; do NOT re-post")
        return 1
    print("PULSE REJECTED (nothing published)")
    return 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(run(sys.argv[1:]))
