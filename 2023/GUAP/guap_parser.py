import requests
from bs4 import BeautifulSoup as soup
import subprocess


def get_the_page(link, number):
    curl_command = f'''curl "{link}" --output guap_{number}.html'''
    resp = subprocess.run(curl_command, stdout=subprocess.PIPE)
    return 0


def get_json_form(main_form, personal_form, amount_of_places):
    data_form = {
        "ВУЗ": "ГУАП",
        "ОСНОВА_ОБУЧЕНИЯ": main_form["ОСНОВА_ОБУЧЕНИЯ"],
        "УРОВЕНЬ_ОБУЧЕНИЯ": main_form["УРОВЕНЬ_ОБУЧЕНИЯ"],
        "НАПРАВЛЕНИЕ": main_form["НАПРАВЛЕНИЕ"],
        "ОП": main_form["ОП"],
        "ФОРМА_ОБУЧЕНИЯ": main_form["ФОРМА_ОБУЧЕНИЯ"],
        "СНИЛС_УК": personal_form["СНИЛС_УК"],
        "ТИП_КОНКУРСА": personal_form["ТИП_КОНКУРСА"],
        "ПРИОРИТЕТ": personal_form["ПРИОРИТЕТ"],
        "ОРИГИНАЛ": personal_form["ОРИГИНАЛ"],
        "ПП": personal_form["ПП"],
        "ЕГЭ_С_ИД": personal_form["ЕГЭ_С_ИД"],
        "ЕГЭ": personal_form["ЕГЭ"],
        "ВИ_1": personal_form["ВИ_1"],
        "ВИ_2": personal_form["ВИ_2"],
        "ВИ_3": personal_form["ВИ_3"],
        "ВИ_4": personal_form["ВИ_4"],
        "ВИ_5": personal_form["ВИ_5"],
        "ВИ_6": personal_form["ВИ_6"],
        "ИД": personal_form["ИД"],
        "МЕСТА": {
            "Бюджет": amount_of_places["Бюджет"],
            "Контракт": amount_of_places["Контракт"]
        }
    }

    return data_form


main_form = {
    "ВУЗ": "ГУАП",
    "ОСНОВА_ОБУЧЕНИЯ": None,
    "УРОВЕНЬ_ОБУЧЕНИЯ": None,
    "НАПРАВЛЕНИЕ": None,
    "ОП": None,
    "ФОРМА_ОБУЧЕНИЯ": None
}
personal_form = {
    "СНИЛС_УК": None,
    "ТИП_КОНКУРСА": None,
    "ПРИОРИТЕТ": None,
    "ОРИГИНАЛ": None,
    "ПП": None,
    "ЕГЭ_С_ИД": None,
    "ЕГЭ": None,
    "ВИ_1": 0,
    "ВИ_2": 0,
    "ВИ_3": 0,
    "ВИ_4": None,
    "ВИ_5": None,
    "ВИ_6": None,
    "ИД": 0
}
amount_of_places = {
    "Бюджет": None,
    "Контракт": None
}

main_links = {
    "Очная": {
        "Бакалавриат": "https://priem.guap.ru/lists/1_1_1",
        "Специалитет": "https://priem.guap.ru/lists/1_1_2"
    },
    "Очно-заочная": {
        "Бакалавриат": "https://priem.guap.ru/lists/1_3_1",
        "Специалитет": None
    },
    "Заочная": {
        "Бакалавриат": "https://priem.guap.ru/lists/1_2_1",
        "Специалитет": "https://priem.guap.ru/lists/1_2_2"
    }
}
for form_of_education in ["Очная", "Очно-заочная", "Заочная"]:
    for level_of_education in ["Бакалавриат", "Специалитет"]:
        main_form["ФОРМА_ОБУЧЕНИЯ"] = form_of_education
        main_form["УРОВЕНЬ_ОБУЧЕНИЯ"] = level_of_education
        programs_page = requests.get(url=main_links[form_of_education][level_of_education]).content.decode("utf-8")
        # get_the_page(main_links[form_of_education][level_of_education], main_links[form_of_education][level_of_education][-5::])
        print(programs_page)
        break
    break
