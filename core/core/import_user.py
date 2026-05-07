# core/import_user.py
from dataclasses import dataclass
from typing import Dict
from .interfaces import UserGateway, Clock, AuditLog

def normalize_user(raw: Dict, imported_at: str) -> Dict:
    """Pure function - no side effects, easily testable with assertEqual"""
    return {
        "id": raw["id"],
        "name": raw["name"].strip(),
        "email": raw["email"].lower(),
        "imported_at": imported_at,
    }

@dataclass
class ImportUserService:
    """Use case with explicit dependencies"""
    gateway: UserGateway
    clock: Clock
    audit_log: AuditLog
    
    def import_user(self, user_id: int) -> Dict:
        raw = self.gateway.fetch_user(user_id)
        user = normalize_user(raw, self.clock.now_iso())
        self.audit_log.record_import(user_id)
        return user