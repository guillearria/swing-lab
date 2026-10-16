"""Guard GATE R1's arithmetic on synthetic data. The real file is read only by the CLI run, after
the bar was committed [FINDINGS GATE R1]; the pinned constants below ARE that bar."""
import pytest

from research import gate_reversal as G


def _names():
    out = []
    for q in range(1, 6):
        for p in range(1, 6):
            size = "SMALL" if q == 1 else ("BIG" if q == 5 else f"ME{q}")
            prior = "LoPRIOR" if p == 1 else ("HiPRIOR" if p == 5 else f"PRIOR{p}")
            out.append(f"{size} {prior}")
    return out


def _row(ym, f):
    return f"{ym}," + ",".join(f"{f(q, p):.2f}" for q in range(1, 6) for p in range(1, 6))


def _file(rows):
    return ("This file was created using the 202608 CRSP database.\n\n"
            "  Average Value Weighted Returns -- Monthly\n,"
            + ",".join(_names()) + "\n" + "\n".join(rows) + "\n\n"
            "  Average Equal Weighted Returns -- Monthly\n," + ",".join(_names()) + "\n"
            + _row(201412, lambda q, p: 99.0) + "\n")


def test_the_pinned_bar_is_the_preregistered_one():
    """These constants are [GATE R1]; changing one after the first run is moving the goalposts."""
    assert (G.START, G.END) == (201501, 202605)
    assert G.SIZE_Q == (2, 3, 4) and G.NW_LAGS == 3 and G.ALPHA == 0.05
    assert G.COST_PER_MONTH == 0.54 and G.STRESS_COSTS == (1.25, 1.65)
    assert all(c > G.COST_PER_MONTH for c in G.STRESS_COSTS)       # stress is never softer
    assert len(G.expected_months()) == 137
    assert G.URL.endswith("25_Portfolios_ME_Prior_1_0_CSV.zip")


def test_parse_reads_only_the_first_block_and_validates_layout():
    text = _file([_row(201501, lambda q, p: 1.0)])
    cols, rows = G.parse_first_block(text)
    assert len(cols) == 25 and [ym for ym, _ in rows] == [201501]   # EW block ignored
    assert G.col_index(cols, 2, 1) == 5 and G.col_index(cols, 4, 5) == 19
    with pytest.raises(ValueError):
        G.col_index(cols[1:] + cols[:1], 2, 1)                      # shuffled header → refuse


def test_series_spread_and_long_leg_average_size_quintiles_2_to_4():
    # losers (p=1) earn 3 + q, middle (p=3) earns 1, winners (p=5) earn 0; q=1 and q=5 are poison
    f = lambda q, p: 50.0 if q in (1, 5) else {1: 3.0 + q, 3: 1.0, 5: 0.0}.get(p, 0.5)
    cols, rows = G.parse_first_block(_file([_row(201501, f)]))
    sp, lg = G.series(cols, rows)
    assert sp[201501] == pytest.approx(6.0)          # mean(5, 6, 7) − 0
    assert lg[201501] == pytest.approx(5.0)          # mean(5, 6, 7) − 1


def test_missing_values_drop_the_month():
    f = lambda q, p: -99.99 if (q, p) == (3, 5) else 1.0
    cols, rows = G.parse_first_block(_file([_row(201501, f)]))
    assert G.series(cols, rows) == ({}, {})


def test_nw_t_matches_iid_formula_at_zero_lags():
    m, se, t, p = G.nw_t([1.0, 2.0, 3.0, 4.0], lags=0)
    assert m == 2.5 and se == pytest.approx((1.25 / 4) ** 0.5) and 0 < p < 0.5


def test_evaluate_refuses_to_run_without_a_cost():
    with pytest.raises(ValueError):
        G.evaluate({201501: 1.0, 201502: 1.0}, {201501: 1.0, 201502: 1.0}, cost=None)


def _months(n, start=201501):
    out, y, m = [], start // 100, start % 100
    for _ in range(n):
        out.append(y * 100 + m)
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def test_evaluate_needs_all_five_conditions():
    ms = _months(24)
    good = {ym: 1.0 + 0.2 * (i % 3) for i, ym in enumerate(ms)}
    long_ok = {ym: 0.5 for ym in ms}
    assert G.evaluate(good, long_ok, ms[0], ms[-1], cost=0.54)["verdict"] == "PASS"
    assert G.evaluate(good, long_ok, ms[0], ms[-1], cost=2.0)["checks"]["beats_cost"] is False
    long_bad = {ym: -0.1 for ym in ms}
    assert G.evaluate(good, long_bad, ms[0], ms[-1], cost=0.54)["checks"]["long_leg"] is False
    split = {ym: (3.0 if i < 12 else -0.5) for i, ym in enumerate(ms)}
    assert G.evaluate(split, long_ok, ms[0], ms[-1], cost=0.0)["checks"]["both_halves"] is False
    one = {ym: (-0.1 if i else 40.0) for i, ym in enumerate(ms)}            # one huge month
    assert G.evaluate(one, long_ok, ms[0], ms[-1], cost=0.0)["checks"]["not_one_month"] is False


def test_window_is_inclusive_and_stops_before_the_ledger():
    sp = {201412: 99.0, 201501: 1.0, 202605: 1.0, 202606: -99.0}
    r = G.evaluate(sp, dict(sp), cost=0.0)
    assert r["first"] == 201501 and r["last"] == 202605 and r["n"] == 2
