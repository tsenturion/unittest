
import unittest
from unittest.mock import Mock, patch, create_autospec

from order_service import OrderService, Order, OrderRepo, PaymentGateway, AuditClient


class TestOrderServicePlainMock(unittest.TestCase):
    @patch("order_service.AuditClient")
    def test_pay_false_green(self, MockAuditClient):
        repo = Mock()
        gateway = Mock()

        order = Order(id=123, amount=500)
        repo.fetch_by_id.return_value = order
        gateway.charge.return_value = "tx-abc-123"

        service = OrderService(repo, gateway)
        result = service.pay(123)

        self.assertEqual(result, "tx-abc-123")
        repo.fetch_by_id.assert_called_once_with(123)
        gateway.charge.assert_called_once_with(amount=500, curr="RUB")
        MockAuditClient.assert_called_once_with("https://audit.local")
        MockAuditClient.return_value.write.assert_called_once()


class TestOrderServiceAutospec(unittest.TestCase):
    @patch("order_service.AuditClient", autospec=True)
    def test_pay_correct(self, MockAuditClient):
        repo = create_autospec(OrderRepo, instance=True)
        gateway = create_autospec(PaymentGateway, instance=True)

        order = Order(id=123, amount=500)
        repo.get.return_value = order
        gateway.charge.return_value = "tx-abc-123"

        service = OrderService(repo, gateway)
        result = service.pay(123)

        self.assertEqual(result, "tx-abc-123")
        repo.get.assert_called_once_with(123)
        gateway.charge.assert_called_once_with(500, currency="RUB")
        MockAuditClient.assert_called_once_with(
            endpoint="https://audit.local",
            token="secret"
        )
        MockAuditClient.return_value.write.assert_called_once_with(
            "payment_processed",
            {"order_id": 123, "tx_id": "tx-abc-123"}
        )