import os, subprocess
import shutil

cwd = os.getcwd()
# subprocess.call(['node', 'main.js'], cwd=cwd)

for i in range(51):
    try:
        if os.path.getsize(rf"{cwd}\МИРЭА{str(i)}.json")//(2**13) > 5:
            shutil.move(rf"{cwd}\МИРЭА{str(i)}.json", '../../out_json')
    except:
        print("НЕ СПАРСИЛОСЬ :C, ПЕРЕЗАПУСТИ!!!")
print('DONE\n')
