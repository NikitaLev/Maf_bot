import pandas  # дополнительно нужно использовать модуль openpyxl
import openpyxl
import json


class RatingManager:

    def __init__(self, file):
        self.file = file
        self.file_rating = 'rating' #Un
        self.file_general_stat = 'general_stat' #G_st
        self.file_role_stat = 'role_stat' #R_st
        self.file_action_red_stat = 'action_red_stat'#A_st_red
        self.file_action_black_stat = 'action_black_stat'#A_st_black
        self.get_rating_stat_to_json()
        self.get_general_stat_to_json()
        self.get_role_stat_to_json()
        self.get_action_red_stat_to_json()
        self.get_action_black_stat_to_json()

    def update_bd(self):
        rating, role_stat, action_red_stat, action_black_stat = self.get_json_data()

    def get_json_data(self):
        f = open(self.file_rating, encoding="utf-8")
        rating_temp = dict(json.load(f))

        #f = open(self.file_general_stat, encoding="utf-8")
        #general_stat_temp = dict(json.load(f))

        f = open(self.file_role_stat, encoding="utf-8")
        role_stat_temp = dict(json.load(f))

        f = open(self.file_action_red_stat, encoding="utf-8")
        action_red_stat_temp = dict(json.load(f))

        f = open(self.file_action_black_stat, encoding="utf-8")
        action_black_stat_temp = dict(json.load(f))

        rating = {}
        for key in rating_temp:
            stat = rating_temp[key]
            temp = {
                'в': stat["в"],
                'п': stat["п"],
                'ли': stat["ли"],
                'лх': stat["лх"],
                'у': stat["у"],
                'д': stat["д"],
                'ш': stat["ш"],
                'очки': stat["очки"],
                'рейтинг': stat["рейтинг"]
            }
            rating[stat['Ник']] = temp

        role_stat = {}
        for key in role_stat_temp:
            stat = rating_temp[key]
            temp = {
                'ик': stat["ик"],
                'пк': stat["пк"],
                'иш': stat["иш"],
                'пш': stat["пш"],
                'ич': stat["ич"],
                'пч': stat["пч"],
                'ид': stat["ид"],
                'пд': stat["пд"]
            }
            role_stat[stat['Ник']] = temp

        action_red_stat = {}
        for key in action_red_stat_temp:
            stat = rating_temp[key]
            temp = {
                'ИС': stat["ИС"],
                'Поражений на 3х3': stat["Поражений на 3х3"],
                'Слом в красного': stat["Слом в красного"],
                'Слом в черного': stat["Слом в черного"],
                'Победа в угадайке': stat["Победа в угадайке"],
                'Проигрыш в угадайке': stat["Проигрыш в угадайке"]
            }
            action_red_stat[stat['Ник']] = temp

        action_black_stat = {}
        for key in action_black_stat_temp:
            stat = rating_temp[key]
            temp = {
                'ИС': stat["ИС"],
                'Побед на 3х3': stat["Побед на 3х3"],
                'Слом в красного': stat["Слом в красного"],
                'Слом в черного': stat["Слом в черного"],
                'Победа в угадайке': stat["Победа в угадайке"],
                'Проигрыш в угадайке': stat["Проигрыш в угадайке"]
            }
            action_black_stat[stat['Ник']] = temp
        return rating, role_stat, action_red_stat, action_black_stat

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
        self.write_sheet(self.file_rating, result)

    def get_general_stat_to_json(self):
        """Функция для выгрузки данных общей статистики игр и загрузки в json файл"""

        # используя функцию, подгружаем необходимый лист таблицы
        general_stat_sheet = self.get_sheet(sheet='G_st', cols=[1, 3], content=3)

        # подготовка записи листа в json формат
        sheet_to_json = general_stat_sheet.to_json(orient='values', force_ascii=False)
        result = json.loads(sheet_to_json)

        # запись в json формат
        self.write_sheet(self.file_general_stat, result)

    def get_role_stat_to_json(self):
        """Функция для выгрузки данных статистики ролей и загрузки в json файл"""

        # используя функцию, подгружаем необходимый лист таблицы
        role_stat_sheet = self.get_sheet(sheet='R_st', cols=['Ник', 'ик', 'пк', 'иш', 'пш', 'ич', 'пч', 'ид', 'пд'],
                                         content=7)

        # подготовка записи листа в json формат
        sheet_to_json = role_stat_sheet.to_json(orient='index', force_ascii=False)
        result = json.loads(sheet_to_json)

        # запись в json формат
        self.write_sheet(self.file_role_stat, result)

    def get_action_red_stat_to_json(self):
        """Функция для выгрузки данных статистики действий за мирную команду и их загрузка в json файл"""

        # используя функцию, подгружаем необходимый лист таблицы
        action_red_stat_sheet = self.get_sheet(sheet='A_st_red', cols=[2, 3, 4, 6, 8, 10, 12], content=7)

        # подготовка записи листа в json формат
        sheet_to_json = action_red_stat_sheet.to_json(orient='index', force_ascii=False)
        result = json.loads(sheet_to_json)

        # запись в json формат
        self.write_sheet(self.file_action_red_stat, result)

    def get_action_black_stat_to_json(self):
        """Функция для выгрузки данных статистики действий за черную команду и их загрузка в json файл"""

        # используя функцию, подгружаем необходимый лист таблицы
        action_black_stat_sheet = self.get_sheet(sheet='A_st_black', cols=[2, 3, 4, 6, 8, 10, 12], content=7)

        # подготовка записи листа в json формат
        sheet_to_json = action_black_stat_sheet.to_json(orient='index', force_ascii=False)
        result = json.loads(sheet_to_json)

        # запись в json формат
        self.write_sheet(self.file_action_black_stat, result)
