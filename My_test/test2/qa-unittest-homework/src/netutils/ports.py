def parse_port(value):
    """Преобразует value в номер порта (int) и валидирует диапазон."""
    # Проверяем тип входных данных (bool должен быть исключен, т.к. bool это подкласс int)
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise TypeError(f"Expected int, float, or str, got {type(value).__name__}")
    
    # Преобразуем в число
    try:
        if isinstance(value, str):
            if not value.strip():
                raise ValueError("Empty string cannot be converted to port number")
            num_value = int(value)
        elif isinstance(value, float):
            if value != int(value):  # Проверяем, есть ли дробная часть
                raise ValueError("Float values with decimal part are not allowed")
            num_value = int(value)
        else:  # int
            num_value = value
    except ValueError:
        raise ValueError(f"Cannot convert '{value}' to integer port number")
    
    # Проверяем диапазон
    if num_value < 0 or num_value > 65535:
        raise ValueError(f"Port number {num_value} is out of range [0, 65535]")
    
    return num_value