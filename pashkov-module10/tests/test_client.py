import unittest
from unittest.mock import patch
# 
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.client import CatalogClient, CatalogTimeoutError, CatalogResponseError
import requests


class TestCatalogClient(unittest.TestCase):
    """Тесты для HTTP-клиента каталога"""
    
    def setUp(self):
        """Подготовка клиента для тестов"""
        self.client = CatalogClient(
            base_url="https://catalog.example.com",
            api_key="test-key",
            timeout=3
        )
    
    @patch("app.client.requests.get")
    def test_fetch_product_success(self, mock_get):
        """Успешный запрос должен вернуть данные товара"""
        response = mock_get.return_value
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "id": 42,
            "name": " Mechanical Keyboard ",
            "price": 15000,
            "currency": "RUB",
            "in_stock": 10
        }
        
        result = self.client.fetch_product(42)
        
        self.assertEqual(result["id"], 42)
        self.assertEqual(result["name"], " Mechanical Keyboard ")
        
        mock_get.assert_called_once_with(
            "https://catalog.example.com/products/42",
            headers={"Authorization": "Bearer test-key"},
            timeout=3
        )
        response.raise_for_status.assert_called_once_with()
        response.json.assert_called_once_with()
    
    @patch("app.client.requests.get")
    def test_fetch_product_timeout(self, mock_get):
        """Таймаут должен преобразовываться в доменное исключение"""
        mock_get.side_effect = requests.Timeout()
        
        with self.assertRaises(CatalogTimeoutError):
            self.client.fetch_product(42)
        
        mock_get.assert_called_once_with(
            "https://catalog.example.com/products/42",
            headers={"Authorization": "Bearer test-key"},
            timeout=3
        )
    
    @patch("app.client.requests.get")
    def test_fetch_product_http_500(self, mock_get):
        """HTTP 500 должен преобразовываться в доменное исключение"""
        response = mock_get.return_value
        response.status_code = 500
        response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
        
        with self.assertRaises(CatalogResponseError):
            self.client.fetch_product(42)
        
        response.raise_for_status.assert_called_once_with()
    
    @patch("app.client.requests.get")
    def test_fetch_product_http_404(self, mock_get):
        """HTTP 404 должен преобразовываться в доменное исключение"""
        response = mock_get.return_value
        response.status_code = 404
        response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        
        with self.assertRaises(CatalogResponseError):
            self.client.fetch_product(999)
        
        response.raise_for_status.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()