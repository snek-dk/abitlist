import os
import json


class JsonOut:
    def __init__(self, json_data=None, filename=None, debug_mode=None):
        if json_data is None:
            json_data = []
        self.basic_information = {
            "ВУЗ": '',
            "ОСНОВА_ОБУЧЕНИЯ": '',
            "УРОВЕНЬ_ОБУЧЕНИЯ": '',
            "НАПРАВЛЕНИЕ": '',
            "ОП": '',
            "ФОРМА_ОБУЧЕНИЯ": ''
        }
        self.personal_information = {
            "СНИЛС_УК": '',
            "ТИП_КОНКУРСА": '',
            "ПРИОРИТЕТ": 0,
            "ОРИГИНАЛ": False,
            "ПП": False,
            "ЕГЭ_С_ИД": 0,
            "ЕГЭ": 0,
            "ВИ_1": 0,
            "ВИ_2": 0,
            "ВИ_3": 0,
            "ВИ_4": None,
            "ВИ_5": None,
            "ВИ_6": None,
            "ИД": 0
        }
        self.places = {
            "БЮДЖЕТ": 0,
            "КОНТРАКТ": 0
        }
        self.json_data = json_data
        self.debug_mode = debug_mode
        self.filename = filename

    def check_json(self):
        for field, value in self.basic_information.items():
            if not isinstance(value, str):
                print(
                    f"Ошибка в поле '{field}'. Ожидается строковый тип данных, получен тип '{type(value).__name__}'")
                return False

        for field, value in self.personal_information.items():
            if field in ["ОРИГИНАЛ", "ПП"]:
                if not isinstance(value, bool):
                    print(
                        f"Ошибка в поле '{field}'. Ожидается логический тип данных, получен тип '{type(value).__name__}'")
                    return False
            elif field in ["ПРИОРИТЕТ", "ЕГЭ_С_ИД", "ЕГЭ", "ВИ_1", "ВИ_2", "ВИ_3", "ИД"]:
                if not isinstance(value, int):
                    print(
                        f"Ошибка в поле '{field}'. Ожидается целочисленный тип данных, получен тип '{type(value).__name__}'")
                    return False
            elif field in ["ВИ_4", "ВИ_5", "ВИ_6"]:
                if value is not None and not isinstance(value, int):
                    print(
                        f"Ошибка в поле '{field}'. Ожидается строковый тип данных или значение None, получен тип '{type(value).__name__}'")
                    return False
            elif not isinstance(value, str):
                print(f"Ошибка в поле '{field}'. Ожидается строковый тип данных, получен тип '{type(value).__name__}'")
                return False
        for field, value in self.places.items():
            if not isinstance(value, int):
                print(
                    f"Ошибка в поле '{field}'. Ожидается целочисленный тип данных, получен тип '{type(value).__name__}'")
                return False
        print("Данные соответствуют своим типам")
        return True

    def complete_form(self):

        if self.debug_mode:
            self.check_json()

        export_form = {}

        for field, value in self.basic_information.items():
            export_form[field] = value

        for field, value in self.personal_information.items():
            export_form[field] = value
        for field, value in self.places.items():
            export_form[field] = value

        return export_form

    def save_json(self):
        if type(self.filename) is str:
            indent = 4 if self.debug_mode else None
            with open(os.getcwd() + '\output.json', 'w', encoding="utf-8") as f:
                json.dump(self.json_data
                          
                          
                          , f, ensure_ascii=False, indent=indent)

        return 0
