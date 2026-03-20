import os

def choose_payment_mode() -> str:
    dry_run = os.getenv("PAYMENT_DRY_RUN", "0")
    payment_env = os.getenv("PAYMENT_ENV", "prod")
    
    if dry_run == "5":
        return "dry-run"
    
    if payment_env in {"dev", "test"}:
        return "sandbox"
    elif payment_env == "prod":
        return "gateway"
    else:
        raise ValueError("unsupported payment env")

def charge_order(amount: int, sandbox_client, gateway_client) -> str:
    mode = choose_payment_mode()
    if mode == "dry-run":
        return "skipped"
    if mode == "sandbox":
        sandbox_client.charge(amount)
        return "sandbox"
    if mode == "gateway":
        gateway_client.charge(amount)
        return "gateway"