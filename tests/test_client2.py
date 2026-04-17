# tests/test_client2.py
import unittest
from unittest.mock import Mock, AsyncMock, call, patch

from app.client2 import UserClient, Response, ApiTimeoutError, ApiResponseError


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

        with patch("app.client2.asyncio.sleep", return_value=None) as mock_sleep:
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

        with patch("app.client2.asyncio.sleep", return_value=None) as mock_sleep:
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

        with patch("app.client2.asyncio.sleep", return_value=None) as mock_sleep:
            with self.assertRaisesRegex(ApiTimeoutError, "timed out after 2 attempts"):
                await client.get_user(7)

        self.assertEqual(transport.send.await_count, 2)
        mock_sleep.assert_awaited_once_with(0.01)

    async def test_raises_server_error_after_last_500(self):
        transport = Mock()
        transport.send = AsyncMock(
            side_effect=[
                Response(500, {}),
                Response(500, {}),
            ]
        )

        client = UserClient(
            transport,
            timeout=0.20,
            retries=1,
            retry_delay=0.01,
        )

        with patch("app.client2.asyncio.sleep", return_value=None) as mock_sleep:
            with self.assertRaisesRegex(ApiResponseError, "server error: 500"):
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

        with patch("app.client2.asyncio.sleep", return_value=None) as mock_sleep:
            with self.assertRaisesRegex(ApiResponseError, "unexpected status: 404"):
                await client.get_user(7)

        transport.send.assert_awaited_once_with("GET", "/users/7")
        mock_sleep.assert_not_awaited()

    async def test_400_does_not_trigger_backoff(self):
        transport = Mock()
        transport.send = AsyncMock(return_value=Response(400, {"detail": "bad request"}))

        client = UserClient(transport, retries=3)

        with patch("app.client2.asyncio.sleep") as mock_sleep:
            with self.assertRaisesRegex(ApiResponseError, "unexpected status: 400"):
                await client.get_user(7)

        transport.send.assert_awaited_once()
        mock_sleep.assert_not_awaited()

    async def test_timeout_wiring(self):
        transport = Mock()
        transport.send = AsyncMock()
        
        expected_timeout = 0.42
        client = UserClient(transport, timeout=expected_timeout, retries=0)
        
        with patch("app.client2.asyncio.wait_for") as mock_wait_for:
            mock_wait_for.return_value = Response(200, {"id": 1, "name": "Test"})
            
            await client.get_user(1)
            
            mock_wait_for.assert_awaited_once()
            args, kwargs = mock_wait_for.await_args
            self.assertEqual(kwargs.get("timeout"), expected_timeout)
            
            transport.send.assert_not_awaited()

    async def test_multiple_retries_with_backoff(self):
        transport = Mock()
        transport.send = AsyncMock(
            side_effect=[
                TimeoutError(),
                TimeoutError(),
                Response(200, {"id": 7, "name": "Alice"}),
            ]
        )

        client = UserClient(
            transport,
            timeout=0.20,
            retries=2,
            retry_delay=0.05,
        )

        with patch("app.client2.asyncio.sleep", return_value=None) as mock_sleep:
            user = await client.get_user(7)

        self.assertEqual(user, {"id": 7, "name": "Alice"})
        self.assertEqual(transport.send.await_count, 3)
        self.assertEqual(mock_sleep.await_count, 2)
        mock_sleep.assert_has_awaits([call(0.05), call(0.05)])

    async def test_transport_exception_propagation(self):
        transport = Mock()
        transport.send = AsyncMock(side_effect=RuntimeError("Network is down"))

        client = UserClient(transport, retries=3)

        with patch("app.client2.asyncio.sleep") as mock_sleep:
            with self.assertRaises(RuntimeError):
                await client.get_user(7)

        transport.send.assert_awaited_once()
        mock_sleep.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()