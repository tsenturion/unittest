from datetime import datetime, timezone

from app.client import CatalogClient
from app.config import load_config

def normalize_product(payload: dict, fetched_at: str) -> dict:
    """Приводит сырые данные продукта к стандартному формату."""
    return {
        "id": payload["id"],
        "name": payload["name"].strip(),
        "price": payload["price"],
        "currency": payload.get("currency", "USD"),
        "in_stock": bool(payload.get("in_stock", False)),
        "fetched_at": fetched_at,
    }


def build_product_snapshot(config_path: str, product_id: int) -> dict:
    """Оркестрирует получение и нормализацию снимка продукта."""
    cfg = load_config(config_path)

    client = CatalogClient(
        base_url=cfg["base_url"],
        api_key=cfg["api_key"],
        timeout=cfg.get("timeout", 3),
    )

    payload = client.fetch_product(product_id)

    fetched_at = datetime.now(timezone.utc).isoformat()

    return normalize_product(payload, fetched_at)