"""Did each upstream feed actually work today?

A dead source is NOT an exception — `scan` just returns zero candidates — so the digest's
per-silo fail-soft cannot see it and the ledger quietly stops growing. On 2026-07-27 the
read run reported "openinsider fetch down" as prose inside a run note; nothing escalated, and
the insider ledger — meant to be the SECOND verdict silo — quietly delivered nothing for five
weeks. Arc 3 has since CLOSED (2026-08-02) and the project runs on ONE silo by design, which
makes this file MORE load-bearing, not less: with a single feed, a silent outage is total.
Each scan records its outcome and `digest._feed_section` escalates a stale `last_ok` to a DO-NOW.

An alarm that can never be cleared is worse than none — it trains the reader to ignore the
channel. When a feed is retired, delete its key here in the SAME diff that retires it.

Deliberately a plain JSON file, not a ledger: this is OPERATIONAL state (is the pipe open),
never evidence. Nothing here counts toward any verdict N.
"""
import json
import logging
import os
from datetime import datetime, timezone

log = logging.getLogger(__name__)
PATH = "research/data/_feed_status.json"


def _load(path: str | None = None) -> dict:
    try:
        with open(path or PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def record(source: str, ok: bool, error: str = "", path: str | None = None,
           last_bar: str = "", n_ok: int | None = None, n_total: int | None = None) -> None:
    """Stamp one feed's outcome. FAIL-SOFT: bookkeeping never breaks a scan.

    `last_ok` says the PIPE opened; `last_bar` (newest COMPLETED session actually used) says
    the WATER was fresh — on 2026-08-04 the feed was "ok" while bars had not advanced past
    07-31 and the scan logged 0 movers silently [FINDINGS 2026-08-04 ops]. `n_ok`/`n_total`
    is fetch coverage: a partial outage otherwise looks exactly like a quiet day. All three
    are write-only-when-provided so a legacy caller never erases them.

    `path` resolves at CALL time, not as a default argument bound at import. That is not a
    style preference: with the default bound, monkeypatching feedstatus.PATH did nothing and a
    test that reached this function OVERWROTE the live _feed_status.json with a synthetic
    error — contaminating the audit trail with a fabricated observation (caught 2026-08-01,
    while writing the test for the outage this module exists to report). A module whose
    redirect hook silently doesn't work is worse than one with no hook at all.
    """
    path = path or PATH
    try:
        status = _load(path)
        st = status.setdefault(source, {})
        if ok:
            st["last_ok"] = datetime.now(timezone.utc).date().isoformat()
            st["last_error"] = ""
        else:
            st["last_error"] = error[:200]
        if last_bar:
            st["last_bar"] = last_bar
        if n_ok is not None:
            st["n_ok"], st["n_total"] = n_ok, n_total
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(status, f, indent=1, sort_keys=True)
    except Exception as e:
        log.debug("feedstatus: could not record %s (%s)", source, e)
