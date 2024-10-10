import logging
import json
from datetime import datetime
import pandas as pd


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


if __name__ == "__main__":
    date_input = "2024-10-23 14:30:00"
    print(greetings(date_input))

    excel_path = 'C:/Users/user/PycharmProjects/sky_pro_4_course_work/data/operations.xlsx'
    transactions_df = reading_file_from_excel(excel_path)
    if transactions_df is not None:
        print(transactions_df.head())  # Печатает первые 5 строк DataFrame

