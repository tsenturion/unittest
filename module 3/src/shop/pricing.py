

from typing import Union, Optional


class PricingError(Exception):
    pass


def validate_percent(value: Union[int, float], name: str) -> int:

    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be int or float, got {type(value)}")
    
    if value < 0 or value > 100:
        raise ValueError(f"{name} must be between 0 and 100, got {value}")
    
    return int(value)


def final_price_cents(
    base_cents: Union[int, float, None],
    discount_percent: int = 0,
    tax_percent: int = 20
) -> int:

    # 1. Validate input types
    if base_cents is None:
        raise TypeError("base_cents cannot be None")
    
    if not isinstance(base_cents, (int, float)):
        raise TypeError(f"base_cents must be int or float, got {type(base_cents)}")
    
    # 2. Validate ranges
    if base_cents < 0:
        raise ValueError(f"base_cents must be >= 0, got {base_cents}")
    
    discount_percent = validate_percent(discount_percent, "discount_percent")
    tax_percent = validate_percent(tax_percent, "tax_percent")
    
    # 3. Apply discount
    discounted = base_cents * (100 - discount_percent) / 100
    
    # 4. Apply tax
    with_tax = discounted * (100 + tax_percent) / 100
    
    # 5. Round to nearest cent
    return int(round(with_tax))


def bulk_price_cents(items: list, discount_percent: int = 0) -> int:

    total = sum(price * quantity for price, quantity in items)
    return final_price_cents(total, discount_percent, 0)
