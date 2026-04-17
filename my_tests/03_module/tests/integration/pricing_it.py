import unittest
from src.shop.pricing import final_price_cents


class TestPricingIntegration(unittest.TestCase):

    def test_chain_small(self):
        result = final_price_cents(1000, 10, 20)
        self.assertTrue(result > 0)

    def test_compare_scenarios(self):
        a = final_price_cents(500, 0, 20)
        b = final_price_cents(500, 50, 20)
        self.assertTrue(a > b)

    def test_multiple_steps(self):
        r1 = final_price_cents(100, 10, 10)
        r2 = final_price_cents(100, 20, 10)
        self.assertTrue(r1 > r2)