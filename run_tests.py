#!/usr/bin/env python
import sys
import os

# Добавляем текущую папку в путь поиска модулей
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f"Python path includes: {current_dir}")
print(f"Current working directory: {os.getcwd()}")
print()

# Проверяем, что модуль app доступен
try:
    import app
    print("✓ Module 'app' found successfully")
except ImportError as e:
    print(f"✗ Module 'app' not found: {e}")
    sys.exit(1)

# Запускаем тесты
import unittest

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Running tests...")
    print("="*60 + "\n")
    
    # Загружаем все тесты из папки tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    
    # Запускаем с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим итог
    print("\n" + "="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60)
    
    # Возвращаем код ошибки если тесты не прошли
    sys.exit(0 if result.wasSuccessful() else 1)