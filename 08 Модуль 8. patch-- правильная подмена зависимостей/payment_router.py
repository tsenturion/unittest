import os

def choose_payment_mode() -> str:
    
    dry_run = os.getenv("PAYMENT_DRY_RUN", "0")
    if dry_run == "1":
        return "dry-run"

    env = os.getenv("PAYMENT_ENV", "prod")
    if env == "prod":
        return "gateway"
    if env in ("dev", "test"):
        return "sandbox"
    raise ValueError("unsupported payment env")


def charge_order(amount: int, sandbox_client, gateway_client) -> str:
    
    mode = choose_payment_mode()

    if mode == "dry-run":
        return "skipped"

    if mode == "sandbox":
        sandbox_client.charge(amount)
        return "sandbox"

    # mode == "gateway"
    gateway_client.charge(amount)
    return "gateway"