import re

def slugify(text: str) -> str:
    #  Приводим к нижнему регистру
    text = text.lower()
    
    # Заменяем пробелы и подчёркивания на дефис
    text = re.sub(r'[ _]+', '-', text)
    
    #  Все остальные символы, кроме букв, цифр и дефиса, заменяем на дефис
    text = re.sub(r'[^a-z0-9-]+', '-', text)
    
    #  Схлопываем несколько дефисов подряд
    text = re.sub(r'-+', '-', text)
    
    #  Удаляем дефисы в начале и конце
    text = text.strip('-')
    
    return text