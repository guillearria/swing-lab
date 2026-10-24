"""Guard GATE M1's arithmetic on synthetic data. The real files are read only by the CLI run, after
the bar was committed [FINDINGS GATE M1]; the pinned constants below ARE that bar."""
import hashlib
import io
import math
import zipfile

import pytest

from research import gate_lottery as G
from research.gate_reversal import nw_t


def _zip(text, name="data.csv"):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(name, text)
    return buf.getvalue()


def _pf_csv(months, f, extra_rows=""):
    """JKP-like portfolio CSV, decimal returns; f(i, pf) → return."""
    lines = ["excntry,characteristic,pf,eom,n,signal,ret_ew,ret_vw,ret_vw_cap"]
    for i, ym in enumerate(months):
        for pf in (1, 2, 3):
            lines.append(f"USA,rmax1_21d,{pf},{ym // 100}-{ym % 100:02d}-28,100,{0.01 * pf},"
                         f"9,9,{f(i, pf)}")
    return "\n".join(lines) + "\n" + extra_rows


def test_the_pinned_bar_is_the_preregistered_one():
    """These constants are [GATE M1]; changing one after the first run is moving the goalposts."""
    assert (G.START, G.END) == (201103, 202512) and len(G.expected_months(G.START, G.END)) == 178
    assert G.PREMISE == (196207, 200512) and G.PREMISE_MIN_MONTHS == 400
    assert G.WP_ERA == (200601, 201102)
    assert G.NW_LAGS == 3 and G.ALPHA == 0.05 and G.CHAR == "rmax1_21d"
    assert (G.PF_MD5, G.MKT_MD5) == ("2cac794c7f22fd4cffdbc83806c2e1ce",
                                     "4cfedead71640b65c9150b4e9e241416")
    assert "%5Brmax1_21d%5D_%5Bmonthly%5D_%5Bvw_cap%5D" in G.PF_URL
    assert "%5Bmkt%5D_%5Bmonthly%5D_%5Bvw%5D" in G.MKT_URL


def test_fetch_refuses_a_file_that_is_not_the_preregistered_one(monkeypatch):
    class R:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b"other bytes"
    monkeypatch.setattr(G.urllib.request, "urlopen", lambda *a, **k: R())
    with pytest.raises(SystemExit):
        G.fetch("https://x", "0" * 32)
    assert G.fetch("https://x", hashlib.md5(b"other bytes").hexdigest()) == b"other bytes"


def test_read_csv_needs_exactly_one_member():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("a.csv", "x\n1\n")
        z.writestr("b.csv", "x\n2\n")
    with pytest.raises(ValueError):
        G.read_csv(buf.getvalue())
    assert G.read_csv(_zip("x\n1\n")) == [{"x": "1"}]


def test_parse_pfs_keeps_usa_rmax_capped_vw_and_converts_to_percent():
    other = "USA,rmax5_21d,3,2011-03-31,100,0.5,9,9,0.9\nGBR,rmax1_21d,3,2011-03-31,100,0.5,9,9,0.9\n"
    rows = G.read_csv(_zip(_pf_csv([201103], lambda i, pf: {1: 0.012, 2: 0.010, 3: -0.004}[pf],
                                   other)))
    rets, sig, n = G.parse_pfs(rows)
    assert rets == {201103: pytest.approx({1: 1.2, 2: 1.0, 3: -0.4})}
    assert sig[201103][3] > sig[201103][1] and n[201103][3] == 100
    with pytest.raises(ValueError):
        G.parse_pfs(G.read_csv(_zip("excntry,pf,eom,ret_vw\nUSA,1,2011-03-31,0.1\n")))


def test_to_pct_tells_decimal_from_percent():
    assert G.to_pct([0.01, -0.02, 0.03]) == 100.0 and G.to_pct([1.0, -2.0, 3.0]) == 1.0


def test_parse_mkt_reads_the_jkp_factor_layout():
    text = ("location,name,freq,weighting,direction,n_stocks,n_stocks_min,date,ret\n"
            "usa,mkt,monthly,vw,1,3000,3000,2011-03-31,0.02\n"
            "usa,mkt,monthly,vw,1,3000,3000,2011-04-30,-0.01\n")
    assert G.parse_mkt(G.read_csv(_zip(text))) == pytest.approx({201103: 2.0, 201104: -1.0})


def test_series_avoid_spread_low():
    avoid, spread, low = G.series({201103: {1: 1.2, 2: 1.0, 3: -0.4}, 201104: {1: 1.0, 2: 1.0}})
    assert list(avoid) == [201103]                                  # a month without pf 3 drops
    assert avoid[201103] == pytest.approx(1.4) and spread[201103] == pytest.approx(1.6)
    assert low[201103] == pytest.approx(0.2)


def _xy(n=120):
    x = [3.0 * math.sin(1.7 * t) + 0.5 for t in range(n)]
    noise = [0.8 * math.cos(2.3 * t + 0.4) for t in range(n)]
    return x, noise


def test_capm_recovers_alpha_and_beta():
    x, noise = _xy()
    c = G.capm([1.0 - 0.3 * xi + e for xi, e in zip(x, noise)], x)
    assert c["alpha"] == pytest.approx(1.0, abs=0.05) and c["beta"] == pytest.approx(-0.3, abs=0.05)
    assert c["t"] > 5 and c["p"] < 0.001


def test_capm_hac_se_matches_the_mean_only_nw_when_x_is_demeaned():
    """With a zero-mean regressor the intercept is the mean of y and its HAC variance is the
    Newey-West variance of the residuals' mean — an independent check of the sandwich."""
    x, noise = _xy()
    mx = sum(x) / len(x)
    xd = [v - mx for v in x]
    c = G.capm([0.4 + 0.5 * v + e for v, e in zip(xd, noise)], xd)
    e = [0.4 + 0.5 * v + ei - c["alpha"] - c["beta"] * v for v, ei in zip(xd, noise)]
    assert c["se"] == pytest.approx(nw_t(e, G.NW_LAGS)[1], rel=1e-9)


def _window_data(f_avoid, months, beta=-0.3):
    x, noise = _xy(len(months))
    mkt = dict(zip(months, x))
    avoid = {ym: f_avoid(i) + beta * x[i] + 0.3 * noise[i] for i, ym in enumerate(months)}
    return avoid, mkt


def test_evaluate_needs_all_four_window_conditions():
    ms = G.expected_months(201103, 202012)
    avoid, mkt = _window_data(lambda i: 1.0, ms)
    sp = {ym: 0.5 + mkt[ym] * 0.1 for ym in ms}
    assert G.evaluate(avoid, sp, mkt, ms[0], ms[-1])["verdict"] == "PASS"
    neg_sp = {ym: -0.5 for ym in ms}
    assert G.evaluate(avoid, neg_sp, mkt, ms[0], ms[-1])["checks"]["spread_alpha_sign"] is False
    split, _ = _window_data(lambda i: 3.0 if i < len(ms) // 2 else -0.5, ms)
    assert G.evaluate(split, sp, mkt, ms[0], ms[-1])["checks"]["both_halves"] is False
    one, _ = _window_data(lambda i: 60.0 if i == 7 else -0.4, ms)
    assert G.evaluate(one, sp, mkt, ms[0], ms[-1])["checks"]["not_one_month"] is False
    weak, _ = _window_data(lambda i: 0.01, ms)
    assert G.evaluate(weak, sp, mkt, ms[0], ms[-1])["checks"]["alpha_significant"] is False


def test_beta_is_removed_before_judging():
    """A pure beta drag in a rising market (alpha 0) must not pass; a stock-specific drag hidden
    by a big market rise must not fail on the raw number."""
    ms = G.expected_months(201103, 202012)
    x = [2.0 + 3.0 * math.sin(1.7 * t) for t in range(len(ms))]
    mkt = dict(zip(ms, x))
    noise = [0.3 * math.cos(2.3 * t + 0.4) for t in range(len(ms))]
    sp = {ym: 0.5 for ym in ms}
    beta_only = {ym: -0.5 * x[i] + noise[i] for i, ym in enumerate(ms)}
    r = G.evaluate(beta_only, sp, mkt, ms[0], ms[-1])
    assert r["raw_mean"] < 0 and r["checks"]["alpha_significant"] is False
    hidden = {ym: 0.6 - 0.5 * x[i] + noise[i] for i, ym in enumerate(ms)}
    r = G.evaluate(hidden, sp, mkt, ms[0], ms[-1])
    assert r["raw_mean"] < 0 and r["verdict"] == "PASS"


def test_premise_needs_enough_months_and_reports_the_sign():
    ms = G.expected_months(196208, 200512)
    avoid, mkt = _window_data(lambda i: 0.5, ms)
    assert G.premise(avoid, mkt)["holds"] is True
    neg, _ = _window_data(lambda i: -0.5, ms)
    assert G.premise(neg, mkt)["holds"] is False
    short = {ym: v for ym, v in avoid.items() if ym >= 199001}
    with pytest.raises(ValueError):
        G.premise(short, mkt)


def test_check_order_refuses_an_inverted_file():
    ms = [201103, 201104]
    rets = {201103: {1: 1.0, 3: 5.0}, 201104: {1: 1.2, 3: -4.0}}     # pf 3 the volatile one
    assert G.check_order({ym: {1: 0.01, 3: 0.09} for ym in ms}, rets, ms, ms).startswith("verified")
    with pytest.raises(ValueError):
        G.check_order({201103: {1: 0.09, 3: 0.01}, 201104: {1: 0.01, 3: 0.09}}, rets, ms, ms)
    assert G.check_order({}, rets, ms, ms).startswith("no signal column; pf 3 SD")
    flipped = {ym: {1: p[3], 3: p[1]} for ym, p in rets.items()}
    with pytest.raises(ValueError):
        G.check_order({}, flipped, ms, ms)                             # no column, pf 1 volatile


def test_check_alignment_refuses_a_one_month_shift():
    ms = G.expected_months(201103, 202512)
    x = [3.0 * math.sin(1.7 * t) + 0.5 for t in range(len(ms))]
    mkt = dict(zip(ms, x))
    rets = {ym: {2: 1.0 * x[i] + 0.2 * math.cos(2.3 * i)} for i, ym in enumerate(ms)}
    assert G.check_alignment(rets, mkt, ms) == pytest.approx(1.0, abs=0.05)
    shifted = {ms[i]: mkt[ms[i - 1]] for i in range(1, len(ms))}
    with pytest.raises(ValueError):
        G.check_alignment(rets, shifted, ms[1:])


def test_parsers_refuse_duplicate_keys_and_filter_weighting():
    dup = _pf_csv([201103], lambda i, pf: 0.01) + "USA,rmax1_21d,2,2011-03-28,100,0.02,9,9,0.5\n"
    with pytest.raises(ValueError):
        G.parse_pfs(G.read_csv(_zip(dup)))
    text = ("location,name,freq,weighting,date,ret\n"
            "usa,mkt,monthly,vw,2011-03-31,0.02\n"
            "usa,mkt,monthly,vw_cap,2011-03-31,0.03\n"
            "usa,mkt,daily,vw,2011-03-31,0.001\n")
    assert G.parse_mkt(G.read_csv(_zip(text))) == pytest.approx({201103: 2.0})
    with pytest.raises(ValueError):
        G.parse_mkt(G.read_csv(_zip(text.replace(",vw_cap,", ",vw,"))))


def test_mde80():
    assert G.mde80(5.0, 178) == pytest.approx((1.6449 + 0.8416) * 5.0 / math.sqrt(178))


def test_run_end_to_end_on_synthetic_files(monkeypatch, capsys):
    """The CLI path prints a verdict from two well-formed files (synthetic, decimal returns)."""
    ms = G.expected_months(196207, 202512)
    x = [0.03 * math.sin(1.7 * t) + 0.005 for t in range(len(ms))]
    pf = _pf_csv(ms, lambda i, p: {1: 0.8 * x[i] + 0.004, 2: x[i] + 0.004,
                                   3: 1.3 * x[i] - 0.002 + 0.01 * math.cos(2.3 * i)}[p])
    mk = "location,name,freq,weighting,date,ret\n" + "\n".join(
        f"usa,mkt,monthly,vw,{ym // 100}-{ym % 100:02d}-28,{x[i]}" for i, ym in enumerate(ms))
    blobs = {G.PF_URL: _zip(pf), G.MKT_URL: _zip(mk + "\n")}
    monkeypatch.setattr(G, "fetch", lambda url, md5: blobs[url])
    assert G.run([]) == 0
    out = capsys.readouterr().out
    assert "VERDICT PASS" in out and "verified in 178 of 178" in out and "premise" in out
