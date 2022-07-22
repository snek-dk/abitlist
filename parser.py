import os
from multiprocessing import Pool

def start_parser(path):
    print(path.split('/')[-1].split('_')[0], 'start')
    os.system('cmd /c python ./' + path)
    print(path.split('/')[-1].split('_')[0], 'DONE')
    
if __name__ == '__main__':
    if 'out_json' not in os.listdir():
        os.mkdir('./out_json')
    rest = ['hse', 'itmo', 'spbsu', 'letu', 'misis', 'guap']
    count = len(os.listdir('vyz')) - len(rest)
    list_vyz = list()
    for folder in os.listdir('./vyz'):
        if folder in rest:
            continue
        list_vyz.append('vyz/' + folder + '/' + folder + '_parser.py')

    with Pool(count) as p:
        p.map(start_parser, list_vyz)
