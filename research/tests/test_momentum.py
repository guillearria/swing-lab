"""Momentum is pure math — test it with synthetic bars, no network."""

from research import momentum, config


def _bars(closes, volumes):
    return [{"date": f"2024-01-{i+1:02d}", "open": c, "high": c, "low": c,
             "close": c, "volume": v} for i, (c, v) in enumerate(zip(closes, volumes))]


def _n():  # minimum bars momentum needs
    return config.LOOKBACK_DAYS + config.TREND_DAYS + 1  # 26


def test_strong_when_volume_spike_and_price_up():
    n = _n()
    closes = [100.0] * n
    closes[-1] = 105.0            # +5% over the 5-day trend window
    volumes = [100.0] * n
    volumes[-1] = 300.0           # 3x the baseline average
    out = momentum.compute(_bars(closes, volumes))
    assert out["strong"] is True
    assert round(out["pct_change"], 4) == 0.05
    assert round(out["rel_volume"], 2) == 3.0
    assert out["price"] == 105.0


def test_weak_when_volume_normal():
    n = _n()
    closes = [100.0] * n
    closes[-1] = 105.0
    volumes = [100.0] * n
    volumes[-1] = 150.0           # only 1.5x — below the 2x bar
    assert momentum.compute(_bars(closes, volumes))["strong"] is False


def test_weak_when_price_flat():
    n = _n()
    closes = [100.0] * n          # no move
    volumes = [100.0] * n
    volumes[-1] = 300.0
    assert momentum.compute(_bars(closes, volumes))["strong"] is False


def test_none_when_too_few_bars():
    assert momentum.compute(_bars([100.0] * 10, [100.0] * 10)) is None
