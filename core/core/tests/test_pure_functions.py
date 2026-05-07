# tests/test_pure_functions.py
import unittest
from core.import_user import normalize_user

class TestNormalizeUser(unittest.TestCase):
    """Pure functions are the easiest to test - no mocks needed!"""
    
    def test_clean_name_and_email(self):
        raw = {"id": 1, "name": "  John  ", "email": "JOHN@EXAMPLE.COM"}
        result = normalize_user(raw, "2026-03-26T10:00:00")
        
        self.assertEqual(result["name"], "John")
        self.assertEqual(result["email"], "john@example.com")
    
    def test_preserves_id_and_timestamp(self):
        raw = {"id": 42, "name": "Jane", "email": "jane@test.com"}
        timestamp = "2026-03-26T10:00:00"
        result = normalize_user(raw, timestamp)
        
        self.assertEqual(result["id"], 42)
        self.assertEqual(result["imported_at"], timestamp)