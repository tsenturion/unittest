# src/shipping/pricing.py

ZONES = {"local", "domestic", "intl"}


def shipping_price_cents(weight_g: int, zone: str, express: bool = False) -> int:
    """
    Рассчитывает цену доставки.

    Контракт:
    - weight_g: int, 1..30000 включительно
    - zone: "local" | "domestic" | "intl"
    - express: bool, если True — +30% к промежуточной сумме (округление вверх)
    """
    if isinstance(weight_g, bool) or not isinstance(weight_g, int):
        raise TypeError("weight_g must be int")
    if not isinstance(zone, str):
        raise TypeError("zone must be str")
    if not isinstance(express, bool):
        raise TypeError("express must be bool")

    if weight_g < 1 or weight_g > 30_000:
        raise ValueError("weight_g out of range")
    if zone not in ZONES:
        raise ValueError("unknown zone")

    base = {"local": 500, "domestic": 900, "intl": 2500}[zone]

    if weight_g <= 500:
        surcharge = 0
    elif weight_g <= 2_000:
        surcharge = 200
    elif weight_g <= 10_000:
        surcharge = 700
    else:
        surcharge = 1500

    subtotal = base + surcharge

    if express:
        subtotal += (subtotal * 30 + 99) // 100  # +30%, округление вверх

    return subtotal