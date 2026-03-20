import unittest
from unittest.mock import Mock, patch

from payment_router import choose_payment_mode, charge_order


class TestChoosePaymentMode(unittest.TestCase):
    
    def test_default_prod_mode_when_no_env_vars(self):
        with patch.dict("os.environ", {}, clear=True):
            result = choose_payment_mode()
        
        self.assertEqual(result, "gateway")
    
    def test_sandbox_mode_for_test_env(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = choose_payment_mode()
        
        self.assertEqual(result, "sandbox")
    
    def test_sandbox_mode_for_dev_env(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "dev"}, clear=True):
            result = choose_payment_mode()
        
        self.assertEqual(result, "sandbox")
    
    def test_dry_run_mode_has_priority(self):
        with patch.dict(
            "os.environ",
            {"PAYMENT_ENV": "prod", "PAYMENT_DRY_RUN": "1"},
            clear=True
        ):
            result = choose_payment_mode()
        
        self.assertEqual(result, "dry-run")
    
    def test_unsupported_env_raises_value_error(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "staging"}, clear=True):
            with self.assertRaises(ValueError) as context:
                choose_payment_mode()
        
        self.assertEqual(str(context.exception), "unsupported payment env")


class TestChargeOrder(unittest.TestCase):
    
    def setUp(self):
        self.sandbox_client = Mock()
        self.gateway_client = Mock()
    
    def test_dry_run_skips_all_clients(self):
        with patch.dict(
            "os.environ",
            {"PAYMENT_DRY_RUN": "1"},
            clear=True
        ):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()
    
    def test_sandbox_mode_calls_sandbox_client(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = charge_order(250, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "sandbox")
        self.sandbox_client.charge.assert_called_once_with(250)
        self.gateway_client.charge.assert_not_called()
    
    def test_gateway_mode_calls_gateway_client(self):
        with patch.dict("os.environ", {}, clear=True):
            result = charge_order(500, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "gateway")
        self.gateway_client.charge.assert_called_once_with(500)
        self.sandbox_client.charge.assert_not_called()
    
    def test_dry_run_priority_over_sandbox(self):
        with patch.dict(
            "os.environ",
            {"PAYMENT_ENV": "test", "PAYMENT_DRY_RUN": "1"},
            clear=True
        ):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()


if __name__ == "__main__":
    unittest.main()