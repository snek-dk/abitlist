import requests
from bs4 import BeautifulSoup as soup
import os

data_form = {
    "ВУЗ": "СПбГУ",
    "ОСНОВА_ОБУЧЕНИЯ": None,
    "УРОВЕНЬ_ОБУЧЕНИЯ": None,
    "НАПРАВЛЕНИЕ": None,
    "ОП": None,
    "ФОРМА_ОБУЧЕНИЯ": None,
    "СНИЛС_УК": None,
    "ТИП_КОНКУРСА": None,
    "ПРИОРИТЕТ": None,
    "ЕГЭ_С_ИД": None,
    "ЕГЭ": None,
    "ВИ_1": None,
    "ВИ_2": None,
    "ВИ_3": None,
    "ВИ_4": None,
    "ВИ_5": None,
    "ВИ_6": None,
    "ИД": None
}

competition_form = {
    "Без ВИ" : "БВИ",
    "По результатам ВИ": "ОБЩИЙ",
    ""
}

def format_data(data, form):
    form["СНИЛС_УК"] = data[0].getText()
    form["ТИП_КОНКУРСА"] = match data[1].getText()

if not os.path.isfile("spbsu_links.txt"):
    os.system("spbsu_links.py 1")

links = []
with open("spbsu_links.txt", "r") as links_file:
    for link in links_file:
        links.append(link[:-1])

link = links[0]

page = soup(requests.get(link).content.decode("utf-8"), "lxml")

main_info = page.find("p").find_all("b")
if len(main_info) < 6:
    print(f"Ранжированный список составлен иначе:{link}\n")
    # continue
data_form["УРОВЕНЬ_ОБУЧЕНИЯ"] = str(main_info[0].next_sibling).strip()
data_form["НАПРАВЛЕНИЕ"] = str(main_info[2].next_sibling).strip()
data_form["ОП"] = str(main_info[3].next_sibling).strip()
data_form["ФОРМА_ОБУЧЕНИЯ"] = str(main_info[4].next_sibling).strip()
data_form["ОСНОВА_ОБУЧЕНИЯ"] = "бюджет" if (str(main_info[5].next_sibling).strip() == "Госбюджетная") else "контракт"

exams_count = len(page.find("thead").find("tr").find_all("th")) - 12 + 3
if exams_count < 3:
    print(f"Ранжированный список составлен иначе:{link}\n")
    # continue
for i in range(exams_count):
    data_form[f"ВИ_{i + 1}"] = 0

print(data_form)
applicants_info = page.find("tbody").find_all("tr")
main_applicant_info = applicants_info[0].find_all("td")[1:-2]
print(main_applicant_info)