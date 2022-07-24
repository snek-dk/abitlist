import http.client
import json
data = []
KON = {'Без': 'БВИ', 'Целевая': 'ЦП', 'Общий': 'ОК', 'По': 'ОК', 'Особое': 'ОП', 'Специальная': 'СК'}
def to_data(abitur):
    spec = f'{abitur["okso"]} {" ".join(abitur["spec_name"].split()[1:]).capitalize()}'
    kon = KON[abitur['konkurs'].split()[0]] if len(abitur['konkurs'].split()) else 'ОК'
    data.append({
            'ВУЗ': 'Горный',
            'Направление': spec,
            'ОП': spec,
            'Форма_обучения': 'Очная',
            'Основа_обучения': 'Контракт' if 'договор' in abitur['konkurs'] else 'Госбюджет',
            'СНИЛС_УК': abitur['snilsnumber_p'] if abitur['snilsnumber_p'] else None,
            'Конкурс': kon,
            'СУММА': abitur['sum_ball'] if abitur['sum_ball'] and abitur['sum_ball'].isdigit() else '0',
            'СУММА_БЕЗ_ИД': str(abitur['ege_ball']),
            'ВИ_1': str(abitur['ege_other']),
            'ВИ_2': str(abitur['ege_math']),
            'ВИ_3': str(abitur['ege_russ']),
            'ВИ_4': None,
            'ВИ_5': None,
            'ИД': str(abitur['id_ball']),
            'Согласие': 'Да' if abitur['rek_sogl'] else 'Нет',
            'Оригинал': 'Да'if abitur['orig'] == 'Оригинал' else 'Нет'
        })

S = http.client.HTTPSConnection('priem2022.spmi.ru')
lists = ('/wave/public/data/naprBakalavrBudjet.json', '/wave/public/data/naprSpecialistBudjet.json', '/wave/public/data/naprBakalavrKontrakt.json', '/wave/public/data/naprSpecialistKontrakt.json')
for url in lists:
    S.request('GET', url)
    for spec in json.loads(S.getresponse().read()):
        S.request('GET', f'/wave/public/data/{spec["program_id"]}{spec["code_p"]}.json')
        for abitur in json.loads(S.getresponse().read()):
            to_data(abitur)
S.close()
with open('./out_json/gorniy.json', 'w', encoding='utf-8') as fp:
    json.dump(data, fp, indent=4, ensure_ascii=False)
