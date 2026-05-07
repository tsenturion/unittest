# bootstrap.py
import os
from infrastructure.adapters import HttpUserGateway, SystemClock, FileAuditLog
from core.import_user import ImportUserService

def build_import_user_service() -> ImportUserService:
    """Wire all dependencies together - this is where configuration lives"""
    token = os.getenv("API_TOKEN")
    if not token:
        raise RuntimeError("API_TOKEN is required")
    
    return ImportUserService(
        gateway=HttpUserGateway(token),
        clock=SystemClock(),
        audit_log=FileAuditLog("audit.log"),
    )