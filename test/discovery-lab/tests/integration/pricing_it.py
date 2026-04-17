import unittest
from src.shop.pricing import final_price_cents


class TestPricingIntegration(unittest.TestCase):
    
    def test_multiple_items_chain(self):
        prices = [1000, 2000, 5000, 10000]
        discount = 10
        tax = 20
        
        results = [
            final_price_cents(price, discount_percent=discount, tax_percent=tax)
            for price in prices
        ]
        
        expected = [1080, 2160, 5400, 10800]
        self.assertEqual(results, expected)
    
    def test_price_rounding_consistency(self):
        base = 199
        discount = 15
        tax = 7
        
        result1 = final_price_cents(base, discount_percent=discount, tax_percent=tax)
        result2 = final_price_cents(base, discount_percent=discount, tax_percent=tax)
        
        self.assertEqual(result1, result2)
    
    def test_zero_percent_scenarios(self):
        self.assertEqual(final_price_cents(1000, 0, 0), 1000)
        
        self.assertEqual(final_price_cents(1000, 20, 0), 800)
        
        self.assertEqual(final_price_cents(1000, 0, 20), 1200)
        
        self.assertEqual(final_price_cents(1000, 100, 100), 0)


if __name__ == '__main__':
    unittest.main()