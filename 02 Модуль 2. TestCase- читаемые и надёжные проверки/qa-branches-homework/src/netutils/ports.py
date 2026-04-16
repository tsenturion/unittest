def parse_port(value):
    """Преобразует value в номер порта (int) и валидирует диапазон."""
    # Тип bool – отдельно, так как bool является подклассом int
    if isinstance(value, bool):
        raise TypeError("bool not allowed, expected int or str")
    if isinstance(value, int):
        if 1 <= value <= 65535:
            return value
        raise ValueError(f"Port number out of range 1..65535: {value}")
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped.isdigit():
            raise ValueError(f"Invalid port string: '{value}'")
        port = int(stripped)
        if 1 <= port <= 65535:
            return port
        raise ValueError(f"Port number out of range 1..65535: {port}")
    raise TypeError(f"Unsupported type: {type(value).__name__}, expected int or str")