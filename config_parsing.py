# config_parsing.py
from __future__ import annotations
import re

_TRUE = {"1", "true", "yes", "y", "on"}
_FALSE = {"0", "false", "no", "n", "off"}


def parse_port(value: str) -> int:
    if not isinstance(value, str):
        raise TypeError("port value must be str")

    raw = value.strip()
    if not raw:
        raise ValueError("port value is empty or whitespace only")

    if not raw.isdigit():
        raise ValueError(f"port value is not a decimal integer: {value!r}")

    port = int(raw)
    if not (1 <= port <= 65535):
        raise ValueError("port out of range (1..65535)")

    return port


def parse_bool(value: str) -> bool:
    if not isinstance(value, str):
        raise TypeError("bool value must be str")

    token = value.strip().lower()
    if token in _TRUE:
        return True
    if token in _FALSE:
        return False
    raise ValueError(f"invalid boolean literal: {value!r}")


def parse_csv(value: str) -> list[str]:
    if not isinstance(value, str):
        raise TypeError("csv value must be str")

    if not value.strip():
        return []

    parts = [part.strip() for part in value.split(",")]
    return [part for part in parts if part]