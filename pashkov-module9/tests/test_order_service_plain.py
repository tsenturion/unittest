import unittest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from order_service import OrderService, Order

class TestOrderServicePlain(unittest.TestCase):
    """Этот тест будет зелёным, хотя код содержит 3 ошибки"""
    
    @patch("order_service.AuditClient")
    def test_pay_success_plain(self, MockAuditClient):
        repo = Mock()
        gateway = Mock()
        
        order = Order(id=1, amount=500)
        repo.find_by_id.return_value = order
        gateway.charge.return_value = "tx-123"
        
        service = OrderService(repo, gateway)
        result = service.pay(1)
        
        self.assertEqual(result, "tx-123")
        repo.find_by_id.assert_called_once_with(1)
        gateway.charge.assert_called_once_with(total=500, curr="USD")
        MockAuditClient.assert_called_once_with("https://audit.local")
        MockAuditClient.return_value.write.assert_called_once()


if __name__ == "__main__":
    unittest.main()