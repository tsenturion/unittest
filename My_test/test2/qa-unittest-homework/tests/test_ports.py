import unittest
from src.netutils.ports import parse_port


class TestParsePort(unittest.TestCase):

    def test_valid_port_range_min(self):
        """Тест: минимальное допустимое значение порта (0)"""
        result = parse_port(0)
        self.assertEqual(result, 0)

    def test_valid_port_range_max(self):
        """Тест: максимальное допустимое значение порта (65535)"""
        result = parse_port(65535)
        self.assertEqual(result, 65535)

    def test_valid_port_in_middle_range(self):
        """Тест: допустимое значение порта в середине диапазона (8080)"""
        result = parse_port(8080)
        self.assertEqual(result, 8080)

    def test_invalid_port_below_range(self):
        """Тест: недопустимое значение порта ниже диапазона (-1)"""
        with self.assertRaises(ValueError):
            parse_port(-1)

    def test_invalid_port_above_range(self):
        """Тест: недопустимое значение порта выше диапазона (65536)"""
        with self.assertRaises(ValueError):
            parse_port(65536)

    def test_string_representation_of_valid_port(self):
        """Тест: строковое представление допустимого порта ('80')"""
        result = parse_port("80")
        self.assertEqual(result, 80)

    def test_string_representation_of_invalid_port_below_range(self):
        """Тест: строковое представление недопустимого порта ниже диапазона ('-1')"""
        with self.assertRaises(ValueError):
            parse_port("-1")

    def test_string_representation_of_invalid_port_above_range(self):
        """Тест: строковое представление недопустимого порта выше диапазона ('65536')"""
        with self.assertRaises(ValueError):
            parse_port("65536")

    def test_none_input_raises_type_error(self):
        """Тест: None в качестве входных данных вызывает TypeError"""
        with self.assertRaises(TypeError):
            parse_port(None)

    def test_boolean_input_raises_type_error(self):
        """Тест: boolean в качестве входных данных вызывает TypeError"""
        with self.assertRaises(TypeError):
            parse_port(True)
        with self.assertRaises(TypeError):
            parse_port(False)

    def test_list_input_raises_type_error(self):
        """Тест: список в качестве входных данных вызывает TypeError"""
        with self.assertRaises(TypeError):
            parse_port([80])

    def test_empty_string_raises_value_error(self):
        """Тест: пустая строка вызывает ValueError"""
        with self.assertRaises(ValueError):
            parse_port("")

    def test_non_numeric_string_raises_value_error(self):
        """Тест: нечисловая строка вызывает ValueError"""
        with self.assertRaises(ValueError):
            parse_port("not_a_number")


if __name__ == '__main__':
    unittest.main()