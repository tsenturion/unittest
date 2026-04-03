# tests/test_order_service_fixed.py
import unittest
from unittest.mock import patch, create_autospec

# Импортируем из исправленной версии
from order_service_fixed import Order, OrderRepo, PaymentGateway, AuditClient, OrderServiceFixed


class TestOrderServiceFinal(unittest.TestCase):
    """Финальные тесты с autospec - все проходят корректно"""
    
    @patch("order_service_fixed.AuditClient", autospec=True)
    def test_pay_happy_path(self, MockAuditClient):
        # Создаем autospec моки
        repo = create_autospec(OrderRepo, instance=True)
        payment_gateway = create_autospec(PaymentGateway, instance=True)
        
        # Настраиваем возвращаемые значения
        repo.get.return_value = Order(id=1, amount=1000)
        payment_gateway.charge.return_value = "tx-12345"
        
        # Настраиваем mock для AuditClient
        mock_audit_instance = MockAuditClient.return_value
        
        # Создаем сервис и вызываем метод
        service = OrderServiceFixed(repo, payment_gateway)
        result = service.pay(1)
        
        # Проверки - теперь все корректные
        self.assertEqual(result, "tx-12345")
        
        repo.get.assert_called_once_with(1)
        
        payment_gateway.charge.assert_called_once_with(1000, currency="RUB")
        
        MockAuditClient.assert_called_once_with(
            endpoint="https://audit.local",
            token="secret"
        )
        
        mock_audit_instance.write.assert_called_once_with(
            "payment_ok",
            {"order_id": 1, "tx_id": "tx-12345"}
        )
        
        print("✅ Все тесты с autospec успешно пройдены!")


if __name__ == "__main__":
    unittest.main()