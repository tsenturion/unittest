"""Unit tests for parse_port function with full branch coverage."""

import unittest
from netutils.ports import parse_port


class TestParsePort(unittest.TestCase):
    """Test suite for parse_port() - validates port numbers from various inputs."""
    
    # ========== ТЕСТЫ НА ТИПЫ (TypeError ветви) ==========
    
    def test_raises_type_error_on_invalid_types(self):
        """Проверка: неподдерживаемые типы вызывают TypeError."""
        invalid_types = [
            (None, "None type"),
            ([], "list"),
            ({}, "dict"),
            (3.14, "float"),
            (True, "bool - подкласс int, но должен считаться неверным"),
            (False, "bool - подкласс int, но должен считаться неверным"),
        ]
        
        for value, description in invalid_types:
            with self.subTest(value=value, description=description):
                with self.assertRaises(TypeError):
                    parse_port(value)
    
    # ========== ТЕСТЫ НА INT (ветви валидации int) ==========
    
    def test_accepts_valid_int_ports(self):
        """Валидные int значения в диапазоне 1..65535 проходят проверку."""
        valid_ports = [1, 65535, 8080, 22, 443, 1024]
        
        for port in valid_ports:
            with self.subTest(port=port):
                result = parse_port(port)
                self.assertEqual(result, port)
    
    def test_raises_value_error_on_int_out_of_range(self):
        """int вне диапазона 1..65535 вызывает ValueError."""
        invalid_ports = [0, -1, 65536, 100000, -100]
        
        for port in invalid_ports:
            with self.subTest(port=port):
                with self.assertRaises(ValueError):
                    parse_port(port)
    
    def test_int_boundary_values_validation(self):
        """Граничные значения: min-1, min, min+1, max-1, max, max+1."""
        test_cases = [
            # (порт, ожидаемое_исключение)
            (0, ValueError),      # min - 1
            (1, None),            # min
            (2, None),            # min + 1
            (65534, None),        # max - 1
            (65535, None),        # max
            (65536, ValueError),  # max + 1
        ]
        
        for port, expected_exception in test_cases:
            with self.subTest(port=port):
                if expected_exception:
                    with self.assertRaises(expected_exception):
                        parse_port(port)
                else:
                    result = parse_port(port)
                    self.assertEqual(result, port)
    
    # ========== ТЕСТЫ НА STR (ветви валидации строк) ==========
    
    def test_accepts_valid_string_ports(self):
        """Валидные строки с цифрами преобразуются в int порт."""
        valid_strings = [
            ("1", 1),
            ("65535", 65535),
            ("8080", 8080),
            ("22", 22),
            ("443", 443),
            ("1024", 1024),
            ("  8080  ", 8080),   # с пробелами по краям
            ("\t443\n", 443),      # с табуляцией и переносом
        ]
        
        for value, expected in valid_strings:
            with self.subTest(value=value):
                result = parse_port(value)
                self.assertEqual(result, expected)
    
    def test_raises_value_error_on_empty_or_whitespace_strings(self):
        """Пустые строки или строки из пробелов после strip() вызывают ValueError."""
        empty_values = ["", "   ", "\t", "\n", " \t\n "]
        
        for value in empty_values:
            with self.subTest(value=repr(value)):
                with self.assertRaises(ValueError):
                    parse_port(value)
    
    def test_raises_value_error_on_non_digit_strings(self):
        """Строки с нецифровыми символами вызывают ValueError."""
        non_digit_strings = [
            "abc",
            "12abc34",
            "port:8080",
            "12.34",
            "-5",
            "+5",
            "0x1F40",  # hex
            "12 34",
            "1,234",
        ]
        
        for value in non_digit_strings:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_port(value)
    
    def test_string_boundary_values_validation(self):
        """Граничные значения для строковых представлений портов."""
        test_cases = [
            ("0", ValueError),        # min - 1
            ("1", None),              # min
            ("2", None),              # min + 1
            ("65534", None),          # max - 1
            ("65535", None),          # max
            ("65536", ValueError),    # max + 1
            ("  1  ", None),          # min с пробелами
            ("  65535  ", None),      # max с пробелами
        ]
        
        for value, expected_exception in test_cases:
            with self.subTest(value=repr(value)):
                if expected_exception:
                    with self.assertRaises(expected_exception):
                        parse_port(value)
                else:
                    result = parse_port(value)
                    self.assertEqual(result, int(value.strip()))
    
    def test_string_leading_zeros_are_accepted(self):
        """Строки с ведущими нулями валидны (преобразуются в int корректно)."""
        test_cases = [
            ("01", 1),
            ("008080", 8080),
            ("00065535", 65535),
        ]
        
        for value, expected in test_cases:
            with self.subTest(value=value):
                result = parse_port(value)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
