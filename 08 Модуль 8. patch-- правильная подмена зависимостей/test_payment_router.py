import unittest
from unittest.mock import Mock, patch

from payment_router import choose_payment_mode, charge_order


class TestPaymentRouter(unittest.TestCase):


    def test_choose_mode_default_prod(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(choose_payment_mode(), "gateway")

    def test_choose_mode_prod_explicit(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "prod"}, clear=True):
            self.assertEqual(choose_payment_mode(), "gateway")

    def test_choose_mode_dev(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "dev"}, clear=True):
            self.assertEqual(choose_payment_mode(), "sandbox")

    def test_choose_mode_test(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            self.assertEqual(choose_payment_mode(), "sandbox")

    def test_choose_mode_dry_run(self):
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "prod"}, clear=True):
            self.assertEqual(choose_payment_mode(), "dry-run")

    def test_choose_mode_unknown_env(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "staging"}, clear=True):
            with self.assertRaises(ValueError) as ctx:
                choose_payment_mode()
            self.assertEqual(str(ctx.exception), "unsupported payment env")

    def setUp(self):
        self.sandbox_client = Mock()
        self.gateway_client = Mock()

    def test_charge_order_prod_gateway(self):
        with patch.dict("os.environ", {}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)

        self.assertEqual(result, "gateway")
        self.gateway_client.charge.assert_called_once_with(100)
        self.sandbox_client.charge.assert_not_called()

    def test_charge_order_sandbox(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = charge_order(200, self.sandbox_client, self.gateway_client)

        self.assertEqual(result, "sandbox")
        self.sandbox_client.charge.assert_called_once_with(200)
        self.gateway_client.charge.assert_not_called()

    def test_charge_order_dry_run(self):
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1"}, clear=True):
            result = charge_order(300, self.sandbox_client, self.gateway_client)

        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()

    def test_charge_order_error_unknown_env(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "unknown"}, clear=True):
            with self.assertRaises(ValueError) as ctx:
                charge_order(400, self.sandbox_client, self.gateway_client)
            self.assertEqual(str(ctx.exception), "unsupported payment env")
            self.sandbox_client.charge.assert_not_called()
            self.gateway_client.charge.assert_not_called()


if __name__ == "__main__":
    unittest.main()