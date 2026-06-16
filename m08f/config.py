import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "m08f" / "config.json"
DEFAULTS = {"baud": 115200, "dpi": 203, "width_dots": 1664, "device": "/dev/ttyACM0"}

def load() -> dict:
    if not CONFIG_PATH.exists():
        return dict(DEFAULTS)
    with open(CONFIG_PATH) as f:
        data = json.load(f)
    merged = dict(DEFAULTS)
    merged.update(data)
    return merged

def save(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged = dict(DEFAULTS)
    merged.update(data)
    with open(CONFIG_PATH, "w") as f:
        json.dump(merged, f, indent=2)
