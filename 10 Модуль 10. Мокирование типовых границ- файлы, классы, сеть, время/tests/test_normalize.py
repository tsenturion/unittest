import unittest
from app.service import normalize_product

class TestNormalizeProduct(unittest.TestCase):
    def test_normalizes_payload_correctly(self):
        raw_payload = {
            "id": 101,
            "name": "  Mechanical Keyboard  ",
            "price": 149,
            "currency": None,
            "in_stock": 1,
        }
        fetched_at = "2026-03-20T12:00:00+00:00"
        result = normalize_product(raw_payload, fetched_at)
        expected = {
            "id": 101,
            "name": "Mechanical Keyboard",
            "price": 149,
            "currency": "USD",
            "in_stock": True,
            "fetched_at": "2026-03-20T12:00:00+00:00",
        }
        self.assertEqual(result, expected)

    def test_normalizes_with_existing_currency(self):
        raw_payload = {
            "id": 102,
            "name": "Gaming Mouse",
            "price": 55,
            "currency": "EUR",
            "in_stock": 0,
        }
        fetched_at = "2026-03-20T12:00:00+00:00"
        result = normalize_product(raw_payload, fetched_at)
        self.assertEqual(result["currency"], "EUR")
        self.assertEqual(result["in_stock"], False)
        