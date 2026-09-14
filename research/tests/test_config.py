"""config.py must import WITHOUT python-dotenv (2026-08-07, 2026-09-11 cold-container strands)."""
import importlib
import sys


def test_config_imports_without_dotenv(monkeypatch):
    # sys.modules[name] = None makes `import name` raise ImportError — the cold-container case.
    monkeypatch.setitem(sys.modules, "dotenv", None)
    monkeypatch.delitem(sys.modules, "research.config", raising=False)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    cfg = importlib.import_module("research.config")
    assert cfg.load_dotenv.__module__ == "research.config"   # the stand-in, not the package
    assert cfg.load_dotenv() is False
    assert cfg.os.environ["TELEGRAM_BOT_TOKEN"] == "t"   # env still IS the config


def test_notify_imports_without_dotenv(monkeypatch):
    monkeypatch.setitem(sys.modules, "dotenv", None)
    for m in ("research.config", "research.notify"):
        monkeypatch.delitem(sys.modules, m, raising=False)
    notify = importlib.import_module("research.notify")
    assert callable(notify.send)
