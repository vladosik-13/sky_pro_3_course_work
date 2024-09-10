import json
from datetime import datetime


def get_greeting():
    """Функция возвращает JSON-ответ - приветствие в зависимости от текущего времени"""

    current_time = datetime.now()

    # Определяем приветствие в зависимости от времени суток
    if current_time.hour < 6:
        greeting = "Доброй ночи"
    elif current_time.hour < 12:
        greeting = "Доброе утро"
    elif current_time.hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    # Формируем JSON-ответ
    response = greeting

    return json.dumps(response, ensure_ascii=False)


# Пример использования
'''if __name__ == "__main__":
    greeting_json = get_greeting()
    print(greeting_json)'''