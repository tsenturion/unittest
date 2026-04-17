import re


def slugify(text):
    # Привести к нижнему регистру
    text = text.lower()
    
    # Заменить пробелы и подчеркивания на дефисы
    text = re.sub(r'[ _]+', '-', text)
    
    # Удалить все символы, кроме латинских букв, цифр и дефиса
    text = re.sub(r'[^a-z0-9-]', '', text)
    
    # Схлопнуть подряд идущие дефисы в один
    text = re.sub(r'-+', '-', text)
    
    # Обрезать дефисы в начале и в конце
    text = text.strip('-')
    
    return text