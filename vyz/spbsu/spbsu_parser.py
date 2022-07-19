import requests
import os
from bs4 import BeautifulSoup
import json


def save_file_at_dir(dir_path: str, filename: str, file_content, mode='wb'):
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, filename), mode) as f:
        f.write(file_content)


def get_all_foses(url='https://cabinet.spbu.ru/Lists/1k_EntryLists/index_comp_groups.html'):
    url = 'https://cabinet.spbu.ru/Lists/1k_EntryLists/index_comp_groups.html'
    r = requests.get('https://cabinet.spbu.ru/Lists/1k_EntryLists/index_comp_groups.html').content.decode('utf-8')
    my_hrefs = []
    t = BeautifulSoup(r, "lxml")
    for y in t.find_all("a")[1:]:
        new_href = 'https://cabinet.spbu.ru/Lists/1k_EntryLists/'
        new_href += y['href']
        my_hrefs.append(new_href)
    return my_hrefs


def vi(x):
    if len(x.strip(' ')) == 0:
        return '0'
    return x


def more(some_data):
    if len(some_data) <= 10:
        return [None, None]
    elif len(some_data) == 11:
        return [vi(some_data[8]), None]
    else:
        return [vi(some_data[8]), vi(some_data[9])]

print('SPBSU')
# r = requests.get('https://cabinet.spbu.ru/Lists/1k_EntryLists/list_846c2a25-562d-4005-9a39-a54804b939e7.html')
# src = r.content
# save_file_at_dir('C:/admlist/СПбГУ', 'first.html', src)
# with open('C:/admlist/СПбГУ/first.html', encoding='utf-8') as f:
#     page = BeautifulSoup(f.read(), "lxml")
# spbsu = db.abitlist(students=None, commit=True)
links = get_all_foses()
k = 0
needed_data = dict()
# print(links)
links.remove('https://cabinet.spbu.ru/Lists/1k_EntryLists/list_d3c5b730-178a-45a8-8a4a-6548218144b8.html')
num = '0123456789'
for link in links:
    page = BeautifulSoup(requests.get(link).content.decode('utf-8'), "lxml")
    persons = page.find('tbody').find_all('tr')

    head_data = page.find('p').find_all('b')
    field_of_study = head_data[2].next_element.next_element.text.strip()
    ed_program = head_data[3].next_element.next_element.text.strip()
    form_of_education = head_data[4].next_element.next_element.text.strip()
    ed_principle = head_data[5].next_element.next_element.text.strip()
    # head_data_parsed = [field_of_study, ed_program, form_of_education, ed_principle]
    for i in range(len(persons)):
        t = persons[i].find_all('td')
        # print(head_data_parsed)
        some_data = []
        for z in t:
            y = z.text.strip()
            if ',' in y:
                some_data.append(y.split(',')[0])
            elif y.count('.') == 1:
                some_data.append(y.split('.')[0])
            else:
                some_data.append(y)

        some_data = some_data[1:-2]
        # print(some_data)
        items = more(some_data)
        if ed_principle == 'Госбюджетная':
            needed_data[str(k)] = {
                'ВУЗ': 'СПбГУ',
                'Направление': field_of_study,
                'ОП': ed_program,
                'Форма_обучения': form_of_education,
                'Основа_обучения': ed_principle,
                'СНИЛС_УК': some_data[0],
                'Конкурс': some_data[1],
                'СУММА': vi(some_data[3]),
                'СУММА_БЕЗ_ИД': vi(some_data[4]),
                'ВИ_1': vi(some_data[5]),
                'ВИ_2': vi(some_data[6]),
                'ВИ_3': vi(some_data[7]),
                'ВИ_4': items[0],
                'ВИ_5': items[1],
                'ИД': vi(some_data[-2]),
                'Согласие': some_data[-1],
                'Оригинал': some_data[-1]
            }
        elif ed_principle == 'Договорная':
            needed_data[str(k)] = {
                'ВУЗ': 'СПбГУ',
                'Направление': field_of_study,
                'ОП': ed_program,
                'Форма_обучения': form_of_education,
                'Основа_обучения': ed_principle,
                'СНИЛС_УК': some_data[0],
                'Конкурс': some_data[1],
                'СУММА': vi(some_data[2]),
                'СУММА_БЕЗ_ИД': vi(some_data[3]),
                'ВИ_1': vi(some_data[4]),
                'ВИ_2': vi(some_data[5]),
                'ВИ_3': vi(some_data[6]),
                'ВИ_4': items[0],
                'ВИ_5': items[1],
                'ИД': vi(some_data[-2]),
                'Согласие': some_data[-1],
                'Оригинал': some_data[-1]
            }
        else:
            needed_data[str(k)] = {
                'ВУЗ': 'СПбГУ',
                'Направление': field_of_study,
                'ОП': ed_program,
                'Форма_обучения': form_of_education,
                'Основа_обучения': ed_principle,
                'СНИЛС_УК': some_data[0],
                'Конкурс': some_data[1],
                'СУММА': vi(some_data[2]),
                'СУММА_БЕЗ_ИД': vi(some_data[3]),
                'ВИ_1': vi(some_data[4]),
                'ВИ_2': vi(some_data[5]),
                'ВИ_3': vi(some_data[6]),
                'ВИ_4': items[0],
                'ВИ_5': items[1],
                'ИД': some_data[-1],
                'Согласие': 'КВОТА',
                'Оригинал': 'КВОТА'
            }
        k += 1

with open('./out_json/spbsu.json', 'w', encoding='utf-8') as fp:
    json.dump(needed_data, fp, indent=4, ensure_ascii=False)
print('DONE\n')
