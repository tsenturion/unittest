from __future__ import annotations

import argparse
import fnmatch
import sys
import unittest
from pathlib import Path
from typing import Iterable, List, Optional


def _iter_cases(suite: unittest.TestSuite) -> Iterable[unittest.TestCase]:
    """
    Разворачивает вложенные TestSuite в плоский список TestCase.
    
    Args:
        suite: TestSuite или TestCase
        
    Yields:
        Отдельные тестовые кейсы
    """
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _iter_cases(item)
        else:
            yield item


def _match_k(test_id: str, patterns: List[str]) -> bool:
    """
    Реализует логику фильтрации -k как в unittest.
    
    Args:
        test_id: Полное имя теста (например, tests.unit.pricing_spec.TestFinalPrice.test_discount)
        patterns: Список паттернов для фильтрации
        
    Returns:
        True если тест должен быть включен
    """
    if not patterns:
        return True
    
    for pattern in patterns:
        if '*' in pattern:
            # Используем fnmatch для wildcard
            if fnmatch.fnmatchcase(test_id, pattern):
                return True
        else:
            # Простое вхождение подстроки
            if pattern in test_id:
                return True
    return False


def build_suite(
    start_dir: str,
    pattern: str,
    top_level_dir: Optional[str],
    k_patterns: List[str]
) -> unittest.TestSuite:
    """
    Строит TestSuite с поддержкой фильтрации -k.
    
    Args:
        start_dir: Директория для начала discovery
        pattern: Glob-паттерн для файлов тестов
        top_level_dir: Верхнеуровневая директория (для импортов)
        k_patterns: Паттерны для фильтрации
        
    Returns:
        Отфильтрованный TestSuite
    """
    # Конвертируем пути в абсолютные для надежности
    start_path = Path(start_dir).resolve()
    top_path = Path(top_level_dir).resolve() if top_level_dir else start_path.parent
    
    # Создаем loader и запускаем discovery
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=str(start_path),
        pattern=pattern,
        top_level_dir=str(top_path)
    )
    
    # Применяем фильтрацию если нужно
    if not k_patterns:
        return suite
    
    filtered = unittest.TestSuite()
    for case in _iter_cases(suite):
        if _match_k(case.id(), k_patterns):
            filtered.addTest(case)
    
    return filtered


def main(argv: Optional[List[str]] = None) -> int:
    """
    Главная функция запуска тестов.
    
    Args:
        argv: Аргументы командной строки
        
    Returns:
        Код возврата (0 = успех, 1 = ошибка)
    """
    parser = argparse.ArgumentParser(
        description="Project test runner with unittest discovery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  # Запуск всех unit-тестов
  %(prog)s -v
  
  # Запуск только тестов со скидками
  %(prog)s -k discount -v
  
  # Запуск integration-тестов
  %(prog)s -s tests/integration -p "*_it.py" -v
  
  # Запуск с остановкой на первой ошибке
  %(prog)s -k invalid -v -f
  
  # Показать 10 самых медленных тестов
  %(prog)s -v --durations 10
        """
    )
    
    # Параметры discovery
    parser.add_argument(
        "-s", "--start-dir",
        default="tests/unit",
        help="Start directory for discovery (default: tests/unit)"
    )
    parser.add_argument(
        "-p", "--pattern",
        default="*_spec.py",
        help="File pattern for tests (default: *_spec.py)"
    )
    parser.add_argument(
        "-t", "--top-level-dir",
        default=".",
        help="Top-level project directory (default: .)"
    )
    
    # Параметры фильтрации
    parser.add_argument(
        "-k",
        action="append",
        default=[],
        help="Filter tests by substring or fnmatch pattern (can be repeated)"
    )
    
    # Параметры запуска
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v, -vv)"
    )
    parser.add_argument(
        "-f", "--failfast",
        action="store_true",
       help="Stop on first failure or error"
    )
    parser.add_argument(
        "-b", "--buffer",
        action="store_true",
        help="Buffer stdout/stderr during tests"
    )
    parser.add_argument(
        "--locals",
        action="store_true",
        help="Show local variables in tracebacks"
    )
    parser.add_argument(
        "--durations",
        type=int,
        metavar="N",
        help="Show N slowest test cases"
    )
    
    args = parser.parse_args(argv)
    
    # Строим test suite
    print(f"🔍 Discovering tests in: {args.start_dir}")
    print(f"📁 Pattern: {args.pattern}")
    if args.k:
        print(f"🎯 Filtering by: {', '.join(args.k)}")
    
    suite = build_suite(
        start_dir=args.start_dir,
        pattern=args.pattern,
        top_level_dir=args.top_level_dir,
        k_patterns=args.k
    )
    
    # Проверяем, что нашлись тесты
    total_tests = suite.countTestCases()
    if total_tests == 0:
        print("⚠️  Warning: No tests found!")
        print("\nDebugging tips:")
        print("  1. Check that files match pattern:", args.pattern)
        print("  2. Verify __init__.py exists in test directories")
        print("  3. Run with -v to see discovery process")
        print("  4. Check file names are valid Python identifiers (no hyphens, no starting with numbers)")
        return 1
    
    print(f"✅ Found {total_tests} test(s)")
    print("🏃 Running tests...\n")
    
    # Настраиваем runner
    verbosity = 1 + args.verbose
    runner = unittest.TextTestRunner(
        verbosity=verbosity,
        failfast=args.failfast,
        buffer=args.buffer,
        tb_locals=args.locals
    )
    
    # Запускаем тесты
    result = runner.run(suite)
    
    # Показываем медленные тесты если запрошено
    if args.durations and hasattr(result, 'slowest_tests'):
        print(f"\n📊 {args.durations} slowest tests:")
        for test, duration in result.slowest_tests[:args.durations]:
            print(f"  {duration:.3f}s - {test}")
    
    # Возвращаем код возврата
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
