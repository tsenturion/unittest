"""
Табличные тесты для модуля config_parsing с использованием subTest()
и условных пропусков в зависимости от окружения.
"""
import importlib.util
import os
import unittest
from typing import List, Optional, Type, Union, Tuple

from config_parsing import parse_port, parse_bool, parse_csv


# Константа для управления медленными тестами
RUN_SLOW = os.environ.get("RUN_SLOW") == "1"


class TestParsePort(unittest.TestCase):
    """Тесты для функции parse_port."""

    def test_valid_ports(self):
        """Табличный тест для валидных значений портов."""
        cases = [
            # (входное_значение, ожидаемый_результат)
            ("1", 1),
            ("80", 80),
            (" 443 ", 443),
            ("\t8080\n", 8080),
            ("65535", 65535),
            (" 00001 ", 1),  # ведущие нули допустимы
            ("  22  ", 22),
        ]

        for raw, expected in cases:
            with self.subTest(raw=raw, expected=expected):
                result = parse_port(raw)
                self.assertEqual(
                    result, expected,
                    f"Для входа {raw!r} ожидалось {expected}, получено {result}"
                )

    def test_invalid_ports(self):
        """Табличный тест для невалидных значений портов."""
        cases: List[Tuple[Union[str, None], Type[Exception], str]] = [
            # (входное_значение, тип_исключения, часть_сообщения)
            (None, TypeError, "must be str"),
            (123, TypeError, "must be str"),  # type: ignore
            ("", ValueError, "empty"),
            ("   ", ValueError, "empty"),
            ("0", ValueError, "out of range"),
            ("65536", ValueError, "out of range"),
            ("-1", ValueError, "decimal integer"),
            ("80.5", ValueError, "decimal integer"),
            ("abc", ValueError, "decimal integer"),
            ("80 80", ValueError, "decimal integer"),
            ("99999", ValueError, "out of range"),
        ]

        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw, exc=exc_type.__name__):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_port(raw)  # type: ignore


class TestParseBool(unittest.TestCase):
    """Тесты для функции parse_bool."""

    def test_valid_bools(self):
        """Табличный тест для валидных булевых значений."""
        cases = [
            # (входное_значение, ожидаемый_результат)
            # True варианты
            ("true", True),
            (" TRUE ", True),
            ("1", True),
            ("yes", True),
            (" YES ", True),
            ("y", True),
            ("on", True),
            (" ON ", True),
            # False варианты
            ("false", False),
            (" FALSE ", False),
            ("0", False),
            ("no", False),
            (" NO ", False),
            ("n", False),
            ("off", False),
            (" OFF ", False),
        ]

        for raw, expected in cases:
            with self.subTest(raw=raw, expected=expected):
                result = parse_bool(raw)
                self.assertEqual(
                    result, expected,
                    f"Для входа {raw!r} ожидалось {expected}, получено {result}"
                )

    def test_invalid_bools(self):
        """Табличный тест для невалидных булевых значений."""
        cases = [
            # (входное_значение, тип_исключения, часть_сообщения)
            (None, TypeError, "must be str"),
            (42, TypeError, "must be str"),  # type: ignore
            ("", ValueError, "invalid boolean literal"),
            ("   ", ValueError, "invalid boolean literal"),
            ("maybe", ValueError, "invalid boolean literal"),
            ("2", ValueError, "invalid boolean literal"),
            ("truefalse", ValueError, "invalid boolean literal"),
            ("onoff", ValueError, "invalid boolean literal"),
        ]

        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw, exc=exc_type.__name__):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_bool(raw)  # type: ignore


class TestParseCsv(unittest.TestCase):
    """Тесты для функции parse_csv."""

    def test_valid_csv(self):
        """Табличный тест для валидных CSV строк."""
        cases = [
            # (входное_значение, ожидаемый_результат)
            ("", []),
            ("   ", []),
            ("a", ["a"]),
            ("a,b", ["a", "b"]),
            ("a, b", ["a", "b"]),
            ("a ,b", ["a", "b"]),
            (" a , b ", ["a", "b"]),
            ("a,b,c", ["a", "b", "c"]),
            ("a,,b", ["a", "b"]),  # пустой элемент отбрасывается
            ("a, ,b", ["a", "b"]),
            (" ,a, ", ["a"]),
            ("значение1,значение2,значение3", ["значение1", "значение2", "значение3"]),
            ("127.0.0.1, localhost,  ::1", ["127.0.0.1", "localhost", "::1"]),
        ]

        for raw, expected in cases:
            with self.subTest(raw=raw, expected=expected):
                result = parse_csv(raw)
                self.assertEqual(
                    result, expected,
                    f"Для входа {raw!r} ожидалось {expected}, получено {result}"
                )

    def test_invalid_csv(self):
        """Табличный тест для невалидных входных данных."""
        cases = [
            # (входное_значение, тип_исключения, часть_сообщения)
            (None, TypeError, "must be str"),
            (42, TypeError, "must be str"),  # type: ignore
            ([], TypeError, "must be str"),  # type: ignore
        ]

        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw, exc=exc_type.__name__):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_csv(raw)  # type: ignore


# ============================================================================
# РАСШИРЕННЫЕ ТЕСТЫ (УСЛОВНЫЙ SKIP)
# Запускаются только при установленной переменной окружения RUN_SLOW=1
# ============================================================================

@unittest.skipUnless(RUN_SLOW, "Медленные тесты: установите RUN_SLOW=1 для запуска")
class TestParsePortSlow(unittest.TestCase):
    """Расширенный набор тестов для parse_port (медленные/объемные)."""

    def test_port_edge_cases_extensive(self):
        """Обширный набор граничных случаев для портов."""
        cases = [
            # Валидные случаи
            ("1", 1),
            ("2", 2),
            ("65534", 65534),
            ("65535", 65535),
            (" 00080 ", 80),
            ("\t\n 443 \n\t", 443),
            (" 00001 ", 1),
            (" 00000 ", ValueError),  # вне диапазона
            (" 99999 ", ValueError),  # вне диапазона
            # Невалидные случаи
            ("-1", ValueError),
            ("-0", ValueError),
            ("+1", ValueError),
            ("0x80", ValueError),
            ("0b1010", ValueError),
            ("80.0", ValueError),
            ("80,0", ValueError),
            ("80 80", ValueError),
            ("80\n80", ValueError),
            ("пятьдесят", ValueError),
            ("", ValueError),
            ("   ", ValueError),
            ("65536", ValueError),
            ("100000", ValueError),
        ]

        for raw, expected in cases:
            with self.subTest(raw=raw, expected=expected):
                if expected is ValueError:
                    with self.assertRaisesRegex(ValueError, "(empty|decimal|range)"):
                        parse_port(raw)
                else:
                    self.assertEqual(parse_port(raw), expected)


@unittest.skipUnless(RUN_SLOW, "Медленные тесты: установите RUN_SLOW=1 для запуска")
class TestParseBoolSlow(unittest.TestCase):
    """Расширенный набор тестов для parse_bool (медленные/объемные)."""

    def test_bool_combinations_extensive(self):
        """Обширный набор комбинаций для булевых значений."""
        cases = [
            # Регистры и пробелы для true-значений
            ("true", True),
            ("TRUE", True),
            ("True", True),
            ("  true  ", True),
            ("\ttrue\n", True),
            ("tRuE", True),
            # Регистры и пробелы для false-значений
            ("false", False),
            ("FALSE", False),
            ("False", False),
            ("  false  ", False),
            ("\tfalse\n", False),
            ("fAlSe", False),
            # Различные представления
            ("1", True),
            ("0", False),
            ("yes", True),
            ("no", False),
            ("y", True),
            ("n", False),
            ("on", True),
            ("off", False),
            # Невалидные значения
            ("2", ValueError),
            ("-1", ValueError),
            ("", ValueError),
            ("   ", ValueError),
            ("truefalse", ValueError),
            ("maybe", ValueError),
            ("да", ValueError),
            ("нет", ValueError),
            ("oui", ValueError),
            ("non", ValueError),
        ]

        for raw, expected in cases:
            with self.subTest(raw=raw, expected=expected):
                if expected is ValueError:
                    with self.assertRaisesRegex(ValueError, "invalid boolean literal"):
                        parse_bool(raw)
                else:
                    self.assertEqual(parse_bool(raw), expected)


# ============================================================================
# ТЕСТЫ, ЗАВИСЯЩИЕ ОТ ОПЦИОНАЛЬНОЙ ЗАВИСИМОСТИ
# Запускаются только при наличии библиотеки PyYAML
# ============================================================================

# Проверяем доступность PyYAML
yaml_spec = importlib.util.find_spec("yaml")


@unittest.skipUnless(
    yaml_spec is not None,
    "Требуется PyYAML: установите с помощью 'pip install pyyaml'"
)
class TestYamlDependentParsing(unittest.TestCase):
    """
    Тесты, демонстрирующие зависимость от внешней библиотеки.
    В реальном проекте здесь могли бы быть тесты для функций,
    которые используют YAML для парсинга конфигурации.
    """

    def setUp(self):
        """Импортируем yaml только внутри тестов, если зависимость доступна."""
        import yaml
        self.yaml = yaml

    def test_yaml_boolean_parsing(self):
        """Демонстрационный тест: парсинг булевых значений из YAML."""
        # Этот тест показывает, как можно использовать YAML
        # для парсинга конфигурации с булевыми значениями
        test_cases = [
            ("bool: true", True),
            ("bool: false", False),
            ("bool: on", True),
            ("bool: off", False),
            ("bool: yes", True),
            ("bool: no", False),
        ]

        for yaml_str, expected in test_cases:
            with self.subTest(yaml=yaml_str.strip(), expected=expected):
                data = self.yaml.safe_load(yaml_str)
                self.assertEqual(data["bool"], expected)

    def test_yaml_port_parsing(self):
        """Демонстрационный тест: парсинг порта из YAML."""
        yaml_str = "port: 8080"
        data = self.yaml.safe_load(yaml_str)
        
        # Используем нашу функцию parse_port для валидации
        port = parse_port(str(data["port"]))
        self.assertEqual(port, 8080)

    def test_yaml_hosts_parsing(self):
        """Демонстрационный тест: парсинг списка хостов из YAML."""
        yaml_str = """
        hosts:
          - localhost
          - 127.0.0.1
          - ::1
        """
        data = self.yaml.safe_load(yaml_str)
        
        # Используем нашу функцию parse_csv для обработки
        for host in data["hosts"]:
            with self.subTest(host=host):
                # Проверяем, что хост не пустой после парсинга CSV
                parsed = parse_csv(host)
                self.assertTrue(parsed)
                self.assertEqual(parsed[0], host)


# ============================================================================
# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ С РАЗЛИЧНЫМИ ПОДХОДАМИ К ОРГАНИЗАЦИИ
# ============================================================================

class TestAdvancedScenarios(unittest.TestCase):
    """
    Тесты для сложных сценариев, демонстрирующие разные подходы
    к организации табличных тестов.
    """

    def test_port_with_environment_context(self):
        """
        Демонстрация фильтрации кейсов на основе окружения
        без использования skip внутри subTest.
        """
        cases = [
            {"name": "min_port", "raw": "1", "expected": 1},
            {"name": "max_port", "raw": "65535", "expected": 65535},
            {"name": "with_whitespace", "raw": "  8080  ", "expected": 8080},
        ]

        # Фильтруем кейсы в зависимости от ОС (пример)
        # В Windows могут быть особые требования к портам
        if os.name == 'nt':
            # Для Windows пропускаем некоторые кейсы
            cases = [c for c in cases if c["name"] != "max_port"]

        for case in cases:
            with self.subTest(case=case["name"], raw=case["raw"]):
                result = parse_port(case["raw"])
                self.assertEqual(result, case["expected"])

    def test_complex_validation_chain(self):
        """
        Тест, демонстрирующий цепочку валидаций.
        """
        test_data = [
            {
                "port": "8080",
                "debug": "true",
                "hosts": "localhost, 127.0.0.1",
                "expected": {
                    "port": 8080,
                    "debug": True,
                    "hosts": ["localhost", "127.0.0.1"]
                }
            },
            {
                "port": "443",
                "debug": "off",
                "hosts": "example.com,  ::1",
                "expected": {
                    "port": 443,
                    "debug": False,
                    "hosts": ["example.com", "::1"]
                }
            },
        ]

        for idx, data in enumerate(test_data):
            with self.subTest(test_case=idx, port=data["port"]):
                # Применяем все функции валидации
                port = parse_port(data["port"])
                debug = parse_bool(data["debug"])
                hosts = parse_csv(data["hosts"])

                self.assertEqual(port, data["expected"]["port"])
                self.assertEqual(debug, data["expected"]["debug"])
                self.assertEqual(hosts, data["expected"]["hosts"])


if __name__ == "__main__":
    unittest.main()