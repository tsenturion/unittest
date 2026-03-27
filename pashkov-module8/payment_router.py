# payment_router.py
import os


def choose_payment_mode() -> str:
    """Выбирает режим оплаты на основе переменных окружения."""
    dry_run = os.getenv("PAYMENT_DRY_RUN", "0")
    if dry_run == "1":
        return "dry-run"

    payment_env = os.getenv("PAYMENT_ENV", "prod")
    if payment_env in {"dev", "test"}:
        return "sandbox"
    if payment_env == "prod":
        return "gateway"

    # Если значение PAYMENT_ENV не поддерживается, выбрасываем исключение
    raise ValueError(f"unsupported payment env: {payment_env}")


def charge_order(amount: int, sandbox_client, gateway_client) -> str:
    """Обрабатывает оплату заказа в зависимости от выбранного режима."""
    mode = choose_payment_mode()

    if mode == "dry-run":
        return "skipped"
    if mode == "sandbox":
        sandbox_client.charge(amount)
        return "sandbox"
    if mode == "gateway":
        gateway_client.charge(amount)
        return "gateway"
    
    # Эта строка не должна быть достигнута, так как choose_payment_mode() выбросит исключение для неверных значений.
    return "unknown"