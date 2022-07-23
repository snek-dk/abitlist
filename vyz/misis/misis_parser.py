import http.client
import json
from lxml import html
TERMS = {'БВИ': 'БВИ', 'ОК': 'ОП', 'СК': 'СК', 'ОКМ': 'ОК', 'ЦП':'ЦП', '+': 'Да', '0': 'Нет'}
WORKURL = '/applicants/admission/progress/baccalaureate-and-specialties/list-of-applicants'
S = http.client.HTTPSConnection("misis.ru")
cols, data = [], []
content, spec, url = '', '', ''

S.request('GET', f'{WORKURL}/')
content = S.getresponse().read()
parsed = html.fromstring(content)
for x in parsed.findall('.//table/tbody/tr/td/a'):
    spec = x.text
    url = x.get('href').lstrip('.')
    S.request('GET', f'{WORKURL}{url}')
    content = S.getresponse().read()
    parsed = html.fromstring(content)
    for row in parsed.findall('.//table/tbody/tr'):
        cols = [td.text if td.text else '0' for td in row.findall('td')]
        data.append({
            'ВУЗ': 'МИСИС',
            'Направление': spec,
            'ОП': spec,
            'Форма_обучения': 'Заочная' if 'Горное дело' in spec else 'Очная',
            'Основа_обучения': 'Госбюджет',
            'СНИЛС_УК': cols[2] if cols[2] != '0' else None,
            'Конкурс': TERMS[cols[11].split(';')[0]],
            'СУММА': cols[4],
            'СУММА_БЕЗ_ИД': str(int(cols[4]) - int(cols[8])),
            'ВИ_1': cols[5],
            'ВИ_2': cols[6],
            'ВИ_3': cols[7],
            'ВИ_4': None,
            'ВИ_5': None,
            'ИД': cols[8],
            'Согласие': TERMS[cols[9]],
            'Оригинал': TERMS[cols[10]]
        })
S.close()
with open('./out_json/misis.json', 'w', encoding='utf-8') as fp:
    json.dump(data, fp, indent=4, ensure_ascii=False)
