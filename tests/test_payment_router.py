import unittest
from unittest.mock import Mock, patch

from payment_router import charge_order, choose_payment_mode


class TestChoosePaymentMode(unittest.TestCase):
    
    def test_default_prod_mode(self):
        with patch.dict("os.environ", {}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "gateway")
    
    def test_prod_mode_explicit(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "prod"}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "gateway")
    
    def test_test_env_returns_sandbox(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "sandbox")
    
    def test_dev_env_returns_sandbox(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "dev"}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "sandbox")
    
    def test_dry_run_returns_dry_run(self):
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1"}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "dry-run")
    
    def test_dry_run_has_priority_over_env(self):
        with patch.dict(
            "os.environ", 
            {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "test"}, 
            clear=True
        ):
            result = choose_payment_mode()
            self.assertEqual(result, "dry-run")
    
    def test_unsupported_env_raises_error(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "staging"}, clear=True):
            with self.assertRaises(ValueError) as context:
                choose_payment_mode()
            self.assertEqual(str(context.exception), "unsupported payment env: staging")
    
    def test_multiple_sandbox_envs_with_subtest(self):
        for env in ("dev", "test"):
            with self.subTest(env=env):
                with patch.dict("os.environ", {"PAYMENT_ENV": env}, clear=True):
                    self.assertEqual(choose_payment_mode(), "sandbox")


class TestChargeOrder(unittest.TestCase):
    
    def setUp(self):
        self.sandbox_client = Mock()
        self.gateway_client = Mock()
    
    def test_default_prod_mode_uses_gateway(self):
        with patch.dict("os.environ", {}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "gateway")
        self.gateway_client.charge.assert_called_once_with(100)
        self.sandbox_client.charge.assert_not_called()
    
    def test_prod_mode_explicit_uses_gateway(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "prod"}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "gateway")
        self.gateway_client.charge.assert_called_once_with(100)
        self.sandbox_client.charge.assert_not_called()
    
    def test_test_env_uses_sandbox(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "sandbox")
        self.sandbox_client.charge.assert_called_once_with(100)
        self.gateway_client.charge.assert_not_called()
    
    def test_dev_env_uses_sandbox(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "dev"}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "sandbox")
        self.sandbox_client.charge.assert_called_once_with(100)
        self.gateway_client.charge.assert_not_called()
    
    def test_dry_run_skips_all_clients(self):
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1"}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()
    
    def test_dry_run_has_priority_over_env(self):
        with patch.dict(
            "os.environ",
            {"PAYMENT_DRY_RUN": "1", "PAYMENT_ENV": "test"},
            clear=True
        ):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()
    
    def test_unsupported_env_raises_error_and_no_calls(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "staging"}, clear=True):
            with self.assertRaises(ValueError) as context:
                charge_order(100, self.sandbox_client, self.gateway_client)
            
            self.assertEqual(str(context.exception), "unsupported payment env: staging")
            self.sandbox_client.charge.assert_not_called()
            self.gateway_client.charge.assert_not_called()
    
    def test_sandbox_clients_are_not_called_in_gateway_mode(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "prod"}, clear=True):
            charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_called_once()
    
    def test_gateway_clients_are_not_called_in_sandbox_mode(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.gateway_client.charge.assert_not_called()
        self.sandbox_client.charge.assert_called_once()


if __name__ == "__main__":
    unittest.main()