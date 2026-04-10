#!/usr/bin/env python3
"""
Скрипт для запуска тестов с различными опциями.
Демонстрирует использование командной строки unittest.
"""
import unittest
import sys


if __name__ == "__main__":
    print("=" * 70)
    print("ЗАПУСК ТЕСТОВ МОДУЛЯ КОНФИГУРАЦИИ")
    print("=" * 70)
    
    # Базовый запуск
    print("\n1. Обычный запуск (без медленных тестов):")
    print("-" * 50)
    unittest.main(module="test_config_parsing", argv=["", "discover"], exit=False)
    
    # Запуск с подробным выводом
    print("\n2. Запуск с подробным выводом (-v):")
    print("-" * 50)
    unittest.main(module="test_config_parsing", argv=["", "discover", "-v"], exit=False)
    
    # Информация о медленных тестах
    print("\n" + "=" * 70)
    print("КАК ЗАПУСТИТЬ МЕДЛЕННЫЕ ТЕСТЫ:")
    print("=" * 70)
    print("export RUN_SLOW=1  # Linux/Mac")
    print("set RUN_SLOW=1     # Windows")
    print("python -m unittest test_config_parsing.py -v")
    print("\nИЛИ")
    print("RUN_SLOW=1 python -m unittest test_config_parsing.py -v  # Linux/Mac")