import unittest
from unittest.mock import Mock, create_autospec
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from order_service_fixed import PaymentGateway


class TestAutospecVsPlain(unittest.TestCase):
    """Демонстрация разницы между plain Mock и autospec"""
    
    def test_plain_mock_too_forgiving(self):
        """Plain Mock не ловит ошибки"""
        gateway = Mock()
        gateway.non_existent_method.return_value = "fake"
        
        result = gateway.non_existent_method("arg")
        self.assertEqual(result, "fake")  
        print("\n✅ Plain Mock позволил вызвать несуществующий метод")
    
    def test_autospec_catches_wrong_method(self):
        """autospec не даёт вызывать несуществующие методы"""
        gateway = create_autospec(PaymentGateway, instance=True)
        
        with self.assertRaises(AttributeError):
            gateway.non_existent_method("arg")
        print("\n✅ autospec поймал вызов несуществующего метода")
    
    def test_autospec_catches_wrong_signature(self):
        """autospec проверяет сигнатуру"""
        gateway = create_autospec(PaymentGateway, instance=True)
        
        with self.assertRaises(TypeError):
            gateway.charge(amount=100, wrong_param="something")
        print("\n✅ autospec поймал неправильный keyword-аргумент")
    
    def test_autospec_catches_wrong_positional_args(self):
        """autospec проверяет количество аргументов"""
        gateway = create_autospec(PaymentGateway, instance=True)
        
        with self.assertRaises(TypeError):
            gateway.charge(100, "USD", "extra_arg")
        print("\n✅ autospec поймал лишний аргумент")

if __name__ == "__main__":
    unittest.main()