import unittest

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.service import normalize_product


class TestNormalizeProduct(unittest.TestCase):
    """Тесты для чистой функции нормализации (без моков!)"""
    
    def test_normalizes_complete_payload(self):
        """Должен нормализовать полные данные товара"""
        result = normalize_product(
            payload={
                "id": 101,
                "name": "  Gaming Mouse  ",
                "price": 3500,
                "currency": "RUB",
                "in_stock": 5,
            },
            fetched_at="2026-04-03T12:00:00+00:00"
        )
        
        self.assertEqual(result["id"], 101)
        self.assertEqual(result["name"], "Gaming Mouse")
        self.assertEqual(result["price"], 3500)
        self.assertEqual(result["currency"], "RUB")
        self.assertEqual(result["in_stock"], True)
        self.assertEqual(result["fetched_at"], "2026-04-03T12:00:00+00:00")
    
    def test_normalizes_payload_without_optional_fields(self):
        """Должен использовать значения по умолчанию для отсутствующих полей"""
        result = normalize_product(
            payload={
                "id": 102,
                "name": "Simple Product",
                "price": 1000,
            },
            fetched_at="2026-04-03T12:00:00+00:00"
        )
        
        self.assertEqual(result["currency"], "USD")
        self.assertEqual(result["in_stock"], False)
    
    def test_normalizes_in_stock_from_various_types(self):
        """Должен корректно преобразовывать in_stock в bool"""
        test_cases = [
            (1, True),
            (5, True),
            (0, False),
            (True, True),
            (False, False),
            (None, False),
        ]
        
        for in_stock_value, expected in test_cases:
            with self.subTest(in_stock_value=in_stock_value):
                result = normalize_product(
                    payload={
                        "id": 1,
                        "name": "Test",
                        "price": 100,
                        "in_stock": in_stock_value,
                    },
                    fetched_at="2026-04-03T12:00:00+00:00"
                )
                self.assertEqual(result["in_stock"], expected)


if __name__ == "__main__":
    unittest.main()