import unittest
from unittest.mock import create_autospec, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from order_service import OrderRepo, PaymentGateway, AuditClient, OrderService, Order

class TestOrderServiceAutospec(unittest.TestCase):
    """Этот тест покажет все 3 ошибки"""
    
    @patch("order_service.AuditClient", autospec=True)
    def test_pay_with_autospec_reveals_errors(self, MockAuditClient):
        repo = create_autospec(OrderRepo, instance=True)
        gateway = create_autospec(PaymentGateway, instance=True)
        
        order = Order(id=1, amount=500)
        repo.get.return_value = order
        gateway.charge.return_value = "tx-123"
        
        service = OrderService(repo, gateway)
        
        with self.assertRaises((AttributeError, TypeError)):
            service.pay(1)


if __name__ == "__main__":
    unittest.main()