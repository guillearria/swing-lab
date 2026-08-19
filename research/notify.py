"""One-way Telegram push — visibility into unattended runs (settlements first).

Transport only: callers build the message, this sends it. Needs TELEGRAM_BOT_TOKEN +
TELEGRAM_CHAT_ID (local .env / cloud-env vars — never committed). FAIL-SOFT by contract:
settle is the audit path, so send() swallows every error and logs one line. Tri-state
return: True = telegram-confirmed · False = definitively rejected, NOTHING delivered ·
None = AMBIGUOUS, the message MAY be delivered — never re-send on None.
html=True sends parse_mode=HTML (callers escape their own dynamic text — html.escape);
a rejected HTML message is retried once as plain text so it is never lost.

  python3 -m research.notify            # config status, nothing sent
  python3 -m research.notify "text"     # manual test send — HUMANS ONLY; a routine must
                                        # never invoke this (routines push via digest --notify)
"""
import json
import logging
import os
import sys
import urllib.error
import urllib.request

from research import config  # noqa: F401  — loads .env

log = logging.getLogger(__name__)
API = "https://api.telegram.org/bot{token}/sendMessage"
TIMEOUT_S = 10
MAX_LEN = 3900  # telegram hard limit 4096; truncate at a newline with margin for the marker
TRUNC_MARK = "\n… truncated — run: python3 -m research.digest"


def configured() -> bool:
    return bool(os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"))


def _post(payload: dict) -> bool:
    req = urllib.request.Request(
        API.format(token=os.environ["TELEGRAM_BOT_TOKEN"]),
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        return bool(json.load(resp).get("ok"))


def send(text: str, html: bool = False) -> bool | None:
    """POST one message. True = confirmed · False = rejected, nothing sent · None = ambiguous."""
    if not configured():
        log.info("notify: skipped (TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID unset)")
        return False
    if len(text) > MAX_LEN:  # composers keep INLINE tags within one line, so a newline cut is
        text = text[:MAX_LEN].rsplit("\n", 1)[0]   # safe — except the digest's card
        if text.count("<blockquote>") > text.count("</blockquote>"):
            text += "</blockquote>"   # a cut INSIDE a card would reject the whole HTML message
        text += TRUNC_MARK
    payload = {"chat_id": os.environ["TELEGRAM_CHAT_ID"], "text": text}
    if html:
        payload["parse_mode"] = "HTML"
    # Retry ONLY on a definitive telegram answer (ok:false or an HTTP status = nothing was
    # delivered). A timeout/connection error is AMBIGUOUS — the message may already be
    # delivered and only the RESPONSE lost; retrying there DOUBLE-POSTED (the duplicate-message
    # bug, fixed 2026-07-24). Prefer one lost message over two sent.
    rejected = False
    try:
        if _post(payload):
            return True
        rejected = True                       # telegram answered ok:false
        log.info("notify: telegram rejected the message")
    except urllib.error.HTTPError as e:       # 4xx/5xx = a definitive answer, nothing delivered
        rejected = True
        log.info("notify: telegram returned HTTP %s", e.code)
    except Exception as e:                    # fail-soft: never break the caller
        log.info("notify: send failed, NOT retrying (ambiguous delivery) (%s)", e)
        return None
    if html and rejected:  # bad entities → deliver ugly rather than lose the message
        try:
            payload.pop("parse_mode")
            return bool(_post(payload))
        except urllib.error.HTTPError as e:   # definitive again — still nothing delivered
            log.info("notify: plain retry returned HTTP %s", e.code)
        except Exception as e:                # the retry itself may have landed
            log.info("notify: plain retry failed, delivery ambiguous (%s)", e)
            return None
    return False


def run(argv: list[str]) -> None:
    if not argv:
        print(f"notify: {'CONFIGURED' if configured() else 'NOT configured'} "
              f"(TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID)")
        return
    ok = send(" ".join(argv))
    print("sent" if ok else
          "UNCONFIRMED — may be delivered, do NOT re-send" if ok is None else
          "REJECTED — nothing sent (see log)")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    run(sys.argv[1:])
