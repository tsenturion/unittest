import unittest
from unittest.mock import mock_open, patch

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import load_config

# 
class TestLoadConfig(unittest.TestCase):
    """Тесты для чтения конфигурационного файла"""
    
    def test_reads_valid_json_config(self):
        """Должен корректно читать и парсить JSON-конфиг"""
        raw_json = """
        {
            "base_url": "https://catalog.example.com",
            "api_key": "secret-key-123",
            "timeout": 5
        }
        """
        
        with patch("app.config.open", mock_open(read_data=raw_json)) as mocked_open:
            result = load_config("config.json")
        
        self.assertEqual(result["base_url"], "https://catalog.example.com")
        self.assertEqual(result["api_key"], "secret-key-123")
        self.assertEqual(result["timeout"], 5)
        
        mocked_open.assert_called_once_with("config.json", "r", encoding="utf-8")
    
    def test_reads_minimal_config_with_defaults(self):
        """Должен работать с минимальным конфигом (без timeout)"""
        raw_json = """
        {
            "base_url": "https://catalog.example.com",
            "api_key": "secret-key-123"
        }
        """
        
        with patch("app.config.open", mock_open(read_data=raw_json)):
            result = load_config("config.json")
        
        self.assertEqual(result["base_url"], "https://catalog.example.com")
        self.assertEqual(result["api_key"], "secret-key-123")
        self.assertNotIn("timeout", result)


if __name__ == "__main__":
    unittest.main()