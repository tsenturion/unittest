"""Slugify function for string transformation."""

import re


def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug.
    
    Args:
        text: Input string to convert
        
    Returns:
        Slugified string or empty string if no valid chars remain
    """
    if not text:
        return ""
    
    # 1. Приводим к нижнему регистру
    text = text.lower()
    
    # 2. Заменяем пробелы и подчеркивания на дефисы
    text = text.replace(' ', '-').replace('_', '-')
    
    # 3. Удаляем все символы, кроме латинских букв a-z, цифр 0-9 и дефиса
    # Точка (.) удаляется, так как не входит в разрешенные символы
    text = re.sub(r'[^a-z0-9-]', '', text)
    
    # 4. Схлопываем подряд идущие дефисы в один
    text = re.sub(r'-+', '-', text)
    
    # 5. Обрезаем дефисы в начале и в конце
    text = text.strip('-')
    
    return text