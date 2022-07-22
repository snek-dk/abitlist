import os, requests, json
from bs4 import BeautifulSoup

def letu_parser():
    #print('LETU')
    json_dict = dict()
    sort_score = {
        "01.03.02" : 'рми',
        "09.03.01" : 'мри',
        "09.03.02" : 'мри',
        "09.03.04" : 'мри',
        "10.05.01" : 'мри',
        "11.03.01" : 'мри',
        "11.03.02" : 'мри',
        "11.03.03" : 'мри',
        "11.03.04" : 'мри',
        "11.05.01" : 'мри',
        "12.03.01" : 'мри',
        "12.03.04" : 'мри',
        "13.03.02" : 'мир',
        "15.03.06" : 'мри',
        "20.03.01" : 'мри',
        "27.03.02" : 'мри',
        "27.03.03" : 'мри',
        "27.03.04" : 'мри',
        "27.03.05" : 'мри',
        "28.03.01" : 'мри',
        "42.03.01": '',
        "45.03.02": ''
    }

#Управление в технических системах. Автоматика и робототехнические системы 27.03.04 мир
#key_words = Автоматика

    k = 0

    with open('vyz/letu/source.json', 'r', encoding='utf-8') as input_file:
        input_json = json.load(input_file)

    for type_o in input_json.keys():

        for faks_of_type_o in input_json[type_o].keys():

            for fak in input_json[type_o][faks_of_type_o]:
                print(*list(map(lambda st: st.strip().replace('_', ' '), fak))[:2], k)
                fak_num, fak_name, fak_url = map(lambda st: st.strip().replace('_', ' '), fak)

                r = requests.get(fak_url)
                soup = BeautifulSoup(r.text, "html.parser")

                for teg in soup.findAll('tr'):

                    if len(teg) == 27:
                        data = teg.text.split('\n')[1:-1]
                        json_dict[str(k)] = {
                            'ВУЗ': 'ЛЭТИ',
                            'Направление': (fak_num + ' ' + fak_name).strip(),
                            'ОП': (fak_num + ' ' + fak_name).strip(),
                            'Форма_обучения': type_o,
                            'Основа_обучения': faks_of_type_o,
                            'СНИЛС_УК': data[1],
                            'Конкурс': data[3],
                            'СУММА': str(data[4]),
                            'СУММА_БЕЗ_ИД': str(data[5]),
                            'ВИ_1': str(data[6]),
                            'ВИ_2': str(data[7]),
                            'ВИ_3': str(data[8]),
                            'ВИ_4': None,
                            'ВИ_5': None,
                            'ИД': str(data[9]),
                            'Согласие': data[12],
                            'Оригинал': data[11]
                        }
                        
                        order_score = sort_score[fak_num]

                        if fak_num not in ("27.03.04", "42.03.01", "45.03.02"):

                            if order_score == 'рми':
                                s1, s2, s3 = [json_dict[str(k)]['ВИ_' + str(j)] for j in range(1,4)]
                                json_dict[str(k)]['ВИ_1'], json_dict[str(k)]['ВИ_2'], json_dict[str(k)]['ВИ_3'] = s2, s3, s1

                            elif order_score == 'мри':
                                s1, s2, s3 = [json_dict[str(k)]['ВИ_' + str(j)] for j in range(1,4)]
                                json_dict[str(k)]['ВИ_1'], json_dict[str(k)]['ВИ_2'], json_dict[str(k)]['ВИ_3'] = s1, s3, s2

                        elif fak_num == "27.03.04" and "Автоматика" not in fak_name:

                            s1, s2, s3 = [json_dict[str(k)]['ВИ_' + str(j)] for j in range(1,4)]
                            json_dict[str(k)]['ВИ_1'], json_dict[str(k)]['ВИ_2'], json_dict[str(k)]['ВИ_3'] = s1, s3, s2

                        k += 1

    with open('./out_json/letu.json', 'w', encoding='utf-8') as out_file:
        json.dump(json_dict, out_file, indent=4, ensure_ascii=False)
    #print('DONE\n')


letu_parser()