import unittest
from netutils.ports import parse_port


class TestParsePort(unittest.TestCase):
    """Спецификация функции parse_port через тесты."""

    # --- Тесты на TypeError (неверные типы) ---

    def test_raises_type_error_on_bool(self):
        """bool недопустим даже как подкласс int."""
        with self.assertRaises(TypeError):
            parse_port(True)
        with self.assertRaises(TypeError):
            parse_port(False)

    def test_raises_type_error_on_invalid_types(self):
        """None, float, list, dict и другие типы вызывают TypeError."""
        invalid_types = [None, 3.14, [], {}, "123", object()]
        # "123" — строка, но мы её проверяем отдельно, здесь просто для полноты
        # Лучше явно указать только нестроковые/неint типы
        for value in [None, 3.14, [], {}, lambda x: x]:
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    parse_port(value)

    # --- Тесты на int с границами диапазона ---

    def test_returns_valid_int_port(self):
        """Целые числа в диапазоне 1..65535 возвращаются как есть."""
        valid_ports = [1, 2, 65534, 65535]
        for port in valid_ports:
            with self.subTest(port=port):
                self.assertEqual(parse_port(port), port)

    def test_raises_value_error_on_int_out_of_range(self):
        """int вне диапазона 1..65535 → ValueError."""
        invalid_ports = [0, -1, 65536, 100000]
        for port in invalid_ports:
            with self.subTest(port=port):
                with self.assertRaises(ValueError):
                    parse_port(port)

    # --- Тесты на str (границы, пустые значения, неверный формат) ---

    def test_parses_valid_string_ports(self):
        """Строки с цифрами и пробелами по краям конвертируются в int порт."""
        test_cases = [
            ("1", 1),
            ("  8080  ", 8080),
            ("65535", 65535),
            ("   22", 22),
            ("443   ", 443),
        ]
        for value, expected in test_cases:
            with self.subTest(value=value):
                self.assertEqual(parse_port(value), expected)

    def test_raises_value_error_on_empty_or_whitespace_string(self):
        """Пустая строка или строка из пробелов → ValueError."""
        empty_strings = ["", "   ", "\t", "\n   \n"]
        for value in empty_strings:
            with self.subTest(value=repr(value)):
                with self.assertRaises(ValueError):
                    parse_port(value)

    def test_raises_value_error_on_string_with_non_digits(self):
        """Строка с буквами, знаками, точками → ValueError."""
        invalid_strings = ["abc", "12a3", "  -80", "+443", "12.34", "0x80"]
        for value in invalid_strings:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_port(value)

    def test_raises_value_error_on_string_port_out_of_range(self):
        """Число в строке вне 1..65535 → ValueError."""
        out_of_range_strings = ["0", "65536", "100000", "  0  ", "  65536  "]
        for value in out_of_range_strings:
            with self.subTest(value=repr(value)):
                with self.assertRaises(ValueError):
                    parse_port(value)

    # --- Дополнительно: проверка границ через BVA (явный тест) ---

    def test_boundary_values_int(self):
        """Анализ граничных значений для int: min, max, min-1, max+1."""
        boundaries = {
            1: True,    # min
            2: True,    # min+1
            65535: True, # max
            65534: True, # max-1
            0: False,   # min-1 → ValueError
            65536: False # max+1 → ValueError
        }
        for port, should_pass in boundaries.items():
            with self.subTest(port=port, should_pass=should_pass):
                if should_pass:
                    self.assertEqual(parse_port(port), port)
                else:
                    with self.assertRaises(ValueError):
                        parse_port(port)

    def test_boundary_values_str(self):
        """Граничные значения для строк: вокруг 1 и 65535."""
        test_cases = [
            ("1", 1, True),
            ("2", 2, True),
            ("65535", 65535, True),
            ("65534", 65534, True),
            ("0", None, False),
            ("65536", None, False),
            ("  0  ", None, False),
            ("  65536  ", None, False),
        ]
        for value, expected, should_pass in test_cases:
            with self.subTest(value=repr(value)):
                if should_pass:
                    self.assertEqual(parse_port(value), expected)
                else:
                    with self.assertRaises(ValueError):
                        parse_port(value)


if __name__ == "__main__":
    unittest.main(verbosity=2)