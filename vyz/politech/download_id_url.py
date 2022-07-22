import requests, json
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

url = 'https://enroll.spbstu.ru/back/api/incoming-lists'
#https://enroll.spbstu.ru/enroll-list/%D0%9A%D0%BE%D0%BD%D0%BA%D1%83%D1%80%D1%81%D0%BD%D1%8B%D0%B9%20%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%202022%20(000000011_01.03.02_%D0%9F%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%B0%D1%8F%20%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0_%D0%BE%D1%87%D0%BD%D0%BE%D0%B5_%D0%BA%D0%BE%D0%BD%D1%82%D1%80%D0%B0%D0%BA%D1%82%20%D0%98%D0%9D%D0%9E_%D0%9F%D0%9E)%20(HTML5).html
json_dict = dict()
k = 0
res = requests.get(url, verify=False)
res.encoding = 'utf-8'

for id_url in res.json():
    url = id_url['name']
    if url[-12::] == "(HTML5).html" and url[:24] == "Конкурсный список 2022 ("  and requests.get('https://enroll.spbstu.ru/enroll-list/' + url, verify=False).status_code == 200:
        print(url)
        json_dict[str(k)] = url
        k += 1
with open('vyz/politech/id_url.json', 'w', encoding='utf-8') as out_file:
    json.dump(json_dict, out_file, ensure_ascii=False, indent=4)
print('DONE\n')