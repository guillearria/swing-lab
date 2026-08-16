"""Momentum signal — a PURE function over daily bars. No I/O, fully testable.

Two questions, both must be yes for STRONG:
  1. Real participation?  (latest volume vs. the recent baseline average)
  2. Actually moving up?   (% change over the trend window)
"""

from research import config


def compute(bars: list[dict]) -> dict | None:
    """`bars`: daily bars oldest->newest, each {date, open, high, low, close, volume}.

    Returns {price, pct_change, rel_volume, strong} or None if too few bars.
    """
    need = config.LOOKBACK_DAYS + config.TREND_DAYS + 1
    if len(bars) < need:
        return None

    closes = [b["close"] for b in bars]
    volumes = [b["volume"] for b in bars]
    trend = config.TREND_DAYS
    lookback = config.LOOKBACK_DAYS

    pct_change = (closes[-1] - closes[-1 - trend]) / closes[-1 - trend]

    # baseline = the `lookback` days ending just before the trend window,
    # so the recent move never contaminates its own baseline.
    baseline = volumes[-(lookback + trend):-trend]
    avg_vol = sum(baseline) / len(baseline) if baseline else 0.0
    rel_volume = volumes[-1] / avg_vol if avg_vol else 0.0

    strong = (rel_volume >= config.REL_VOLUME_STRONG
              and pct_change >= config.PCT_STRONG)

    return {
        "price": closes[-1],
        "pct_change": pct_change,
        "rel_volume": rel_volume,
        "strong": strong,
    }
