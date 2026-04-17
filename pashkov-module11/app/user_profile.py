import logging
import time
import warnings

logger = logging.getLogger(__name__)


def normalize_username(raw: str) -> str:
    clean = raw.strip().lower()
    if len(clean) < 3:
        warnings.warn(
            "usernames shorter than 3 characters are deprecated and will be rejected in v2",
            DeprecationWarning,
            stacklevel=2,
        )
    return clean


def build_profile(payload: dict) -> dict:
    logger.info("building profile for user_id=%s", payload["id"])
    username = normalize_username(payload["username"])
    role = payload.get("role", "user").upper()
    return {
        "id": payload["id"],
        "username": username,
        "role": role,
    }


def wait_until_ready(check_status, *, timeout: float = 0.30, interval: float = 0.10) -> bool:
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if check_status() == "ready":
            logger.info("job became ready")
            return True
        time.sleep(interval)

    logger.error("job did not become ready before timeout")
    return False