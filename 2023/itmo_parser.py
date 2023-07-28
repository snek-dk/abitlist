import json
import time
import requests
import os


def itmo_parser():
    '''Parsing itmo site'''
    # print('ITMO')
    with open('url_id.json', 'r', encoding='utf-8') as input_id:
        urls_id = json.load(input_id)['id_fak']
    k = 0
    json_dict = list()
    name_qu = {'without_entry_tests': 'БВИ',
               'by_unusual_quota': 'ОСК',
               'by_special_quota': 'ОТК',
               'by_target_quota': 'ЦК',
               'general_competition': 'ОК'}
    name_o = {'budget': 'госбюджет',
              'contract': 'контракт'}

    def trans_snils(snils, case):
        if snils != None:
            return snils[:3] + '-' + snils[3:6] + '-' + snils[6:9] + ' ' + snils[9::]
        return case

    for url_id in urls_id:


        urls = {'budget': 'https://abit.itmo.ru/_next/data/YOFhRKl2jyKZVxRx3CkjC/ru/rating/bachelor/budget/' +  url_id + '.json?degree=bachelor&financing=budget&id=' + url_id,
                'contract': 'https://abit.itmo.ru/_next/data/YOFhRKl2jyKZVxRx3CkjC/ru/rating/bachelor/contract/' +  url_id + '.json?degree=bachelor&financing=contract&id=' + url_id}
        for type_o, url in urls.items():
            time.sleep(0.2)
            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
            res = requests.get(url, headers=head, verify='certs.pem').json()

            try:
                fakultet = res['pageProps']['programList']['direction']['direction_title']
            except:

                print('ссылка битая')
                continue
            if len(res['pageProps']['programList'].keys()) == 7:
                # print(fakultet, type_o, k) ## debug!!!
                for quota in name_qu.keys():
                    for abbi in res['pageProps']['programList'][quota]:

                        json_dict.append({
                            'ВУЗ': 'ИТМО',
                            'ОСНОВА_ОБУЧЕНИЯ': "Контракт" if name_o[type_o].strip() == "контракт" else "Бюджет",
                            "УРОВЕНЬ_ОБУЧЕНИЯ": "Бакалавриат",
                            'НАПРАВЛЕНИЕ': fakultet,
                            'ОП': fakultet,
                            'ФОРМА_ОБУЧЕНИЯ': 'Очная',
                            'СНИЛС_УК': trans_snils(abbi['snils'], abbi['case_number']),
                            'ТИП_КОНКУРСА': name_qu[quota].strip(),
                            'ПРИОРИТЕТ':abbi['priority'],
                            'ОРИГИНАЛ':abbi['is_send_original'],
                            'ПП' : abbi['is_have_advantages'],
                            'ЕГЭ_С_ИД': int(abbi['total_scores']) if abbi['total_scores'] != None else 0,
                            'ЕГЭ': (int(abbi['total_scores'] if abbi['total_scores'] != None else 0) - int(abbi['ia_scores'] if abbi['ia_scores'] != None else 0)),
                            'ВИ_1': 0,
                            'ВИ_2': 0,
                            'ВИ_3': 0,
                            'ВИ_4': None,
                            'ВИ_5': None,
                            "ВИ_6": None,
                            'ИД': int(abbi['ia_scores']) if abbi['ia_scores'] != None else 0,
                            "МЕСТА": {
                                "Бюджет": res['pageProps']['programList']['direction']['budget_min'],
                                "Контракт": res['pageProps']['programList']['direction']['target_reception']}
                    }
                        )

                        if abbi['disciplines_scores'] != None and len(abbi['disciplines_scores']) > 0:
                            for keys_disp, values_disp in abbi['disciplines_scores'].items():
                                if 'матем' in str(keys_disp).lower():
                                    json_dict[k]['ВИ_1'] = int(
                                        values_disp) if values_disp else 0
                                elif 'русс' in str(keys_disp).lower():
                                    json_dict[k]['ВИ_3'] = int(
                                        values_disp) if values_disp else 0
                                else:
                                    json_dict[k]['ВИ_2'] = int(
                                        values_disp) if values_disp else 0
                        for i in range(1, 4):
                            if json_dict[k]['ВИ_'+str(i)] == "None":
                                json_dict[k]['ВИ_'+str(i)] = 0

                        k += 1

            else:

                # res['result']['items']
                for abbi in res['pageProps']['programList']['items']:
                    json_dict.append({
                            'ВУЗ': 'ИТМО',
                            'ОСНОВА_ОБУЧЕНИЯ': "Контракт" if name_o[type_o].strip() == "контракт" else "Бюджет",
                            "УРОВЕНЬ_ОБУЧЕНИЯ": "Бакалавриат",
                            'НАПРАВЛЕНИЕ': fakultet,
                            'ОП': fakultet,
                            'ФОРМА_ОБУЧЕНИЯ': 'Очная',
                            'СНИЛС_УК': trans_snils(abbi['snils'], abbi['case_number']),
                            'ТИП_КОНКУРСА': name_qu[quota].strip(),
                            'ПРИОРИТЕТ':abbi['priority'],
                            'ОРИГИНАЛ':abbi['is_send_original'],
                            'ПП' : abbi['is_have_advantages'],
                            'ЕГЭ_С_ИД': int(abbi['total_scores']) if abbi['total_scores'] != None else 0,
                            'ЕГЭ': (int(abbi['total_scores'] if abbi['total_scores'] != None else 0) - int(abbi['ia_scores'] if abbi['ia_scores'] != None else 0)),
                            'ВИ_1': 0,
                            'ВИ_2': 0,
                            'ВИ_3': 0,
                            'ВИ_4': None,
                            'ВИ_5': None,
                            "ВИ_6": None,
                            'ИД': int(abbi['ia_scores']) if abbi['ia_scores'] != None else 0,
                            "МЕСТА": {
                                "Бюджет": res['pageProps']['programList']['direction']['budget_min'],
                                "Контракт": res['pageProps']['programList']['direction']['target_reception']}
                    })

                    if abbi['disciplines_scores'] != None and len(abbi['disciplines_scores']) > 0:
                        for keys_disp, values_disp in abbi['disciplines_scores'].items():
                            if 'матем' in str(keys_disp).lower():
                                json_dict[k]['ВИ_1'] = int(values_disp) if values_disp else 0
                            elif 'русс' in str(keys_disp).lower():
                                json_dict[k]['ВИ_3'] = int(values_disp) if values_disp else 0
                            else:
                                json_dict[k]['ВИ_2'] = int(values_disp) if values_disp else 0

                    for i in range(1, 4):
                        if json_dict[k]['ВИ_'+str(i)] == "None":
                            json_dict[k]['ВИ_'+str(i)] = 0
                    k += 1

    with open('itmo.json', 'w', encoding='utf-8') as out_file:
        json.dump(json_dict, out_file, indent=4, ensure_ascii=False)
    # print('DONE\n')


itmo_parser()