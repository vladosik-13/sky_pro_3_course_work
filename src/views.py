import json
import logging
import os

from config import VIEWS_LOGS
from src.utils import (
    get_cardmask_costs_and_cashback,
    get_exchange_rates,
    greetings,
    get_file_from_json,
    reading_file_from_excel,
    get_top_transactions,
)

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(VIEWS_LOGS, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def views(date: str, transactions_df) -> str:
    """Функция принимает дату (строка) и DataFrame с данными по транзакциям.
    Возвращает ответ с приветствием, информацией по картам,
    топ-5 транзакций стоимость валюты в виде json-строки."""
    try:
        logger.info("Функция начала свою работу.")
        transactions = transactions_df.to_dict(orient="records")
        logger.info("Функция собирает результаты работ своих подфункций.")

        greeting = greetings(date)
        logger.info("Функция приветствия завершила свою работу.")

        info_about_cards = get_cardmask_costs_and_cashback(transactions)
        logger.info("Функция по сбору информации по картам завершила свою работу.")

        five_transactions = get_top_transactions(transactions)
        logger.info("Функция топ-5 транзакций завершила свою работу.")

        users_settings = get_file_from_json()  # Не используется в дальнейшем

        # Получаем курсы валют
        currency_rates = get_exchange_rates()

        logger.info("Функция формирует общий результат.")

        result_dict = {
            "greeting": greeting,
            "cards": info_about_cards,
            "top_transactions": five_transactions,
            "currency_rates": currency_rates,
        }

        result_json = json.dumps(result_dict, ensure_ascii=False)
        logger.info("Функция успешно завершила свою работу.")

        return result_json

    except Exception as e:
        logger.error(f"При работе функции произошла ошибка: {e}")
        raise ValueError("При работе функции произошла ошибка.")


if __name__ == "__main__":
    transaction_info = reading_file_from_excel("operations.xls")
    print("2023-07-06 10:42:30", transaction_info)
