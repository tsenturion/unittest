import unittest
from app.user_profile import build_profile, normalize_username, wait_until_ready


class TestBuildProfileImproved(unittest.TestCase):
    """Улучшенные тесты с subTest и правильными assert"""
    
    maxDiff = None  # Показываем полный diff
    
    def test_examples_with_subtest(self):
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
            {
                "case": "short username should still work (but warn)",
                "payload": {"id": 3, "username": "x", "role": "guest"},
                "expected": {"id": 3, "username": "x", "role": "guest"},
            },
        ]
        
        for case in cases:
            with self.subTest(case=case["case"], payload=case["payload"]):
                self.assertEqual(
                    build_profile(case["payload"]),
                    case["expected"],
                    msg="build_profile() должен нормализовать username и приводить role к нижнему регистру"
                )


class TestWarningsAndLogs(unittest.TestCase):
    """Тесты на warnings и logs как часть контракта"""
    
    def test_warns_on_short_username(self):
        """Проверяем, что короткое имя вызывает DeprecationWarning"""
        with self.assertWarnsRegex(
            DeprecationWarning,
            r"usernames shorter than 3 characters are deprecated"
        ):
            normalize_username("x")
    
    def test_logs_profile_build(self):
        """Проверяем, что build_profile логирует INFO"""
        with self.assertLogs("app.user_profile", level="INFO") as cm:
            build_profile({"id": 7, "username": " Alice ", "role": "ADMIN"})
        
        self.assertEqual(len(cm.records), 1)
        self.assertEqual(cm.records[0].getMessage(), "building profile for user_id=7")
        self.assertEqual(cm.records[0].levelname, "INFO")