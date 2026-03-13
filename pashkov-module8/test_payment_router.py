# tests/test_payment_router.py\//
import os
import unittest
from unittest.mock import Mock, patch
import payment_router


class TestChoosePaymentMode(unittest.TestCase):
    """Тесты для функции choose_payment_mode"""
    
    def test_default_prod_mode_when_no_env_vars(self):
        """Тест: по умолчанию должен быть prod режим"""
        with patch.dict("os.environ", {}, clear=True):
            result = payment_router.choose_payment_mode()
            self.assertEqual(result, "gateway")
    
    def test_sandbox_mode_when_env_is_test(self):
        """Тест: PAYMENT_ENV=test должен давать sandbox режим"""
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = payment_router.choose_payment_mode()
            self.assertEqual(result, "sandbox")
    
    def test_sandbox_mode_when_env_is_dev(self):
        """Тест: PAYMENT_ENV=dev должен давать sandbox режим"""
        with patch.dict("os.environ", {"PAYMENT_ENV": "dev"}, clear=True):
            result = payment_router.choose_payment_mode()
            self.assertEqual(result, "sandbox")
    
    def test_dry_run_overrides_other_modes(self):
        """Тест: dry-run имеет высший приоритет"""
        # Проверяем для разных комбинаций
        test_cases = [
            {"PAYMENT_DRY_RUN": "1"},  # только dry-run
            {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "prod"},
            {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "test"},
            {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "dev"},
        ]
        
        for env_vars in test_cases:
            with self.subTest(env_vars=env_vars):
                with patch.dict("os.environ", env_vars, clear=True):
                    result = payment_router.choose_payment_mode()
                    self.assertEqual(result, "dry-run")
    
    def test_unsupported_env_raises_error(self):
        """Тест: неподдерживаемое значение PAYMENT_ENV вызывает ошибку"""
        with patch.dict("os.environ", {"PAYMENT_ENV": "staging"}, clear=True):
            with self.assertRaises(ValueError) as context:
                payment_router.choose_payment_mode()
            
            self.assertEqual(str(context.exception), "unsupported payment env: staging")
    
    def test_dry_run_works_without_payment_env(self):
        """Тест: dry-run работает даже без PAYMENT_ENV"""
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1"}, clear=True):
            result = payment_router.choose_payment_mode()
            self.assertEqual(result, "dry-run")


class TestChargeOrder(unittest.TestCase):
    """Тесты для функции charge_order"""
    
    def setUp(self):
        """Создаем моки клиентов перед каждым тестом"""
        self.sandbox_client = Mock()
        self.gateway_client = Mock()
    
    def test_gateway_mode_by_default(self):
        """Тест: по умолчанию используем gateway_client"""
        with patch.dict("os.environ", {}, clear=True):
            result = payment_router.charge_order(
                1000, 
                self.sandbox_client, 
                self.gateway_client
            )
        
        self.assertEqual(result, "gateway")
        self.gateway_client.charge.assert_called_once_with(1000)
        self.sandbox_client.charge.assert_not_called()
    
    def test_sandbox_mode_with_test_env(self):
        """Тест: в test окружении используем sandbox_client"""
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = payment_router.charge_order(
                500,
                self.sandbox_client,
                self.gateway_client
            )
        
        self.assertEqual(result, "sandbox")
        self.sandbox_client.charge.assert_called_once_with(500)
        self.gateway_client.charge.assert_not_called()
    
    def test_sandbox_mode_with_dev_env(self):
        """Тест: в dev окружении используем sandbox_client"""
        with patch.dict("os.environ", {"PAYMENT_ENV": "dev"}, clear=True):
            result = payment_router.charge_order(
                750,
                self.sandbox_client,
                self.gateway_client
            )
        
        self.assertEqual(result, "sandbox")
        self.sandbox_client.charge.assert_called_once_with(750)
        self.gateway_client.charge.assert_not_called()
    
    def test_dry_run_skips_all_clients(self):
        """Тест: dry-run режим не вызывает ни одного клиента"""
        test_envs = [
            {"PAYMENT_DRY_RUN": "1"},
            {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "prod"},
            {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "test"},
        ]
        
        for env_vars in test_envs:
            with self.subTest(env_vars=env_vars):
                # Сбрасываем моки для каждого подтеста
                self.sandbox_client.reset_mock()
                self.gateway_client.reset_mock()
                
                with patch.dict("os.environ", env_vars, clear=True):
                    result = payment_router.charge_order(
                        1000,
                        self.sandbox_client,
                        self.gateway_client
                    )
                
                self.assertEqual(result, "skipped")
                self.sandbox_client.charge.assert_not_called()
                self.gateway_client.charge.assert_not_called()
    
    def test_unsupported_env_propagates_error(self):
        """Тест: ошибка из choose_payment_mode пробрасывается наружу"""
        with patch.dict("os.environ", {"PAYMENT_ENV": "invalid"}, clear=True):
            with self.assertRaises(ValueError) as context:
                payment_router.charge_order(
                    1000,
                    self.sandbox_client,
                    self.gateway_client
                )
            
            self.assertEqual(str(context.exception), "unsupported payment env: invalid")
            self.sandbox_client.charge.assert_not_called()
            self.gateway_client.charge.assert_not_called()


class TestEdgeCases(unittest.TestCase):
    """Тесты для граничных случаев"""
    
    def test_clear_true_is_important_for_defaults(self):
        """
        Демонстрация: почему важно использовать clear=True.
        Если не очищать окружение, тест может зависеть от реальных переменных.
        """
        # Этот тест должен проходить даже если в системе есть реальные переменные
        with patch.dict("os.environ", {}, clear=True):
            # В пустом окружении должен быть prod режим
            mode = payment_router.choose_payment_mode()
            self.assertEqual(mode, "gateway")
        
        # Проверим, что после теста окружение восстановлено
        # (это просто проверка, что patch.dict работает)
        self.assertNotEqual(os.environ.get("PAYMENT_ENV"), "test")
    
    def test_dry_run_has_highest_priority_with_all_envs(self):
        """Тест: dry-run имеет приоритет над любыми другими настройками"""
        with patch.dict(
            "os.environ", 
            {
                "PAYMENT_DRY_RUN": "1",
                "PAYMENT_ENV": "prod",
                "OTHER_VAR": "some_value"
            }, 
            clear=True
        ):
            mode = payment_router.choose_payment_mode()
            self.assertEqual(mode, "dry-run")
    
    def test_payment_env_values_case_sensitivity(self):
        """Тест: значения PAYMENT_ENV чувствительны к регистру"""
        # "PROD" с заглавными буквами - не поддерживается
        with patch.dict("os.environ", {"PAYMENT_ENV": "PROD"}, clear=True):
            with self.assertRaises(ValueError):
                payment_router.choose_payment_mode()
        
        # "prod" с маленькими буквами - поддерживается
        with patch.dict("os.environ", {"PAYMENT_ENV": "prod"}, clear=True):
            mode = payment_router.choose_payment_mode()
            self.assertEqual(mode, "gateway")
    
    def test_dry_run_with_non_one_value(self):
        """Тест: dry-run срабатывает только при exact значении "1" """
        test_values = ["0", "", "true", "yes", "on", "True"]
        
        for value in test_values:
            with self.subTest(dry_run_value=value):
                with patch.dict("os.environ", {"PAYMENT_DRY_RUN": value}, clear=True):
                    mode = payment_router.choose_payment_mode()
                    # Должен быть prod режим по умолчанию
                    self.assertEqual(mode, "gateway")


if __name__ == "__main__":
    unittest.main()