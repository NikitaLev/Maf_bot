import pandas #дополнительно нужно использовать модуль openpyxl
import openpyxl
import json


class RatingManager:


    def __init__(self, file):
        self.file = file
        self.get_rating_stat_to_json()
        self.get_general_stat_to_json()
        self.get_role_stat_to_json()
        self.get_action_red_stat_to_json()
        self.get_action_black_stat_to_json()

    def get_sheet(self, sheet: str, cols: list, content: int):
        """Функция для чтения xlsx файла, принимает аргументы: наименование листа,
        количество колонок, отображаемый контент, возвращает объект: pandas.core.frame.DataFrame"""

        unloading_sheet = pandas.read_excel(self.file, sheet_name=sheet, usecols=cols, header=content)
        return unloading_sheet

    def write_sheet(self, filename: str, result: dict):
        """Функция для записи в json файл, принимает аргуементы: наименование файла,
        результат обработки"""

        with open(f'{filename}.json', 'w+', encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

    def get_rating_stat_to_json(self):
        """Функция для выгрузки данных рейтинга и загрузки в json файл"""

        # используя функцию, подгружаем необходимый лист таблицы
        rating_sheet = self.get_sheet(sheet='Un', cols=['Ник', 'в', 'п', 'ли', 'лх', 'у', 'д', 'ш', 'очки', 'рейтинг'],
                                 content=2)

        # подготовка записи листа в json формат
        sheet_to_json = rating_sheet.to_json(orient='index', force_ascii=False)
        result = json.loads(sheet_to_json)

        # запись в json формат
        self.write_sheet('rating', result)

    def get_general_stat_to_json(self):
        """Функция для выгрузки данных общей статистики игр и загрузки в json файл"""

        # используя функцию, подгружаем необходимый лист таблицы
        general_stat_sheet = self.get_sheet(sheet='G_st', cols=[1, 3], content=3)

        # подготовка записи листа в json формат
        sheet_to_json = general_stat_sheet.to_json(orient='values', force_ascii=False)
        result = json.loads(sheet_to_json)

        # запись в json формат
        self.write_sheet('general_stat', result)

    def get_role_stat_to_json(self):
        """Функция для выгрузки данных статистики ролей и загрузки в json файл"""

        # используя функцию, подгружаем необходимый лист таблицы
        role_stat_sheet = self.get_sheet(sheet='R_st', cols=['Ник', 'ик', 'пк', 'иш', 'пш', 'ич', 'пч', 'ид', 'пд'],
                                    content=7)

        # подготовка записи листа в json формат
        sheet_to_json = role_stat_sheet.to_json(orient='index', force_ascii=False)
        result = json.loads(sheet_to_json)

        # запись в json формат
        self.write_sheet('role_stat', result)

    def get_action_red_stat_to_json(self):
        """Функция для выгрузки данных статистики действий за мирную команду и их загрузка в json файл"""

        # используя функцию, подгружаем необходимый лист таблицы
        action_red_stat_sheet = self.get_sheet(sheet='A_st_red', cols=[2, 3, 4, 6, 8, 10, 12], content=7)

        # подготовка записи листа в json формат
        sheet_to_json = action_red_stat_sheet.to_json(orient='index', force_ascii=False)
        result = json.loads(sheet_to_json)

        # запись в json формат
        self.write_sheet('action_red_stat', result)

    def get_action_black_stat_to_json(self):
        """Функция для выгрузки данных статистики действий за черную команду и их загрузка в json файл"""

        # используя функцию, подгружаем необходимый лист таблицы
        action_black_stat_sheet = self.get_sheet(sheet='A_st_black', cols=[2, 3, 4, 6, 8, 10, 12], content=7)

        # подготовка записи листа в json формат
        sheet_to_json = action_black_stat_sheet.to_json(orient='index', force_ascii=False)
        result = json.loads(sheet_to_json)

        # запись в json формат
        self.write_sheet('action_black_stat', result)