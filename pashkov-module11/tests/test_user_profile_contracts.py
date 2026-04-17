import unittest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.user_profile import build_profile, normalize_username, wait_until_ready


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
        
        self.assertEqual(len(cm.records), 1)
        self.assertEqual(cm.records[0].getMessage(), "building profile for user_id=7")
    
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
    
    def test_timeout_logs_error(self):
        with (
            patch("app.user_profile.time.sleep"),
            patch("app.user_profile.time.monotonic", side_effect=[0.00, 0.00, 0.10, 0.20, 0.31]),
        ):
            with self.assertLogs("app.user_profile", level="ERROR") as cm:
                result = wait_until_ready(
                    lambda: "pending",
                    timeout=0.30,
                    interval=0.10,
                )
        
        self.assertFalse(result)
        self.assertEqual(cm.records[0].levelname, "ERROR")
        self.assertEqual(
            cm.records[0].getMessage(),
            "job did not become ready before timeout",
        )


if __name__ == "__main__":
    unittest.main()