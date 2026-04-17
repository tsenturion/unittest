"""Модуль с функцией расчета финальной цены."""

from typing import Union


def final_price_cents(
    base_cents: int, discount_percent: int = 0, tax_percent: int = 20
) -> int:
    """
    Рассчитывает финальную цену в центах с учетом скидки и налога.
    
    Контракт:
    - base_cents: int, >= 0
    - discount_percent: int, 0..100
    - tax_percent: int, 0..100
    
    Логика:
    - discount применяется к base
    - затем добавляется tax
    - результат округляется до целых центов (int)
    
    """
    # Проверка типов
    if not isinstance(base_cents, int):
        raise TypeError(f"base_cents must be int, got {type(base_cents).__name__}")
    if not isinstance(discount_percent, int):
        raise TypeError(f"discount_percent must be int, got {type(discount_percent).__name__}")
    if not isinstance(tax_percent, int):
        raise TypeError(f"tax_percent must be int, got {type(tax_percent).__name__}")
    
    # Проверка значений
    if base_cents < 0:
        raise ValueError(f"base_cents must be >= 0, got {base_cents}")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError(f"discount_percent must be in [0, 100], got {discount_percent}")
    if tax_percent < 0 or tax_percent > 100:
        raise ValueError(f"tax_percent must be in [0, 100], got {tax_percent}")
    

    after_discount = base_cents * (100 - discount_percent) / 100
    
    after_tax = after_discount * (100 + tax_percent) / 100

    result = int(round(after_tax))
    
    return result