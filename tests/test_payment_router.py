import unittest
from unittest.mock import Mock, patch
from payment_router import charge_order, choose_payment_mode


class TestPaymentRouter(unittest.TestCase):
    """Test payment routing logic with environment variable control."""
    
    def setUp(self):
        """Create mock clients before each test."""
        self.sandbox_client = Mock()
        self.gateway_client = Mock()
    
    def test_choose_payment_mode_default_prod(self):
        """Test that with no env vars, mode is 'gateway'."""
        with patch.dict("os.environ", {}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "gateway")
    
    def test_choose_payment_mode_test_env(self):
        """Test that PAYMENT_ENV=test returns 'sandbox'."""
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "sandbox")
    
    def test_choose_payment_mode_dev_env(self):
        """Test that PAYMENT_ENV=dev returns 'sandbox'."""
        with patch.dict("os.environ", {"PAYMENT_ENV": "dev"}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "sandbox")
    
    def test_choose_payment_mode_prod_env(self):
        """Test that PAYMENT_ENV=prod returns 'gateway'."""
        with patch.dict("os.environ", {"PAYMENT_ENV": "prod"}, clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "gateway")
    
    def test_choose_payment_mode_dry_run_override(self):
        """Test that DRY_RUN=1 overrides environment settings."""
        # Dry-run should win even in prod
        with patch.dict("os.environ", 
                       {"PAYMENT_ENV": "prod", "PAYMENT_DRY_RUN": "1"}, 
                       clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "dry-run")
        
        # Dry-run should win even in test
        with patch.dict("os.environ", 
                       {"PAYMENT_ENV": "test", "PAYMENT_DRY_RUN": "1"}, 
                       clear=True):
            result = choose_payment_mode()
            self.assertEqual(result, "dry-run")
    
    def test_choose_payment_mode_unsupported_env(self):
        """Test that unsupported environment raises ValueError."""
        unsupported_values = ["staging", "local", "development", "production"]
        
        for env_value in unsupported_values:
            with self.subTest(env_value=env_value):
                with patch.dict("os.environ", {"PAYMENT_ENV": env_value}, clear=True):
                    with self.assertRaises(ValueError) as context:
                        choose_payment_mode()
                    self.assertIn(env_value, str(context.exception))
    
    def test_charge_order_gateway_mode(self):
        """Test charge_order uses gateway client in default prod mode."""
        with patch.dict("os.environ", {}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "gateway")
        self.gateway_client.charge.assert_called_once_with(100)
        self.sandbox_client.charge.assert_not_called()
    
    def test_charge_order_sandbox_mode(self):
        """Test charge_order uses sandbox client in test mode."""
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "sandbox")
        self.sandbox_client.charge.assert_called_once_with(100)
        self.gateway_client.charge.assert_not_called()
    
    def test_charge_order_dry_run_mode(self):
        """Test charge_order skips payment in dry-run mode."""
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1"}, clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()
    
    def test_charge_order_dry_run_overrides_env(self):
        """Test that dry-run has priority even when other env vars are set."""
        with patch.dict("os.environ", 
                       {"PAYMENT_ENV": "prod", "PAYMENT_DRY_RUN": "1"}, 
                       clear=True):
            result = charge_order(100, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()
    
    def test_charge_order_propagates_value_error(self):
        """Test that ValueError from choose_payment_mode propagates."""
        with patch.dict("os.environ", {"PAYMENT_ENV": "invalid"}, clear=True):
            with self.assertRaises(ValueError) as context:
                charge_order(100, self.sandbox_client, self.gateway_client)
            self.assertIn("invalid", str(context.exception))
    
    def test_multiple_scenarios_with_subtests(self):
        """Test multiple scenarios using subTest for cleaner organization."""
        scenarios = [
            # (env_vars, expected_mode, expected_client_called, other_client_called)
            ({}, "gateway", "gateway", False),
            ({"PAYMENT_ENV": "prod"}, "gateway", "gateway", False),
            ({"PAYMENT_ENV": "test"}, "sandbox", "sandbox", False),
            ({"PAYMENT_ENV": "dev"}, "sandbox", "sandbox", False),
            ({"PAYMENT_DRY_RUN": "1"}, "skipped", None, False),
            ({"PAYMENT_ENV": "test", "PAYMENT_DRY_RUN": "1"}, "skipped", None, False),
            ({"PAYMENT_ENV": "prod", "PAYMENT_DRY_RUN": "1"}, "skipped", None, False),
        ]
        
        for env_vars, expected_mode, expected_client, other_called in scenarios:
            with self.subTest(env_vars=env_vars):
                # Reset mocks for each test
                self.sandbox_client.reset_mock()
                self.gateway_client.reset_mock()
                
                with patch.dict("os.environ", env_vars, clear=True):
                    result = charge_order(100, self.sandbox_client, self.gateway_client)
                
                self.assertEqual(result, expected_mode)
                
                if expected_client == "gateway":
                    self.gateway_client.charge.assert_called_once_with(100)
                    self.sandbox_client.charge.assert_not_called()
                elif expected_client == "sandbox":
                    self.sandbox_client.charge.assert_called_once_with(100)
                    self.gateway_client.charge.assert_not_called()
                else:
                    self.sandbox_client.charge.assert_not_called()
                    self.gateway_client.charge.assert_not_called()


if __name__ == "__main__":
    unittest.main()