import requests
import json
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import time


def get_url():
    mypath = "vyz\mai"
    names = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    names = [x for x in names if x[-3:] != '.py' and x[-5:] != '.html']
    ed_principle = ''
    form_of_education = ''
    links_budget = []
    links_contract = []
    main_link = 'https://public.mai.ru/priem/rating/data/'
    for i in names:
        ed_principle, form_of_education = i.split('+')[1], i.split('+')[2]
        ed_principle, form_of_education
        with open(mypath + '\\' + i, 'rb') as f:
            for j in f.readlines():
                s = j.decode('utf-8')
                link = main_link + s.split('"')[1] + '.html'
                if ed_principle == 'госбюджет':
                    links_budget.append(
                        (link, s.split('"')[2].replace('>', '').replace('\r', '').replace('\n', ''), i.split('+')[-1]))
                else:
                    links_contract.append(
                        (link, s.split('"')[2].replace('>', '').replace('\r', '').replace('\n', ''), i.split('+')[-1]))
    
    return links_budget + links_contract


def main():

    
    #res = requests.get(url, headers=header)
    # print(res)
    #res.encoding = 'utf-8'
    # with open('vyz/mai/out.html', 'w', encoding='utf-8') as res:
    #     out_file.write(res.text)
    
    json_dict = list()
    for url, _, form_edu in get_url():
        time.sleep(0.2)
       
        header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
        url = 'https://public.mai.ru/priem/rating/data/p20220728150006_1_l1_p1_f1_s5.html'
        res = requests.get(url, headers=header)
        if res.status_code != 200:
            print('alarm', res.status_code)
            continue
        print(url)
        soup = BeautifulSoup(res.text, "html.parser")

        tables = list(map(lambda st: st.text.strip(),
                      soup.findAll('h4', {'class': 'mt-5 mb-3'})))
        fak = tables.pop(0)
        fak_num = fak[:8].strip()
        fak = fak[9:]
        fak_name, base_edu = fak.split('(')
        fak_name = fak_name.strip()
        base_edu = base_edu[:-1].strip()

        tables_dict = {'Лица, поступающие по особой квоте': 'ОП',
                       'Лица, поступающие в рамках специальной квоты приема': 'СК',
                       'Лица, поступающие в рамках квоты приема на целевое обучение': 'ЦК',
                       'Лица, поступающие по общему конкурсу': 'ОК'}

        base_edu_dict = {'Бюджет': 'Госбюджет',
                         'Платная': 'Контракт'}

        #tree = lxml.html.document_fromstring(res)
        k = 0
        for table_teg in soup.findAll('table', {'class': 'table'}):

            for abb_teg in table_teg.findAll('tr'):
                abb_data = [
                    abb_teg_info.text for abb_teg_info in abb_teg.findAll('td')][:9]
                #['1', '134-680-920 67', '278', '92', '88', '98', ' 0 ', 'Копия', '\xa0']
                if len(abb_data) == 9:

                    json_dict.append({

                        'ВУЗ': 'МАИ',
                        'Направление': (fak_num + ' ' + fak_name).strip(),
                        'ОП':  (fak_num + ' ' + fak_name).strip(),
                        'Форма_обучения': form_edu,
                        'Основа_обучения': base_edu_dict[base_edu],
                        'СНИЛС_УК': abb_data[1].strip() if len(abb_data[1].strip()) > 0 else None,
                        'Конкурс': tables_dict[tables[k]],
                        'СУММА': abb_data[2].strip() if len(abb_data[2].strip()) > 0 else "0",
                        'СУММА_БЕЗ_ИД': str(int(abb_data[2]) - int(abb_data[6].strip())) if len(str(int(abb_data[6].strip()))) > 0 else abb_data[2].strip(),
                        'ВИ_1': abb_data[3].strip() if len(abb_data[3].strip()) > 0 else "0",
                        'ВИ_2': abb_data[4].strip() if len(abb_data[4].strip()) > 0 else "0",
                        'ВИ_3': abb_data[5].strip() if len(abb_data[5].strip()) > 0 else "0",
                        'ВИ_4': None,
                        'ВИ_5': None,
                        'ИД': abb_data[6].strip() if len(abb_data[6].strip()) > 0 else "0",
                        'Согласие': 'ДА' if abb_data[8].strip() == '✓' else 'Нет',
                        'Оригинал': 'ДА' if abb_data[7].strip() != 'Копия' else 'Нет'
                    })

            k += 1

        with open('out_json\mai.json', 'w', encoding='utf-8') as output:
            json.dump(json_dict, output, indent=4, ensure_ascii=False)
        print('DONE')

main()
