import re

def slugify(text: str) -> str:
    """
    Преобразует строку в slug для URL.
    """
    if not text:
        return ""
    
    result = text.lower()
    
    result = re.sub(r'[\s_]+', '-', result)
    
    result = re.sub(r'[^a-z0-9-]', '', result)
    
    result = re.sub(r'-+', '-', result)
    
    result = result.strip('-')
    
    return result
