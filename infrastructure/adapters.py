# infrastructure/adapters.py
from datetime import datetime, timezone
from pathlib import Path
import os
from core.interfaces import UserGateway, Clock, AuditLog

# Предположим, у нас есть HTTP-клиент
class ApiClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
    
    def fetch_user(self, user_id: int) -> dict:
        # Реальный HTTP-вызов
        return {"id": user_id, "name": " Test ", "email": "TEST@EXAMPLE.COM"}

class HttpUserGateway(UserGateway):
    def __init__(self, token: str):
        self._client = ApiClient(base_url="https://api.example.com", token=token)
    
    def fetch_user(self, user_id: int) -> dict:
        return self._client.fetch_user(user_id)

class SystemClock(Clock):
    def now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

class FileAuditLog(AuditLog):
    def __init__(self, path: str):
        self._path = Path(path)
    
    def record_import(self, user_id: int) -> None:
        self._path.write_text(f"imported:{user_id}\n", encoding="utf-8")