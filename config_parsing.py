"""
Модуль для парсинга и валидации конфигурационных значений.
Поддерживает преобразование строк в int, bool и список строк.
"""
from __future__ import annotations

import re
from typing import List

# Константы для парсинга boolean значений
_TRUE = {"1", "true", "yes", "y", "on"}
_FALSE = {"0", "false", "no", "n", "off"}


def parse_port(value: str) -> int:
    """
    Парсит номер порта из строки.

    Args:
        value: Строковое представление порта (допустимы пробелы по краям)

    Returns:
        int: Номер порта в диапазоне 1..65535

    Raises:
        TypeError: Если value не является строкой
        ValueError: Если строка пустая, не является десятичным числом
                   или число вне допустимого диапазона
    """
    if not isinstance(value, str):
        raise TypeError(f"port value must be str, got {type(value).__name__}")

    raw = value.strip()
    if not raw:
        raise ValueError("port value is empty")

    # Проверяем, что строка содержит только цифры
    if not re.fullmatch(r"\d+", raw):
        raise ValueError(f"port must be decimal integer, got: {value!r}")

    port = int(raw)
    if not (1 <= port <= 65535):
        raise ValueError(f"port out of range (1..65535): {port}")

    return port


def parse_bool(value: str) -> bool:
    """
    Парсит булево значение из строки.

    Поддерживаются значения (регистронезависимо):
    - True: '1', 'true', 'yes', 'y', 'on'
    - False: '0', 'false', 'no', 'n', 'off'

    Args:
        value: Строковое представление булева значения

    Returns:
        bool: Результат парсинга

    Raises:
        TypeError: Если value не является строкой
        ValueError: Если строка не соответствует ни одному из допустимых значений
    """
    if not isinstance(value, str):
        raise TypeError(f"bool value must be str, got {type(value).__name__}")

    token = value.strip().lower()
    if token in _TRUE:
        return True
    if token in _FALSE:
        return False
    raise ValueError(f"invalid boolean literal: {value!r}")


def parse_csv(value: str) -> List[str]:
    """
    Парсит строку как CSV, возвращая список непустых строк.

    Правила:
    - Разделитель - запятая
    - Пробелы вокруг элементов игнорируются
    - Пустые элементы отбрасываются

    Args:
        value: Строка с CSV данными

    Returns:
        List[str]: Список непустых строк

    Raises:
        TypeError: Если value не является строкой
    """
    if not isinstance(value, str):
        raise TypeError(f"csv value must be str, got {type(value).__name__}")

    if not value.strip():
        return []

    # Разделяем по запятой, убираем пробелы, фильтруем пустые
    items = [
        item.strip()
        for item in value.split(",")
    ]
    return [item for item in items if item]