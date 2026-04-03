# tests/test_order_service.py
import unittest
from unittest.mock import Mock, patch, create_autospec

from order_service import Order, OrderRepo, PaymentGateway, AuditClient, OrderService


class TestOrderServicePlainMock(unittest.TestCase):
    """Тесты с plain Mock - показывают ложнозеленый сценарий"""
    
    @patch("order_service.AuditClient")
    def test_pay_false_green(self, MockAuditClient):
        # Создаем plain mocks для зависимостей
        repo = Mock()
        payment_gateway = Mock()
        
        # Настраиваем поведение моков
        repo.find_by_id.return_value = Order(id=1, amount=1000)
        payment_gateway.charge.return_value = "tx-12345"
        
        # Создаем сервис и вызываем метод
        service = OrderService(repo, payment_gateway)
        result = service.pay(1)
        
        # Проверки - ВСЕ ПРОХОДЯТ, хотя код содержит ошибки!
        self.assertEqual(result, "tx-12345")
        repo.find_by_id.assert_called_once_with(1)
        payment_gateway.charge.assert_called_once_with(total=1000, curr="RUB")
        MockAuditClient.assert_called_once_with("https://audit.local")
        MockAuditClient.return_value.write.assert_called_once()
        
        print("✅ Тест на plain mock ПРОШЕЛ - хотя production-код сломан!")


class TestOrderServiceAutospec(unittest.TestCase):
    """Тесты с autospec - вскрывают реальные ошибки"""
    
    @patch("order_service.AuditClient", autospec=True)
    def test_pay_with_autospec_catches_errors(self, MockAuditClient):
        # Используем create_autospec для строгих моков
        repo = create_autospec(OrderRepo, instance=True)
        payment_gateway = create_autospec(PaymentGateway, instance=True)
        
        # Настраиваем поведение
        repo.get.return_value = Order(id=1, amount=1000)
        payment_gateway.charge.return_value = "tx-12345"
        
        # Создаем сервис
        service = OrderService(repo, payment_gateway)
        
        # Ожидаем, что вызов упадет с ошибкой
        with self.assertRaises(AttributeError) as context:
            service.pay(1)
        
        print(f"✅ Autospec поймал ошибку: {context.exception}")


if __name__ == "__main__":
    unittest.main()