import unittest

from app.service import normalize_product


class TestNormalizeProduct(unittest.TestCase):
    def test_normalizes_payload_without_mocks(self):
        result = normalize_product(
            payload={
                "id": 101,
                "name": " Keyboard ",
                "price": 99,
                "currency": "USD",
                "in_stock": 1,
            },
            fetched_at="2026-03-20T12:00:00+00:00",
        )

        self.assertEqual(
            result,
            {
                "id": 101,
                "name": "Keyboard",
                "price": 99,
                "currency": "USD",
                "in_stock": True,
                "fetched_at": "2026-03-20T12:00:00+00:00",
            },
        )