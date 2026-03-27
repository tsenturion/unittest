import unittest
from unittest.mock import mock_open, patch
from app.config import load_config

class TestLoadConfig(unittest.TestCase):
    def test_loads_json_config_from_file(self):
        raw_config = '''
        {
            "base_url": "https://api.example.com",
            "api_key": "test-key-123",
            "timeout": 10
        }
        '''
        with patch("app.config.open", mock_open(read_data=raw_config)) as mock_file_open:
            result = load_config("dummy_path.json")
        self.assertEqual(result["base_url"], "https://api.example.com")
        self.assertEqual(result["api_key"], "test-key-123")
        self.assertEqual(result["timeout"], 10)
        
        mock_file_open.assert_called_once_with("dummy_path.json", "r", encoding="utf-8")