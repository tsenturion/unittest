import unittest

from app.service import normalize_product


class TestNormalizeProduct(unittest.TestCase):
    """Tests for pure data normalization function (no mocks needed)."""

    def test_normalizes_payload_without_mocks(self):
        """Should transform raw payload into clean snapshot format."""
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

        expected = {
            "id": 101,
            "name": "Keyboard",
            "price": 99,
            "currency": "USD",
            "in_stock": True,
            "fetched_at": "2026-03-20T12:00:00+00:00",
        }
        self.assertEqual(result, expected)

    def test_uses_default_currency(self):
        """Should use USD as default currency when missing."""
        result = normalize_product(
            payload={
                "id": 102,
                "name": "Mouse",
                "price": 49,
                "in_stock": True,
            },
            fetched_at="2026-03-20T12:00:00+00:00",
        )

        self.assertEqual(result["currency"], "USD")

    def test_converts_in_stock_to_bool(self):
        """Should convert in_stock to boolean."""
        result = normalize_product(
            payload={
                "id": 103,
                "name": "Monitor",
                "price": 299,
                "currency": "EUR",
                "in_stock": 0,
            },
            fetched_at="2026-03-20T12:00:00+00:00",
        )

        self.assertFalse(result["in_stock"])