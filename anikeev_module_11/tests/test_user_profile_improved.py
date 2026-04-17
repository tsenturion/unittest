# tests/test_user_profile_improved.py
import unittest

from app.user_profile import build_profile


class TestBuildProfile(unittest.TestCase):
    maxDiff = None

    def test_examples(self):
        cases = [
            {
                "case": "admin role should be lower-cased",
                "payload": {"id": 1, "username": " Alice ", "role": "ADMIN"},
                "expected": {"id": 1, "username": "alice", "role": "admin"},
            },
            {
                "case": "default role should stay user",
                "payload": {"id": 2, "username": " Bob "},
                "expected": {"id": 2, "username": "bob", "role": "user"},
            },
        ]

        for case in cases:
            with self.subTest(case=case["case"], payload=case["payload"]):
                self.assertEqual(
                    build_profile(case["payload"]),
                    case["expected"],
                    msg="build_profile() должен нормализовать username и приводить role к нижнему регистру",
                )


if __name__ == "__main__":
    unittest.main()