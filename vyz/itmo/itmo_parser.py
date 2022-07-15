import json, time, requests, os

def itmo_parser():
    '''Parsing itmo site'''
    print('ITMO')
    with open('url_id.json', 'r', encoding='utf-8') as input_id:
        urls_id = json.load(input_id)['id_fak']
    k = 0
    os.chdir('..')
    os.chdir('..') 
    json_dict = dict()
    name_qu = {'without_entry_tests':'БВИ',
               'by_unusual_quota':'ОП',
               'by_special_quota':'СК',
               'by_target_quota': 'ЦК',
               'general_competition': 'ОК'}
    name_o = {'budget':'госбюджет',
              'contract':'контракт'}
    
    def trans_snils(snils, case):
        if snils != None:
            return snils[:3] + '-' + snils[3:6] + '-' + snils[6:9] + ' ' + snils[9::]
        return case

    for url_id in urls_id:
        
        urls = {'budget':'https://abitlk.itmo.ru/api/v1/9e2eee80b266b31c8d65f1dd3992fa26eb8b4c118ca9633550889a8ff2cac429/rating/bachelor/' + 'budget' + '?program_id=' + url_id + '&manager_key=',
               'contract':'https://abitlk.itmo.ru/api/v1/9e2eee80b266b31c8d65f1dd3992fa26eb8b4c118ca9633550889a8ff2cac429/rating/bachelor/' + 'contract' +'?program_id=' + url_id + '&manager_key='}

        for type_o, url in urls.items():
            
            res = requests.get(url, verify='./certificate/certs.pem').json()    
            fakultet = res['result']['direction']['direction_title']
            if len(res['result'].keys()) == 7:
               print(fakultet, type_o, k) ## debug!!! 
               for quota in name_qu.keys():
                   for abbi in res['result'][quota]:
                                                      
                        json_dict[str(k)] = {
                                    'ВУЗ': 'ИТМО',
                                    'Направление': fakultet,
                                    'ОП': fakultet,
                                    'Форма_обучения': 'очная',
                                    'Основа_обучения': (name_o[type_o] + ' ' + name_qu[quota]).strip(),
                                    'СНИЛС_УК': trans_snils(abbi['snils'], abbi['case_number']),
                                    'Конкурс': abbi['exam_type'],
                                    'СУММА': str(abbi['total_scores']) if abbi['total_scores'] != None else '0',
                                    'СУММА_БЕЗ_ИД': str(int(abbi['total_scores'] if abbi['total_scores'] != None else 0) - int(abbi['ia_scores'] if abbi['ia_scores']!= None else 0)),
                                    'ВИ_1': '0',
                                    'ВИ_2': '0',
                                    'ВИ_3': '0',
                                    'ВИ_4': None,
                                    'ВИ_5': None,
                                    'ИД': str(abbi['ia_scores']) if abbi['ia_scores']!= None else '0',
                                    'Согласие': 'ДА' if abbi['send_agreement'] else 'НЕТ',
                                    'Оригинал': 'ДА' if abbi['is_send_original'] else 'НЕТ'                            
                                    } 
                         
                        if abbi['disciplines_scores'] != None and len(abbi['disciplines_scores'])>0:   
                            predmets = [i for i in list(abbi['disciplines_scores'].values()) if str(i).isdigit()]
                            if len(predmets) == 3:
                                json_dict[str(k)]['ВИ_1'] = str(predmets[0])
                                json_dict[str(k)]['ВИ_2'] = str(predmets[1])
                                json_dict[str(k)]['ВИ_3'] = str(predmets[2])
                            elif len(predmets) == 2:
                                json_dict[str(k)]['ВИ_1'] = str(predmets[0])
                                json_dict[str(k)]['ВИ_2'] = str(predmets[1])
                            elif len(predmets) == 1:
                                json_dict[str(k)]['ВИ_1'] = str(predmets[0])
                            
                        k += 1

            else:
                #res['result']['items']
                for abbi in res['result']['items']:
                    json_dict[str(k)] = {
                                    'ВУЗ': 'ИТМО',
                                    'Направление': fakultet,
                                    'ОП': fakultet,
                                    'Форма_обучения': 'очная',
                                    'Основа_обучения': 'контракт',
                                    'СНИЛС_УК': trans_snils(abbi['snils'], abbi['case_number']),
                                    'Конкурс': abbi['exam_type'],
                                    'СУММА': str(abbi['total_scores']) if abbi['total_scores'] != None else '0',
                                    'СУММА_БЕЗ_ИД': str(int(abbi['total_scores'] if abbi['total_scores'] != None else 0) - int(abbi['ia_scores'] if abbi['ia_scores']!= None else '0')),
                                    'ВИ_1': '0',
                                    'ВИ_2': '0',
                                    'ВИ_3': '0',
                                    'ВИ_4': None,
                                    'ВИ_5': None,
                                    'ИД': str(abbi['ia_scores']) if abbi['ia_scores']!= None else '0',
                                    'Согласие': 'ДА' if abbi['send_agreement'] else 'НЕТ',
                                    'Оригинал': 'ДА' if abbi['is_send_original'] else 'НЕТ'                            
                                    } 
                         
                    if abbi['disciplines_scores'] != None and len(abbi['disciplines_scores'])>0:   
                        predmets = [i for i in list(abbi['disciplines_scores'].values()) if str(i).isdigit()]
                        if len(predmets) == 3:
                            json_dict[str(k)]['ВИ_1'] = str(predmets[0])
                            json_dict[str(k)]['ВИ_2'] = str(predmets[1])
                            json_dict[str(k)]['ВИ_3'] = str(predmets[2])
                        elif len(predmets) == 2:
                            json_dict[str(k)]['ВИ_1'] = str(predmets[0])
                            json_dict[str(k)]['ВИ_2'] = str(predmets[1])
                        elif len(predmets) == 1:
                            json_dict[str(k)]['ВИ_1'] = str(predmets[0])
                            
                    k += 1    




           
    with open('./out_json/itmo.json', 'w', encoding='utf-8') as out_file:
        json.dump(json_dict, out_file,indent=4, ensure_ascii=False)
    print('DONE\n')

itmo_parser()

