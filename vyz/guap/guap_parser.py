import http.client
import json
import re
from lxml import html
CONN = http.client.HTTPSConnection('priem.guap.ru')
TERMS = {'14': 'ОК', '15': 'ОК', '16': 'ЦП', '20': 'ОП', '25': 'СК', '50': 'ИН'}
content = ''
special = {}
cols, data = [], []

CONN.request('GET', '/_lists/Pred_37')
content = CONN.getresponse().read().decode('utf-8')
parsed = html.fromstring(content)
for row in parsed.findall('.//*/table/tbody/tr'):
    cols = row.findall('td')
    special[f'{cols[0].text} {cols[1].text}'] = [a.get('href') for a in row.findall('td/a')]

for spec in special:
    for url in special[spec]:
        CONN.request('GET', url)
        content = CONN.getresponse().read().decode('utf-8')
        parsed = html.fromstring(content)
        for row in parsed.findall('.//*/table/tbody/tr'):
            cols = [i.text_content() for i in row.findall('td')]
            conc = TERMS[url[-2:]]
            if cols[4] == 'Без В/И':
                cols[4] = "0"
                cols[2] = "0"
                conc = 'БВИ'
            ege = re.findall(r"(\d+)", cols[1], flags=re.M)
            ege += ['0'] * (3 - len(ege))
            data.append({
            'ВУЗ': 'ГУАП',
            'Направление': spec,
            'ОП': spec,
            'Форма_обучения': 'Очная',
            'Основа_обучения': 'Госбюджет' if url[-2:] != '15' else 'Контракт',
            'СНИЛС_УК': cols[0] if cols[0] else None,
            'Конкурс': conc,
            'СУММА': cols[4] if cols[4] else None,
            'СУММА_БЕЗ_ИД': cols[2] if cols[2] else None,
            'ВИ_1': ege[0] if ege[0] else None,
            'ВИ_2': ege[1] if ege[1] else None,
            'ВИ_3': ege[2] if ege[2] else None,
            'ВИ_4': None,
            'ВИ_5': None,
            'ИД': cols[3] if cols[3] else None,
            'Согласие': cols[6],
            'Оригинал': cols[7]
        })
CONN.close()
with open('./out_json/guap.json', 'w', encoding='utf-8') as fp:
    json.dump(data, fp, indent=4, ensure_ascii=False)
