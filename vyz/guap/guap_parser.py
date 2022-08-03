import requests
import json
from bs4 import BeautifulSoup


def abiturient_to_dict(person):
    to_save = {
        "ВУЗ": "ГУАП",
        "Направление": person["Направление"],
        "ОП": person["ОП"],
        "Форма_обучения": person["Форма_обучения"],
        "Основа_обучения": person["Основа_обучения"],
        "СНИЛС_УК": person["СНИЛС_УК"],
        "Конкурс": person["Конкурс"],
        "СУММА": person["СУММА"],
        "СУММА_БЕЗ_ИД": person["СУММА_БЕЗ_ИД"],
        "ВИ_1": person["ВИ_1"],
        "ВИ_2": person["ВИ_2"],
        "ВИ_3": person["ВИ_3"],
        "ВИ_4": None,
        "ВИ_5": None,
        "ИД": person["ИД"],
        "Согласие": person["Согласие"],
        "Оригинал": person["Оригинал"]
    }
    return to_save


to_save = []
for i in range(6, 8):
    bachelor = requests.get(url=f'https://priem.guap.ru/bach/ratings/Main_{i}')
    bachelor.encoding = 'utf-8'
    bachelor_list = BeautifulSoup(bachelor.text, "lxml")
    bachelor_items = bachelor_list.find_all('tr')[1:]
    for each in bachelor_items:
        field_of_study = each.find_all('td')[1].text
        print(field_of_study)
        link = "https://priem.guap.ru" + each.find('a').attrs["href"].replace('\\', '/')
        field_of_study_page = requests.get(link)
        field_of_study_page.encoding = 'utf-8'
        converted_page = BeautifulSoup(field_of_study_page.text, "lxml")
        program = converted_page.find('h3').text.replace('"', '')
        print(program)
        abitura = converted_page.find('tbody').find_all('tr')

        for each_person in abitura:
            person = each_person.find_all('td')

            ege = person[2].text.replace('\n', ' ').split(' ')
            ege_to_save = []
            for i in ege:
                if i.isdigit():
                    ege_to_save.append(i)
            person_data = {
                "СНИЛС_УК": person[1].text,
                "Направление": field_of_study,
                "ОП": program,
                "Форма_обучения": "очная",
                "Основа_обучения": "Госбюджет",
                "Конкурс": "ОК",
                "ВИ_1": ege_to_save[0] if ege_to_save[0] else "0",
                "ВИ_2": ege_to_save[1] if ege_to_save[1] else "0",
                "ВИ_3": ege_to_save[2] if ege_to_save[2] else "0",
                "СУММА_БЕЗ_ИД": person[3].text if person[3].text else "0",
                "ИД": person[4].text if person[4].text else "0",
                "СУММА": person[5].text if person[5].text else "0",
                "Согласие": person[7].text if person[7].text else "Нет",
                "Оригинал": person[8].text if person[8].text else "Нет"
            }
            to_save.append(abiturient_to_dict(person_data))
with open("./out_json/bonch.json", "w", encoding='utf-8') as f:
    json.dump(to_save, f, ensure_ascii=False)
