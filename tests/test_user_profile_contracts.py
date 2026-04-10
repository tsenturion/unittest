# tests/test_user_profile_contracts.py
import unittest
from unittest.mock import patch

from app.user_profile import (
    build_profile,
    normalize_username,
    wait_until_ready,
)


class TestWarningsAndLogs(unittest.TestCase):
    def test_warns_on_short_username(self):
        with self.assertWarnsRegex(
            DeprecationWarning,
            "shorter than 3 characters",
        ):
            normalize_username(" Bo ")

    def test_logs_profile_build(self):
        with self.assertLogs("app.user_profile", level="INFO") as cm:
            build_profile({"id": 7, "username": " Alice ", "role": "ADMIN"})

        self.assertEqual(
            cm.records[0].getMessage(),
            "building profile for user_id=7",
        )

    def test_ready_path_has_no_error_logs(self):
        with (
            patch("app.user_profile.time.sleep"),
            patch("app.user_profile.time.monotonic", side_effect=[0.00, 0.00]),
        ):
            with self.assertNoLogs("app.user_profile", level="ERROR"):
                result = wait_until_ready(
                    lambda: "ready",
                    timeout=0.30,
                    interval=0.10,
                )

        self.assertTrue(result)