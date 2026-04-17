import unittest
from src.shop.pricing import final_price_cents

class TestPricingUnit(unittest.TestCase):
    def test_final_price_cents_base_case(self):
        """Базовый сценарий: стандартные скидка и налог"""
        self.assertEqual(final_price_cents(100, 20, 20), 96)

    def test_final_price_cents_no_discount_no_tax(self):
        """Проверка без скидки и налога"""
        self.assertEqual(final_price_cents(150, 0, 0), 150)

    def test_final_price_cents_full_discount(self):
        """Полная скидка (100%) приводит к нулевой цене"""
        self.assertEqual(final_price_cents(200, 100, 25), 0)

    def test_final_price_cents_full_tax(self):
        """Максимальный налог (100%) удваивает цену после скидки"""
        self.assertEqual(final_price_cents(50, 0, 100), 100)

    def test_final_price_cents_rounding_up(self):
        """Округление вверх при .5 (11.5 → 12)"""
        self.assertEqual(final_price_cents(10, 0, 15), 12)  # 10 * 1.15 = 11.5

    def test_final_price_cents_rounding_down(self):
        """Округление вниз при <.5 (10.4 → 10)"""
        self.assertEqual(final_price_cents(10, 0, 4), 10)    # 10 * 1.04 = 10.4

    def test_final_price_cents_negative_base_invalid(self):
        """Отрицательная базовая цена вызывает ошибку"""
        with self.assertRaises(ValueError) as cm:
            final_price_cents(-50, 10, 20)
        self.assertIn("non-negative integer", str(cm.exception))

    def test_final_price_cents_invalid_discount_percent(self):
        """Скидка за пределами 0-100 вызывает ошибку"""
        with self.assertRaises(ValueError) as cm:
            final_price_cents(100, 101, 20)
        self.assertIn("between 0 and 100", str(cm.exception))

    def test_final_price_cents_invalid_tax_percent(self):
        """Налог за пределами 0-100 вызывает ошибку"""
        with self.assertRaises(ValueError) as cm:
            final_price_cents(100, 10, -5)
        self.assertIn("between 0 and 100", str(cm.exception))

    def test_final_price_cents_invalid_base_type(self):
        """Некорректный тип базовой цены вызывает ошибку"""
        with self.assertRaises(ValueError) as cm:
            final_price_cents("100", 10, 20)
        self.assertIn("integer", str(cm.exception))

    def test_final_price_cents_invalid_discount_type(self):
        """Некорректный тип скидки вызывает ошибку"""
        with self.assertRaises(ValueError) as cm:
            final_price_cents(100, None, 20)
        self.assertIn("integer", str(cm.exception))

    def test_final_price_cents_zero_base_with_taxes(self):
        """Нулевая базовая цена остается нулевой при любых налогах/скидках"""
        self.assertEqual(final_price_cents(0, 50, 100), 0)