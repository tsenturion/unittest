import unittest
from unittest.mock import patch

import requests

from app.client import CatalogClient, CatalogTimeoutError, CatalogResponseError


class TestCatalogClientSuccess(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_fetch_product_success(self, mock_get):
        """Should return parsed JSON on successful API response."""
        # Arrange
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "id": 101,
            "name": "Keyboard",
            "price": 99.99,
            "currency": "USD",
            "in_stock": True
        }

        client = CatalogClient(
            base_url="https://catalog.example",
            api_key="secret-token",
            timeout=5
        )

        # Act
        result = client.fetch_product(101)

        # Assert
        self.assertEqual(result["id"], 101)
        self.assertEqual(result["name"], "Keyboard")
        mock_get.assert_called_once_with(
            "https://catalog.example/products/101",
            headers={"Authorization": "Bearer secret-token"},
            timeout=5
        )
        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()


class TestCatalogClientTimeout(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_fetch_product_timeout(self, mock_get):
        """Should raise CatalogTimeoutError when request times out."""
        # Arrange
        mock_get.side_effect = requests.Timeout()

        client = CatalogClient(
            base_url="https://catalog.example",
            api_key="secret-token",
            timeout=5
        )

        # Act & Assert
        with self.assertRaises(CatalogTimeoutError):
            client.fetch_product(101)

        mock_get.assert_called_once()


class TestCatalogClientHTTPError(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_fetch_product_http_404(self, mock_get):
        """Should raise CatalogResponseError on 404 status."""
        # Arrange
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

        client = CatalogClient(
            base_url="https://catalog.example",
            api_key="secret-token",
            timeout=5
        )

        # Act & Assert
        with self.assertRaises(CatalogResponseError):
            client.fetch_product(101)

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_not_called()

    @patch("app.client.requests.get")
    def test_fetch_product_http_500(self, mock_get):
        """Should raise CatalogResponseError on 500 status."""
        # Arrange
        mock_response = mock_get.return_value
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")

        client = CatalogClient(
            base_url="https://catalog.example",
            api_key="secret-token",
            timeout=5
        )

        # Act & Assert
        with self.assertRaises(CatalogResponseError):
            client.fetch_product(101)

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_not_called()


class TestCatalogClientURLTrailingSlash(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_strips_trailing_slash_from_base_url(self, mock_get):
        """Should handle base_url with trailing slash correctly."""
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"id": 101, "name": "Test"}

        client = CatalogClient(
            base_url="https://catalog.example/",
            api_key="secret-token"
        )

        client.fetch_product(101)

        # URL should not have double slash
        mock_get.assert_called_once_with(
            "https://catalog.example/products/101",
            headers={"Authorization": "Bearer secret-token"},
            timeout=3
        )