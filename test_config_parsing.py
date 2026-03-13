# test_config_parsing.py
import unittest
import os
import importlib.util
from typing import Any, Type

from config_parsing import parse_port, parse_bool, parse_csv


class TestParsePort(unittest.TestCase):
    def test_valid_ports(self):
        cases = [
            ("1", 1),
            (" 80 ", 80),
            ("\t443\n", 443),
            ("65535", 65535),
            ("00001", 1),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                got = parse_port(raw)
                self.assertEqual(got, expected)

    def test_invalid_ports(self):
        cases: list[tuple[Any, Type[Exception], str]] = [
            (None, TypeError, "must be str"),
            (123, TypeError, "must be str"),
            ("", ValueError, "empty or whitespace"),
            ("   ", ValueError, "empty or whitespace"),
            ("0", ValueError, "out of range"),
            ("65536", ValueError, "out of range"),
            ("-1", ValueError, "decimal integer"),
            ("80.0", ValueError, "decimal integer"),
            ("abc", ValueError, "decimal integer"),
            ("80 80", ValueError, "decimal integer"),
        ]
        for raw, expected_exc, msg_part in cases:
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(expected_exc, msg_part):
                    parse_port(raw)


class TestParseBool(unittest.TestCase):
    def test_valid_bools(self):
        cases = [
            ("true", True),
            (" TRUE ", True),
            ("1", True),
            ("yes", True),
            ("on", True),
            ("false", False),
            ("0", False),
            (" No ", False),
            ("off", False),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_bool(raw), expected)

    def test_invalid_bools(self):
        cases: list[tuple[Any, Type[Exception], str]] = [
            (None, TypeError, "must be str"),
            (42, TypeError, "must be str"),
            ("", ValueError, "invalid boolean literal"),
            ("   ", ValueError, "invalid boolean literal"),
            ("maybe", ValueError, "invalid boolean literal"),
            ("2", ValueError, "invalid boolean literal"),
            ("TRUE ", ValueError, "invalid boolean literal"),
        ]
        for raw, expected_exc, msg_part in cases:
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(expected_exc, msg_part):
                    parse_bool(raw)


class TestParseCsv(unittest.TestCase):
    def test_valid_csv(self):
        cases = [
            ("", []),
            ("   ", []),
            ("a", ["a"]),
            (" a ", ["a"]),
            ("a,b", ["a", "b"]),
            (" a , b ", ["a", "b"]),
            ("a,,b", ["a", "b"]),
            (",,a,,b,,", ["a", "b"]),
            ("one,two,three", ["one", "two", "three"]),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_csv(raw), expected)

    def test_invalid_csv(self):
        cases: list[tuple[Any, Type[Exception], str]] = [
            (None, TypeError, "must be str"),
            (123, TypeError, "must be str"),
            ([], TypeError, "must be str"),
        ]
        for raw, expected_exc, msg_part in cases:
            with self.subTest(raw=repr(raw)):
                with self.assertRaisesRegex(expected_exc, msg_part):
                    parse_csv(raw)


RUN_SLOW = os.environ.get("RUN_SLOW") == "1"


@unittest.skipUnless(RUN_SLOW, "set RUN_SLOW=1 to enable slow/extended tests")
class TestParsePortExtended(unittest.TestCase):
    def test_more_edge_cases(self):
        cases = [
            ("00080", 80),
            (" 00001 ", 1),
            ("99999", ValueError),
            ("65535", 65535),
            ("65536", ValueError),
            ("0", ValueError),
            ("-0", ValueError),
            (" 80 ", 80),
            (" 80", 80),
            ("80 ", 80),
            ("\n80\t", 80),
            ("", ValueError),
            ("    ", ValueError),
            ("1.0", ValueError),
            ("1e5", ValueError),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                if expected is ValueError:
                    with self.assertRaises(ValueError):
                        parse_port(raw)
                else:
                    self.assertEqual(parse_port(raw), expected)


yaml_spec = importlib.util.find_spec("yaml")


@unittest.skipUnless(yaml_spec is not None, "requires PyYAML: pip install pyyaml")
class TestYamlIntegration(unittest.TestCase):
    def test_parse_yaml_like_port(self):
        import yaml

        yaml_data = "port: 8080"
        data = yaml.safe_load(yaml_data)
        self.assertIn("port", data)
        self.assertIsInstance(data["port"], int)
        self.assertEqual(data["port"], 8080)

    def test_parse_yaml_like_bool(self):
        import yaml

        yaml_data = "debug: yes"
        data = yaml.safe_load(yaml_data)
        self.assertIn("debug", data)
        self.assertIsInstance(data["debug"], bool)
        self.assertTrue(data["debug"])