import json


def load_config(path: str) -> dict:
    """Load JSON configuration from file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)