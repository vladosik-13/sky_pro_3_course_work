import datetime
import json
import logging
import os
import re
from functools import wraps
from typing import Any, Callable, Dict, List

import pandas as pd

from config import REPORTS_LOGS, ROOT_DIR

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(REPORTS_LOGS, mode="w")
formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def log(filename: str = "log_file.json") -> Any:
    """Декоратор для записи результата функции (pd.DataFrame) в JSON-файл."""
    logger.info("Запуск декоратора.")

    def decorator(func: Callable) -> Any:
        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            logger.info("Получение результата функции.")
            result = func(*args, **kwargs)
            logger.info("Запись результата в файл.")
            with open(os.path.join(ROOT_DIR, filename), "w", encoding="utf-8") as f:
                json.dump(result.to_dict(orient="records"), f, ensure_ascii=False, indent=4)
            logger.info("Работа декоратора завершена.")
            return result

        return wrapped

    return decorator


def filter_by_category(category: str, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """функция фильтрации транзакций по категории."""
    logger.info("Начало фильтрации по категории.")
    regex_pattern = rf"{category}"
    logger.info("Обработка транзакций.")
    filtered_transactions = [
        transaction
        for transaction in transactions
        if re.search(regex_pattern, transaction["Категория"], flags=re.IGNORECASE)
    ]
    logger.info("Фильтрация по категории завершена.")
    return filtered_transactions


def filter_by_date(transactions: List[Dict], date: str = "") -> List[Dict[str, Any]]:
    """функция ильтрации транзакций по дате."""
    logger.info("Начало фильтрации по дате.")

    if not date:
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(weeks=12)
    else:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        start_date = end_date - datetime.timedelta(weeks=12)

    filtered_transactions = []
    logger.info("Обработка транзакций по дате.")
    for transaction in transactions:
        transaction_date = datetime.datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if start_date <= transaction_date <= end_date:
            filtered_transactions.append(transaction)
    logger.info("Фильтрация по дате завершена.")
    return filtered_transactions


@log()
def transactions_by_category(transactions: pd.DataFrame, category: str, date: str = "") -> pd.DataFrame:
    """Основная функция для получения транзакций по категории и дате."""
    logger.info("Начало обработки транзакций по категории.")
    valid_transactions = transactions[transactions["Категория"].notnull()]
    logger.info("Удаление пустых значений в категории.")
    transactions_list = valid_transactions.to_dict(orient="records")

    logger.info("Передача данных для дальнейшей обработки.")
    filtered_by_date_list = filter_by_date(transactions_list, date)
    filtered_by_category_list = filter_by_category(category, filtered_by_date_list)

    result_df = pd.DataFrame(filtered_by_category_list)
    logger.info("Обработка транзакций завершена.")
    return result_df


data_from_excel = pd.DataFrame(
    [
        {"Дата операции": "01.10.2023 17:53:24", "Сумма операции": -152, "Категория": "Фастфуд"},
        {"Дата операции": "07.10.2023 17:53:24", "Сумма операции": -47.85, "Категория": "Каршеринг"},
        {"Дата операции": "15.10.2023 17:53:24", "Сумма операции": -10385, "Категория": "Фастфуд"},
        {"Дата операции": "07.10.2023 17:53:24", "Сумма операции": -101, "Категория": "Супермаркет"},
        {"Дата операции": "17.10.2023 17:53:24", "Сумма операции": -52, "Категория": "Супермаркет"},
        {"Дата операции": "27.10.2023 17:53:24", "Сумма операции": -887.65, "Категория": "Детские товары"},
        {"Дата операции": "01.10.2023 17:53:24", "Сумма операции": -152, "Категория": "Фастфуд"},
        {"Дата операции": "07.10.2023 17:53:24", "Сумма операции": -47.85, "Категория": "Каршеринг"},
        {"Дата операции": "15.10.2023 17:53:24", "Сумма операции": -10385, "Категория": "Фастфуд"},
        {"Дата операции": "07.10.2023 17:53:24", "Сумма операции": -101, "Категория": "Супермаркет"},
        {"Дата операции": "17.10.2023 17:53:24", "Сумма операции": -52, "Категория": "Супермаркет"},
        {"Дата операции": "27.10.2023 17:53:24", "Сумма операции": -887.65, "Категория": "Детские товары"},
    ]
)


if __name__ == "__main__":
    print(transactions_by_category(data_from_excel, "Каршеринг", "2023-10-15"))
