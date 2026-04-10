import unittest
import requests
from unittest.mock import patch
from app.client import CatalogClient, CatalogTimeoutError, CatalogResponseError

class TestCatalogClientSuccess(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_fetch_product_success(self, mock_requests_get):
        mock_response = mock_requests_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "id": 100,
            "name": "Wireless Mouse",
            "price": 25,
            "currency": "USD",
            
            "in_stock": True,
        }
        client = CatalogClient(base_url="https://api.test", api_key="key", timeout=2)
        result = client.fetch_product(100)
        self.assertEqual(result["name"], "Wireless Mouse")
        mock_requests_get.assert_called_once_with(
            "https://api.test/products/100",
            headers={"Authorization": "Bearer key"},
            timeout=2,
        )
        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()

class TestCatalogClientTimeout(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_fetch_product_timeout(self, mock_requests_get):
        mock_requests_get.side_effect = requests.Timeout()
        client = CatalogClient(base_url="https://api.test", api_key="key", timeout=1)
        with self.assertRaises(CatalogTimeoutError):
            client.fetch_product(200)
        mock_requests_get.assert_called_once()

class TestCatalogClientHttpError(unittest.TestCase):
    @patch("app.client.requests.get")
    def test_fetch_product_http_500(self, mock_requests_get):
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
        client = CatalogClient(base_url="https://api.test", api_key="key", timeout=2)
        with self.assertRaises(CatalogResponseError) as context:
            client.fetch_product(300)
        self.assertIn("500", str(context.exception))
        mock_response.json.assert_not_called()