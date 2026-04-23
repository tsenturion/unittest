import io
import sqlite3
import unittest
from pathlib import Path

from tests.demo_suite import (
    TMP_DIRS, CONNS,
    InnerPass, InnerFail, InnerError, InnerSetupError
)


class TestCleanupProof(unittest.TestCase):
    """Доказательство гарантированной очистки ресурсов"""
    
    def setUp(self):
        """Очищаем глобальные коллекции перед каждым тестом"""
        TMP_DIRS.clear()
        CONNS.clear()
    
    def test_cleanup_on_success_fail_error_and_setup_error(self):
        # 1. Собираем внутренний набор тестов
        suite = unittest.TestSuite()
        loader = unittest.defaultTestLoader
        
        suite.addTests(loader.loadTestsFromTestCase(InnerPass))
        suite.addTests(loader.loadTestsFromTestCase(InnerFail))
        suite.addTests(loader.loadTestsFromTestCase(InnerError))
        suite.addTests(loader.loadTestsFromTestCase(InnerSetupError))
        
        # 2. Запускаем внутренний набор
        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=0)
        result = runner.run(suite)
        
        # 3. Проверяем, что были FAIL и ERROR
        self.assertGreaterEqual(
            len(result.failures), 1,
            f"Должен быть хотя бы один FAIL. Получено failures: {len(result.failures)}"
        )
        self.assertGreaterEqual(
            len(result.errors), 1,
            f"Должна быть хотя бы одна ERROR. Получено errors: {len(result.errors)}"
        )
        
        # 4. ПРОВЕРКА ФАЙЛОВОЙ СИСТЕМЫ
        # Проверяем, что все директории были очищены (cleaned_flag == True)
        not_cleaned = []
        for path, cleaned in TMP_DIRS:
            if not cleaned:
                # Если флаг очистки False, проверяем физически
                if Path(path).exists():
                    not_cleaned.append(path)
        
        self.assertEqual(
            not_cleaned, [],
            f"Директории не были очищены: {not_cleaned}"
        )
        
        # 5. ПРОВЕРКА СОЕДИНЕНИЙ БД
        # Проверяем, что все соединения были закрыты
        not_closed = []
        for conn, closed in CONNS:
            if not closed:
                # Если флаг закрытия False, проверяем состояние соединения
                try:
                    conn.execute("SELECT 1")
                    not_closed.append(str(conn))
                except sqlite3.ProgrammingError:
                    # Соединение закрыто, но флаг не обновлен - обновляем
                    pass
        
        self.assertEqual(
            not_closed, [],
            f"Соединения не были закрыты: {not_closed}"
        )
        
        # 6. Статистика
        print(f"\n✅ Доказательство очистки:")
        print(f"   - Всего директорий создано: {len(TMP_DIRS)}")
        print(f"   - Всего соединений создано: {len(CONNS)}")
        print(f"   - Внутренних FAIL: {len(result.failures)}")
        print(f"   - Внутренних ERROR: {len(result.errors)}")
        print(f"   - Успешно очищено директорий: {sum(1 for _, c in TMP_DIRS if c)}")
        print(f"   - Успешно закрыто соединений: {sum(1 for _, c in CONNS if c)}")
    
    def test_individual_resource_isolation(self):
        """Проверяет, что ресурсы изолированы между тестами"""
        TMP_DIRS.clear()
        CONNS.clear()
        
        suite = unittest.TestSuite()
        loader = unittest.defaultTestLoader
        suite.addTests(loader.loadTestsFromTestCase(InnerPass))
        
        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=0)
        result = runner.run(suite)
        
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(len(result.errors), 0)
        
        # Проверяем, что ресурсы были очищены
        for path, cleaned in TMP_DIRS:
            self.assertTrue(cleaned, f"Директория {path} не была очищена")
            self.assertFalse(Path(path).exists(), f"Директория {path} физически существует")
        
        for conn, closed in CONNS:
            self.assertTrue(closed, f"Соединение {conn} не было закрыто")
            with self.assertRaises(sqlite3.ProgrammingError):
                conn.execute("SELECT 1")


class TestEdgeCases(unittest.TestCase):
    """Дополнительные тесты для граничных случаев"""
    
    def test_cleanup_order_lifo(self):
        """Проверяем порядок вызова cleanup функций (LIFO)"""
        cleanup_log = []
        
        class TestOrder(unittest.TestCase):
            def setUp(self):
                self.addCleanup(lambda: cleanup_log.append("first"))
                self.addCleanup(lambda: cleanup_log.append("second"))
                self.addCleanup(lambda: cleanup_log.append("third"))
            
            def test_dummy(self):
                pass
        
        suite = unittest.TestSuite()
        suite.addTest(TestOrder('test_dummy'))
        
        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=0)
        runner.run(suite)
        
        self.assertEqual(cleanup_log, ['third', 'second', 'first'])
    
    def test_cleanup_happens_even_on_setup_error(self):
        """Специальный тест: проверяем очистку при ошибке в setUp"""
        cleanup_called = []
        
        class TestWithSetupError(unittest.TestCase):
            def setUp(self):
                # Создаем ресурс
                self.tmp = tempfile.TemporaryDirectory()
                self.addCleanup(lambda: cleanup_called.append(True))
                self.addCleanup(lambda: self.tmp.cleanup())
                # Ошибка после регистрации cleanup
                raise RuntimeError("Setup error")
            
            def test_nothing(self):
                pass
        
        suite = unittest.TestSuite()
        suite.addTest(TestWithSetupError('test_nothing'))
        
        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=0)
        result = runner.run(suite)
        
        # Проверяем, что cleanup был вызван, несмотря на ошибку в setUp
        self.assertTrue(cleanup_called, "Cleanup не был вызван при ошибке в setUp!")
        self.assertEqual(len(result.errors), 1, "Должна быть зарегистрирована ошибка")


class TestResourceTracking(unittest.TestCase):
    """Тесты для проверки механизма отслеживания ресурсов"""
    
    def test_tracking_mechanism_works(self):
        """Проверяем, что механизм отслеживания работает корректно"""
        TMP_DIRS.clear()
        CONNS.clear()
        
        # Создаем временный тест
        class TrackingTest(_BaseWithResources):
            def test_track(self):
                # Проверяем, что ресурсы зарегистрированы
                self.assertGreater(len(TMP_DIRS), 0)
                self.assertGreater(len(CONNS), 0)
                
                # Проверяем, что флаги очистки еще False
                for _, cleaned in TMP_DIRS:
                    self.assertFalse(cleaned)
                for _, closed in CONNS:
                    self.assertFalse(closed)
        
        suite = unittest.TestSuite()
        suite.addTest(TrackingTest('test_track'))
        
        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=0)
        result = runner.run(suite)
        
        # После выполнения теста все должно быть очищено
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(len(result.errors), 0)
        
        # Проверяем, что все ресурсы отмечены как очищенные
        for _, cleaned in TMP_DIRS:
            self.assertTrue(cleaned)
        for _, closed in CONNS:
            self.assertTrue(closed)
