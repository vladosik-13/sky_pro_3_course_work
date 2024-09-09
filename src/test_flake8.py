import pandas as pd
import json
from datetime import datetime


def get_greeting(current_time):
    if current_time.hour < 6:
        return "Доброй ночи"
    elif current_time.hour < 12:
        return "Доброе утро"
    elif current_time.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def process_transactions(date_str, excel_file):
    # Парсим строку с датой и временем
    current_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    # Получаем приветствие
    greeting = get_greeting(current_time)

    # Читаем данные из excel файла
    transactions = pd.read_excel(excel_file)

    # Структура для хранения результатов
    cards_summary = {}

    for index, row in transactions.iterrows():
        card = row['Card']
        amount = row['Amount']

        # Берем последние 4 цифры карты
        last_four_digits = str(card)[-4:]

        # Инициализируем данные по карте, если еще не добавляли
        if last_four_digits not in cards_summary:
            cards_summary[last_four_digits] = {
                'total_amount': 0,
                'cashback': 0
            }

        # Обновляем сумму расходов
        cards_summary[last_four_digits]['total_amount'] += amount
        # Обновляем кешбэк (1 рубль на каждые 100 рублей)
        cards_summary[last_four_digits]['cashback'] += amount // 100

    # Формируем окончательный json-ответ
    response = {
        'greeting': greeting,
        'cards': {}
    }

    for card, data in cards_summary.items():
        response['cards'][card] = {
            'total_amount': data['total_amount'],
            'cashback': data['cashback']
        }

    return json.dumps(response, ensure_ascii=False)


# Главная функция
if __name__ == '__main__':
    # Пример входных данных
    date_input = '2023-10-10 14:30:00'  # Задайте свою дату и время
    excel_file_path = 'transactions.xlsx'  # Задайте путь к вашему excel файлу

    # Получаем JSON-ответ
    json_response = process_transactions(date_input, excel_file_path)
    print(json_response)