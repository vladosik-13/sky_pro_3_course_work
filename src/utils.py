import pandas as pd


def excel_import(path_file):
    """Функция принимает аргументом путь к файлу Excel и возвращает список словарей с транзакциями, в котором ключами
     служат названия столбцов"""
    try:
        excel_data = pd.read_excel('C:/Users/user/PycharmProjects/sky_pro_4_course_work/data/operations.xlsx')
        return excel_data
    except Exception as e:
        print(f"Ошибка при считывании файла: {e}")
        return []


'''test_func = excel_import('C:/Users/user/PycharmProjects/sky_pro_4_course_work/data/operations.xlsx')
print(test_func)'''
