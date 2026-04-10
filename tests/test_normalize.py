import unittest

from app.service import normalize_product


class TestNormalizeProduct(unittest.TestCase):
    def test_normalizes_product_data_correctly(self):
        """Should normalize product data without any mocks."""
        result = normalize_product(
            payload={
                "id": 101,
                "name": "  Gaming Mouse  ",
                "price": 49.99,
                "currency": "USD",
                "in_stock": True,
            },
            fetched_at="2026-03-20T12:00:00+00:00",
        )

        self.assertEqual(
            result,
            {
                "id": 101,
                "name": "Gaming Mouse",
                "price": 49.99,
                "currency": "USD",
                "in_stock": True,
                "fetched_at": "2026-03-20T12:00:00+00:00",
            }
        )

    def test_uses_default_currency_when_missing(self):
        """Should use USD as default currency."""
        result = normalize_product(
            payload={
                "id": 202,
                "name": "Monitor",
                "price": 299.99,
                "in_stock": True,
            },
            fetched_at="2026-03-20T12:00:00+00:00",
        )

        self.assertEqual(result["currency"], "USD")

    def test_converts_in_stock_to_boolean(self):
        """Should convert various truthy values to boolean."""
        test_cases = [
            (1, True),
            ("true", True),  # In real API, might come as string
            (True, True),
            (0, False),
            (False, False),
            (None, False),
            ({}, False),
        ]

        for in_stock_value, expected in test_cases:
            with self.subTest(in_stock_value=in_stock_value):
                result = normalize_product(
                    payload={
                        "id": 303,
                        "name": "Test",
                        "price": 10,
                        "in_stock": in_stock_value,
                    },
                    fetched_at="2026-03-20T12:00:00+00:00",
                )
                self.assertEqual(result["in_stock"], expected)

    def test_strips_whitespace_from_name(self):
        """Should remove leading/trailing whitespace from name."""
        test_cases = [
            ("  Keyboard  ", "Keyboard"),
            ("\tMouse\n", "Mouse"),
            ("Monitor", "Monitor"),
            ("  ", ""),
        ]

        for input_name, expected_name in test_cases:
            with self.subTest(input_name=input_name):
                result = normalize_product(
                    payload={
                        "id": 404,
                        "name": input_name,
                        "price": 10,
                    },
                    fetched_at="2026-03-20T12:00:00+00:00",
                )
                self.assertEqual(result["name"], expected_name)