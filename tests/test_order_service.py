import unittest
from unittest.mock import Mock, create_autospec, patch

from order_service import Order, OrderRepo, PaymentGateway, AuditClient, OrderService


class TestOrderServicePlainMock(unittest.TestCase):
    @patch("order_service.AuditClient")
    def test_pay_false_green(self, MockAuditClient):
        repo = Mock()
        gateway = Mock()
        
        repo.find_by_id.return_value = Order(id=1, amount=100)
        gateway.charge.return_value = "tx-123"
        
        service = OrderService(repo, gateway)
        result = service.pay(1)
        
        self.assertEqual(result, "tx-123")
        repo.find_by_id.assert_called_once_with(1)
        gateway.charge.assert_called_once_with(amount=100, curr="USD")
        MockAuditClient.assert_called_once_with("https://audit.local")
        MockAuditClient.return_value.write.assert_called_once_with(
            "payment_success",
            {"order_id": 1, "tx_id": "tx-123"}
        )


class TestOrderServiceAutospec(unittest.TestCase):
    @patch("order_service.AuditClient", autospec=True)
    def test_pay_with_autospec(self, MockAuditClient):
        repo = create_autospec(OrderRepo, instance=True)
        gateway = create_autospec(PaymentGateway, instance=True)
        
        repo.get.return_value = Order(id=1, amount=100)
        gateway.charge.return_value = "tx-123"
        
        service = OrderService(repo, gateway)
        result = service.pay(1)
        
        self.assertEqual(result, "tx-123")
        repo.get.assert_called_once_with(1)
        gateway.charge.assert_called_once_with(100, currency="RUB")
        MockAuditClient.assert_called_once_with(
            endpoint="https://audit.local",
            token="secret"
        )
        MockAuditClient.return_value.write.assert_called_once_with(
            "payment_success",
            {"order_id": 1, "tx_id": "tx-123"}
        )