import pytest
from typing import List, Dict, Any
from src.reports import filter_by_category
import re


def test_filter_by_category_success():
    """Тест успешной фильтрации транзакций по категории."""
    transactions = [
        {"ID": 1, "Категория": "Продукты", "Сумма операции": 100},
        {"ID": 2, "Категория": "Развлечения", "Сумма операции": 200},
        {"ID": 3, "Категория": "Продукты", "Сумма операции": 150},
        {"ID": 4, "Категория": "Транспорт", "Сумма операции": 50},
    ]
    category = "Продукты"
    expected = [
        {"ID": 1, "Категория": "Продукты", "Сумма операции": 100},
        {"ID": 3, "Категория": "Продукты", "Сумма операции": 150},
    ]

    result = filter_by_category(category, transactions)

    assert result == expected


def test_filter_by_category_no_matches():
    """Тест, когда нет совпадений по категории."""
    transactions = [
        {"ID": 1, "Категория": "Продукты", "Сумма операции": 100},
        {"ID": 2, "Категория": "Развлечения", "Сумма операции": 200},
    ]
    category = "Транспорт"

    result = filter_by_category(category, transactions)

    assert result == []  # Проверяем, что возвращается пустой список


def test_filter_by_category_case_insensitivity():
    """Тест, чтобы проверить нечувствительность к регистру при фильтрации."""
    transactions = [
        {"ID": 1, "Категория": "Продукты", "Сумма операции": 100},
        {"ID": 2, "Категория": "развлечения", "Сумма операции": 200},
        {"ID": 3, "Категория": "Продукты", "Сумма операции": 150},
    ]
    category = "РАЗВЛЕЧЕНИЯ"
    expected = [
        {"ID": 2, "Категория": "развлечения", "Сумма операции": 200},
    ]

    result = filter_by_category(category, transactions)

    assert result == expected


def test_filter_by_category_empty_transactions():
    """Тест обработки пустого списка транзакций."""
    transactions = []
    category = "Продукты"

    result = filter_by_category(category, transactions)

    assert result == []  # Проверяем, что возвращается пустой список


def test_filter_by_category_special_characters():
    """Тест фильтрации с категорией, содержащей специальные символы."""
    transactions = [
        {"ID": 1, "Категория": "Продукты & Snacks", "Сумма операции": 100},
        {"ID": 2, "Категория": "Развлечения", "Сумма операции": 200},
        {"ID": 3, "Категория": "Продукты", "Сумма операции": 150},
    ]
    category = "Продукты & Snacks"
    expected = [
        {"ID": 1, "Категория": "Продукты & Snacks", "Сумма операции": 100},
    ]

    result = filter_by_category(category, transactions)

    assert result == expected