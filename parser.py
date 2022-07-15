import os

if 'out_json' not in os.listdir():
    os.mkdir('./out_json')
    
for folder in os.listdir('./vyz'):
    path = './vyz/' + folder# + '/' + folder + '_parser.py'
    os.chdir(path)   
    os.system('cmd /c python ' + folder + '_parser.py')
    #os. _exit()
    os.chdir('..'); os.chdir('..')