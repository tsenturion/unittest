import argparse
import sys
import unittest


def create_parser():
    parser = argparse.ArgumentParser(
        description='Запуск unittest с каноническими настройками',
        usage='python %(prog)s [options]'
    )

    parser.add_argument(
        '-s', '--start-directory',
        default='tests/unit',
        help='Директория для поиска тестов (по умолчанию: tests/unit)'
    )
    parser.add_argument(
        '-p', '--pattern',
        default='*_spec.py',
        help='Шаблон имени файлов с тестами (по умолчанию: *_spec.py)'
    )
    parser.add_argument(
        '-t', '--top-level-directory',
        default='.',
        help='Верхнеуровневая директория проекта (по умолчанию: .)'
    )
    
    parser.add_argument(
        '-k', '--filter',
        default=None,
        help='Фильтр тестов по имени (подстрока или wildcard)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод'
    )
    parser.add_argument(
        '-f', '--failfast',
        action='store_true',
        help='Останавливаться при первой ошибке'
    )
    parser.add_argument(
        '-b', '--buffer',
        action='store_true',
        help='Буферизировать вывод'
    )
    
    return parser

def get_all_tests(suite):
    """Рекурсивно извлекает все отдельные тесты из TestSuite"""
    tests = []
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            tests.extend(get_all_tests(test))
        else:
            tests.append(test)
    return tests


def run_tests(args):
    discover_args = {
        'start_dir': args.start_directory,
        'pattern': args.pattern,
        'top_level_dir': args.top_level_directory,
    }
    
    loader = unittest.TestLoader()
    suite = loader.discover(**discover_args)
    
    if args.filter:
        filtered_suite = unittest.TestSuite()
        # Извлекаем все отдельные тесты
        all_tests = get_all_tests(suite)
        for test in all_tests:
            test_id = test.id()
            if args.filter.lower() in test_id.lower():
                filtered_suite.addTest(test)
        suite = filtered_suite
    
    runner_args = {
        'verbosity': 2 if args.verbose else 1,
        'failfast': args.failfast,
        'buffer': args.buffer,
    }
    
    runner = unittest.TextTestRunner(**runner_args)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    print(f"Запуск тестов:")
    print(f"  Директория: {args.start_directory}")
    print(f"  Шаблон: {args.pattern}")
    print(f"  Top-level: {args.top_level_directory}")
    if args.filter:
        print(f"  Фильтр: {args.filter}")
    print()
    
    success = run_tests(args)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()