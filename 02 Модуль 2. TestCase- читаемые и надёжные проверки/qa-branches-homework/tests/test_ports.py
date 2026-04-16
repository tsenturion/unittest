import unittest
from netutils.ports import parse_port

class TestParsePort(unittest.TestCase):

    # ---------- Успешные случаи ----------
    def test_valid_ints(self):
        cases = [1, 65535, 8080, 22, 443]
        for port in cases:
            with self.subTest(port=port):
                self.assertEqual(parse_port(port), port)

    def test_valid_str_digits(self):
        cases = ["1", "65535", "8080", "22", "443"]
        for port_str in cases:
            with self.subTest(port_str=port_str):
                self.assertEqual(parse_port(port_str), int(port_str))

    def test_valid_str_with_whitespace(self):
        cases = [" 8080 ", "\t443\n", "  22  "]
        for port_str in cases:
            with self.subTest(port_str=port_str):
                self.assertEqual(parse_port(port_str), int(port_str.strip()))

    # ---------- Границы для int ----------
    def test_int_boundaries(self):
        # границы внутри
        self.assertEqual(parse_port(1), 1)
        self.assertEqual(parse_port(65535), 65535)
        # рядом внутри
        self.assertEqual(parse_port(2), 2)
        self.assertEqual(parse_port(65534), 65534)

    def test_int_out_of_range_raises(self):
        for port in (0, -1, 65536, 100000):
            with self.subTest(port=port):
                with self.assertRaises(ValueError):
                    parse_port(port)

    # ---------- Границы для строк ----------
    def test_str_boundaries_valid(self):
        self.assertEqual(parse_port("1"), 1)
        self.assertEqual(parse_port("65535"), 65535)

    def test_str_out_of_range_raises(self):
        for port_str in ("0", "-1", "65536", "100000"):
            with self.subTest(port_str=port_str):
                with self.assertRaises(ValueError):
                    parse_port(port_str)

    # ---------- Неверные строки ----------
    def test_str_non_digit_raises(self):
        cases = ["", "   ", "abc", "12a", "a12", "12.3", "+123", "-123"]
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    parse_port(case)

    # ---------- Неверные типы ----------
    def test_wrong_types_raise_type_error(self):
        cases = [None, [], {}, 3.14, True, False]
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(TypeError):
                    parse_port(case)

if __name__ == "__main__":
    unittest.main(verbosity=2)