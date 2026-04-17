# src/shop/pricing.py
def final_price_cents(
    base_cents: int, discount_percent: int = 0, tax_percent: int = 20
) -> int:
    """
    Контракт:
    - base_cents: int, >= 0
    - discount_percent: int, 0..100
    - tax_percent: int, 0..100
    Логика:
    - discount применяется к base
    - затем добавляется tax
    - результат округляется до целых центов (int)
    """
    if 0 >= base_cents:
        raise ValueError("base_cents должен быть больше 0")
    if 0 > discount_percent or discount_percent > 100:
        raise ValueError("discount_percent должен быть в диапазоне от 0 до 100")
    if 0 > tax_percent or tax_percent > 100:
        raise ValueError("tax_percent должен быть в диапазоне от 0 до 100")
    raise NotImplementedError