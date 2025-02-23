import pytest
import json
from src.utils import greetings, reading_file_from_excel, get_top_transactions
import pandas as pd
from unittest.mock import patch
from typing import List, Dict


def test_greeting_morning():
    result = greetings("2023-10-01 08:00:00")
    assert json.loads(result) == {"greeting": "Доброе утро"}


def test_greeting_afternoon():
    result = greetings("2023-10-01 14:00:00")
    assert json.loads(result) == {"greeting": "Добрый день"}


def test_greeting_evening():
    result = greetings("2023-10-01 20:00:00")
    assert json.loads(result) == {"greeting": "Добрый вечер"}


def test_greeting_night():
    result = greetings("2023-10-01 02:00:00")
    assert json.loads(result) == {"greeting": "Доброй ночи"}


@pytest.fixture
def mock_read_excel():
    """Фикстура для мока функции pd.read_excel."""
    with patch('pandas.read_excel') as mock:
        yield mock


def test_reading_file_success(mock_read_excel):
    """Тест успешного чтения файла Excel."""
    mock_data = pd.DataFrame({'Column1': [1, 2], 'Column2': [3, 4]})
    mock_read_excel.return_value = mock_data

    result = reading_file_from_excel('mock_file.xlsx')

    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2  # Проверка количества строк
    assert 'Column1' in result.columns  # Проверка наличия колонки


def test_reading_file_failure(mock_read_excel):
    """Тест обработки ошибки чтения файла Excel."""
    mock_read_excel.side_effect = Exception("Ошибка чтения файла")

    result = reading_file_from_excel('mock_file.xlsx')

    assert result is None


def test_get_top_transactions_success():
    """Тест успешного получения топ-5 транзакций."""
    transactions = [
        {"ID": 1, "Сумма операции": 100},
        {"ID": 2, "Сумма операции": 200},
        {"ID": 3, "Сумма операции": -300},
        {"ID": 4, "Сумма операции": 400},
        {"ID": 5, "Сумма операции": 250},
        {"ID": 6, "Сумма операции": -1000},
    ]

    expected = [
        {"ID": 6, "Сумма операции": -1000},
        {"ID": 4, "Сумма операции": 400},
        {"ID": 3, "Сумма операции": -300},
        {"ID": 5, "Сумма операции": 250},
        {"ID": 2, "Сумма операции": 200},
    ]

    result = get_top_transactions(transactions)
    assert result == expected


def test_get_top_transactions_empty_list():
    """Тест обработки пустого списка транзакций."""
    transactions = []

    result = get_top_transactions(transactions)

    assert result == []  # Проверяем, что возвращается пустой список


def test_get_top_transactions_less_than_five():
    """Тест, когда меньше пяти транзакций."""
    transactions = [
        {"ID": 1, "Сумма операции": 100},
        {"ID": 2, "Сумма операции": 200},
    ]

    expected = [
        {"ID": 2, "Сумма операции": 200},
        {"ID": 1, "Сумма операции": 100},
    ]

    result = get_top_transactions(transactions)

    assert result == expected  # Проверяем, что возвращается корректный список


def test_get_top_transactions_all_same_value():
    """Тест, когда все транзакции имеют одинаковую сумму."""
    transactions = [
        {"ID": 1, "Сумма операции": 100},
        {"ID": 2, "Сумма операции": 100},
        {"ID": 3, "Сумма операции": 100},
        {"ID": 4, "Сумма операции": 100},
        {"ID": 5, "Сумма операции": 100},
        {"ID": 6, "Сумма операции": 100},
    ]

    expected = [
        {"ID": 1, "Сумма операции": 100},
        {"ID": 2, "Сумма операции": 100},
        {"ID": 3, "Сумма операции": 100},
        {"ID": 4, "Сумма операции": 100},
        {"ID": 5, "Сумма операции": 100},
    ]

    result = get_top_transactions(transactions)

    assert result == expected


