import os, requests, json
from bs4 import BeautifulSoup

def letu_parser():
    print('LETU')
    json_dict = dict()
    
    k = 0
    
    with open('source.json', 'r', encoding='utf-8') as input_file:
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
                            'СУММА': data[4],
                            'СУММА_БЕЗ_ИД': data[5],
                            'ВИ_1': data[6],
                            'ВИ_2': data[7],
                            'ВИ_3': data[8],
                            'ВИ_4': None,
                            'ВИ_5': None,
                            'ИД': data[9],
                            'Согласие': data[12],
                            'Оригинал': data[11]                            
                            }

                        k += 1
                            
    with open('/../../out_json/letu.json', 'w', encoding='utf-8') as out_file:
            json.dump(json_dict, out_file,indent=4, ensure_ascii=False)
    print('DONE\n')

letu_parser()   
