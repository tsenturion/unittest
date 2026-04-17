import re

def slugify(text: str) -> str:
    # приводим к нижнему регистру
    text = text.lower()

    # заменяем пробелы и _ на -
    text = re.sub(r"[ _]+", "-", text)

    # удаляем все символы кроме a-z, 0-9 и -
    text = re.sub(r"[^a-z0-9-]", "", text)

    # схлопываем повторяющиеся дефисы
    text = re.sub(r"-{2,}", "-", text)

    # обрезаем дефисы по краям
    text = text.strip("-")

    return text

