import unittest
import requests
from unittest.mock import patch
from app.client import CatalogClient, CatalogTimeoutError, CatalogResponseError

class TestCatalogClientSuccess(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_fetch_product_success(self, mocked_get):
        response = mocked_get.return_value
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "id": 101,
            "name": "Keyboard",
            "price": 99,
            "currency": "USD",
            "in_stock": True,
        }

        client = CatalogClient("https://api.example", "key123", timeout=5)
        result = client.fetch_product(101)

        self.assertEqual(result["name"], "Keyboard")
        mocked_get.assert_called_once_with(
            "https://api.example/products/101",
            headers={"Authorization": "Bearer key123"},
            timeout=5,
        )
        response.raise_for_status.assert_called_once()
        response.json.assert_called_once()


class TestCatalogClientTimeout(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_fetch_product_timeout(self, mocked_get):
        mocked_get.side_effect = requests.Timeout()

        client = CatalogClient("https://api.example", "key123", timeout=5)
        with self.assertRaises(CatalogTimeoutError):
            client.fetch_product(101)

        mocked_get.assert_called_once()


class TestCatalogClientHttp500(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_fetch_product_http_500(self, mocked_get):
        response = mocked_get.return_value
        response.status_code = 500
        response.raise_for_status.side_effect = requests.HTTPError("500 Error")

        client = CatalogClient("https://api.example", "key123", timeout=5)
        with self.assertRaises(CatalogResponseError):
            client.fetch_product(101)

        response.raise_for_status.assert_called_once()