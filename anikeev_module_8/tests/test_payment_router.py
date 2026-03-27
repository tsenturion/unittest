import unittest
from unittest.mock import Mock, patch

from payment_router import charge_order, choose_payment_mode


class TestChoosePaymentMode(unittest.TestCase):
    
    def test_default_mode_when_no_env_vars(self):
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
    
    def test_dry_run_has_priority_over_env(self):
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "prod"}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "dry-run")
    
    def test_unsupported_env_raises_value_error(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "staging"}, clear=True):
            with self.assertRaises(ValueError) as context:
                choose_payment_mode()
            self.assertIn("staging", str(context.exception))
    
    def test_gateway_mode_for_prod_env_explicit(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "prod"}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "gateway")


class TestChargeOrder(unittest.TestCase):
    
    def setUp(self):
        self.sandbox_client = Mock()
        self.gateway_client = Mock()
    
    def test_gateway_mode_by_default(self):
        with patch.dict("os.environ", {}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "gateway")
        self.gateway_client.charge.assert_called_once_with(100)
        self.sandbox_client.charge.assert_not_called()
    
    def test_sandbox_mode_for_test_env(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "sandbox")
        self.sandbox_client.charge.assert_called_once_with(100)
        self.gateway_client.charge.assert_not_called()
    
    def test_dry_run_skips_all_clients(self):
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "prod"}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()
    
    def test_dry_run_has_priority_over_sandbox(self):
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "test"}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()
    
    def test_error_propagates_from_choose_mode(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "staging"}, clear=True):
            with self.assertRaises(ValueError):
                charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()


if __name__ == "__main__":
    unittest.main()