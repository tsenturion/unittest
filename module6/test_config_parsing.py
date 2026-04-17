import importlib.util
import os
import unittest

from config_parsing import parse_bool, parse_csv, parse_port


class TestParsePort(unittest.TestCase):
    def test_valid_ports(self):
        cases = [
            ("1", 1),
            (" 80 ", 80),
            ("\t443\n", 443),
            ("65535", 65535),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                got = parse_port(raw)
                self.assertEqual(got, expected)

    def test_invalid_ports(self):
        cases = [
            ("", ValueError, "empty"),
            ("   ", ValueError, "empty"),
            ("0", ValueError, "out of range"),
            ("65536", ValueError, "out of range"),
            ("-1", ValueError, "decimal integer"),
            ("80.0", ValueError, "decimal integer"),
            ("abc", ValueError, "decimal integer"),
            (None, TypeError, "must be str"),
        ]
        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw, exc=exc_type.__name__):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_port(raw)


class TestParseBool(unittest.TestCase):
    def test_valid_bools(self):
        cases = [
            ("true", True),
            (" TRUE ", True),
            ("1", True),
            ("yes", True),
            ("off", False),
            ("0", False),
            (" No ", False),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_bool(raw), expected)

    def test_invalid_bools(self):
        cases = [
            ("", ValueError, "invalid"),
            ("maybe", ValueError, "invalid"),
            ("2", ValueError, "invalid"),
            (123, TypeError, "must be str"),
        ]
        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_bool(raw)


class TestParseCSV(unittest.TestCase):
    def test_valid_csv(self):
        cases = [
            ("foo,bar,baz", ["foo", "bar", "baz"]),
            ("  foo , bar , , baz  ", ["foo", "bar", "baz"]),
            ("single", ["single"]),
            ("", []),
            ("   ", []),
            (",,,", []),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_csv(raw), expected)

    def test_invalid_type_csv(self):
        with self.assertRaisesRegex(TypeError, "must be str"):
            parse_csv(42)


RUN_SLOW = os.environ.get("RUN_SLOW") == "1"


@unittest.skipUnless(RUN_SLOW, "set RUN_SLOW=1 to enable slow parsing tests")
class TestParsePortSlow(unittest.TestCase):
    def test_more_edge_cases(self):
        cases = [
            ("00080", 80),
            (" 00001 ", 1),
            ("99999", ValueError),
            ("65535", 65535),
            ("1", 1),
            ("   8080   ", 8080),
            ("\n123\n", 123),
            ("0x1A", ValueError),
            ("1.0", ValueError),
            ("1e2", ValueError),
            ("", ValueError),
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
class TestYamlParsing(unittest.TestCase):
    def test_parse_yaml_config(self):
        import yaml

        data = yaml.safe_load("port: 80\ndebug: true\n")
        self.assertEqual(data["port"], 80)
        self.assertTrue(data["debug"])


if __name__ == "__main__":
    unittest.main()