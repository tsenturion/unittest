import unittest
from unittest.mock import Mock, patch

from order_service import OrderService, Order


class TestOrderServicePlainMock(unittest.TestCase):

    @patch("order_service.AuditClient") 
    def test_pay_happy_path_plain(self, MockAuditClient):
        repo = Mock()
        gateway = Mock()

        repo.find_by_id.return_value = Order(id=1, amount=1000)
        gateway.charge.return_value = "tx_123"

        service = OrderService(repo, gateway)

        result = service.pay(order_id=1)

        self.assertEqual(result, "tx_123")
        repo.find_by_id.assert_called_once_with(1)
        gateway.charge.assert_called_once_with(total=1000, curr="RUB")
        MockAuditClient.assert_called_once_with("https://audit.local")
        MockAuditClient.return_value.write.assert_called_once_with(
            "payment_ok",
            {"order_id": 1, "tx_id": "tx_123"}
        )


if __name__ == "__main__":
    unittest.main()