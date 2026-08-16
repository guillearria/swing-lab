"""Outcome labeling is pure — and must never peek past the horizon."""

from research import outcome, config


def _fb(high, low, close):
    return {"date": "x", "open": close, "high": high, "low": low,
            "close": close, "volume": 0.0}


ENTRY = 100.0   # tp = 110, sl = 95 (config: +10% / -5%)


def test_target_hit_first():
    bars = [_fb(111, 98, 109)]            # touches +10% before any stop
    assert outcome.settle(ENTRY, bars)["hit_tp1_before_stop"] == 1


def test_stop_hit_first():
    bars = [_fb(102, 94, 96)]             # touches -5%
    assert outcome.settle(ENTRY, bars)["hit_tp1_before_stop"] == 0


def test_same_day_touch_is_conservative_stop():
    bars = [_fb(111, 94, 100)]            # both touched same day -> assume stop
    assert outcome.settle(ENTRY, bars)["hit_tp1_before_stop"] == 0


def test_neither_within_horizon():
    bars = [_fb(104, 97, 101)] * config.HORIZON_DAYS
    oc = outcome.settle(ENTRY, bars)
    assert oc["hit_tp1_before_stop"] is None


def test_no_lookahead_past_horizon():
    # 5 range-bound days, then a huge spike on day 6 that MUST be ignored.
    bars = [_fb(104, 97, 101)] * config.HORIZON_DAYS + [_fb(200, 200, 200)]
    oc = outcome.settle(ENTRY, bars)
    assert oc["hit_tp1_before_stop"] is None          # day 6 not consulted
    assert oc["max_favorable"] < 0.10                 # spike excluded from MFE


def test_forward_returns():
    bars = [_fb(101, 100, 101), _fb(103, 101, 103), _fb(106, 104, 106)]
    oc = outcome.settle(ENTRY, bars)
    assert round(oc["ret_1d"], 4) == 0.01
    assert round(oc["ret_3d"], 4) == 0.06
    assert oc["ret_5d"] is None                       # only 3 forward bars exist
