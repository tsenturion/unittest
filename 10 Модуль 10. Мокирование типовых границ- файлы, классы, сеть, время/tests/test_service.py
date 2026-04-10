import unittest
from datetime import datetime, timezone
from unittest.mock import patch
from app.service import build_product_snapshot

class TestBuildProductSnapshot(unittest.TestCase):
    def test_orchestrates_config_client_and_timestamp(self):
        fixed_now = datetime(2026, 3, 20, 12, 0, 0, tzinfo=timezone.utc)
        fixed_now_str = fixed_now.isoformat()
        with (
            patch("app.service.load_config") as mock_load_config,
            patch("app.service.CatalogClient", autospec=True) as MockCatalogClient,
            patch("app.service.datetime") as mock_datetime,
        ):
            mock_load_config.return_value = {
                "base_url": "https://api.example",
                "api_key": "test-key",
                "timeout": 7,
            }
            mock_client_instance = MockCatalogClient.return_value
            mock_client_instance.fetch_product.return_value = {
                "id": 999,
                "name": "  Test Product  ",
                "price": 100,
                "currency": "EUR",
                "in_stock": 0,
            }
            mock_datetime.now.return_value = fixed_now
            result = build_product_snapshot("fake_config.json", 999)

        self.assertEqual(result["name"], "Test Product")
        self.assertEqual(result["currency"], "EUR")
        self.assertEqual(result["in_stock"], False)
        self.assertEqual(result["fetched_at"], fixed_now_str)

        mock_load_config.assert_called_once_with("fake_config.json")
        MockCatalogClient.assert_called_once_with(
            base_url="https://api.example", api_key="test-key", timeout=7
        )
        mock_client_instance.fetch_product.assert_called_once_with(999)
        mock_datetime.now.assert_called_once_with(timezone.utc)
        