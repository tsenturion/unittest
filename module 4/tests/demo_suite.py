import sqlite3
import tempfile
import unittest
from pathlib import Path

# Глобальные коллекции для отслеживания ресурсов
# Теперь храним кортежи (путь, был_ли_очищен)
TMP_DIRS: list[tuple[str, bool]] = []  # (path, cleaned_flag)
CONNS: list[tuple[sqlite3.Connection, bool]] = []  # (connection, cleaned_flag)


class _BaseWithResources(unittest.TestCase):
    """Базовый класс с гарантированной очисткой ресурсов"""
    
    def setUp(self):
        # 1. Временная директория
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        TMP_DIRS.append((self.tmp_path, False))  # Пока не очищена
        self.addCleanup(self._cleanup_tmp_directory)
        
        # 2. Тестовый файл
        self.test_file = self.tmp_path / "test.txt"
        self.test_file.write_text("initial data", encoding="utf-8")
        
        # 3. SQLite соединение
        self.conn = sqlite3.connect(":memory:")
        CONNS.append((self.conn, False))  # Пока не закрыто
        self.addCleanup(self._cleanup_database_connection)
        
        # 4. Инициализация БД
        self.conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        self.conn.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob')")
        self.conn.commit()
    
    def _cleanup_tmp_directory(self):
        """Очистка временной директории"""
        if hasattr(self, '_tmp'):
            try:
                self._tmp.cleanup()
                # Обновляем статус в глобальном списке
                for i, (path, _) in enumerate(TMP_DIRS):
                    if path == self.tmp_path:
                        TMP_DIRS[i] = (path, True)
                        break
            except Exception as e:
                print(f"Cleanup error for {self.tmp_path}: {e}")
    
    def _cleanup_database_connection(self):
        """Закрытие соединения с БД"""
        if hasattr(self, 'conn'):
            try:
                self.conn.close()
                # Обновляем статус в глобальном списке
                for i, (conn, _) in enumerate(CONNS):
                    if conn == self.conn:
                        CONNS[i] = (conn, True)
                        break
            except Exception as e:
                print(f"DB cleanup error: {e}")
    
    def _get_user_count(self) -> int:
        cursor = self.conn.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]


class InnerPass(_BaseWithResources):
    def test_success_scenario(self):
        self.assertTrue(self.test_file.exists())
        self.assertEqual(self.test_file.read_text(encoding="utf-8"), "initial data")
        self.assertEqual(self._get_user_count(), 2)
        
        self.test_file.write_text("modified", encoding="utf-8")
        self.conn.execute("INSERT INTO users (name) VALUES ('Charlie')")
        
        self.assertEqual(self.test_file.read_text(encoding="utf-8"), "modified")
        self.assertEqual(self._get_user_count(), 3)


class InnerFail(_BaseWithResources):
    def test_fail_scenario(self):
        self.assertTrue(self.test_file.exists())
        self.assertEqual(self._get_user_count(), 2)
        self.assertEqual(1, 2, "Это намеренный FAIL для проверки очистки")


class InnerError(_BaseWithResources):
    def test_error_scenario(self):
        self.test_file.write_text("data before error", encoding="utf-8")
        self.conn.execute("INSERT INTO users (name) VALUES ('ErrorUser')")
        self.conn.commit()
        raise RuntimeError("Это намеренный ERROR для проверки очистки")


class InnerSetupError(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        TMP_DIRS.append((self._tmp.name, False))
        self.addCleanup(self._cleanup_tmp_directory)
        
        self.test_file = Path(self._tmp.name) / "precious.txt"
        self.test_file.write_text("This file should be cleaned up!", encoding="utf-8")
        
        self.conn = sqlite3.connect(":memory:")
        CONNS.append((self.conn, False))
        self.addCleanup(self._cleanup_database_connection)
        
        self.conn.execute("CREATE TABLE test (data TEXT)")
        self.conn.execute("INSERT INTO test VALUES ('setup data')")
        
        raise RuntimeError("Ошибка в setUp() после захвата ресурсов")
    
    def _cleanup_tmp_directory(self):
        if hasattr(self, '_tmp'):
            try:
                self._tmp.cleanup()
                for i, (path, _) in enumerate(TMP_DIRS):
                    if path == self._tmp.name:
                        TMP_DIRS[i] = (path, True)
                        break
            except Exception as e:
                print(f"Cleanup error: {e}")
    
    def _cleanup_database_connection(self):
        if hasattr(self, 'conn'):
            try:
                self.conn.close()
                for i, (conn, _) in enumerate(CONNS):
                    if conn == self.conn:
                        CONNS[i] = (conn, True)
                        break
            except Exception as e:
                print(f"DB cleanup error: {e}")
    
    def test_never_runs(self):
        self.assertTrue(False)
