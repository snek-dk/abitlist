import requests
from bs4 import BeautifulSoup as soup
import os
import sys

sys.path.insert(0, os.getcwd().replace('\\SPBSU', ''))
from data_form import JsonOut

if not os.path.isfile("spbsu_links.txt"):
    os.system("spbsu_links.py 1")

links = []
with open("spbsu_links.txt", "r") as links_file:
    for link in links_file:
        links.append(link[:-1])

to_export = []
for link in links:
    print(link)
    page = soup(requests.get(link).content.decode("utf-8"), "lxml")
    applicant = JsonOut(debug_mode=False, filename="spbsu")
    basic_info = applicant.basic_information
    personal_info = applicant.personal_information
    places_info = applicant.places

    meta_html = page.find('p').find_all("b")
    basic_info["ВУЗ"] = "СПбГУ"
    basic_info["УРОВЕНЬ_ОБУЧЕНИЯ"] = meta_html[0].next_sibling.replace(' ', '').title()
    basic_info["НАПРАВЛЕНИЕ"] = meta_html[2].next_sibling
    basic_info["ОП"] = meta_html[3].next_sibling
    basic_info["ФОРМА_ОБУЧЕНИЯ"] = meta_html[4].next_sibling.replace(' ', '').title()
    basic_info["ОСНОВА_ОБУЧЕНИЯ"] = "Бюджет" if "Гос" in meta_html[5].next_sibling else "Контракт"
    max_exams = 3
    if "ВИ 5" in meta_html[-1].text:
        max_exams = 5
    elif "ВИ 4" in meta_html[-1].text:
        max_exams = 4
    if basic_info["ОСНОВА_ОБУЧЕНИЯ"] == "Бюджет":
        try:
            places_info["БЮДЖЕТ"] = int(meta_html[6].next_sibling.replace(' ', ''))
        except:
            places_info["БЮДЖЕТ"] = 0
    else:
        try:
            places_info["КОНТРАКТ"] = int(meta_html[6].next_sibling.replace(' ', ''))
        except:
            places_info["КОНТРАКТ"] = 0
    table_html = page.find("table")
    rows = table_html.find("tbody").find_all("tr")
    for row in rows:
        person_html = row.find_all("td")
        person_html = [info.text for info in person_html]
        personal_info["СНИЛС_УК"] = person_html[1]
        if "Без" in person_html[2]:
            personal_info["ТИП_КОНКУРСА"] = "БВИ"
        elif "Особая" in meta_html[5].next_sibling:
            personal_info["ТИП_КОНКУРСА"] = "ОСК"
        elif "Отдельная" in meta_html[5].next_sibling:
            personal_info["ТИП_КОНКУРСА"] = "ОТК"
        elif "Целевая" in meta_html[5].next_sibling:
            personal_info["ТИП_КОНКУРСА"] = "ЦК"
        else:
            personal_info["ТИП_КОНКУРСА"] = "ОК"
        subjects_start_index = 4
        if (personal_info["ТИП_КОНКУРСА"] == "ОК" or personal_info["ТИП_КОНКУРСА"] == "БВИ") and basic_info[
            "ОСНОВА_ОБУЧЕНИЯ"] == "Бюджет":
            try:
                personal_info["ПРИОРИТЕТ"] = int(person_html[3])
            except:
                personal_info["ПРИОРИТЕТ"] = 0
        else:
            personal_info["ПРИОРИТЕТ"] = 0
            subjects_start_index = 3
        j = 0
        for i in range(subjects_start_index + 2, subjects_start_index + 2 + max_exams):
            if person_html[i].replace(' ', '').split('.')[0].isdigit():
                personal_info[f"ВИ_{j + 1}"] = int(person_html[i].replace(' ', '').split('.')[0])
            else:
                personal_info[f"ВИ_{j + 1}"] = 0
            j += 1
        if person_html[subjects_start_index].replace(' ', '').split(',')[0].isdigit():
            personal_info["ЕГЭ_С_ИД"] = int(person_html[subjects_start_index].replace(' ', '').split(',')[0])
        else:
            personal_info["ЕГЭ_С_ИД"] = 0
        if person_html[subjects_start_index + 1].replace(' ', '').split(',')[0].isdigit():
            personal_info["ЕГЭ"] = int(person_html[subjects_start_index + 1].replace(' ', '').split(',')[0])
        else:
            personal_info["ЕГЭ"] = 0
        if person_html[subjects_start_index + 2 + max_exams].replace(' ', '').split(',')[0].isdigit():
            personal_info["ИД"] = int(person_html[subjects_start_index + 2 + max_exams].replace(' ', '').split(',')[0])
        to_export.append(applicant.complete_form())
res = JsonOut(json_data=to_export, filename='spbsu', debug_mode=False)
res.save_json()
