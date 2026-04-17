# run_tests.py
import subprocess
import sys

def run_command(cmd, description):
    print("\n" + "=" * 70)
    print(f"▶ {description}")
    print(f"  Команда: {cmd}")
    print("=" * 70)
    result = subprocess.run(cmd, shell=True, capture_output=False)
    return result.returncode

def main():
    print("🐍 Демонстрация unittest-диагностики")
    print("=" * 70)

    run_command(
        "python -m unittest discover -s tests -p '*_initial.py' -v",
        "ШАГ 1: Плохие тесты (шумные, без subTest, медленные)"
    )

    run_command(
        "python -m unittest discover -s tests -p '*_initial.py' -b -v",
        "ШАГ 2: Те же тесты, но с -b/--buffer (шум успешных тестов скрыт)"
    )

    run_command(
        "python -m unittest tests.test_user_profile_improved -v --locals",
        "ШАГ 3: Улучшенный тест (subTest + assertEqual) - показывает точную причину падения"
    )

    print("\n" + "=" * 70)
    print("⚠️  ВНИМАНИЕ: Баг в build_profile() ещё не исправлен!")
    print("   Чтобы исправить, замените .upper() на .lower() в строке 20 файла app/user_profile.py")
    print("   После исправления запустите тесты ещё раз.")
    print("=" * 70)

    input("\nНажмите Enter после исправления бага в коде...")

    run_command(
        "python -m unittest tests.test_user_profile_contracts -v",
        "ШАГ 5: Контрактные тесты (warnings + logs)"
    )

    run_command(
        "python -m unittest tests.test_user_profile_slow --durations=0 -v",
        "ШАГ 6: Измерение скорости - показываем все durations"
    )

    run_command(
        "python -m unittest tests.test_user_profile_fast -v",
        "ШАГ 7: Быстрые тесты (без реальных time.sleep)"
    )

    print("\n" + "=" * 70)
    print("✅ Демонстрация завершена!")
    print("\nКлючевые выводы:")
    print("  1. -b/--buffer убирает шум от успешных тестов")
    print("  2. --locals показывает локальные переменные в traceback")
    print("  3. subTest() + assertEqual() дают понятный diff и параметры кейса")
    print("  4. assertWarnsRegex/assertLogs фиксируют контракты")
    print("  5. --durations показывает самые медленные тесты")
    print("  6. Мокание времени ускоряет тесты на порядки")
    print("=" * 70)

if __name__ == "__main__":
    main()