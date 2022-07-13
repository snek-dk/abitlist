import json
import os

def csv_to_json():
    json_dict = dict()
    path = 'source'
    k = 0
    json_out = dict()
    for folder in os.listdir(path):
        json_out[folder] = dict()

        path_folder = path + '/' + folder
        files = os.listdir(path_folder)
        
        for file in files:
            
            json_out[folder][file[:-4]] = list()

            path_file = path_folder + '/' + file
            
            with open(path_file, 'r') as file_csv:
                for line in file_csv:
                    num, name, url = map(lambda st: st.strip(), line.split(';'))
                    json_out[folder][file[:-4]].append([num, name, url])
    with open('source.json', 'w', encoding = 'utf-8') as out_file:
        json.dump(json_out, out_file, indent=4, ensure_ascii=False)
    print('DONE')
csv_to_json()
