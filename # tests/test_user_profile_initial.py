import unittest

from app.user_profile import build_profile, wait_until_ready


class TestNoise(unittest.TestCase):
    def test_green_but_chatty(self):
        print("debug: connected to fake service")
        print("debug: ready")
        self.assertTrue(True)


class TestBuildProfileInitial(unittest.TestCase):
    def test_examples(self):
        cases = [
            {
                "payload": {"id": 1, "username": " Alice ", "role": "ADMIN"},
                "expected": {"id": 1, "username": "alice", "role": "admin"},
            },
            {
                "payload": {"id": 2, "username": " Bob "},
                "expected": {"id": 2, "username": "bob", "role": "user"},
            },
        ]

        for case in cases:
            print("checking payload", case["payload"])
            self.assertTrue(build_profile(case["payload"]) == case["expected"])


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