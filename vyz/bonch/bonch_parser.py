import subprocess
from bs4 import BeautifulSoup
import json


def get_the_page():
    resp = subprocess.run('curl  "http://priem.sut.ru/new_site/page/competitive_selection.php?a=2" '
                          '--data-raw "general=101&education_base_to=3&training_form=4&training_type=0&1cunv_groupab=0&action=get_result&rekzach=1" '
                          '--output bonch.html', stdout=subprocess.PIPE)
    return 0


def program_to_save(main_info):
    program = {
        "ВУЗ": "Бонч",
        "Программа": main_info["ОП"],
        "Форма_обучения": main_info["Форма_обучения"].lower(),
        "Конкурс": main_info["Основа_обучения"],
        "Количество_мест": main_info["Количество_мест"] if main_info["Количество_мест"] else None
    }

    if program["Конкурс"] == "Бюджет":
        program["Конкурс"] = "ОК"
    elif program["Конкурс"] == "Специальная квота":
        program["Конкурс"] = "СК"
    elif program["Конкурс"] == "Особая квота":
        program["Конкурс"] = "ОП"
    elif program["Конкурс"] == "Целевая квота":
        program["Конкурс"] = "ЦП"
    else:
        program["Конкурс"] = "Контракт"

    return program


get_the_page()


def new_one(main_info, person_info):
    person_to_save = {
        "ВУЗ": "Бонч",
        "Направление": main_info["Направление"],
        "ОП": main_info["ОП"],
        "Форма_обучения": main_info["Форма_обучения"].lower(),
        "Основа_обучения": 'Гос' + main_info["Основа_обучения"].lower() if main_info[
                                                                               "Основа_обучения"] != "Контракт" else "Контракт",
        "СНИЛС_УК": person_info["СНИЛС"],
        "Конкурс": main_info["Основа_обучения"],
        "СУММА": person_info["СУММА"],
        "СУММА_БЕЗ_ИД": person_info["СУММА_БЕЗ_ИД"],
        "ВИ_1": person_info["ВИ_1"],
        "ВИ_2": person_info["ВИ_2"],
        "ВИ_3": person_info["ВИ_3"],
        "ВИ_4": None,
        "ВИ_5": None,
        "ИД": person_info["ИД"],
        "Согласие": person_info["Согласие"],
        "Оригинал": person_info['Оригинал']
    }
    if person_to_save["Конкурс"] == "Бюджет":
        person_to_save["Конкурс"] = "ОК"
    elif person_to_save["Конкурс"] == "Специальная квота":
        person_to_save["Конкурс"] = "СК"
    elif person_to_save["Конкурс"] == "Особая квота":
        person_to_save["Конкурс"] = "ОП"
    elif person_to_save["Конкурс"] == "Целевая квота":
        person_to_save["Конкурс"] = "ЦП"
    else:
        person_to_save["Конкурс"] = "Контракт"

    return person_to_save


with open('bonch.html', encoding='utf-8') as f:
    bachelor = f.read()
page = BeautifulSoup(bachelor, "lxml")
programs = []
persons = []
for t in page.find_all(class_="table"):
    temp_2 = t.find('th').text.split('\n')
    temp_3 = temp_2[0][19:].split(' ')
    main_info = {'Форма_обучения': temp_3[1],
                 'Основа_обучения': temp_3[2],
                 'Направление': temp_3[0] + ' ' + ' '.join(temp_3[3:]),
                 'ОП': ' '.join(temp_3[3:]),
                 'Количество_мест': temp_2[2].strip().split(' ')[-1]
                 }
    programs.append(program_to_save(main_info=main_info))
    abitura = t.find_all('tr')[2:]
    for each_abitur in abitura:
        abiturient = each_abitur.find_all('td')
        person_info = {
            'СНИЛС': abiturient[1].text,
            'СУММА': abiturient[2].text,
            'СУММА_БЕЗ_ИД': abiturient[3].text,
            'ВИ_1': abiturient[4].text.split('/')[-3] if abiturient[4].text.split('/')[-3] else "0",
            'ВИ_2': abiturient[4].text.split('/')[-2] if abiturient[4].text.split('/')[-2] else "0",
            'ВИ_3': abiturient[4].text.split('/')[-1] if abiturient[4].text.split('/')[-1] else "0",
            'ИД': abiturient[5].text if abiturient[5].text else "0",
            'Согласие': abiturient[7].text if abiturient[7].text else None,
            'Оригинал': abiturient[8].text if abiturient[8].text else None
        }
        persons.append(new_one(main_info, person_info))
with open(r"C:\Users\dmitr\PycharmProjects\abitlist\out_json\bonch.json", "w", encoding="utf-8") as f:
    json.dump(persons, f, indent=4, ensure_ascii=False)
with open(r"C:\Users\dmitr\PycharmProjects\abitlist\out_json\mesta\bonch.json", "w", encoding="utf-8") as f:
    json.dump(programs, f, indent=4, ensure_ascii=False)
