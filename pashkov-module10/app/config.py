import json
 #

def load_config(path: str) -> dict:
    """Читает JSON-конфиг из файла"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)