import unittest
from unittest.mock import mock_open, patch
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import load_config

class TestLoadConfig(unittest.TestCase):
    def test_reads_json_config_from_file(self):
        raw = """
        {
            "base_url": "https://catalog.example",
            "api_key": "secret-token",
            "timeout": 5
        }
        """
        with patch("app.config.open", mock_open(read_data=raw)) as mocked_open:
            result = load_config("config.json")

        self.assertEqual(result, {
            "base_url": "https://catalog.example",
            "api_key": "secret-token",
            "timeout": 5,
        })
        mocked_open.assert_called_once_with("config.json", "r", encoding="utf-8")