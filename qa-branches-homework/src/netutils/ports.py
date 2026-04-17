# src/netutils/ports.py - ПОЛНАЯ РЕАЛИЗАЦИЯ

def parse_port(value):
    """
    Преобразует value в номер порта (int) и валидирует диапазон.
    """
    # Ветвь 1: bool должен быть отвергнут ДО проверки на int
    if isinstance(value, bool):
        raise TypeError(f"Unsupported type: {type(value).__name__}. Port must be int or str.")
    
    # Ветвь 2: обработка int
    if isinstance(value, int):
        if 1 <= value <= 65535:
            return value
        else:
            raise ValueError(f"Port number must be in range 1..65535, got {value}")
    
    # Ветвь 3: обработка str
    if isinstance(value, str):
        stripped = value.strip()
        
        if not stripped:
            raise ValueError("Empty string or whitespace only is not a valid port")
        
        if not stripped.isdigit():
            raise ValueError(f"String must contain only digits, got '{value}'")
        
        port = int(stripped)
        
        if 1 <= port <= 65535:
            return port
        else:
            raise ValueError(f"Port number must be in range 1..65535, got {port}")
    
    # Ветвь 4: все остальные типы
    raise TypeError(f"Unsupported type: {type(value).__name__}. Port must be int or str.")
