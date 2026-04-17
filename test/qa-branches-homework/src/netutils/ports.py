from typing import Union


def parse_port(value: Union[int, str]) -> int:
    
    if isinstance(value, bool):
        raise TypeError(f"Invalid type: {type(value).__name__}")
    
    if isinstance(value, int):
        port = value
    elif isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError(f"Empty string after strip: '{value}'")
        
        if not stripped.isdigit():
            raise ValueError(f"String contains non-digit characters: '{value}'")
        
        port = int(stripped)
    else:
        raise TypeError(f"Invalid type: {type(value).__name__}")

    if port < 1 or port > 65535:
        raise ValueError(f"Port {port} is out of range [1, 65535]")
    
    return port