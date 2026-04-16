
def final_price_cents(
    base_cents: int, discount_percent: int = 0, tax_percent: int = 20
) -> int:
   
    # Проверки контракта (для тестирования исключений)
    if not isinstance(base_cents, int):
        raise TypeError("base_cents must be int")
    if not isinstance(discount_percent, int):
        raise TypeError("discount_percent must be int")
    if not isinstance(tax_percent, int):
        raise TypeError("tax_percent must be int")
    
    if base_cents < 0:
        raise ValueError("base_cents must be >= 0")
    if not (0 <= discount_percent <= 100):
        raise ValueError("discount_percent must be between 0 and 100")
    if not (0 <= tax_percent <= 100):
        raise ValueError("tax_percent must be between 0 and 100")
    
    # 1. применяем скидку
    discounted = base_cents * (100 - discount_percent) / 100
    # 2. добавляем налог
    with_tax = discounted * (100 + tax_percent) / 100
    # 3. округляем до ближайшего целого (стандартное округление)
    return int(round(with_tax))