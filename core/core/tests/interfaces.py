# core/interfaces.py
from typing import Protocol, Dict

class UserGateway(Protocol):
    def fetch_user(self, user_id: int) -> Dict:
        """Fetch raw user data from external source"""
        ...

class Clock(Protocol):
    def now_iso(self) -> str:
        """Return current time as ISO format string"""
        ...

class AuditLog(Protocol):
    def record_import(self, user_id: int) -> None:
        """Record user import event"""
        ...