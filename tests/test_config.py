import json
import unittest
from unittest.mock import mock_open, patch

from app.config import load_config


class TestLoadConfig(unittest.TestCase):
    def test_reads_json_config_from_file(self):
        """Should read and parse JSON config file correctly."""
        raw_config = {
            "base_url": "https://catalog.example",
            "api_key": "secret-token",
            "timeout": 5
        }
        raw_json = json.dumps(raw_config)

        with patch("app.config.open", mock_open(read_data=raw_json)) as mocked_open:
            result = load_config("config.json")

        self.assertEqual(result, raw_config)
        mocked_open.assert_called_once_with(
            "config.json",
            "r",
            encoding="utf-8"
        )

    def test_handles_invalid_json(self):
        """Should propagate JSON decode errors."""
        invalid_json = "{this is not valid json}"

        with patch("app.config.open", mock_open(read_data=invalid_json)):
            with self.assertRaises(json.JSONDecodeError):
                load_config("config.json")