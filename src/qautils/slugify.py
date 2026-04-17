# Модуль 1

import string

def slugify(text: str) -> str:
    text = text.lower() # Приводим текст к нижнему регистру
    punctuation_translator = str.maketrans(
        {char: " " for char in string.punctuation}
    )   # Формируем словарь знаков пунктуации с заменой всех знаков на " "
    text = text.translate(punctuation_translator)  # Замена знаков во входной строке
    text_split = text.split()   # Разделение строки по " "
    text = ' '.join(text_split) # Сбор строки обратно, исключив лишние пробелы
    text = text.replace(" ", "-")   # Замена пробелов на "-"
    return text 


print(slugify("   Hello, World!  ------A----B----"))