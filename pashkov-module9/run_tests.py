# run_tests.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_all_tests():
    print("=" * 60)
    print("ЗАПУСК ВСЕХ ТЕСТОВ")
    print("=" * 60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.discover('tests', pattern='test_*.py'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)