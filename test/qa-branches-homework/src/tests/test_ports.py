import unittest
from netutils.ports import parse_port


class TestParsePortInt(unittest.TestCase):
    def test_int_valid_min_boundary(self):
        self.assertEqual(parse_port(1), 1)
    
    def test_int_valid_max_boundary(self):
        self.assertEqual(parse_port(65535), 65535)
    
    def test_int_valid_middle(self):
        self.assertEqual(parse_port(8080), 8080)
        self.assertEqual(parse_port(22), 22)
        self.assertEqual(parse_port(443), 443)
    
    def test_int_invalid_below_min(self):
        with self.assertRaises(ValueError) as context:
            parse_port(0)
        self.assertIn("out of range", str(context.exception))
    
    def test_int_invalid_negative(self):
        with self.assertRaises(ValueError):
            parse_port(-1)
    
    def test_int_invalid_above_max(self):
        with self.assertRaises(ValueError):
            parse_port(65536)
    
    def test_int_invalid_large_number(self):
        with self.assertRaises(ValueError):
            parse_port(100000)


class TestParsePortStr(unittest.TestCase):

    def test_str_valid_min_boundary(self):
        self.assertEqual(parse_port("1"), 1)
    
    def test_str_valid_max_boundary(self):
        self.assertEqual(parse_port("65535"), 65535)
    
    def test_str_valid_middle(self):
        self.assertEqual(parse_port("3000"), 3000)
        self.assertEqual(parse_port("8080"), 8080)
    
    def test_str_valid_with_whitespace(self):
        self.assertEqual(parse_port("  80  "), 80)
        self.assertEqual(parse_port("\t443\n"), 443)
        self.assertEqual(parse_port("  22  "), 22)
    
    def test_str_invalid_empty_string(self):
        with self.assertRaises(ValueError):
            parse_port("")
    
    def test_str_invalid_only_spaces(self):
        """Строка только из пробелов."""
        with self.assertRaises(ValueError):
            parse_port("   ")
    
    def test_str_invalid_tabs_only(self):
        """Строка только из табуляций."""
        with self.assertRaises(ValueError):
            parse_port("\t\t")
    
    def test_str_invalid_mixed_whitespace(self):
        """Строка только из разных пробельных символов."""
        with self.assertRaises(ValueError):
            parse_port(" \t\n ")
    
    # НЕВАЛИДНЫЕ значения: символы
    def test_str_invalid_contains_plus(self):
        with self.assertRaises(ValueError):
            parse_port("+8080")
    
    def test_str_invalid_contains_minus(self):
        with self.assertRaises(ValueError):
            parse_port("-80")
    
    def test_str_invalid_contains_letters(self):
        with self.assertRaises(ValueError):
            parse_port("80abc")
    
    def test_str_invalid_contains_special_chars(self):
        with self.assertRaises(ValueError):
            parse_port("80@#$")
    
    def test_str_invalid_decimal_point(self):
        with self.assertRaises(ValueError):
            parse_port("80.5")
    
    def test_str_invalid_leading_zeros_valid(self):
       self.assertEqual(parse_port("0080"), 80)
    
    def test_str_invalid_below_min(self):
        with self.assertRaises(ValueError):
            parse_port("0")
    
    def test_str_invalid_above_max(self):
        with self.assertRaises(ValueError):
            parse_port("65536")
    
    def test_str_invalid_negative_number(self):
        with self.assertRaises(ValueError):
            parse_port("-100")


class TestParsePortInvalidType(unittest.TestCase):
    
    def test_type_bool_true(self):
        with self.assertRaises(TypeError):
            parse_port(True)
    
    def test_type_bool_false(self):
        with self.assertRaises(TypeError):
            parse_port(False)
    
    def test_type_none(self):
        with self.assertRaises(TypeError):
            parse_port(None)
    
    def test_type_list(self):
        with self.assertRaises(TypeError):
            parse_port([])
    
    def test_type_dict(self):
        with self.assertRaises(TypeError):
            parse_port({})
    
    def test_type_float(self):
        with self.assertRaises(TypeError):
            parse_port(3.14)
    
    def test_type_float_integer(self):
        with self.assertRaises(TypeError):
            parse_port(80.0)
    
    def test_type_bytes(self):
        with self.assertRaises(TypeError):
            parse_port(b"8080")
    
    def test_type_tuple(self):
        with self.assertRaises(TypeError):
            parse_port((8080,))


if __name__ == '__main__':
    unittest.main()