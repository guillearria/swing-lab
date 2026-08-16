"""Guard the chart-endpoint price path: adjustment math, null bars, settle semantics."""
import io
import json

from research import prices


def _payload(timestamps, closes, adjcloses, opens=None, splits=None):
    n = len(timestamps)
    quote = {"open": opens or closes, "high": closes, "low": closes,
             "close": closes, "volume": [100] * n}
    res = {"meta": {"exchangeTimezoneName": "America/New_York"},
           "timestamp": timestamps,
           "indicators": {"quote": [quote], "adjclose": [{"adjclose": adjcloses}]}}
    if splits:
        res["events"] = {"splits": splits}
    return {"chart": {"result": [res]}}


class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _mock(monkeypatch, payload):
    monkeypatch.setattr(prices.urllib.request, "urlopen",
                        lambda *a, **k: _Resp(json.dumps(payload).encode()))


# 2025-01-02 .. 2025-01-06 at 14:30 UTC (09:30 ET — the date must not shift)
TS = [1735828200, 1735914600, 1736173800]


def test_adjusted_close_and_date(monkeypatch):
    _mock(monkeypatch, _payload(TS, [100.0, 102.0, 104.0], [50.0, 51.0, 52.0],
                                opens=[99.0, 101.0, 103.0]))
    bars = prices.daily_history("SPY", "2y")
    assert [b["date"] for b in bars] == ["2025-01-02", "2025-01-03", "2025-01-06"]
    assert bars[0]["close"] == 50.0                      # close == adjclose
    assert abs(bars[0]["open"] - 99.0 * 0.5) < 1e-9      # OHL scaled by adj factor


def test_null_bars_dropped(monkeypatch):
    _mock(monkeypatch, _payload(TS, [100.0, None, 104.0], [50.0, None, 52.0]))
    assert len(prices.daily_history("SPY", "2y")) == 2


def test_bars_after_strictly_after_and_capped(monkeypatch):
    _mock(monkeypatch, _payload(TS, [100.0, 102.0, 104.0], [100.0, 102.0, 104.0]))
    bars = prices.bars_after("SPY", "2025-01-02", 1)
    assert [b["date"] for b in bars] == ["2025-01-03"]   # excludes start day, caps at n


def test_split_repair_when_adjclose_ignores_the_split(monkeypatch):
    """The MNST regression [ARC 5 #12a]: Yahoo shipped adjclose == close ACROSS a 2:1 split, so
    f = a/c was a no-op and a 90→45 print read as a −50% move. With the split in the events
    block and an unreflecting adjclose, pre-split closes must be halved."""
    # TS[2] (2025-01-06) is the split day; closes 100,102 → 51,52 post-split
    split = {"0": {"date": TS[2], "numerator": 2, "denominator": 1, "splitRatio": "2:1"}}
    _mock(monkeypatch, _payload(TS, [100.0, 102.0, 51.0], [100.0, 102.0, 51.0], splits=split))
    bars = prices.daily_history("MNST", "2y")
    assert [round(b["close"], 2) for b in bars] == [50.0, 51.0, 51.0]
    assert abs(bars[0]["open"] - 50.0) < 1e-9        # OHL scaled by the repaired factor too


def test_split_repair_is_a_noop_when_adjclose_already_reflects_it(monkeypatch):
    """A correctly-adjusted feed must NOT be double-adjusted just because events lists the
    split — the pre-split a/c ratio sits at den/num, so the repair detects 'reflected'."""
    split = {"0": {"date": TS[2], "numerator": 2, "denominator": 1, "splitRatio": "2:1"}}
    _mock(monkeypatch, _payload(TS, [100.0, 102.0, 51.0], [50.0, 51.0, 51.0], splits=split))
    bars = prices.daily_history("MNST", "2y")
    assert [round(b["close"], 2) for b in bars] == [50.0, 51.0, 51.0]


def test_no_events_block_unchanged(monkeypatch):
    _mock(monkeypatch, _payload(TS, [100.0, 102.0, 104.0], [100.0, 102.0, 104.0]))
    bars = prices.daily_history("SPY", "2y")
    assert [b["close"] for b in bars] == [100.0, 102.0, 104.0]


def test_fallback_on_chart_failure(monkeypatch):
    def boom(*a, **k):
        raise OSError("egress denied")
    monkeypatch.setattr(prices.urllib.request, "urlopen", boom)
    sentinel = [{"date": "2025-01-03", "close": 1.0}]
    monkeypatch.setattr(prices, "_yf_rows", lambda *a, **k: sentinel)
    assert prices.daily_history("SPY", "2y") == sentinel
    assert prices.bars_after("SPY", "2025-01-02", 5) == sentinel
