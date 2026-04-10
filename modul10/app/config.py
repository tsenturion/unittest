# app/config.py
import json
import os

def load_config(config_path: str = None) -> dict:
    """
    Загружает конфигурацию из JSON файла
    
    Args:
        config_path: Путь к JSON файлу конфигурации
    
    Returns:
        dict: Словарь с конфигурацией
    """
    # Базовый конфиг по умолчанию
    default_config = {
        "base_url": "https://catalog.example.com",
        "api_key": "secret-key-123"
    }
    
    # Если путь не указан, возвращаем конфиг по умолчанию
    if config_path is None:
        return default_config.copy()
    
    # Пытаемся прочитать файл с указанием encoding='utf-8'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Обновляем конфиг значениями по умолчанию для отсутствующих ключей
        result = default_config.copy()
        result.update(config)
        
        # Возвращаем результат
        return result
        
    except (FileNotFoundError, json.JSONDecodeError, IOError):
        # Если файл не найден или ошибка чтения, возвращаем конфиг по умолчанию
        return default_config.copy()