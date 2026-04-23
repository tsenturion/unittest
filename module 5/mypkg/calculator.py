def add(a, b):
    return a + b

def save_to_db(value):
    # Имитация работы с БД
    if not isinstance(value, (int, float)):
        raise ValueError("Only numbers can be saved")
    return f"Saved {value} to database"
