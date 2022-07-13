import os, requests, json
from bs4 import BeautifulSoup

def letu_parser():
    print('LETU')
    json_dict = dict()
    path = 'source'
    k = 0

    for folder in os.listdir(path):
        path_folder = path + '/' + folder
        files = os.listdir(path_folder)
        
        for file in files:
            path_file = path_folder + '/' + file
            
            with open(path_file, 'r') as file_csv:
                for line in file_csv:
                    
                    fak_num, fak_name, fak_url = map(lambda st: st.strip().replace('_', ' '), line.split(';'))
                    print(fak_name, k)
                    r = requests.get(fak_url)
                    soup = BeautifulSoup(r.text, "html.parser")
                    print(fak_num, fak_name, folder)
                    for teg in soup.findAll('tr'):#перебор аббов
                        
                        if len(teg) == 27:

                            data = teg.text.split('\n')[1:-1]                       
                            json_dict[str(k)] = {
                                'ВУЗ': 'ЛЭТИ',
                                'Направление': (fak_num + ' ' + fak_name).strip(),
                                'ОП': (fak_num + ' ' + fak_name).strip(),
                                'Форма_обучения': folder,
                                'Основа_обучения': file[:-4],
                                'СНИЛС_УК': data[1],
                                'Конкурс': data[3],
                                'СУММА': data[4],
                                'СУММА_БЕЗ_ИД': data[5],
                                'ВИ_1': data[6],
                                'ВИ_2': data[7],
                                'ВИ_3': data[8],
                                'ИД': data[9],
                                'Согласие': data[12],
                                'Оригинал': data[11]                            
                                }

                            k += 1
                            
    os.chdir('..')    
    os.chdir('..')
    with open('./out_json/letu.json', 'w', encoding='utf-8') as out_file:
            json.dump(json_dict, out_file,indent=4, ensure_ascii=False)
    print('DONE\n')
letu_parser()    
