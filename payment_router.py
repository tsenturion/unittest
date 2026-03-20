import os


def choose_payment_mode() -> str:
    """
    Determine payment routing mode based on environment variables.
    
    Rules:
    - If PAYMENT_DRY_RUN == "1" -> "dry-run" (highest priority)
    - If PAYMENT_ENV in {"dev", "test"} -> "sandbox"
    - If PAYMENT_ENV == "prod" -> "gateway"
    - If PAYMENT_ENV is any other value -> ValueError
    
    Default: PAYMENT_ENV defaults to "prod", PAYMENT_DRY_RUN defaults to "0"
    """
    dry_run = os.getenv("PAYMENT_DRY_RUN", "0")
    payment_env = os.getenv("PAYMENT_ENV", "prod")
    
    # Highest priority: dry-run mode
    if dry_run == "1":
        return "dry-run"
    
    # Route based on environment
    if payment_env in {"dev", "test"}:
        return "sandbox"
    elif payment_env == "prod":
        return "gateway"
    else:
        raise ValueError(f"unsupported payment env: {payment_env}")


def charge_order(amount: int, sandbox_client, gateway_client) -> str:
    """
    Charge an order using the appropriate payment client.
    
    Args:
        amount: Amount to charge
        sandbox_client: Client with .charge(amount) method for test mode
        gateway_client: Client with .charge(amount) method for production mode
    
    Returns:
        str: The mode that was used ("skipped", "sandbox", or "gateway")
    """
    mode = choose_payment_mode()
    
    if mode == "dry-run":
        return "skipped"
    elif mode == "sandbox":
        sandbox_client.charge(amount)
        return "sandbox"
    elif mode == "gateway":
        gateway_client.charge(amount)
        return "gateway"
    else:
        # This should never happen with proper implementation
        raise RuntimeError(f"Unknown payment mode: {mode}")