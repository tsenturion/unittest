import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from app.service import build_product_snapshot


class TestBuildProductSnapshot(unittest.TestCase):
    def test_orchestrates_config_client_and_timestamp(self):
        """Should properly orchestrate all components."""
        fixed_now = datetime(2026, 3, 20, 12, 0, 0, tzinfo=timezone.utc)

        # Для Python < 3.9 нужно использовать вложенные with или отдельные строки
        with patch("app.service.load_config") as mock_load_config:
            with patch("app.service.CatalogClient", autospec=True) as MockCatalogClient:
                with patch("app.service.datetime") as mock_datetime:
                    # Setup config mock
                    mock_load_config.return_value = {
                        "base_url": "https://catalog.example",
                        "api_key": "secret-token",
                        "timeout": 5,
                    }

                    # Setup client mock
                    mock_client_instance = MockCatalogClient.return_value
                    mock_client_instance.fetch_product.return_value = {
                        "id": 101,
                        "name": "  Mechanical Keyboard  ",
                        "price": 149.99,
                        "currency": "EUR",
                        "in_stock": 1,
                    }

                    # Setup datetime mock
                    mock_datetime.now.return_value = fixed_now

                    # Act
                    result = build_product_snapshot("config.json", 101)

                    # Assert - check normalized result
                    self.assertEqual(
                        result,
                        {
                            "id": 101,
                            "name": "Mechanical Keyboard",
                            "price": 149.99,
                            "currency": "EUR",
                            "in_stock": True,
                            "fetched_at": "2026-03-20T12:00:00+00:00",
                        }
                    )

                    # Assert - check all components were called correctly
                    mock_load_config.assert_called_once_with("config.json")
                    MockCatalogClient.assert_called_once_with(
                        base_url="https://catalog.example",
                        api_key="secret-token",
                        timeout=5
                    )
                    mock_client_instance.fetch_product.assert_called_once_with(101)
                    mock_datetime.now.assert_called_once_with(timezone.utc)

    def test_uses_default_timeout_when_not_in_config(self):
        """Should use default timeout (3) when config doesn't provide it."""
        with patch("app.service.load_config") as mock_load_config:
            with patch("app.service.CatalogClient", autospec=True) as MockCatalogClient:
                with patch("app.service.datetime") as mock_datetime:
                    # Config without timeout
                    mock_load_config.return_value = {
                        "base_url": "https://catalog.example",
                        "api_key": "secret-token",
                    }

                    mock_client_instance = MockCatalogClient.return_value
                    mock_client_instance.fetch_product.return_value = {
                        "id": 101,
                        "name": "Test",
                        "price": 10,
                        "in_stock": True,
                    }
                    mock_datetime.now.return_value = datetime(2026, 3, 20, 12, 0, 0, tzinfo=timezone.utc)

                    build_product_snapshot("config.json", 101)

                    # Should use default timeout (3)
                    MockCatalogClient.assert_called_once_with(
                        base_url="https://catalog.example",
                        api_key="secret-token",
                        timeout=3
                    )