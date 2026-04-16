
from __future__ import annotations

import argparse
import fnmatch
import sys
import unittest
from typing import Iterable, List

def _iter_cases(suite: unittest.TestSuite) -> Iterable[unittest.TestCase]:
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _iter_cases(item)
        else:
            yield item

def _match_k(test_id: str, patterns: List[str]) -> bool:
    for p in patterns:
        if "*" in p:
            if fnmatch.fnmatchcase(test_id, p):
                return True
        else:
            if p in test_id:
                return True
    return False

def build_suite(start: str, pattern: str, top: str, k: List[str]) -> unittest.TestSuite:
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=start, pattern=pattern, top_level_dir=top)

    if not k:
        return suite

    filtered = unittest.TestSuite()
    for case in _iter_cases(suite):
        if _match_k(case.id(), k):
            filtered.addTest(case)
    return filtered

def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project test runner (unittest discovery wrapper)")
    parser.add_argument("-s", "--start", default="tests/unit", help="Start directory for discovery")
    parser.add_argument("-p", "--pattern", default="*_spec.py", help="File pattern for tests (glob)")
    parser.add_argument("-t", "--top", default=".", help="Top-level project directory")
    parser.add_argument("-k", action="append", default=[], help="Filter by substring or fnmatch pattern")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (-v, -vv)")
    parser.add_argument("-f", "--failfast", action="store_true", help="Stop on first fail/error")
    parser.add_argument("-b", "--buffer", action="store_true", help="Buffer stdout/stderr during tests")

    args = parser.parse_args(argv)

    suite = build_suite(start=args.start, pattern=args.pattern, top=args.top, k=args.k)

    verbosity = 1 + args.verbose
    runner = unittest.TextTestRunner(verbosity=verbosity, failfast=args.failfast, buffer=args.buffer)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(main())