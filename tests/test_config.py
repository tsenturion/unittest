import unittest
from unittest.mock import mock_open, patch

from app.config import load_config


class TestLoadConfig(unittest.TestCase):
    """Tests for config loading module."""

    def test_reads_json_config_from_file(self):
        """Should read and parse JSON config file."""
        raw_json = """
        {
            "base_url": "https://catalog.example",
            "api_key": "secret-token",
            "timeout": 5
        }
        """

        with patch("app.config.open", mock_open(read_data=raw_json)) as mocked_open:
            result = load_config("config.json")

        expected = {
            "base_url": "https://catalog.example",
            "api_key": "secret-token",
            "timeout": 5,
        }
        self.assertEqual(result, expected)

        mocked_open.assert_called_once_with(
            "config.json",
            "r",
            encoding="utf-8",
        )