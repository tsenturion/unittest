# tests/test_port.py
import unittest

from netutils.ports import parse_port


class TestPort(unittest.TestCase):
    def test_raises_type_port(self):
        with self.assertRaises(TypeError):
            parse_port(True)  # weight_g не int

        with self.assertRaises(TypeError):
            parse_port({"port": 3443})  # zone не str

    def test_raises_value_port(self):
        with self.assertRaises(ValueError):
            parse_port(-20)

        with self.assertRaises(ValueError):
            parse_port("-2")

        with self.assertRaises(ValueError):
            parse_port(128000)
        
        with self.assertRaises(ValueError):
            parse_port(605536)


    def test_value_port(self):
        cases = [
            (53323),  # base 500 + 0
            (1),
            (501),  # base 500 + 200
            (2000),
            (65535),  # base 500 + 700
        ]

        for port in cases:
            with self.subTest(port=port):
                # Act
                actual = parse_port(port)
                # Assert
                self.assertEqual(actual, True)


if __name__ == "__main__":
    unittest.main(verbosity=2)