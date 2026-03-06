# test_config_parsing.py
import importlib.util
import os
import unittest
from typing import Any

from config_parsing import parse_port, parse_bool, parse_csv

class TestParsePort(unittest.TestCase):
    """Тесты для функции parse_port."""

    def test_valid_ports(self):
        """Табличный тест для валидных значений port."""
        cases = [
            ("1", 1),
            (" 80 ", 80),
            ("\t443\n", 443),
            ("65535", 65535),
            ("00001", 1),  
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_port(raw), expected)

    def test_invalid_ports(self):
        """Табличный тест для невалидных значений port."""
        cases: list[tuple[Any, type[Exception], str]] = [
            ("", ValueError, "empty"),
            ("   ", ValueError, "empty"),
            ("0", ValueError, "out of range"),
            ("65536", ValueError, "out of range"),
            ("-1", ValueError, "decimal integer"),
            ("80.0", ValueError, "decimal integer"),
            ("abc", ValueError, "decimal integer"),
            (None, TypeError, "must be str"),
            (123, TypeError, "must be str"),  
        ]
        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw, exc=exc_type.__name__):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_port(raw)  # type: ignore[arg-type]

class TestParseBool(unittest.TestCase):
    """Тесты для функции parse_bool."""

    def test_valid_bools(self):
        """Табличный тест для валидных значений bool."""
        cases = [
            ("true", True),
            (" TRUE ", True),
            ("1", True),
            ("yes", True),
            ("y", True),
            ("on", True),
            ("false", False),
            ("FALSE", False),
            ("0", False),
            ("no", False),
            ("n", False),
            ("off", False),
            ("  off  ", False),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_bool(raw), expected)

    def test_invalid_bools(self):
        """Табличный тест для невалидных значений bool."""
        cases: list[tuple[Any, type[Exception], str]] = [
            ("", ValueError, "invalid"),
            ("   ", ValueError, "invalid"),
            ("maybe", ValueError, "invalid"),
            ("2", ValueError, "invalid"),
            (None, TypeError, "must be str"),
            (123, TypeError, "must be str"),
        ]
        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_bool(raw)  


class TestParseCsv(unittest.TestCase):
    """Тесты для функции parse_csv."""

    def test_valid_csv(self):
        """Табличный тест для валидных CSV-строк."""
        cases = [
            ("a,b,c", ["a", "b", "c"]),
            ("  a  ,  b  ,  c  ", ["a", "b", "c"]),
            ("a, b, c", ["a", "b", "c"]),
            ("a,,b", ["a", "b"]),  
            ("a,b,", ["a", "b"]),  
            (",,a,,b,,", ["a", "b"]),  
            ("", []),  
            ("   ", []),  
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_csv(raw), expected)

    def test_invalid_csv(self):
        """Табличный тест для невалидных входных данных CSV (не строки)."""
        cases: list[tuple[Any, type[Exception], str]] = [
            (None, TypeError, "must be str"),
            (123, TypeError, "must be str"),
            ([], TypeError, "must be str"),
        ]
        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_csv(raw)  

RUN_SLOW = os.environ.get("RUN_SLOW") == "1"


@unittest.skipUnless(RUN_SLOW, "set RUN_SLOW=1 to enable slow/edge case parsing tests")
class TestParsePortSlow(unittest.TestCase):
    """Расширенный набор тестов для parse_port, запускаемый только по запросу."""

    def test_more_edge_cases(self):
        """Табличный тест с большим количеством граничных случаев."""
        valid_cases = [
            ("00080", 80),
            (" 00001 ", 1),
            ("65535", 65535),
        ]
        for raw, expected in valid_cases:
            with self.subTest(raw=raw, category="valid"):
                self.assertEqual(parse_port(raw), expected)

        invalid_cases = [
            ("99999", ValueError),  
            ("65536", ValueError),
            ("-0", ValueError),  
            ("+80", ValueError),  
        ]
        for raw, expected_exc in invalid_cases:
            with self.subTest(raw=raw, category="invalid"):
                with self.assertRaises(expected_exc):
                    parse_port(raw)

yaml_spec = importlib.util.find_spec("yaml")


@unittest.skipUnless(yaml_spec is not None, "requires PyYAML: pip install pyyaml")
class TestYamlDependentFeature(unittest.TestCase):
    """Пример тестов, которые зависят от наличия опциональной зависимости."""

    def test_yaml_parsing_logic(self):
        """Простой тест, использующий PyYAML."""
        import yaml

        data = yaml.safe_load("port: 80\n")
        self.assertEqual(data["port"], 80)

    def test_yaml_bool_parsing(self):
        """Еще один тест с PyYAML."""
        import yaml

        data = yaml.safe_load("debug: on\nverbose: false")
        self.assertTrue(data["debug"])
        self.assertFalse(data["verbose"])


class TestWithConditionalSetup(unittest.TestCase):
    """Демонстрация пропуска в setUp."""

    def setUp(self):
        if not RUN_SLOW:  
            self.skipTest("Skipping in setUp because RUN_SLOW is not set")
        self.resource_initialized = True

    def test_using_resource(self):
        """Тест, который выполняется только если setUp не вызвал skipTest."""
        self.assertTrue(self.resource_initialized)
