import datetime
import logging
import json
from math import ceil, floor
from typing import Any, Dict, List, Union

from config import SERVICES_LOGS
from src.utils import reading_file_from_excel


# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("services_logs", mode='w')
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
