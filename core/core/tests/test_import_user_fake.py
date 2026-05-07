# tests/test_import_user_fake.py
import unittest
from core.import_user import ImportUserService

class FakeGateway:
    def __init__(self, raw):
        self.raw = raw
        self.calls = []
    
    def fetch_user(self, user_id: int) -> dict:
        self.calls.append(user_id)
        return self.raw

class FixedClock:
    def __init__(self, value: str):
        self.value = value
    
    def now_iso(self) -> str:
        return self.value

class SpyAuditLog:
    def __init__(self):
        self.imported = []
    
    def record_import(self, user_id: int) -> None:
        self.imported.append(user_id)

class TestImportUserService(unittest.TestCase):
    def setUp(self):
        self.gateway = FakeGateway(
            {"id": 7, "name": " Alice ", "email": "ALICE@EXAMPLE.COM"}
        )
        self.clock = FixedClock("2026-03-26T10:00:00+00:00")
        self.audit_log = SpyAuditLog()
        self.service = ImportUserService(
            gateway=self.gateway,
            clock=self.clock,
            audit_log=self.audit_log,
        )
    
    def test_import_user_returns_normalized_payload(self):
        result = self.service.import_user(7)
        
        self.assertEqual(result, {
            "id": 7,
            "name": "Alice",
            "email": "alice@example.com",
            "imported_at": "2026-03-26T10:00:00+00:00",
        })
        self.assertEqual(self.gateway.calls, [7])
        self.assertEqual(self.audit_log.imported, [7])