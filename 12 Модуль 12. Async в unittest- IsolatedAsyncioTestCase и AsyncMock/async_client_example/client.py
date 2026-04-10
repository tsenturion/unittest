import asyncio
from dataclasses import dataclass


@dataclass
class Response:
    status: int
    payload: dict


class ApiTimeoutError(Exception):
    pass


class ApiResponseError(Exception):
    pass


class AsyncTransport:
    async def send(self, method: str, path: str) -> Response:
        raise NotImplementedError


class UserClient:
    def __init__(
        self,
        transport: AsyncTransport,
        *,
        timeout: float = 0.20,
        retries: int = 1,
        retry_delay: float = 0.01,
    ) -> None:
        self._transport = transport
        self._timeout = timeout
        self._retries = retries
        self._retry_delay = retry_delay

    async def get_user(self, user_id: int) -> dict:
        path = f"/users/{user_id}"

        for attempt in range(self._retries + 1):
            try:
                response = await asyncio.wait_for(
                    self._transport.send("GET", path),
                    timeout=self._timeout,
                )
            except TimeoutError as exc:
                if attempt == self._retries:
                    raise ApiTimeoutError(
                        f"GET {path} timed out after {self._retries + 1} attempts"
                    ) from exc
                await asyncio.sleep(self._retry_delay)
                continue

            if response.status >= 500:
                if attempt == self._retries:
                    raise ApiResponseError(f"server error: {response.status}")
                await asyncio.sleep(self._retry_delay)
                continue

            if response.status != 200:
                raise ApiResponseError(f"unexpected status: {response.status}")

            return {
                "id": response.payload["id"],
                "name": response.payload["name"].strip(),
            }

        raise ApiTimeoutError("unreachable")