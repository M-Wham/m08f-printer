import json
from pathlib import Path
from m08f import config

def test_save_then_load_roundtrip(tmp_path, monkeypatch):
    cfg_path = tmp_path / "config.json"
    monkeypatch.setattr(config, "CONFIG_PATH", cfg_path)
    config.save({"baud": 115200, "dpi": 203, "width_dots": 1664})
    loaded = config.load()
    assert loaded["baud"] == 115200
    assert loaded["dpi"] == 203
    assert loaded["width_dots"] == 1664

def test_load_missing_returns_defaults(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CONFIG_PATH", tmp_path / "nope.json")
    loaded = config.load()
    assert loaded == config.DEFAULTS
