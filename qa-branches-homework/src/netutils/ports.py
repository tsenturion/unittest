def parse_port(value):
    """Преобразует value в номер порта (int) и валидирует диапазон 1..65535.

    Контракт:
    - Принимает int или str.
    - bool считается неверным типом (несмотря на subclass int).
    - None, float, list, dict и другие типы → TypeError.
    - int должен быть в диапазоне 1..65535 включительно, иначе ValueError.
    - str сначала strip(), затем должна состоять только из цифр, иначе ValueError.
    - После конвертации str → int проверяется диапазон 1..65535.
    """
    # Отдельная проверка на bool (важно, так как bool — подкласс int)
    if isinstance(value, bool):
        raise TypeError(f"bool недопустим: {value!r}")

    # Проверка типа int (исключая bool, уже отловленный)
    if isinstance(value, int):
        if 1 <= value <= 65535:
            return value
        raise ValueError(f"int вне диапазона 1..65535: {value}")

    # Проверка типа str
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError(f"строка пуста или состоит из пробелов: {value!r}")
        if not stripped.isdigit():
            raise ValueError(f"строка содержит нецифровые символы: {value!r}")
        port = int(stripped)
        if 1 <= port <= 65535:
            return port
        raise ValueError(f"число вне диапазона 1..65535: {port}")

    # Любой другой тип
    raise TypeError(f"неподдерживаемый тип: {type(value).__name__}")