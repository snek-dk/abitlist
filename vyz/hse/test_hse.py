import openpyxl
from os import listdir
from os.path import isfile, join


cities = ["moscow", "nn", "perm", "spb"]
for city in cities:
    mypath = rf"C:\Users\dmitr\PycharmProjects\abitlist\vyz\hse\tables\{city}"
    names = [f[:-5] for f in listdir(mypath) if isfile(join(mypath, f))]
    for name in names:
        path = rf"C:\Users\dmitr\PycharmProjects\abitlist\vyz\hse\tables\{city}\{name}.xlsx"
        print(path)

path = rf"C:\Users\dmitr\PycharmProjects\abitlist\vyz\hse\tables\{cities[0]}\Информатика_и_вычислительная_техника.xlsx"
book = openpyxl.open(path, data_only=True, read_only=True)
sheet = book.active
for row in sheet.iter_rows(min_row=18, max_col=17 * 2, max_row=19, min_col=2):
    flag = False
    for cell in row:
        if flag:
            print(cell.value)
        flag = not (flag)
    break
