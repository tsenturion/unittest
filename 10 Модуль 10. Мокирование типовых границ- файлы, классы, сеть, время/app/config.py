import json

def load_config(path: str) -> dict:
    """Загружает JSON-конфигурацию из файла."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    