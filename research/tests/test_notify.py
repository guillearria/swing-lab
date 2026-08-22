"""Guard the notify path: fail-soft (never breaks settle) + settle-message formatting."""
from research import bets as B
from research import heartbeat as HB
from research import notify


def test_send_unconfigured_is_false_no_network(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    assert notify.configured() is False
    assert notify.send("x") is False      # skips silently — settle path unharmed


def test_send_swallows_transport_errors(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "c")

    def boom(*a, **k):
        raise OSError("no network")
    monkeypatch.setattr(notify.urllib.request, "urlopen", boom)
    assert notify.send("x") is None       # fail-soft AND ambiguous — may be delivered


def test_send_truncates_oversize_at_newline(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "c")
    sent = {}
    monkeypatch.setattr(notify, "_post", lambda p: sent.update(p) or True)
    assert notify.send("<b>line</b>\n" * 1000) is True
    assert len(sent["text"]) <= 4096
    assert sent["text"].endswith(notify.TRUNC_MARK)
    cut = sent["text"][: -len(notify.TRUNC_MARK)]
    assert cut.endswith("</b>")            # cut fell on a newline — no split tag


def test_truncating_inside_a_card_closes_the_blockquote(monkeypatch):
    """The digest's \U0001f7e2 card is the ONE element that spans lines [2026-08-19]; a cut inside it
    would leave <blockquote> open, telegram would reject the whole HTML message, and the owner
    would get the plain-text retry with every tag showing."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "c")
    sent = {}
    monkeypatch.setattr(notify, "_post", lambda p: sent.update(p) or True)
    body = "filler\n" * 500 + "<blockquote>card\n" + "row\n" * 200 + "last</blockquote>"
    assert body.index("<blockquote>") < notify.MAX_LEN < len(body)   # the cut lands INSIDE it
    assert notify.send(body) is True
    assert sent["text"].count("<blockquote>") == sent["text"].count("</blockquote>")
    assert sent["text"].endswith(notify.TRUNC_MARK)


def test_send_html_retries_plain_on_reject(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "c")
    calls = []

    def post(payload):
        calls.append(dict(payload))
        if "parse_mode" in payload:
            # what urllib actually raises on a telegram 400 — a DEFINITIVE answer (nothing
            # delivered), which is the only case it is safe to retry.
            raise notify.urllib.error.HTTPError("u", 400, "bad entities", {}, None)
        return True
    monkeypatch.setattr(notify, "_post", post)
    assert notify.send("<b>unclosed", html=True) is True       # delivered ugly, not lost
    assert calls[0].get("parse_mode") == "HTML" and "parse_mode" not in calls[1]


def test_send_does_not_double_post_on_ambiguous_failure(monkeypatch):
    """A timeout may mean 'delivered, response lost' — retrying double-posts (the duplicate
    Telegram message bug, 2026-07-24). Exactly ONE post attempt, never two."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "c")
    calls = []

    def post(payload):
        calls.append(dict(payload))
        raise TimeoutError("read timed out")
    monkeypatch.setattr(notify, "_post", post)
    assert notify.send("<b>x</b>", html=True) is None          # ambiguous, not rejected
    assert len(calls) == 1                                     # NOT retried → no duplicate


def test_send_definitive_reject_is_false_one_post(monkeypatch):
    """HTTP 4xx on a plain send = telegram answered, nothing delivered → False (safe to
    re-send once), and exactly one post — False vs None is what a routine keys on."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "c")
    calls = []

    def post(payload):
        calls.append(dict(payload))
        raise notify.urllib.error.HTTPError("u", 400, "bad request", {}, None)
    monkeypatch.setattr(notify, "_post", post)
    assert notify.send("x") is False
    assert len(calls) == 1


def test_bets_settle_msg_format():
    done = [{"direction": "long", "ticker": "ACN", "horizon_d": "63",
             "benchmark": "XLK", "excess_pct": "+4.20"}]
    msg = B.settle_msg(done, (1, 4.2, 4.2, 100.0))
    assert msg.startswith("📊")           # v3 [MSG 2026-08-18]: 🚨 means failure ONLY
    assert "SCORED — ACN 63d vs XLK: 4.2% ahead ✓" in msg
    assert "now 1 of 30 scored · 1 of 1 beat · median 4.2% ahead" in msg


def test_heartbeat_msg_clean_vs_failure():
    bet_rows = [{"status": "open"}, {"status": "open"}, {"status": "closed"}]
    ok = HB.msg("2026-07-03", bet_rows, [])
    assert ok.startswith("✅") and "general 1 closed / 2 open" in ok
    assert "insider" not in ok            # Arc 3 retired 2026-08-02 — ONE silo, not two
    bad = HB.msg("2026-07-03", bet_rows, ["bets", "push"])
    assert bad.startswith("🚨") and "failed: bets, push" in bad and "cron.log" in bad


def _hb_run(monkeypatch, argv):
    """Run heartbeat.run() with the transport captured; returns what (if anything) was sent."""
    sent = []
    monkeypatch.setattr(notify, "send", lambda t: sent.append(t) or True)
    monkeypatch.setattr(HB.bets, "_load", lambda: [{"status": "open"}, {"status": "closed"}])
    HB.run(argv)
    return sent


def test_heartbeat_alarm_always_sends_without_a_flag(monkeypatch):
    """The 🚨 path must NEVER need a flag — an alarm gated behind one is an alarm forgotten.

    Both automated callers land here: daily.sh runs this only when $FAILS is non-empty, and
    READ_LOOP step 7 passes `digest-read` on a non-DELIVERED verdict. Gating these would have
    silenced the settle leg AND the read-leg parity added after the 2026-08-10 silent death.
    """
    assert _hb_run(monkeypatch, ["push"])[0].startswith("🚨")
    assert _hb_run(monkeypatch, ["digest-read"])[0].startswith("🚨")     # READ_LOOP step 7
    assert _hb_run(monkeypatch, ["bets", "push"])[0].startswith("🚨")    # daily.sh $FAILS shape


def test_heartbeat_success_ping_needs_notify(monkeypatch):
    """A ✅ is the one message this system's contract says must never arrive unbidden.

    It was a bare send while this module sat in the live command index beside `digest`, which
    needs --notify — same index, opposite behaviour. On 2026-08-21 a session ran the bare
    command to LOOK at it and pushed "✅ settle ran clean" to the owner's phone; 2026-08-05 was
    the first. Dry by default makes the violation impossible to reach by accident.
    """
    assert _hb_run(monkeypatch, []) == []                               # printed, NOT sent
    assert _hb_run(monkeypatch, ["--notify"])[0].startswith("✅")        # explicit == allowed


def test_heartbeat_flags_never_become_failed_step_names(monkeypatch):
    """$FAILS arrives unquoted as argv, so an unfiltered flag renders INSIDE the alarm as a
    failed step — sending the human to look for a step called '--notify'."""
    out = _hb_run(monkeypatch, ["--notify", "push"])[0]
    assert out.startswith("🚨") and "failed: push" in out and "--notify" not in out
