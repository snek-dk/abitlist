import requests
import json
import time
from bs4 import BeautifulSoup
from multiprocessing import Pool
requests.packages.urllib3.disable_warnings()


def get_base_edu(base_edu):
    if base_edu == 'бюджет':
        return 'Госбюджет'
    elif base_edu == 'контракт':
        return 'Контракт'
    return 'Госбюджет'


def get_konkurs(base_edu, bvi):
    if base_edu in ('бюджет', 'контракт') and bvi != '✓':
        return 'ОК'
    elif base_edu in ('бюджет', 'контракт') and bvi == '✓':
        return 'БВИ'
    elif base_edu == 'целевое':
        return 'ЦК'
    elif base_edu == 'спецквота':
        return 'СК'
    return 'ОП'


def get_sum_with_id(base_edu, bvi, sum_with_id):
    if base_edu in ('бюджет', 'контракт'):
        return str(sum_with_id)
    elif bvi != '✓':
        return str(sum_with_id)
    return '310'


def spbpu_parser(url):

    temp_dict = list()
    url_temp = 'https://enroll.spbstu.ru/enroll-list/'
    try:
        res = requests.get(url_temp + url, verify=False)
    except:
        time.sleep(0.2)
        try:
            res = requests.get(url_temp + url, verify=False)
        except:
            print(url_temp + url)
            return []
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "html.parser")
    k = 0

    id_fak, name_fak, form_edu, base_edu = (url[24::].split(') ')[0].split('_')[1:-1])
    for i in soup.findAll('tr'):  # , {'class': 'R9'}):

        k += 1

        if k >= 25:
            data = i.text.strip().split('\n')
            if not(len(data) > 10):
                continue
            try:
                snils, sum_with_id, sum_without_id, v1, v2, v3, score_id, pp, bvi, original, soglasie = data[1:12]
            except:
                snils, sum_with_id, sum_without_id, v1, v2, v3, score_id, pp, bvi, original, soglasie = data[1:12] + ['']
            temp_dict.append({

                'ВУЗ': 'СПбПУ',
                'Направление': (id_fak + " " + name_fak),
                'ОП': (id_fak + " " + name_fak),
                'Форма_обучения': form_edu,  # .lower().capitalize(),
                'Основа_обучения': get_base_edu(base_edu),
                'СНИЛС_УК': snils,
                'Конкурс': get_konkurs(base_edu, bvi),
                'СУММА': get_sum_with_id(base_edu, bvi, sum_with_id),
                'СУММА_БЕЗ_ИД': sum_without_id.strip(),
                'ВИ_1': str(v1) if len(str(v1)) != 0 else '0',
                'ВИ_2': str(v2) if len(str(v2)) != 0 else '0',
                'ВИ_3': str(v3) if len(str(v3)) != 0 else '0',
                'ВИ_4': None,
                'ВИ_5': None,
                'ИД': str(score_id).strip(),
                'Согласие': "Да" if soglasie == '✓' else "Нет",
                'Оригинал': "Да" if original == 'Оригинал' else "Нет"
            })
    return temp_dict


if __name__ == '__main__':

    with open('./vyz/spbpu/id_url.json', 'r', encoding='utf-8') as input_file:
        url_id = json.load(input_file).values()
    #Pool(число одновременных потоков), по-умолчанию использует все потоки
    with Pool() as p:
        temp_dict = list(p.map(spbpu_parser, [url for url in url_id]))

    json_dict = list()
    for nested_list in temp_dict:
        json_dict.extend(nested_list)
        
    with open('out_json/spbpu.json', 'w', encoding='utf-8') as out_file:
        json.dump(json_dict, out_file, indent=4, ensure_ascii=False)
