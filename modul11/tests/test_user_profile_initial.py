import unittest
from app.user_profile import build_profile, wait_until_ready


class TestNoise(unittest.TestCase):
    """Тест, который создаёт шум в консоли"""
    
    def test_green_but_chatty(self):
        print("debug: connecting to database...")
        print("debug: loading fixtures...")
        print("debug: ready to test")
        self.assertTrue(True)


class TestBuildProfileInitial(unittest.TestCase):
    """Плохо написанные тесты: assertTrue вместо assertEqual, нет subTest"""
    
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
            {
                "payload": {"id": 3, "username": "x", "role": "guest"},
                "expected": {"id": 3, "username": "x", "role": "guest"},
            },
        ]
        
        for case in cases:
            print(f"checking payload: {case['payload']}")
            # Плохо: теряем информацию о различиях
            self.assertTrue(build_profile(case["payload"]) == case["expected"])


class TestWaitUntilReadySlow(unittest.TestCase):
    """Медленные тесты с реальными задержками"""
    
    def test_ready_after_two_polls(self):
        states = iter(["pending", "pending", "ready"])
        
        def check():
            return next(states, "ready")
        
        # Реальная задержка ~0.20-0.30 секунды
        self.assertTrue(wait_until_ready(check, timeout=0.30, interval=0.10))
    
    def test_timeout(self):
        # Ещё одна реальная задержка ~0.25 секунды
        self.assertFalse(
            wait_until_ready(lambda: "pending", timeout=0.25, interval=0.05)
        )