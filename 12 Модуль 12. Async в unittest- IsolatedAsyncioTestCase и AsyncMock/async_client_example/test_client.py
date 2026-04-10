import unittest
from unittest.mock import AsyncMock, Mock, call, patch

from client import UserClient, Response, ApiTimeoutError, ApiResponseError


class TestUserClient(unittest.IsolatedAsyncioTestCase):
    async def test_success_path(self):
        transport = Mock()
        transport.send = AsyncMock(
            return_value=Response(200, {"id": 7, "name": " Alice "})
        )
        client = UserClient(transport, timeout=0.20, retries=1)

        user = await client.get_user(7)

        self.assertEqual(user, {"id": 7, "name": "Alice"})
        transport.send.assert_awaited_once_with("GET", "/users/7")


class TestUserClientRetryOnTimeout(unittest.IsolatedAsyncioTestCase):
    async def test_retries_once_after_timeout(self):
        transport = Mock()
        transport.send = AsyncMock(
            side_effect=[
                TimeoutError(),
                Response(200, {"id": 7, "name": "Alice"}),
            ]
        )
        client = UserClient(transport, timeout=0.20, retries=1, retry_delay=0.01)

        with patch("client.asyncio.sleep", return_value=None) as mock_sleep:
            user = await client.get_user(7)

        self.assertEqual(user, {"id": 7, "name": "Alice"})
        transport.send.assert_has_awaits(
            [call("GET", "/users/7"), call("GET", "/users/7")]
        )
        mock_sleep.assert_awaited_once_with(0.01)


class TestUserClientRetryOnServerError(unittest.IsolatedAsyncioTestCase):
    async def test_retries_after_500(self):
        transport = Mock()
        transport.send = AsyncMock(
            side_effect=[
                Response(500, {"detail": "temporary problem"}),
                Response(200, {"id": 7, "name": " Alice "}),
            ]
        )
        client = UserClient(transport, timeout=0.20, retries=1, retry_delay=0.01)

        with patch("client.asyncio.sleep", return_value=None) as mock_sleep:
            user = await client.get_user(7)

        self.assertEqual(user, {"id": 7, "name": "Alice"})
        transport.send.assert_has_awaits(
            [call("GET", "/users/7"), call("GET", "/users/7")]
        )
        mock_sleep.assert_awaited_once_with(0.01)


class TestUserClientFinalTimeout(unittest.IsolatedAsyncioTestCase):
    async def test_raises_domain_timeout_after_last_attempt(self):
        transport = Mock()
        transport.send = AsyncMock(side_effect=[TimeoutError(), TimeoutError()])
        client = UserClient(transport, timeout=0.20, retries=1, retry_delay=0.01)

        with patch("client.asyncio.sleep", return_value=None) as mock_sleep:
            with self.assertRaisesRegex(ApiTimeoutError, "timed out after 2 attempts"):
                await client.get_user(7)

        self.assertEqual(transport.send.await_count, 2)
        mock_sleep.assert_awaited_once_with(0.01)


class TestUserClientNoRetryOn404(unittest.IsolatedAsyncioTestCase):
    async def test_404_does_not_trigger_backoff(self):
        transport = Mock()
        transport.send = AsyncMock(return_value=Response(404, {"detail": "not found"}))
        client = UserClient(transport, timeout=0.20, retries=3, retry_delay=0.01)

        with patch("client.asyncio.sleep", return_value=None) as mock_sleep:
            with self.assertRaisesRegex(ApiResponseError, "unexpected status: 404"):
                await client.get_user(7)

        transport.send.assert_awaited_once_with("GET", "/users/7")
        mock_sleep.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()