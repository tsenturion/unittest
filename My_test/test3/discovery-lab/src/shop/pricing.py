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
    # Проверка контракта
    if not isinstance(base_cents, int) or base_cents < 0:
        raise ValueError("base_cents must be non-negative integer")
    if not isinstance(discount_percent, int) or not (0 <= discount_percent <= 100):
        raise ValueError("discount_percent must be integer between 0 and 100")
    if not isinstance(tax_percent, int) or not (0 <= tax_percent <= 100):
        raise ValueError("tax_percent must be integer between 0 and 100")
    
    # Расчет цены после скидки
    price_after_discount = base_cents * (100 - discount_percent) / 100.0
    # Применение налога
    total = price_after_discount * (100 + tax_percent) / 100.0
    # Округление до целых центов
    return int(round(total))