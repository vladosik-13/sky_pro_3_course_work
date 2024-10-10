import json
from datetime import datetime


def greetings(date_str: str) -> str:
    input_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    hour = input_datetime.hour
    if hour < 6:
        greeting = "Доброй ночи"
    elif hour < 12:
        greeting = "Доброе утро"
    elif hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    response = {
        "greeting": greeting
    }

    return json.dumps(response)


if __name__ == "__main__":
    date_input = "2024-10-23 14:30:00"
    print(greetings(date_input))
