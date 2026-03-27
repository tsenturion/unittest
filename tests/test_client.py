import unittest
from unittest.mock import patch

import requests

from app.client import CatalogClient, CatalogResponseError, CatalogTimeoutError


class TestCatalogClientSuccess(unittest.TestCase):
    """Tests for successful API responses."""

    @patch("app.client.requests.get")
    def test_fetch_product_success(self, mocked_get):
        """Should return parsed JSON on successful response."""

        response = mocked_get.return_value
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "id": 101,
            "name": "Keyboard",
            "price": 99,
            "currency": "USD",
            "in_stock": True,
        }

        client = CatalogClient(
            base_url="https://catalog.example",
            api_key="secret-token",
            timeout=5,
        )

        result = client.fetch_product(101)

        self.assertEqual(result["name"], "Keyboard")


        mocked_get.assert_called_once_with(
            "https://catalog.example/products/101",
            headers={"Authorization": "Bearer secret-token"},
            timeout=5,
        )
        response.raise_for_status.assert_called_once_with()
        response.json.assert_called_once_with()


class TestCatalogClientTimeout(unittest.TestCase):
    """Tests for request timeout scenarios."""

    @patch("app.client.requests.get")
    def test_fetch_product_timeout(self, mocked_get):
        """Should raise CatalogTimeoutError when request times out."""
        mocked_get.side_effect = requests.Timeout()

        client = CatalogClient(
            base_url="https://catalog.example",
            api_key="secret-token",
            timeout=5,
        )

        with self.assertRaises(CatalogTimeoutError):
            client.fetch_product(101)

        mocked_get.assert_called_once_with(
            "https://catalog.example/products/101",
            headers={"Authorization": "Bearer secret-token"},
            timeout=5,
        )


class TestCatalogClientHttpError(unittest.TestCase):
    """Tests for HTTP error responses."""

    @patch("app.client.requests.get")
    def test_fetch_product_http_500(self, mocked_get):
        """Should raise CatalogResponseError on HTTP 500."""
        response = mocked_get.return_value
        response.status_code = 500
        response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")

        client = CatalogClient(
            base_url="https://catalog.example",
            api_key="secret-token",
            timeout=5,
        )

        with self.assertRaises(CatalogResponseError):
            client.fetch_product(101)

        response.raise_for_status.assert_called_once_with()
        response.json.assert_not_called()