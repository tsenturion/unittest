import unittest
from unittest.mock import create_autospec, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from order_service_fixed import OrderRepo, PaymentGateway, AuditClient, OrderService, Order

class TestOrderServiceFixed(unittest.TestCase):
    """Полноценный тест после исправления всех ошибок"""
    
    @patch("order_service_fixed.AuditClient", autospec=True)
    def test_pay_success(self, MockAuditClient):
        repo = create_autospec(OrderRepo, instance=True)
        gateway = create_autospec(PaymentGateway, instance=True)
        
        order = Order(id=1, amount=500)
        repo.get.return_value = order
        gateway.charge.return_value = "tx-123"
        
        mock_audit_instance = MockAuditClient.return_value
        
        service = OrderService(repo, gateway)
        result = service.pay(1)
        
        self.assertEqual(result, "tx-123")
        repo.get.assert_called_once_with(1)
        gateway.charge.assert_called_once_with(500, currency="USD")
        MockAuditClient.assert_called_once_with(
            endpoint="https://audit.local",
            token="secret"
        )
        mock_audit_instance.write.assert_called_once_with(
            "payment_success",
            {"order_id": 1, "tx_id": "tx-123"}
        )


if __name__ == "__main__":
    unittest.main()