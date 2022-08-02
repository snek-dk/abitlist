import os
from multiprocessing import Pool

def start_parser(path):
    print(path.split('/')[-1].split('_')[0], 'start')
    os.system('cmd /c python ./' + path)
    print(path.split('/')[-1].split('_')[0], 'DONE')
    
if __name__ == '__main__':
    if 'out_json' not in os.listdir():
        os.mkdir('./out_json')
    rest = ['mai']
    count = len(os.listdir('vyz')) - len(rest)
    list_vyz = list()
    for name_vyz in os.listdir('./vyz'):
        if name_vyz in rest:
            continue
        path = 'vyz/' + name_vyz + '/'
        for file in os.listdir(path):
            name, exten  = file.split('.')
            if name == name_vyz + '_parser':
                list_vyz.append(path + name + '.' + exten)
                break       

    with Pool(count) as p:
        p.map(start_parser, list_vyz)
