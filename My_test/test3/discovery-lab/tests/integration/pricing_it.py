import unittest
from src.shop.pricing import final_price_cents

class TestPricingIntegration(unittest.TestCase):
    def test_pricing_integration_chain_multiple_items(self):
        """Интеграционный тест: цепочка вычислений с несколькими товарами"""
        total = (
            final_price_cents(200, 10, 15) +  # 200 → 180 → 207
            final_price_cents(50, 0, 20) +     # 50 → 50 → 60
            final_price_cents(75, 20, 10)      # 75 → 60 → 66
        )
        self.assertEqual(total, 207 + 60 + 66)

    def test_pricing_integration_edge_values_combined(self):
        """Интеграционный тест: комбинация крайних значений"""
        self.assertEqual(final_price_cents(0, 0, 0), 0)
        self.assertEqual(final_price_cents(1_000_000, 50, 100), 1_000_000)  # 500k → 1M
        self.assertEqual(final_price_cents(1, 99, 99), 0)  # 0.01 → 0.0199 → 0

    def test_pricing_integration_rounding_scenarios(self):
        """Интеграционный тест: сценарии округления"""
        self.assertEqual(final_price_cents(1, 0, 99), 2)    # 1.99 → 2
        self.assertEqual(final_price_cents(3, 33, 0), 2)     # 2.01 → 2
        self.assertEqual(final_price_cents(1, 67, 0), 0)     # 0.33 → 0