def parse_port(value):
    if isinstance(value, bool):
        raise TypeError()

    if isinstance(value, int):
        if 1 <= value <= 65535:
            return value
        raise ValueError()

    if isinstance(value, str):
        value = value.strip()

        if not value.isdigit():
            raise ValueError()

        port = int(value)

        if 1 <= port <= 65535:
            return port

        raise ValueError()

    raise TypeError()

