# tests/test_payment_router.py
import unittest
from unittest.mock import Mock, patch

from payment_router import charge_order, choose_payment_mode


class TestPaymentRouter(unittest.TestCase):
    """Тесты для модуля payment_router."""

    def setUp(self):
        """Создаем мок-клиентов для каждого теста."""
        self.mock_sandbox_client = Mock()
        self.mock_gateway_client = Mock()

    # ========== Тесты для функции choose_payment_mode ==========
    def test_choose_payment_mode_prod_by_default(self):
        """Тест 1: По умолчанию (без переменных) должен возвращаться 'gateway'."""
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(choose_payment_mode(), "gateway")

    def test_choose_payment_mode_sandbox_for_test_env(self):
        """Тест 2: При PAYMENT_ENV=test должен возвращаться 'sandbox'."""
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            self.assertEqual(choose_payment_mode(), "sandbox")

    def test_choose_payment_mode_sandbox_for_dev_env(self):
        """Тест 3: При PAYMENT_ENV=dev должен возвращаться 'sandbox'."""
        with patch.dict("os.environ", {"PAYMENT_ENV": "dev"}, clear=True):
            self.assertEqual(choose_payment_mode(), "sandbox")

    def test_choose_payment_mode_dry_run_priority(self):
        """Тест 4: При PAYMENT_DRY_RUN=1 должен возвращаться 'dry-run', даже если есть другие переменные."""
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "prod"}, clear=True):
            self.assertEqual(choose_payment_mode(), "dry-run")

    def test_choose_payment_mode_unsupported_env_raises_error(self):
        """Тест 5: При неподдерживаемом значении PAYMENT_ENV должно выбрасываться ValueError."""
        with patch.dict("os.environ", {"PAYMENT_ENV": "staging"}, clear=True):
            with self.assertRaises(ValueError) as context:
                choose_payment_mode()
            self.assertEqual(str(context.exception), "unsupported payment env: staging")

    # ========== Тесты для функции charge_order ==========
    def test_charge_order_gateway_by_default(self):
        """Тест 6: По умолчанию (без переменных) charge_order должен вызывать gateway_client."""
        with patch.dict("os.environ", {}, clear=True):
            result = charge_order(100, self.mock_sandbox_client, self.mock_gateway_client)

        self.assertEqual(result, "gateway")
        self.mock_gateway_client.charge.assert_called_once_with(100)
        self.mock_sandbox_client.charge.assert_not_called()

    def test_charge_order_sandbox_for_test_env(self):
        """Тест 7: При PAYMENT_ENV=test charge_order должен вызывать sandbox_client."""
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = charge_order(100, self.mock_sandbox_client, self.mock_gateway_client)

        self.assertEqual(result, "sandbox")
        self.mock_sandbox_client.charge.assert_called_once_with(100)
        self.mock_gateway_client.charge.assert_not_called()

    def test_charge_order_dry_run_skips_all_clients(self):
        """Тест 8: При PAYMENT_DRY_RUN=1 charge_order не должен вызывать клиентов."""
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "prod"}, clear=True):
            result = charge_order(100, self.mock_sandbox_client, self.mock_gateway_client)

        self.assertEqual(result, "skipped")
        self.mock_sandbox_client.charge.assert_not_called()
        self.mock_gateway_client.charge.assert_not_called()


if __name__ == "__main__":
    unittest.main()