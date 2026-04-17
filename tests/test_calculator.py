import unittest
from app.calculator import divide


class TestDivide(unittest.TestCase):
    def test_divides_numbers(self):
        self.assertEqual(divide(10, 2), 5)

    def test_raises_on_zero_division(self):
        with self.assertRaises(ValueError):
            divide(1, 0)


if __name__ == "__main__":
    unittest.main()