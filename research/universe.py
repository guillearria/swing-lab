"""Broad symbol universes for less-biased backtesting.

S&P 500 current constituents (free CSV). NOTE: 'current' members are still a mild
survivorship filter — dropped/delisted names are gone. But it removes OUR
hand-picking bias, which is the big one. Truly point-in-time history is deferred
(not free).

The S&P 400/600 TAIL caches [ARC 5 #11] are committed, read-only on the live path —
no free machine-readable source exists, so a one-off local build (Reproduce line in
FINDINGS 2026-08-04 [ARC 5 #11]) refreshes them. A stale cache surfaces as a fetch-
coverage DO-NOW in the digest, which is the rebuild trigger.
"""

import csv
import io
import logging
import os

import requests

log = logging.getLogger(__name__)

_SP500_CSV = ("https://raw.githubusercontent.com/datasets/"
              "s-and-p-500-companies/main/data/constituents.csv")
_CACHE = "research/data/sp500_current.csv"  # no-egress fallback (cloud allowlist gap)
_CACHE_400 = "research/data/sp400_current.csv"
_CACHE_600 = "research/data/sp600_current.csv"


def sp500() -> list[str]:
    """Current S&P 500 tickers, yfinance-formatted. Cache fallback if egress is blocked; [] only if both fail."""
    try:
        r = requests.get(_SP500_CSV, headers={"User-Agent": "claude_trader"}, timeout=20)
        r.raise_for_status()
        reader = csv.DictReader(io.StringIO(r.text))
        syms = [row["Symbol"].strip().replace(".", "-")  # BRK.B -> BRK-B
                for row in reader if row.get("Symbol")]
        if syms:
            _write_cache(syms)
        return syms
    except Exception:
        log.exception("sp500 fetch failed — trying cache %s", _CACHE)
        return _read_cache()


def sp500_cached() -> list[str]:
    """S&P 500 from the committed cache ONLY — for callers documented as no-network (engine)."""
    return _read_cache()


def sp400() -> list[str]:
    return _read_cache(_CACHE_400)


def sp600() -> list[str]:
    return _read_cache(_CACHE_600)


def tail() -> list[str]:
    """The mid+small TAIL cohort [ARC 5 #11]: S&P 400 + 600, committed caches only."""
    return sp400() + sp600()


def _write_cache(syms: list[str], path: str | None = None) -> None:
    with open(path or _CACHE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Symbol"])
        w.writerows([s] for s in syms)


def _read_cache(path: str | None = None) -> list[str]:
    # Path resolves at CALL time (feedstatus lesson): tests monkeypatch the module constants.
    path = path or _CACHE
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return [row["Symbol"].strip() for row in csv.DictReader(f) if row.get("Symbol")]
