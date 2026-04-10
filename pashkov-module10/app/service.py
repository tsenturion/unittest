from datetime import datetime, timezone

from app.client import CatalogClient
from app.config import load_config


def normalize_product(payload: dict, fetched_at: str) -> dict:
    """Нормализует данные товара в единый формат"""
    return {
        "id": payload["id"],
        "name": payload["name"].strip(),
        "price": payload["price"],
        "currency": payload.get("currency", "USD"),
        "in_stock": bool(payload.get("in_stock", False)),
        "fetched_at": fetched_at,
    }


def build_product_snapshot(config_path: str, product_id: int) -> dict:
    """
    Основная оркестрирующая функция:
    1. Читает конфиг
    2. Создаёт клиента
    3. Запрашивает данные товара
    4. Добавляет временную метку
    5. Нормализует и возвращает результат
    """
    cfg = load_config(config_path)

    client = CatalogClient(
        base_url=cfg["base_url"],
        api_key=cfg["api_key"],
        timeout=cfg.get("timeout", 3),
    )

    payload = client.fetch_product(product_id)
    fetched_at = datetime.now(timezone.utc).isoformat()
    return normalize_product(payload, fetched_at)