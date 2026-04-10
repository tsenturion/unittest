import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_all_tests():
    print("=" * 60)
    print("ЗАПУСК ВСЕХ ТЕСТОВ МИНИ-ПРОЕКТА")
    print("=" * 60)
    print()
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.discover('tests', pattern='test_*.py'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 60)
    print(f"ИТОГО: {result.testsRun} тестов")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Падений: {len(result.failures)}")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)