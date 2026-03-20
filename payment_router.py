import os


def choose_payment_mode() -> str:
    dry_run = os.getenv("PAYMENT_DRY_RUN", "0")
    if dry_run == "1":
        return "dry-run"
    
    env = os.getenv("PAYMENT_ENV", "prod")
    
    if env in ("dev", "test"):
        return "sandbox"
    elif env == "prod":
        return "gateway"
    else:
        raise ValueError(f"unsupported payment env: {env}")


def charge_order(amount: int, sandbox_client, gateway_client) -> str:
    mode = choose_payment_mode()
    
    if mode == "dry-run":
        return "skipped"
    
    if mode == "sandbox":
        sandbox_client.charge(amount)
        return "sandbox"
    
    gateway_client.charge(amount)
    return "gateway"