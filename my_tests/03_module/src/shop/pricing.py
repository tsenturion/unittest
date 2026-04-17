

def final_price_cents(base_cents: int, discount_percent: int = 0, tax_percent: int = 20) -> int:
    if not isinstance(base_cents, int):
        raise TypeError("base_cents must be int")
    if base_cents < 0:
        raise ValueError("base_cents must be >= 0")

    if not isinstance(discount_percent, int) or not isinstance(tax_percent, int):
        raise TypeError("percent values must be int")

    if not (0 <= discount_percent <= 100):
        raise ValueError("discount_percent must be 0..100")

    if not (0 <= tax_percent <= 100):
        raise ValueError("tax_percent must be 0..100")

    discounted = base_cents * (1 - discount_percent / 100)
    taxed = discounted * (1 + tax_percent / 100)

    return int(round(taxed))