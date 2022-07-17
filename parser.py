import os

if 'out_json' not in os.listdir():
    os.mkdir('./out_json')
rest = ['politech']
for folder in os.listdir('./vyz'):
    if folder in rest:
        continue
    path = './vyz/' + folder# + '/' + folder + '_parser.py'
    os.chdir(path)   
    os.system('cmd /c python ' + folder + '_parser.py')
    os.chdir('..')
    os.chdir('..')