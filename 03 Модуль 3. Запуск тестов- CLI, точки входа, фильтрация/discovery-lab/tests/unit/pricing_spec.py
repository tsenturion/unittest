import unittest
from src.shop.pricing import final_price_cents

class TestFinalPrice(unittest.TestCase):
    
    def test_discount_0_percent(self):
        # discount = 0, tax = 20
        self.assertEqual(final_price_cents(1000, 0, 20), 1200)
    
    def test_discount_100_percent(self):
        # discount = 100% -> цена 0, налог не меняет
        self.assertEqual(final_price_cents(1000, 100, 20), 0)
    
    def test_discount_50_percent_tax_20(self):
        # 1000 -50% = 500, +20% = 600
        self.assertEqual(final_price_cents(1000, 50, 20), 600)
    
    def test_tax_0_percent(self):
        # только скидка 10% от 1000 = 900, налог 0
        self.assertEqual(final_price_cents(1000, 10, 0), 900)
    
    def test_tax_100_percent(self):
        # 1000 -10% = 900, +100% = 1800
        self.assertEqual(final_price_cents(1000, 10, 100), 1800)
    
    def test_invalid_base_negative(self):
        with self.assertRaises(ValueError):
            final_price_cents(-100, 10, 20)
    
    def test_invalid_discount_out_of_range(self):
        with self.assertRaises(ValueError):
            final_price_cents(1000, 150, 20)
        with self.assertRaises(ValueError):
            final_price_cents(1000, -10, 20)
    
    def test_invalid_tax_out_of_range(self):
        with self.assertRaises(ValueError):
            final_price_cents(1000, 10, 200)
    
    def test_invalid_type_base_str(self):
        with self.assertRaises(TypeError):
            final_price_cents("1000", 10, 20)
    
    def test_invalid_type_discount_none(self):
        with self.assertRaises(TypeError):
            final_price_cents(1000, None, 20)
    
    def test_rounding_edge(self):
        # Проверка округления: 100 * (100-33)/100 = 67, +20% = 80.4 -> 80
        self.assertEqual(final_price_cents(100, 33, 20), 80)