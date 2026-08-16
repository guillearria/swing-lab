"""Guard the P7b autopost policy's load-bearing properties: the gate posts ONLY on
verdict-surface change (never a short, never movers), the text stays within X's cap, the
1/day metered-fuel cap holds, the OAuth signing matches the documented reference vector
(a signing bug otherwise fails as an opaque 401), and failed sends exit 1 without retry."""
import csv

from research import pulse


def _long(t, excess, status="closed", direction="long"):
    return {"logged_at": f"2026-01-05T12:00:{hash(t) % 60:02d}+00:00", "ticker": t,
            "direction": direction, "horizon_d": "21", "benchmark": "SPY",
            "thesis": "x", "status": status, "entry_date": "2026-01-06", "entry": "100",
            "excess_pct": excess if status == "closed" else "", "pattern_tag": "",
            "notified": ""}


def test_gate_is_quiet_without_a_newly_scored_long():
    rows = [_long("AAA", "+5.00"), _long("BBB", "", status="open")]
    assert pulse.compose(rows, rows) is None                      # nothing changed
    with_short = rows + [_long("CCC", "+9.00", direction="short")]
    assert pulse.compose(with_short, rows) is None                # a scored SHORT never posts


def test_scored_long_posts_verdict_grade_numbers_only():
    head = [_long("AAA", "+5.00"), _long("MU", "", status="open")]
    now = [_long("AAA", "+5.00"), _long("MU", "-7.99")]
    text = pulse.compose(now, head)
    assert "MU -7.99% vs SPY (21d)" in text
    assert "Pool: 2/30 settled longs" in text and "median" in text
    assert "publishes pass OR fail" in text and "Not investment advice." in text
    assert pulse._x_len(text) <= 280


def test_milestone_takes_the_headline():
    head = [_long(f"T{i:02d}", "+2.00") for i in range(9)] + [_long("NEW", "", status="open")]
    now = [_long(f"T{i:02d}", "+2.00") for i in range(9)] + [_long("NEW", "+1.00")]
    text = pulse.compose(now, head)
    assert text.startswith("Milestone: 10 settled longs")


def test_long_batches_degrade_to_count_only_within_the_cap():
    # 11 already settled + 8 new (n 11→19) so NO milestone fires — the batch is what overflows.
    base = [_long(f"T{i:02d}", "+2.00") for i in range(11)]
    head = base + [_long(f"LONGTICKER{i:02d}", "", status="open") for i in range(8)]
    now = base + [_long(f"LONGTICKER{i:02d}", "+12.34") for i in range(8)]
    text = pulse.compose(now, head)
    assert pulse._x_len(text) <= 280
    assert "8 bets scored" in text and "LONGTICKER00" not in text  # names dropped, count kept


def test_oauth_signature_matches_the_documented_reference_vector():
    # X's own worked example ("Creating a signature", api.twitter.com docs) — every value
    # public test data. Form-encoded body params join the signature there; our v2 JSON call
    # passes only oauth_* params through the SAME function.
    params = {
        "status": "Hello Ladies + Gentlemen, a signed OAuth request!",
        "include_entities": "true",
        "oauth_consumer_key": "xvz1evFS4wEEPTGEFPHBog",
        "oauth_nonce": "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg",
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": "1318622958",
        "oauth_token": "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb",
        "oauth_version": "1.0",
    }
    sig = pulse.signature("POST", "https://api.twitter.com/1.1/statuses/update.json", params,
                          "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw",
                          "LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE")
    assert sig == "hCtSmYh+iHYCEqBWrE7C7hYmtUk="


def test_posted_today_cap():
    log = [{"date_utc": "2026-08-15", "verdict": "POSTED", "tweet_id": "1", "chars": "200"},
           {"date_utc": "2026-08-14", "verdict": "REJECTED", "tweet_id": "", "chars": "200"}]
    assert pulse.posted_today(log, "2026-08-15")
    assert not pulse.posted_today(log, "2026-08-16")
    assert not pulse.posted_today([log[1]], "2026-08-14")   # a REJECTED row never caps


def _wire(monkeypatch, tmp_path, head, now):
    from research import bets, digest
    monkeypatch.chdir(tmp_path)
    (tmp_path / "research" / "data").mkdir(parents=True)
    monkeypatch.setattr(bets, "_load", lambda: now)
    monkeypatch.setattr(digest, "_committed", lambda path: head)
    for k in pulse.ENV_KEYS:
        monkeypatch.setenv(k, "k")


def test_run_unconfigured_is_a_clean_noop(monkeypatch, tmp_path, capsys):
    _wire(monkeypatch, tmp_path, [_long("MU", "", status="open")], [_long("MU", "-7.99")])
    for k in pulse.ENV_KEYS:
        monkeypatch.delenv(k)
    assert pulse.run(["--post"]) == 0
    assert "SKIPPED" in capsys.readouterr().out
    assert not (tmp_path / "research" / "data" / "pulse_log.csv").exists()


def test_run_rejected_exits_1_and_stamps(monkeypatch, tmp_path):
    _wire(monkeypatch, tmp_path, [_long("MU", "", status="open")], [_long("MU", "-7.99")])
    monkeypatch.setattr(pulse, "post_tweet", lambda text: (False, ""))
    assert pulse.run(["--post"]) == 1
    rows = list(csv.DictReader(open(tmp_path / "research" / "data" / "pulse_log.csv")))
    assert rows[0]["verdict"] == "REJECTED" and rows[0]["tweet_id"] == ""


def test_run_posted_then_capped(monkeypatch, tmp_path, capsys):
    _wire(monkeypatch, tmp_path, [_long("MU", "", status="open")], [_long("MU", "-7.99")])
    monkeypatch.setattr(pulse, "post_tweet", lambda text: (True, "123"))
    assert pulse.run(["--post"]) == 0
    assert pulse.run(["--post"]) == 0                       # second run same day: capped, clean
    out = capsys.readouterr().out
    assert "PULSE POSTED (id 123)" in out and "cap is" in out
    rows = list(csv.DictReader(open(tmp_path / "research" / "data" / "pulse_log.csv")))
    assert len(rows) == 1                                   # the capped run stamped nothing


def test_run_dry_never_posts(monkeypatch, tmp_path, capsys):
    _wire(monkeypatch, tmp_path, [_long("MU", "", status="open")], [_long("MU", "-7.99")])
    monkeypatch.setattr(pulse, "post_tweet",
                        lambda text: (_ for _ in ()).throw(AssertionError("posted on dry run")))
    assert pulse.run([]) == 0
    assert "dry run" in capsys.readouterr().out
