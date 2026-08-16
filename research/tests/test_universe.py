"""Guard the no-egress cache fallback: if the live constituents fetch is blocked (cloud
allowlist gap), sp500() must serve the last-good cache instead of [] — the mover-scan
denominator depends on it. Also check the live path writes that cache + normalizes tickers."""
from research import universe as U


class _Resp:
    def __init__(self, text): self.text = text
    def raise_for_status(self): pass


_CSV = "Symbol,Security\nAAPL,Apple\nBRK.B,Berkshire\nMSFT,Microsoft\n"


def test_live_fetch_normalizes_and_writes_cache(tmp_path, monkeypatch):
    cache = tmp_path / "sp500_current.csv"
    monkeypatch.setattr(U, "_CACHE", str(cache))
    monkeypatch.setattr(U.requests, "get", lambda *a, **k: _Resp(_CSV))
    syms = U.sp500()
    assert syms == ["AAPL", "BRK-B", "MSFT"]   # BRK.B -> BRK-B (yfinance format)
    assert cache.exists()                       # cache written for the no-egress path


def test_blocked_fetch_falls_back_to_cache(tmp_path, monkeypatch):
    cache = tmp_path / "sp500_current.csv"
    monkeypatch.setattr(U, "_CACHE", str(cache))
    monkeypatch.setattr(U.requests, "get", lambda *a, **k: _Resp(_CSV))
    U.sp500()                                   # seed the cache via a good fetch

    def _blocked(*a, **k): raise RuntimeError("403 egress blocked")
    monkeypatch.setattr(U.requests, "get", _blocked)
    assert U.sp500() == ["AAPL", "BRK-B", "MSFT"]  # served from cache, not []


def test_blocked_fetch_no_cache_returns_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(U, "_CACHE", str(tmp_path / "missing.csv"))

    def _blocked(*a, **k): raise RuntimeError("403 egress blocked")
    monkeypatch.setattr(U.requests, "get", _blocked)
    assert U.sp500() == []                       # both fail -> [] (unchanged terminal behavior)


def _write(path, syms):
    path.write_text("Symbol\n" + "\n".join(syms) + "\n")


def test_tail_concatenates_committed_caches(tmp_path, monkeypatch):
    c4, c6 = tmp_path / "sp400.csv", tmp_path / "sp600.csv"
    _write(c4, ["MIDA", "MIDB"])
    _write(c6, ["SMLA"])
    monkeypatch.setattr(U, "_CACHE_400", str(c4))
    monkeypatch.setattr(U, "_CACHE_600", str(c6))
    assert U.sp400() == ["MIDA", "MIDB"]
    assert U.sp600() == ["SMLA"]
    assert U.tail() == ["MIDA", "MIDB", "SMLA"]


def test_tail_missing_cache_is_empty_not_error(tmp_path, monkeypatch):
    monkeypatch.setattr(U, "_CACHE_400", str(tmp_path / "missing400.csv"))
    monkeypatch.setattr(U, "_CACHE_600", str(tmp_path / "missing600.csv"))
    assert U.tail() == []                        # a missing cache degrades, never raises


def test_sp500_cached_never_fetches(tmp_path, monkeypatch):
    cache = tmp_path / "sp500_current.csv"
    _write(cache, ["AAPL"])
    monkeypatch.setattr(U, "_CACHE", str(cache))

    def _boom(*a, **k): raise AssertionError("sp500_cached must not touch the network")
    monkeypatch.setattr(U.requests, "get", _boom)
    assert U.sp500_cached() == ["AAPL"]
