#!/usr/bin/env python3
import sys
import os
import subprocess

# Получаем директорию, где находится ЭТОТ скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"📁 Скрипт находится в: {script_dir}")

# Переходим в директорию скрипта
os.chdir(script_dir)
print(f"📁 Рабочая директория: {os.getcwd()}\n")

# Проверяем, что файлы на месте
if not os.path.exists("app/user_profile.py"):
    print(f"❌ Ошибка: файл app/user_profile.py не найден в {os.getcwd()}")
    print("Содержимое текущей папки:")
    for item in os.listdir("."):
        print(f"  - {item}")
    sys.exit(1)

print("✅ Все файлы найдены!\n")

def run_test(test_name, description, flags=""):
    """Запускает тест"""
    print(f"\n{'='*70}")
    print(f"📋 {description}")
    print(f"{'='*70}\n")
    
    cmd = f'python -m unittest {test_name} {flags}'
    print(f"💻 {cmd}\n")
    
    result = subprocess.run(cmd, shell=True)
    return result.returncode

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     🧪 Практика: От красного набора к зелёному и быстрому    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Этап 1: Плохие тесты
    run_test(
        "tests.test_user_profile_initial",
        "🔴 ЭТАП 1: Плохие тесты (шумные, медленные)",
        "-v"
    )
    
    input("\n⏸️ Нажмите Enter для продолжения...")
    
    # Этап 2: С улучшенной диагностикой
    run_test(
        "tests.test_user_profile_initial",
        "🟡 ЭТАП 2: Улучшенная диагностика с -b и --locals",
        "-b --locals -v"
    )
    
    input("\n⏸️ Нажмите Enter для продолжения...")
    
    # Этап 3: Улучшенные тесты
    print("\n⚠️ ВНИМАНИЕ: В production-коде есть баг!\n")
    
    run_test(
        "tests.test_user_profile_improved",
        "🟠 ЭТАП 3: Улучшенные тесты (показывают точную причину)",
        "-b --locals -v"
    )
    
    print("\n" + "="*70)
    print("🔧 ТЕПЕРЬ ИСПРАВЬТЕ БАГ В КОДЕ:")
    print("="*70)
    print("Откройте файл: app/user_profile.py")
    print("Найдите строку: role = payload.get('role', 'user').upper()")
    print("Замените на:     role = payload.get('role', 'user').lower()")
    print("="*70)
    
    input("\n⏸️ Нажмите Enter ПОСЛЕ того, как исправили баг...")
    
    # Этап 4: После исправления
    run_test(
        "tests.test_user_profile_improved",
        "🟢 ЭТАП 4: Тесты после исправления бага",
        "-b --locals -v"
    )
    
    input("\n⏸️ Нажмите Enter для запуска быстрых тестов...")
    
    # Этап 5: Быстрые тесты
    run_test(
        "tests.test_user_profile_final",
        "⚡ ЭТАП 5: Быстрые тесты с моками",
        "-b --locals -v"
    )
    
    print("\n" + "="*70)
    print("🎉 ПРАКТИКА УСПЕШНО ЗАВЕРШЕНА!")
    print("="*70)

if __name__ == "__main__":
    main()