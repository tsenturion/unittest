import unittest
from src.shop.pricing import final_price_cents


class TestFinalPrice(unittest.TestCase):
    
    # ========== базовое ==========
    
    def test_base_price_no_discount_no_tax(self):
        result = final_price_cents(1000, discount_percent=0, tax_percent=0)
        self.assertEqual(result, 1000)
    
    def test_base_price_with_discount_no_tax(self):
        result = final_price_cents(1000, discount_percent=20, tax_percent=0)
        self.assertEqual(result, 800) 
    
    def test_base_price_with_tax_no_discount(self):
        result = final_price_cents(1000, discount_percent=0, tax_percent=20)
        self.assertEqual(result, 1200)  
    
    def test_base_price_with_discount_and_tax(self):
        result = final_price_cents(1000, discount_percent=10, tax_percent=20)
        self.assertEqual(result, 1080)
    
    # ========== пограничные значения ==========
    
    def test_discount_0_percent(self):
        result = final_price_cents(500, discount_percent=0, tax_percent=20)
        self.assertEqual(result, 600)
    
    def test_discount_100_percent(self):
        result = final_price_cents(500, discount_percent=100, tax_percent=20)
        self.assertEqual(result, 0)
    
    def test_tax_0_percent(self):
        result = final_price_cents(500, discount_percent=10, tax_percent=0)
        self.assertEqual(result, 450)
    
 
    # ========== неправильные значения  ==========
    
    def test_invalid_negative_base(self):
        with self.assertRaises(ValueError):
            final_price_cents(-100, discount_percent=10, tax_percent=20)
    
    def test_invalid_discount_below_zero(self):
        with self.assertRaises(ValueError):
            final_price_cents(1000, discount_percent=-10, tax_percent=20)
    
    def test_invalid_discount_above_100(self):
        with self.assertRaises(ValueError):
            final_price_cents(1000, discount_percent=150, tax_percent=20)
    
    def test_invalid_tax_below_zero(self):
        with self.assertRaises(ValueError):
            final_price_cents(1000, discount_percent=10, tax_percent=-5)
    
    def test_invalid_tax_above_100(self):
        with self.assertRaises(ValueError):
            final_price_cents(1000, discount_percent=10, tax_percent=200)
    
    # ========== окугление ==========
    
    def test_rounding_down(self):
        result = final_price_cents(1000, discount_percent=33, tax_percent=20)
        self.assertEqual(result, 804)
    
    def test_rounding_up(self):
        result = final_price_cents(1000, discount_percent=20, tax_percent=10)
        self.assertEqual(result, 880)


if __name__ == '__main__':
    unittest.main()