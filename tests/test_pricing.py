# tests/test_pricing.py
import unittest

from shipping.pricing import shipping_price_cents


class TestShippingPrice(unittest.TestCase):
    def test_raises_type_error_on_wrong_types(self):
        # Arrange / Act / Assert
        with self.assertRaises(TypeError):
            shipping_price_cents("100", "local")  # weight_g не int

        with self.assertRaises(TypeError):
            shipping_price_cents(100, 123)  # zone не str

        with self.assertRaises(TypeError):
            shipping_price_cents(100, "local", "yes")  # express не bool

        # Важно: bool — подкласс int, часто это нежелательно
        with self.assertRaises(TypeError):
            shipping_price_cents(True, "local")

    def test_raises_value_error_on_out_of_range_weight(self):
        # Arrange / Act / Assert
        for w in (0, -1, 30_001):
            with self.subTest(weight_g=w):
                with self.assertRaises(ValueError):
                    shipping_price_cents(w, "local")

    def test_raises_value_error_on_unknown_zone(self):
        # Arrange / Act / Assert
        with self.assertRaises(ValueError):
            shipping_price_cents(100, "mars")

    def test_price_by_weight_boundaries_local_no_express(self):
        # Arrange: таблица граничных значений и ожидаемых цен
        cases = [
            (1, 500),  # base 500 + 0
            (500, 500),
            (501, 700),  # base 500 + 200
            (2000, 700),
            (2001, 1200),  # base 500 + 700
            (10000, 1200),
            (10001, 2000),  # base 500 + 1500
            (30000, 2000),
        ]

        for weight_g, expected in cases:
            with self.subTest(weight_g=weight_g):
                # Act
                actual = shipping_price_cents(weight_g, "local", express=False)
                # Assert
                self.assertEqual(actual, expected)

    def test_express_adds_30_percent_rounded_up(self):
        # Arrange
        weight_g = 501  # local: 500 + 200 = 700
        expected = 700 + (700 * 30 + 99) // 100  # 700 + 210 = 910

        # Act
        actual = shipping_price_cents(weight_g, "local", express=True)

        # Assert
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)