import http.client
import json
import re
from lxml import html
S = http.client.HTTPSConnection('priem.guap.ru')
SUFF = {'26': 'Заочная', '27': 'Заочная', '29': 'Очно-заочная', '36': 'Очная', '37': 'Очная'}
TERMS = {'14': 'ОК', '15': 'К', '16': 'ЦП', '20': 'ОП', '25': 'СК', '50': 'ИН'}
cols, data, ege = [], [], []
content, spec, url, conc = '', '', '', ''
for suff in SUFF:
    S.request('GET', f'/_lists/Pred_{suff}')
    content = S.getresponse().read()
    parsed = html.fromstring(content)
    for a in parsed.findall('.//table/tbody/tr/td/a'):
        url = a.get('href')
        S.request('GET', url)
        content = S.getresponse().read()
        parsed = html.fromstring(content)
        spec = parsed.findall('.//h3')[1].text
        for row in parsed.findall('.//table/tbody/tr'):
            cols = [i.text for i in row.findall('td')]
            conc = TERMS[url[-2:]]
            if cols[4] == 'Без В/И':
                conc = 'БВИ'
                cols[2] = cols[4] = "0"
            if cols[1]:
                ege = re.findall(r"(\d+)", cols[1])
            ege += ["0"] * (3-len(ege))
            data.append({
                'ВУЗ': 'ГУАП',
                'Направление': spec,
                'ОП': spec,
                'Форма_обучения': SUFF[suff],
                'Основа_обучения': 'Госбюджет' if url[-2:] != '15' else 'Контракт',
                'СНИЛС_УК': cols[0] if cols[0] != '0' else None,
                'Конкурс': conc,
                'СУММА': cols[4],
                'СУММА_БЕЗ_ИД': cols[2],
                'ВИ_1': ege[0],
                'ВИ_2': ege[1],
                'ВИ_3': ege[2],
                'ВИ_4': None,
                'ВИ_5': None,
                'ИД': cols[3],
                'Согласие': cols[6],
                'Оригинал': cols[7]
            })
S.close()
with open('./out_json/guap.json', 'w', encoding='utf-8') as fp:
    json.dump(data, fp, indent=4, ensure_ascii=False)
