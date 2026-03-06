from __future__ import annotations
import re
_TRUE = {"1", "true", "yes", "y", "on"}
_FALSE = {"0", "false", "no", "n", "off"}
def parse_port(value: str) -> int:
    """Parse TCP port from string.

    Accepts decimal ASCII digits, with surrounding whitespace.
    Range: 1..65535 inclusive.

    Raises:
        TypeError: if value is not str
        ValueError: if empty / not a decimal integer / out of range
    """
    if not isinstance(value, str):
        raise TypeError("port value must be str")

    raw = value.strip()
    if raw == "":
        raise ValueError("port is empty")

    if not re.fullmatch(r"[0-9]+", raw):
        raise ValueError(f"port is not a decimal integer: {value!r}")

    port = int(raw)
    if not (1 <= port <= 65535):
        raise ValueError("port out of range: 1..65535")

    return port


def parse_bool(value: str) -> bool:
    """Parse boolean from string.

    True: 1/true/yes/y/on
    False: 0/false/no/n/off
    Case-insensitive, ignores surrounding whitespace.
    """
    if not isinstance(value, str):
        raise TypeError("bool value must be str")

    token = value.strip().lower()
    if token in _TRUE:
        return True
    if token in _FALSE:
        return False
    raise ValueError(f"invalid boolean literal: {value!r}")


def parse_csv(value: str) -> list[str]:
    """Parse a comma-separated string into a list of stripped, non-empty strings."""
    if not isinstance(value, str):
        raise TypeError("csv value must be str")

    parts = [part.strip() for part in value.split(',')]
    result = [p for p in parts if p != '']
    return result