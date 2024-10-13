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
