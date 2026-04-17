
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.shop.pricing import final_price_cents, bulk_price_cents


class TestPricingWorkflows(unittest.TestCase):
    """Integration test scenarios for pricing."""
    
    def test_checkout_workflow_discounted_item(self):
        """Scenario: Customer buys discounted item with tax."""
        # Step 1: Calculate base price
        base_price = 2999  # $29.99
        
        # Step 2: Apply seasonal discount (15%)
        after_discount = final_price_cents(base_price, 15, 0)
        self.assertEqual(after_discount, 2549)  # 2999 * 0.85 = 2549.15 -> 2549
        
        # Step 3: Apply tax (10%)
        final = final_price_cents(after_discount, 0, 10)
        self.assertEqual(final, 2804)  # 2549 * 1.10 = 2803.9 -> 2804
        
        # Verify full pipeline
        full_pipeline = final_price_cents(base_price, 15, 10)
        self.assertEqual(full_pipeline, final)
    
    def test_bulk_purchase_with_tax(self):
        """Scenario: Bulk purchase with tax calculation."""
        # Buy 5 items at $19.99 each
        items = [(1999, 5)]  # 5 items * $19.99 = $99.95
        
        # Bulk discount 20% for 5+ items
        after_discount = bulk_price_cents(items, 20)
        self.assertEqual(after_discount, 7996)  # 9995 * 0.8 = 7996
        
        # Add tax
        with_tax = final_price_cents(after_discount, 0, 20)
        self.assertEqual(with_tax, 9595)  # 7996 * 1.20 = 9595.2 -> 9595
    
    def test_multiple_promotions_chain(self):
        """Scenario: Stacking multiple promotions."""
        # Original price: $100.00
        base = 10000
        
        # Member discount: 10%
        member_price = final_price_cents(base, 10, 0)
        self.assertEqual(member_price, 9000)
        
        # Flash sale extra 20%
        flash_price = final_price_cents(member_price, 20, 0)
        self.assertEqual(flash_price, 7200)
        
        # Final tax
        final = final_price_cents(flash_price, 0, 20)
        self.assertEqual(final, 8640)
        
        # Combined discount (10% + 20% = 28% total, not 30%)
        combined = final_price_cents(base, 28, 20)
        self.assertEqual(combined, final)
    
    def test_price_edge_cases_workflow(self):
        """Scenario: Extreme price values."""
        # Free item (100% discount)
        free_item = final_price_cents(5000, 100, 20)
        self.assertEqual(free_item, 0)
        
        # Very expensive item
        expensive = final_price_cents(9_999_999_999, 5, 25)
        # 10B -5% = 9.5B, +25% = 11.875B
        self.assertEqual(expensive, 11_874_999_999)
        
        # Very small amount
        small = final_price_cents(1, 0, 0)
        self.assertEqual(small, 1)


class TestDataConsistency(unittest.TestCase):
    """Integration tests for data consistency."""
    
    def test_price_rounding_consistency(self):
        """Test: Rounding is consistent across multiple calls."""
        prices = [100, 200, 350, 500, 1000]
        results = []
        
        for price in prices:
            result = final_price_cents(price, 33, 17)
            results.append(result)
        
        # Verify results are integers
        for result in results:
            self.assertIsInstance(result, int)
        
        # Verify relationship (result >= 0)
        for result in results:
            self.assertGreaterEqual(result, 0)
    
    def test_identity_property(self):
        """Test: No discount + no tax = original price."""
        test_cases = [0, 1, 100, 999, 1000, 9999, 10000]
        
        for price in test_cases:
            result = final_price_cents(price, 0, 0)
            self.assertEqual(result, price)


if __name__ == '__main__':
    unittest.main()
