"""Forward-outcome labeling — a PURE function. No I/O, and NO lookahead.

Given the snapshot's entry price and only the bars that came AFTER the snapshot,
compute forward returns and whether the +10% target was hit before the -5% stop.
Uses intraday high/low so a target/stop "touch" counts, like a real trade.
"""

from research import config


def settle(entry_price: float, forward_bars: list[dict]) -> dict | None:
    """`forward_bars`: daily bars strictly AFTER the snapshot, oldest->newest.

    Only the first HORIZON_DAYS bars are consulted — never the future beyond it.
    Returns outcome metrics, or None if there are no forward bars.
    """
    if not forward_bars:
        return None

    window = forward_bars[:config.HORIZON_DAYS]
    closes = [b["close"] for b in window]

    def ret_after(n: int) -> float | None:
        return (closes[n - 1] - entry_price) / entry_price if len(closes) >= n else None

    tp = entry_price * (1 + config.TP1_PCT)
    sl = entry_price * (1 - config.STOP_PCT)

    hit = None          # 1 = target first, 0 = stop first, None = neither in window
    max_fav = 0.0       # best favorable excursion (high vs entry)
    max_adv = 0.0       # worst adverse excursion (low vs entry)
    for b in window:
        max_fav = max(max_fav, (b["high"] - entry_price) / entry_price)
        max_adv = min(max_adv, (b["low"] - entry_price) / entry_price)
        hit_tp = b["high"] >= tp
        hit_sl = b["low"] <= sl
        # Same-day ambiguity: we can't know intraday order from a daily bar,
        # so we assume the stop hit first (conservative — never overstates edge).
        if hit_sl:
            hit = 0
            break
        if hit_tp:
            hit = 1
            break

    return {
        "ret_1d": ret_after(1),
        "ret_3d": ret_after(3),
        "ret_5d": ret_after(5),
        "max_favorable": max_fav,
        "max_adverse": max_adv,
        "hit_tp1_before_stop": hit,
    }
