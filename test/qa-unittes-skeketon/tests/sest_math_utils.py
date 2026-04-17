# tests/test_math_utils.py
import unittest

from qautils.math_utils import add


def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    unittest.main()