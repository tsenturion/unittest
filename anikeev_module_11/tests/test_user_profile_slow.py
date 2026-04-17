# tests/test_user_profile_slow.py
import unittest

from app.user_profile import wait_until_ready


class TestWaitUntilReadySlow(unittest.TestCase):
    def test_ready_after_two_polls(self):
        states = iter(["pending", "pending", "ready"])

        def check():
            return next(states, "ready")

        self.assertTrue(wait_until_ready(check, timeout=0.30, interval=0.10))

    def test_timeout(self):
        self.assertFalse(
            wait_until_ready(lambda: "pending", timeout=0.25, interval=0.05)
        )


if __name__ == "__main__":
    unittest.main()