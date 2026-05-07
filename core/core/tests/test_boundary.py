# tests/test_boundary.py
import unittest
from unittest.mock import patch
from infrastructure.adapters import HttpUserGateway

class TestHttpUserGateway(unittest.TestCase):
    @patch("infrastructure.adapters.ApiClient", autospec=True)
    def test_fetch_user_delegates_to_api_client(self, MockApiClient):
        # Arrange
        MockApiClient.return_value.fetch_user.return_value = {"id": 7}
        
        # Act
        gateway = HttpUserGateway("secret")
        result = gateway.fetch_user(7)
        
        # Assert
        self.assertEqual(result, {"id": 7})
        MockApiClient.assert_called_once_with(
            base_url="https://api.example.com",
            token="secret",
        )
        MockApiClient.return_value.fetch_user.assert_called_once_with(7)