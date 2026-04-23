import unittest
import sys
import os

# Добавляем src в путь импорта (для запуска из любого места)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.shop.pricing import final_price_cents, validate_percent, PricingError


class TestFinalPrice(unittest.TestCase):
    """Test suite for final_price_cents function."""
    
    # === Базовые сценарии ===
    
    def test_normal_price_no_discount_no_tax(self):
        """Test: regular price without discount or tax."""
        result = final_price_cents(1000, 0, 0)
        self.assertEqual(result, 1000)
    
    def test_normal_price_with_discount_only(self):
        """Test: price with discount but no tax."""
        # 1000 - 10% = 900
        result = final_price_cents(1000, 10, 0)
        self.assertEqual(result, 900)
    
    def test_normal_price_with_tax_only(self):
        """Test: price with tax but no discount."""
        # 1000 + 20% = 1200
        result = final_price_cents(1000, 0, 20)
        self.assertEqual(result, 1200)
    
    def test_normal_price_with_both(self):
        """Test: price with both discount and tax."""
        # 1000 -10% = 900, +20% = 1080
        result = final_price_cents(1000, 10, 20)
        self.assertEqual(result, 1080)
    
    # === Крайние значения процентов ===
    
    def test_discount_0_percent(self):
        """Test: 0% discount changes nothing."""
        result = final_price_cents(1000, 0, 20)
        self.assertEqual(result, 1200)
    
    def test_discount_100_percent(self):
        """Test: 100% discount makes product free."""
        result = final_price_cents(1000, 100, 20)
        self.assertEqual(result, 0)  # Free!
    
    def test_tax_0_percent(self):
        """Test: 0% tax."""
        result = final_price_cents(1000, 10, 0)
        self.assertEqual(result, 900)
    
    def test_tax_100_percent(self):
        """Test: 100% tax doubles the price after discount."""
        # 1000 -10% = 900, +100% = 1800
        result = final_price_cents(1000, 10, 100)
        self.assertEqual(result, 1800)
    
    # === Граничные значения base_cents ===
    
    def test_zero_price(self):
        """Test: zero price always results in zero."""
        result = final_price_cents(0, 50, 20)
        self.assertEqual(result, 0)
    
    def test_very_large_price(self):
        """Test: large numbers work correctly."""
        result = final_price_cents(1_000_000_000, 10, 20)
        # 1e9 -10% = 900M, +20% = 1.08e9
        self.assertEqual(result, 1_080_000_000)
    
    # === Округление ===
    
    def test_rounding_down(self):
        """Test: prices round down to nearest cent."""
        # 100 -10% = 90, +15% = 103.5 -> round to 104
        result = final_price_cents(100, 10, 15)
        # 100 * 0.9 = 90, 90 * 1.15 = 103.5 -> round(103.5) = 104
        self.assertEqual(result, 104)
    
    def test_rounding_up(self):
        """Test: prices round up to nearest cent."""
        # 100 -10% = 90, +14% = 102.6 -> round to 103
        result = final_price_cents(100, 10, 14)
        self.assertEqual(result, 103)
    
    # === Неправильные типы (TypeError) ===
    
    def test_invalid_type_string(self):
        """Test: string as base_cents raises TypeError."""
        with self.assertRaises(TypeError) as context:
            final_price_cents("1000")
        self.assertIn("must be int or float", str(context.exception))
    
    def test_invalid_type_none(self):
        """Test: None as base_cents raises TypeError."""
        with self.assertRaises(TypeError) as context:
            final_price_cents(None)
        self.assertIn("cannot be None", str(context.exception))
    
    def test_invalid_type_float_discount(self):
        """Test: discount as string raises TypeError."""
        with self.assertRaises(TypeError):
            validate_percent("50", "discount")
    
    # === Неправильные значения (ValueError) ===
    
    def test_negative_base_price(self):
        """Test: negative base_cents raises ValueError."""
        with self.assertRaises(ValueError) as context:
            final_price_cents(-100)
        self.assertIn("must be >= 0", str(context.exception))
    
    def test_discount_below_0(self):
        """Test: discount less than 0 raises ValueError."""
        with self.assertRaises(ValueError) as context:
            final_price_cents(1000, -10)
        self.assertIn("between 0 and 100", str(context.exception))
    
    def test_discount_above_100(self):
        """Test: discount greater than 100 raises ValueError."""
        with self.assertRaises(ValueError) as context:
            final_price_cents(1000, 150)
        self.assertIn("between 0 and 100", str(context.exception))
    
    def test_tax_below_0(self):
        """Test: tax less than 0 raises ValueError."""
        with self.assertRaises(ValueError):
            final_price_cents(1000, 0, -5)
    
    def test_tax_above_100(self):
        """Test: tax greater than 100 raises ValueError."""
        with self.assertRaises(ValueError):
            final_price_cents(1000, 0, 200)
    
    # === Float input ===
    
    def test_float_base_price(self):
        """Test: float base_cents works correctly."""
        result = final_price_cents(100.75, 10, 20)
        # 100.75 * 0.9 = 90.675, *1.2 = 108.81 -> round to 109
        self.assertEqual(result, 109)
    
    def test_float_percentages(self):
        """Test: float percentages are converted to int."""
        # Should work with float percentages
        result = final_price_cents(1000, 10.5, 20.5)
        # 1000 * 0.895 = 895, *1.205 = 1078.475 -> 1078
        self.assertEqual(result, 1078)


class TestValidatePercent(unittest.TestCase):
    """Test suite for validate_percent helper."""
    
    def test_valid_int(self):
        """Test: valid integer percentages."""
        self.assertEqual(validate_percent(0, "test"), 0)
        self.assertEqual(validate_percent(50, "test"), 50)
        self.assertEqual(validate_percent(100, "test"), 100)
    
    def test_valid_float(self):
        """Test: valid float percentages are converted to int."""
        self.assertEqual(validate_percent(50.0, "test"), 50)
        self.assertEqual(validate_percent(33.33, "test"), 33)  # Truncated
    
    def test_invalid_type_string(self):
        """Test: string raises TypeError."""
        with self.assertRaises(TypeError):
            validate_percent("50", "test")
    
    def test_invalid_type_list(self):
        """Test: list raises TypeError."""
        with self.assertRaises(TypeError):
            validate_percent([50], "test")
    
    def test_value_below_range(self):
        """Test: value below 0 raises ValueError."""
        with self.assertRaises(ValueError):
            validate_percent(-1, "test")
    
    def test_value_above_range(self):
        """Test: value above 100 raises ValueError."""
        with self.assertRaises(ValueError):
            validate_percent(101, "test")


class TestBulkDiscount(unittest.TestCase):
    """Test suite for bulk discounts."""
    
    def test_single_item_no_discount(self):
        """Test: single item without discount."""
        from src.shop.pricing import bulk_price_cents
        items = [(1000, 1)]
        result = bulk_price_cents(items, 0)
        self.assertEqual(result, 1000)
    
    def test_multiple_items_with_discount(self):
        """Test: multiple items with bulk discount."""
        from src.shop.pricing import bulk_price_cents
        items = [(1000, 3), (500, 2)]  # 3000 + 1000 = 4000
        result = bulk_price_cents(items, 10)  # 4000 -10% = 3600
        self.assertEqual(result, 3600)
    
    def test_empty_list(self):
        """Test: empty item list."""
        from src.shop.pricing import bulk_price_cents
        result = bulk_price_cents([], 0)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
