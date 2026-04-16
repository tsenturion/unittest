import unittest
from src.shop.pricing import final_price_cents

class IntegrationPricingTest(unittest.TestCase):
    
    def test_multiple_products_scenario(self):
        # Имитация заказа из нескольких товаров
        products = [(1000, 10, 20), (2000, 0, 20), (500, 100, 20)]
        total = sum(final_price_cents(*p) for p in products)
        # Ручной расчёт: (1000-10%=900+20%=1080) + (2000+20%=2400) + (0) = 3480
        self.assertEqual(total, 1080 + 2400 + 0)
    
    def test_high_discount_high_tax(self):
        # Скидка 80%, налог 50%
        result = final_price_cents(10000, 80, 50)
        # 10000 -80% = 2000, +50% = 3000
        self.assertEqual(result, 3000)
    
    def test_zero_base(self):
        result = final_price_cents(0, 50, 20)
        self.assertEqual(result, 0)