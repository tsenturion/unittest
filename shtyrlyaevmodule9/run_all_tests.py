# run_all_tests.py
import unittest

if __name__ == "__main__":
    # Загружаем все тесты
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем тесты
    from tests.test_order_service import TestOrderServicePlainMock, TestOrderServiceAutospec
    from tests.test_order_service_fixed import TestOrderServiceFinal
    
    suite.addTests(loader.loadTestsFromTestCase(TestOrderServicePlainMock))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderServiceAutospec))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderServiceFinal))
    
    # Запускаем с детализацией
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)