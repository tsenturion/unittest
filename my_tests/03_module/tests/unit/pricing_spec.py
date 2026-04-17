import unittest
from src.shop.pricing import final_price_cents


class TestFinalPrice(unittest.TestCase):

    def test_discount_0_tax_20(self):
        self.assertEqual(final_price_cents(100, 0, 20), 120)

    def test_discount_100(self):
        self.assertEqual(final_price_cents(100, 100, 20), 0)

    def test_discount_50_no_tax(self):
        self.assertEqual(final_price_cents(200, 50, 0), 100)

    def test_tax_only(self):
        self.assertEqual(final_price_cents(100, 0, 0), 100)

    def test_discount_edge_invalid_high(self):
        with self.assertRaises(ValueError):
            final_price_cents(100, 150, 20)

    def test_tax_edge_invalid_low(self):
        with self.assertRaises(ValueError):
            final_price_cents(100, 0, -1)

    def test_invalid_type_base(self):
        with self.assertRaises(TypeError):
            final_price_cents("100")

    def test_invalid_negative_base(self):
        with self.assertRaises(ValueError):
            final_price_cents(-10)