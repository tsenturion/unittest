import asyncio
import unittest
from unittest.mock import Mock, AsyncMock, call, patch

from app.client import UserClient, Response, ApiTimeoutError, ApiResponseError


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

    async def test_retries_once_after_timeout(self):
        transport = Mock()
        transport.send = AsyncMock(
            side_effect=[
                TimeoutError(),
                Response(200, {"id": 7, "name": "Alice"}),
            ]
        )

        client = UserClient(
            transport,
            timeout=0.20,
            retries=1,
            retry_delay=0.01,
        )

        with patch("app.client.asyncio.sleep", return_value=None) as mock_sleep:
            user = await client.get_user(7)

        self.assertEqual(user, {"id": 7, "name": "Alice"})
        transport.send.assert_has_awaits(
            [call("GET", "/users/7"), call("GET", "/users/7")]
        )
        mock_sleep.assert_awaited_once_with(0.01)

    async def test_retries_after_500(self):
        transport = Mock()
        transport.send = AsyncMock(
            side_effect=[
                Response(500, {"detail": "temporary problem"}),
                Response(200, {"id": 7, "name": " Alice "}),
            ]
        )

        client = UserClient(
            transport,
            timeout=0.20,
            retries=1,
            retry_delay=0.01,
        )

        with patch("app.client.asyncio.sleep", return_value=None) as mock_sleep:
            user = await client.get_user(7)

        self.assertEqual(user, {"id": 7, "name": "Alice"})
        transport.send.assert_has_awaits(
            [call("GET", "/users/7"), call("GET", "/users/7")]
        )
        mock_sleep.assert_awaited_once_with(0.01)

    async def test_raises_domain_timeout_after_last_attempt(self):
        transport = Mock()
        transport.send = AsyncMock(side_effect=[TimeoutError(), TimeoutError()])

        client = UserClient(
            transport,
            timeout=0.20,
            retries=1,
            retry_delay=0.01,
        )

        with patch("app.client.asyncio.sleep", return_value=None) as mock_sleep:
            with self.assertRaisesRegex(ApiTimeoutError, "timed out after 2 attempts"):
                await client.get_user(7)

        self.assertEqual(transport.send.await_count, 2)
        mock_sleep.assert_awaited_once_with(0.01)

    async def test_404_does_not_trigger_backoff(self):
        transport = Mock()
        transport.send = AsyncMock(return_value=Response(404, {"detail": "not found"}))

        client = UserClient(
            transport,
            timeout=0.20,
            retries=3,
            retry_delay=0.01,
        )

        with patch("app.client.asyncio.sleep", return_value=None) as mock_sleep:
            with self.assertRaisesRegex(ApiResponseError, "unexpected status: 404"):
                await client.get_user(7)

        transport.send.assert_awaited_once_with("GET", "/users/7")
        mock_sleep.assert_not_awaited()

    async def test_wiring_timeout_parameter(self):
        transport = Mock()
        transport.send = AsyncMock(return_value=Response(200, {"id": 1, "name": "x"}))

        with patch("app.client.asyncio.wait_for", wraps=asyncio.wait_for) as mock_wait_for:
            client = UserClient(transport, timeout=0.42, retries=0)
            await client.get_user(7)

        mock_wait_for.assert_awaited_once()
        args, kwargs = mock_wait_for.await_args
        self.assertEqual(kwargs.get("timeout"), 0.42)