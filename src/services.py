import datetime
import logging
import json
from math import ceil, floor
from typing import Any, Dict, List, Union

from config import SERVICES_LOGS
from src.utils import reading_file_from_excel


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(SERVICES_LOGS, mode='w')
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def round_payment(limit: int, payment: Union[int, float]) -> int:
    """Функция округляет сумму операции согласно лимиту."""
    logger.info("Начало работы функции round_payment.")

    try:
        rounded_payment = (floor(payment / limit) if payment < 0 else ceil(payment / limit)) * limit
    except Exception as e:
        logger.error("Ошибка при округлении платежа: %s", e)
        return 0

    logger.info("Завершение работы функции round_payment.")
    return rounded_payment


def filter_transactions_by_month(month: str, transactions: List[Dict[str, Any]]) -> List[Dict]:
    """Функция возвращает транзакции, отфильтрованные по указанному месяцу."""
    logger.info("Начало работы функции filter_transactions_by_month.")

    try:
        target_date = datetime.datetime.strptime(month, "%Y-%m")
    except ValueError as e:
        logger.error("Неверный формат месяца: %s", e)
        return []

    filtered_transactions = [
        tx for tx in transactions if
        datetime.datetime.strptime(tx["Дата операции"], "%d.%m.%Y %H:%M:%S").month == target_date.month
        and datetime.datetime.strptime(tx["Дата операции"], "%d.%m.%Y %H:%M:%S").year == target_date.year
    ]

    logger.info("Завершение работы функции filter_transactions_by_month.")
    return filtered_transactions


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> str:
    """ функция ычисляет общую сумму инвестиций за указанный месяц с учетом лимита округления."""
    logger.info("Начало работы функции calculate_investment.")

    investment_sum = 0
    filtered_transactions = filter_transactions_by_month(month, transactions)

    for transaction in filtered_transactions:
        rounded_value = round_payment(limit, transaction["Сумма операции"])
        investment_sum += abs(rounded_value) - abs(transaction["Сумма операции"])

    logger.info("Завершение работы функции calculate_investment.")
    return json.dumps(round(investment_sum, 2), ensure_ascii=False)


if __name__ == "__main__":
    try:
        data_from_excel = reading_file_from_excel("operations.xls")
        result = investment_bank("2021-10", data_from_excel.to_dict(orient="records"), 100)
        print(result)
    except Exception as e:
        logger.error("Ошибка при выполнении программы: %s", e)
