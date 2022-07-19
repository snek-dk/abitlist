from re import U
import requests, json, os

url_temp = ['https://enroll.spbstu.ru/back/api/', '?trajectory=1']
level_edu = {'Бакалавр': '&training_level=2'}  # , 'Специалитет':'&training_level=5'}
count = 0
temp_dict = dict()

for keys_level_edu, values_level_edu in level_edu.items():
    url = ''.join(url_temp[0] + 'formEducation' + url_temp[1])
    parametrs_url = [values_level_edu]
    res = requests.get(url + ''.join(parametrs_url), verify=False).json()
    form_edu = {i['form_education_translate'][0]['name']: '&form_education=' + str(i['id']) for i in res}

    for keys_form_edu, values_form_edu in form_edu.items():
        url = ''.join(url_temp[0] + 'statements/formPayments' + url_temp[1])
        if len(parametrs_url) == 2:
            parametrs_url[1] = values_form_edu
        else:
            parametrs_url.append(values_form_edu)
        res = requests.get(url + ''.join(parametrs_url), verify=False).json()
        gfa = {i['translate'][0]['name']: '&form_payment=' + str(i['id']) for i in res}

        for keys_gfa, values_gfa in gfa.items():
            url = ''.join(url_temp[0] + 'faculty' + url_temp[1])
            if len(parametrs_url) == 3:
                parametrs_url[-1] = values_gfa
            else:
                parametrs_url.append(values_gfa)
            res = requests.get(url + ''.join(parametrs_url), verify=False).json()
            instituts = {i['faculty_translate'][0]['name'].replace('\xa0', ' '): '&faculty=' + str(i['id']) for i in
                         res}

            for key_insituts, values_instituts in instituts.items():
                url = ''.join(url_temp[0] + 'direction-trainings' + url_temp[1])
                if len(parametrs_url) == 4:
                    parametrs_url[-1] = values_instituts
                else:
                    parametrs_url.append(values_instituts)
                res = requests.get(url + ''.join(parametrs_url), verify=False).json()
                dir_edu = {i['translate'][0]['name']: '&direction_training=' + str(i['id']) for i in res}

                for key_dir_edu, values_dir_edu in dir_edu.items():
                    if len(parametrs_url) == 5:
                        parametrs_url[-1] = values_dir_edu
                    else:
                        parametrs_url.append(values_dir_edu)

                    url = 'https://enroll.spbstu.ru/back/api/statements/lists-applicants?' + ''.join(parametrs_url)[1:] + '&benefits=0&page=1&per_page=5&trajectory=1'

                    res = requests.get(url, verify=False).json()['data']

                    for abb in res:
                        # snils = abb['users']['snils']
                        # print(parametrs_url)
                        # abb['ege']["result_ege"]
                        # temp_dict[str(count)] = {
                        #            'ВУЗ': 'Политех',
                        #            'Направление': (fak_num + ' ' + fak_name).strip(),
                        #           'ОП': (fak_num + ' ' + fak_name).strip(),
                        #          'Форма_обучения': keys_form_edu,
                        #         'Основа_обучения': keys_gfa,
                        #        'СНИЛС_УК': abb['users']['snils']
                        #           'Конкурс': data[3],
                        #          'СУММА': str(data[4]),
                        #         'СУММА_БЕЗ_ИД': str(data[5]),
                        #        'ВИ_1': ,
                        #      'ВИ_2': str(data[7]),
                        #       'ВИ_3': str(data[8]),
                        #           'ВИ_4': None,
                        #          'ВИ_5': None,
                        #         'ИД': str(data[9]),
                        #        'Согласие': data[12],
                        #       'Оригинал': data[11]
                        # }

                        temp_dict[str(count)] = abb
                        count += 1

                        print(count)

print(len(temp_dict))
with open('vyz/politech/out.json', 'w', encoding='utf-8') as out_file:
    json.dump(temp_dict, out_file, ensure_ascii=False, indent=4)
