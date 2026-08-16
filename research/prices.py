"""Price/volume data — the one I/O seam for prices.

Primary path: Yahoo's public v8 chart endpoint via stdlib urllib. No cookie/crumb
handshake — yfinance's crumb host (fc.yahoo.com) is egress-blocked in the cloud env
while the chart host (query1) is open [BACKLOG 2026-07-02], and the settle routine
must be able to score matured bets unattended. yfinance remains the fallback.

Returns plain lists of dicts with OHLC auto-adjusted (close == adjclose, like
yfinance auto_adjust=True), never DataFrames. To swap providers, reimplement these
functions and nothing else changes.
"""

import json
import logging
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

log = logging.getLogger(__name__)

CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) swing_lab research"}
TIMEOUT_S = 20
_SECONDS = {"d": 86_400, "mo": 86_400 * 31, "y": 86_400 * 366}


def _epoch_from_period(period: str) -> int:
    """'40d' / '6mo' / '20y' -> epoch seconds that far back from now."""
    num = int("".join(ch for ch in period if ch.isdigit()))
    unit = "".join(ch for ch in period if ch.isalpha())
    return int(time.time()) - num * _SECONDS[unit]


def _chart_rows(symbol: str, qs: dict) -> list[dict]:
    """One chart-endpoint call -> adjusted bars (oldest->newest). Raises on failure."""
    url = (CHART.format(sym=urllib.parse.quote(symbol)) + "?"
           + urllib.parse.urlencode({"interval": "1d", "events": "div,split", **qs}))
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                timeout=TIMEOUT_S) as resp:
        res = json.load(resp)["chart"]["result"][0]
    quote = res["indicators"]["quote"][0]
    adj = (res["indicators"].get("adjclose", [{}])[0].get("adjclose")
           or quote["close"])  # some symbols ship no adjclose block
    try:
        tz = ZoneInfo(res["meta"]["exchangeTimezoneName"])
    except Exception:
        tz = timezone.utc
    raw = []
    for i, ts in enumerate(res.get("timestamp") or []):
        c, a = quote["close"][i], adj[i]
        if c is None or a is None:
            # halted/blank bar. KNOWN-LATENT [ARC 5 #12a]: dropping it means "N bars back" can
            # span more than N sessions — tolerated, the windows here are approximate anyway.
            continue
        raw.append((datetime.fromtimestamp(ts, tz).date().isoformat(), i, c, a))
    # SPLIT REPAIR [ARC 5 #12a]: Yahoo sometimes ships adjclose == close ACROSS a split (seen
    # live: MNST 2:1 on 2026-08-10 — the events block reported it, adjclose ignored it), which
    # makes f = a/c a no-op and poisons every window straddling the split (movers logged MNST
    # -50.6% as a real move). For each split event, look at the last bar BEFORE it: a reflected
    # adjclose sits near den/num there, an unreflected one near 1.0 — whichever it is closer to
    # wins (dividends only nudge the ratio a few %, far less than any real split factor).
    unreflected = []  # (split_date, den/num) events the adjclose failed to carry
    for ev in (res.get("events", {}).get("splits") or {}).values():
        try:
            sd = datetime.fromtimestamp(ev["date"], tz).date().isoformat()
            num, den = float(ev["numerator"]), float(ev["denominator"])
        except Exception:
            continue
        if num <= 0 or den <= 0 or num == den:
            continue
        true_f = den / num
        pre = next(((c, a) for d, i, c, a in reversed(raw) if d < sd), None)
        if pre is None:
            continue
        ratio = pre[1] / pre[0]
        if abs(ratio - 1.0) < abs(ratio - true_f):
            unreflected.append((sd, true_f))
    out = []
    for d, i, c, a in raw:
        extra = 1.0
        for sd, tf in unreflected:
            if d < sd:
                extra *= tf  # cumulative across multiple missed splits
        f = (a / c) * extra  # auto-adjust: scale OHLC so close == (repaired) adjclose
        aa = a * extra
        out.append({
            "date": d,
            "open": float(quote["open"][i] * f) if quote["open"][i] is not None else float(aa),
            "high": float(quote["high"][i] * f) if quote["high"][i] is not None else float(aa),
            "low": float(quote["low"][i] * f) if quote["low"][i] is not None else float(aa),
            "close": float(aa),
            "volume": float(quote["volume"][i] or 0),
        })
    return out


def _yf_rows(symbol: str, **history_kwargs) -> list[dict]:
    """Fallback: the original yfinance path (needs fc.yahoo.com — fine locally)."""
    import yfinance as yf
    try:
        df = yf.Ticker(symbol).history(auto_adjust=True, **history_kwargs)
    except Exception:
        log.exception("yfinance fallback failed for %s", symbol)
        return []
    if df is None or df.empty:
        log.warning("No bars for %s", symbol)
        return []
    return [{"date": ts.date().isoformat(), "open": float(r["Open"]),
             "high": float(r["High"]), "low": float(r["Low"]),
             "close": float(r["Close"]), "volume": float(r["Volume"])}
            for ts, r in df.iterrows()]


def daily_bars(symbol: str, min_days: int) -> list[dict]:
    """The most recent daily bars (oldest->newest). [] on failure."""
    period = max(min_days + 10, 40)  # pad for weekends/holidays
    try:
        return _chart_rows(symbol, {"period1": _epoch_from_period(f"{period}d"),
                                    "period2": int(time.time())})
    except Exception as e:
        log.warning("chart fetch failed for %s (%s); trying yfinance", symbol, e)
        return _yf_rows(symbol, period=f"{period}d")


def daily_history(symbol: str, period: str = "2y") -> list[dict]:
    """Long daily history for backtesting (oldest->newest). [] on failure."""
    try:
        # NB not range=max: that silently downgrades bars to monthly despite interval=1d
        qs = {"period1": 0 if period == "max" else _epoch_from_period(period),
              "period2": int(time.time())}
        return _chart_rows(symbol, qs)
    except Exception as e:
        log.warning("chart fetch failed for %s (%s); trying yfinance", symbol, e)
        return _yf_rows(symbol, period=period)


def bars_after(symbol: str, start_date: str, n_days: int) -> list[dict]:
    """Up to `n_days` trading bars strictly AFTER start_date (for settlement)."""
    try:
        p1 = int(datetime.fromisoformat(start_date)
                 .replace(tzinfo=timezone.utc).timestamp())
        bars = _chart_rows(symbol, {"period1": p1, "period2": int(time.time())})
    except Exception as e:
        log.warning("chart fetch failed for %s (%s); trying yfinance", symbol, e)
        bars = _yf_rows(symbol, start=start_date)
    return [b for b in bars if b["date"] > start_date][:n_days]
