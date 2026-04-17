def parse_port(value: int|str):
    """Преобразует value в номер порта (int) и валидирует диапазон."""
    if type(value) != str and type(value) != int:
        raise TypeError("Передан не допустимый тип данных")
    elif type(value) == str:
        value = value.strip()
        if not value.isdigit():
            raise ValueError("Введено не число")
        value = int(value)
    if 0 > value or value > 65535:
        raise ValueError("Значение не может быть меньше 0 и больше 65535")
    return True


# print(parse_port(122220)) 1760591 1760810 1760858