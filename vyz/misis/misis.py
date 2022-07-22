import http.client
import json
from lxml import html
TERMS = {'БВИ': 'БВИ', 'ОК': 'ОП', 'СК': 'СК', 'ОКМ': 'ОК', 'ЦП':'ЦП'}
STATE = {'+': 'Да', '': 'Нет'}
CONN = http.client.HTTPSConnection("misis.ru")
special, data = {}, {}
cols = []
content = ''
k = 0


CONN.request('GET', '/applicants/admission/progress/baccalaureate-and-specialties/list-of-applicants/')
content = CONN.getresponse().read().decode('utf-8')
parsed = html.fromstring(content)
table = parsed.findall('.//*/table/tbody/tr/td/a')
special = {x.text_content(): x.get('href').lstrip('.') for x in table}
for spec in special:
    CONN.request('GET', f'/applicants/admission/progress/baccalaureate-and-specialties/list-of-applicants{special[spec]}')
    content = CONN.getresponse().read().decode('utf-8')
    parsed = html.fromstring(content)
    for row in parsed.findall('.//*/table/tbody/tr'):
        cols = [i.text_content() for i in row.findall('td')]
        data[str(k)] = {
            'ВУЗ': 'МИСИС',
            'Направление': spec,
            'ОП': spec,
            'Основа_обучения': 'Госбюджет',
            'СНИЛС УК': cols[2],
            'Конкурс': TERMS[cols[11].split(';')[0]],
            'СУММА': cols[4],
            'СУММА_БЕЗ_ИД': str(int(cols[4]) - int(cols[8])),
            'ВИ_1': cols[5],
            'ВИ_2': cols[6],
            'ВИ_3': cols[7],
            'ВИ_4': None,
            'ВИ_5': None,
            'ИД': cols[8],
            'Согласие': STATE[cols[9]],
            'Оригинал': STATE[cols[10]]
        }
        k += 1
        
CONN.close()
with open('./out_json/misis.json', 'w', encoding='utf-8') as fp:
    json.dump(data, fp, indent=4, ensure_ascii=False)