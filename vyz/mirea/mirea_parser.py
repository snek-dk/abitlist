import os, subprocess
import shutil

cwd = os.getcwd()
subprocess.call(['node', 'main.js'], cwd=cwd)

for i in range(51):
    try:
        if os.path.getsize(cwd + '\\' + f'МИРЭА{str(i)}.json')//(2**13) > 5:
            shutil.move(cwd + '\\' + f'МИРЭА{str(i)}.json', '../../out_json')
    except:
        print("НЕ СПАРСИЛОСЬ :C, ПЕРЕЗАПУСТИ!!!")
print('DONE\n')
