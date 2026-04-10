import subprocess
import time
import sys

def run_command(cmd, description, expected_exit_code=None):
    print(f"\n{'='*70}")
    print(f">>> {description}")
    print(f"Команда: {cmd}")
    print('='*70)
    
    start_time = time.time()
    result = subprocess.run(cmd, shell=True, capture_output=False)
    elapsed = time.time() - start_time
    
    print(f"\n  Время выполнения: {elapsed:.2f} секунд")

    if expected_exit_code is not None:
        if result.returncode == expected_exit_code:
            print(f" Код возврата {result.returncode} (ожидался {expected_exit_code})")
        else:
            print(f"  Код возврата {result.returncode} (ожидался {expected_exit_code})")
    
    return result.returncode

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║     ПОЛНЫЙ ЦИКЛ ТЕСТИРОВАНИЯ: от красного набора к ускорению     ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("\n ШАГ 1: Запуск плохих тестов с -b --locals")
    print("-" * 70)
    print("Ожидаем: падение, но с неинформативным сообщением 'False is not true'")
    
    run_command(
        "python -m unittest tests.test_user_profile_initial -b --locals -v",
        "Плохие тесты (неинформативное падение)",
        expected_exit_code=1
    )
    
    input("\n Нажмите Enter, чтобы продолжить к улучшенным тестам...")
    
    print("\n🟡 ШАГ 2: Запуск улучшенных тестов с -b --locals")
    print("-" * 70)
    print("Ожидаем: падение с подробным diff и указанием конкретного подслучая")
    
    run_command(
        "python -m unittest tests.test_user_profile -b --locals -v",
        "Улучшенные тесты (теперь видно, что именно упало)",
        expected_exit_code=1
    )
    
    input("\n Нажмите Enter, чтобы продолжить к измерению скорости...")
    
    print("\n ШАГ 3: Измерение скорости медленных тестов")
    print("-" * 70)
    print("Ожидаем: тесты с реальными sleep() занимают ~0.5-1 секунду")
    
    run_command(
        "python -m unittest tests.test_user_profile_initial.TestWaitUntilReadySlow -v",
        "Медленные тесты с реальными sleep()"
    )
    
    input("\n Нажмите Enter, чтобы продолжить к быстрым тестам...")
    
    print("\n ШАГ 4: Запуск быстрых тестов (с моками времени)")
    print("-" * 70)
    print("Ожидаем: тесты выполняются за миллисекунды вместо секунд")
    
    run_command(
        "python -m unittest tests.test_user_profile_fast -v",
        "Быстрые тесты без реальных задержек"
    )
    
    print("\n" + "="*70)
    print(" ПОЛНЫЙ ЦИКЛ ЗАВЕРШЕН!")
    print("="*70)
    
    print("\n КЛЮЧЕВЫЕ ВЫВОДЫ:")
    print("="*70)
    print("1.  -b/--buffer скрывает шум успешных тестов")
    print("2.  --locals показывает локальные переменные при падении")
    print("3.  subTest() + assertEqual() дают точную локализацию проблемы")
    print("4.   Для замера медленных тестов в Python 3.12+ есть --durations")
    print("5.  patch времени ускоряет тесты в сотни раз")
    print("6.  assertLogs() и assertWarnsRegex() проверяют контракты")
    print("="*70)

if __name__ == "__main__":
    main()