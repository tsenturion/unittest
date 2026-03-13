# payment_router.py
import os


def choose_payment_mode() -> str:
    """
    Определяет режим работы платежной системы на основе переменных окружения.
    
    Returns:
        "dry-run" - если PAYMENT_DRY_RUN == "1"
        "sandbox" - если PAYMENT_ENV в {"dev", "test"}
        "gateway" - если PAYMENT_ENV == "prod"
    
    Raises:
        ValueError: если PAYMENT_ENV содержит неподдерживаемое значение
    """
    # Проверяем dry-run режим (имеет высший приоритет)
    if os.getenv("PAYMENT_DRY_RUN", "0") == "1":
        return "dry-run"
    
    # Получаем окружение с дефолтным значением "prod"
    env = os.getenv("PAYMENT_ENV", "prod")
    
    # Определяем режим по окружению
    if env in {"dev", "test"}:
        return "sandbox"
    elif env == "prod":
        return "gateway"
    else:
        raise ValueError(f"unsupported payment env: {env}")


def charge_order(amount: int, sandbox_client, gateway_client) -> str:
    """
    Проводит оплату заказа в зависимости от выбранного режима.
    
    Args:
        amount: сумма заказа
        sandbox_client: клиент для тестового режима
        gateway_client: клиент для реального шлюза
    
    Returns:
        "skipped" - dry-run режим
        "sandbox" - оплата через sandbox
        "gateway" - оплата через реальный шлюз
    """
    mode = choose_payment_mode()
    
    if mode == "dry-run":
        return "skipped"
    
    if mode == "sandbox":
        sandbox_client.charge(amount)
        return "sandbox"
    
    if mode == "gateway":
        gateway_client.charge(amount)
        return "gateway"
    
    # Эта строка не должна достигаться, но для безопасности
    raise RuntimeError(f"unexpected mode: {mode}")