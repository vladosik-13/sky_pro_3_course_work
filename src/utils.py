import logging
import json
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import requests


from collections import defaultdict
from typing import List, Dict


# Настройка логгера
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("utils_logs.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def greetings(date_str: str) -> str:
    """Функция принимает на вход строку с временем и возвращает доброе утро, день, вечер, ночь"""

    logger.info(f"Получена дата: {date_str}")

    try:

        logger.info("Обработка входных данных (строки)")

        input_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        hour = input_datetime.hour
        logger.info(f"Час: {hour}")

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

        logger.info(f"функция успешно отработала с ответом:  {response}")
        return json.dumps(response)

    except ValueError as e:
        logger.error(f"Ошибка ввода даты: {e}")
        return json.dumps({"error": "Неверный формат даты. Используйте 'YYYY-MM-DD HH:MM:SS'."})


def reading_file_from_excel(path_file: str):
    """Функция преобразования xls в DataFrame."""

    logger.info(f"Начало чтения файла: {path_file}")

    try:
        transactions = pd.read_excel(path_file)
        logger.info("Файл успешно прочитан.")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении файла: {e}")
        return None


def get_cardmask_costs_and_cashback(transactions: List[Dict]) -> List[Dict]:
    """Функция принимает список транзакций словарией и возвращает информацию по каждой карте:
    последние 4 цифры номера карты, общая сумма расходов, кэшбек"""

    logger.info("Функция начала свою работу.")

    try:
        if not transactions:
            logger.warning("Список транзакций пуст.")
            return []

        expenditure_by_card = defaultdict(int)

        logger.info("Функция обрабатывает данные транзакций.")

        for transaction in transactions:
            card_num = transaction.get("Номер карты")
            amount = transaction.get("Сумма операции", 0)
            if card_num:
                expenditure_by_card[card_num] += amount

        result_transaction_list = []

        logger.info("Функция формирует итоговый результат.")

        for card_num, total_spent in expenditure_by_card.items():
            result_transaction_list.append(
                {
                    "last_digits": card_num[-4:],
                    "total_spent": round(total_spent, 2),
                    "cashback": round(total_spent / 100, 2),
                }
            )
        logger.info("Функция успешно завершила свою работу.")

        return result_transaction_list

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return []


def get_top_transactions(transactions: List[Dict]) -> List[Dict]:
    """Функция принимает список транзакций словарей и Возвращает список словарей с пятью максимальными
    транзакциями по сумме операции."""

    logger.info("Функция начала свою работу.")

    if not transactions:
        logger.warning("Список транзакций пуст.")
        return []

    top_transactions = sorted(transactions, key=lambda x: abs(x["Сумма операции"]), reverse=True)[:5]

    logger.info("Функция успешно завершила свою работу.")

    return top_transactions


def get_exchange_rates(base_currency="RUB", symbols="EUR,USD,CNY"):
    load_dotenv()
    api_key = os.getenv("API_KEY")

    logger.info("Получение курсов валют")

    url = f"https://api.apilayer.com/fixer/latest?symbols={symbols}&base={base_currency}"
    payload = {}
    headers = {
        "apikey": api_key
    }

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code == 200:
        logger.info("Успешный запрос. Полученные данные:", response.json())
        return response.json()  # Возвращаем данные в формате JSON
    else:
        logger.error("Ошибка при получении данных. Статус-код: %d", response.status_code)
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}


if __name__ == "__main__":
    date_input = "2024-10-23 14:30:00"
    print(greetings(date_input))

    excel_path = 'C:/Users/user/PycharmProjects/sky_pro_4_course_work/data/operations.xlsx'
    transactions_df = reading_file_from_excel(excel_path)

    if transactions_df is not None:
        transactions = transactions_df.to_dict(orient='records')
        card_info = get_cardmask_costs_and_cashback(transactions)
        print(card_info)

    top_transactions = get_top_transactions(transactions)
    print("Топ-5 транзакций по сумме платежа:", top_transactions)

    exchange_rates = get_exchange_rates()
    print(exchange_rates)