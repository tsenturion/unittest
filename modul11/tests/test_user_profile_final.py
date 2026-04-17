import unittest
from unittest.mock import patch
from app.user_profile import build_profile, normalize_username, wait_until_ready


class TestBuildProfileFixed(unittest.TestCase):
    """Тесты после исправления бага в production-коде"""
    
    maxDiff = None
    
    def test_examples_after_fix(self):
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
            with self.subTest(case=case["case"]):
                self.assertEqual(
                    build_profile(case["payload"]),
                    case["expected"],
                    msg="role должен быть в нижнем регистре"
                )


class TestWaitUntilReadyFast(unittest.TestCase):
    """Быстрые тесты с моками времени"""
    
    def test_ready_after_two_polls_mocked(self):
        """Тест без реального ожидания - используем mock"""
        states = iter(["pending", "pending", "ready"])
        
        def check():
            return next(states)
        
        with (
            patch("app.user_profile.time.sleep") as mock_sleep,
            patch(
                "app.user_profile.time.monotonic",
                side_effect=[0.00, 0.00, 0.10, 0.20]  # Имитируем время
            ),
        ):
            with self.assertLogs("app.user_profile", level="INFO") as cm:
                result = wait_until_ready(check, timeout=0.30, interval=0.10)
        
        self.assertTrue(result)
        # Проверяем, что sleep вызывался нужное количество раз
        self.assertEqual(mock_sleep.call_count, 2)
        # Проверяем, что был лог об успехе
        self.assertEqual(cm.records[-1].getMessage(), "job became ready")
    
    def test_timeout_mocked(self):
        """Тест таймаута без реального ожидания"""
        with (
            patch("app.user_profile.time.sleep") as mock_sleep,
            patch(
                "app.user_profile.time.monotonic",
                side_effect=[0.00, 0.00, 0.10, 0.20, 0.31]  # Превысили timeout
            ),
        ):
            with self.assertLogs("app.user_profile", level="ERROR") as cm:
                result = wait_until_ready(
                    lambda: "pending",
                    timeout=0.30,
                    interval=0.10
                )
        
        self.assertFalse(result)
        self.assertEqual(mock_sleep.call_count, 3)
        self.assertEqual(cm.records[0].getMessage(), "job did not become ready before timeout")
    
    def test_immediate_ready(self):
        """Сразу готов - проверяем, что нет лишних sleep"""
        with (
            patch("app.user_profile.time.sleep") as mock_sleep,
            patch("app.user_profile.time.monotonic", return_value=0.00),
        ):
            result = wait_until_ready(lambda: "ready", timeout=0.30, interval=0.10)
        
        self.assertTrue(result)
        mock_sleep.assert_not_called()


class TestIntegrationWithLocals(unittest.TestCase):
    """Тест, который демонстрирует полезность --locals"""
    
    def test_complex_state_error(self):
        """При падении --locals покажет все локальные переменные"""
        user_data = {
            "id": 999,
            "username": "  test_user  ",
            "role": "admin",
            "extra_field": "should be ignored"
        }
        
        expected = {
            "id": 999,
            "username": "test_user",
            "role": "admin"
        }
        
        # Этот тест покажет, как работает сравнение словарей
        self.assertEqual(
            build_profile(user_data),
            expected,
            msg="Профиль должен содержать только id, username и role"
        )