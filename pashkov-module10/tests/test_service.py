import unittest
from datetime import datetime, timezone
from unittest.mock import patch
#
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.service import build_product_snapshot


class TestBuildProductSnapshot(unittest.TestCase):
    """Тесты для оркестрирующей функции (с моками зависимостей)"""
    
    def test_orchestrates_config_client_and_timestamp(self):
        """Должен правильно скоординировать все шаги"""
        fixed_now = datetime(2026, 4, 3, 12, 0, 0, tzinfo=timezone.utc)
        
        with (
            patch("app.service.load_config") as mock_load_config,
            patch("app.service.CatalogClient", autospec=True) as MockCatalogClient,
            patch("app.service.datetime") as mock_datetime,
        ):
            mock_load_config.return_value = {
                "base_url": "https://catalog.example.com",
                "api_key": "secret-key",
                "timeout": 5,
            }
            
            client_instance = MockCatalogClient.return_value
            client_instance.fetch_product.return_value = {
                "id": 42,
                "name": "  Test Product  ",
                "price": 1000,
                "currency": "RUB",
                "in_stock": 3,
            }
            
            mock_datetime.now.return_value = fixed_now
            
            result = build_product_snapshot("config.json", 42)
        
        self.assertEqual(result["id"], 42)
        self.assertEqual(result["name"], "Test Product")
        self.assertEqual(result["price"], 1000)
        self.assertEqual(result["currency"], "RUB")
        self.assertEqual(result["in_stock"], True)
        self.assertEqual(result["fetched_at"], "2026-04-03T12:00:00+00:00")
        
        mock_load_config.assert_called_once_with("config.json")
        
        MockCatalogClient.assert_called_once_with(
            base_url="https://catalog.example.com",
            api_key="secret-key",
            timeout=5,
        )
        
        client_instance.fetch_product.assert_called_once_with(42)
        
        mock_datetime.now.assert_called_once_with(timezone.utc)
    
    def test_handles_config_without_timeout(self):
        """Должен использовать timeout по умолчанию (3 секунды)"""
        fixed_now = datetime(2026, 4, 3, 12, 0, 0, tzinfo=timezone.utc)
        
        with (
            patch("app.service.load_config") as mock_load_config,
            patch("app.service.CatalogClient", autospec=True) as MockCatalogClient,
            patch("app.service.datetime") as mock_datetime,
        ):
            mock_load_config.return_value = {
                "base_url": "https://catalog.example.com",
                "api_key": "secret-key",
            }
            
            client_instance = MockCatalogClient.return_value
            client_instance.fetch_product.return_value = {"id": 1, "name": "x", "price": 100}
            mock_datetime.now.return_value = fixed_now
            
            build_product_snapshot("config.json", 1)
            
            MockCatalogClient.assert_called_once_with(
                base_url="https://catalog.example.com",
                api_key="secret-key",
                timeout=3,
            )


if __name__ == "__main__":
    unittest.main()