import requests
from bs4 import BeautifulSoup as soup

main_link = 'https://ba.hse.ru/base2022'
req = requests.get(main_link, ascii(False)).text
data = soup(req, "lxml")
hse_all = data.find_all('tbody')
moscow_tds = hse_all[0].find_all('tr')[1:]  # href = hse_all[0].find_all('tr')[1:][0].a.text
nn_tds = hse_all[1].find_all('tr')[1:]
perm_tds = hse_all[2].find_all('tr')[1:]
spb_tds = hse_all[3].find_all('tr')[1:]
moscow_list = [[moscow_tds[i].next_element.next_element.text, moscow_tds[i].a.text] for i in range(len(moscow_tds))]
nn_list = [[nn_tds[i].next_element.next_element.text, nn_tds[i].a.text] for i in range(len(nn_tds))]
perm_list = [[perm_tds[i].next_element.next_element.text, perm_tds[i].a.text] for i in range(len(perm_tds))]
spb_list = [[spb_tds[i].next_element.next_element.text, spb_tds[i].a.text] for i in range(len(spb_tds))]
for each in moscow_list:
    name = each[0].replace(',', '').replace(' ', '_').replace('"', '')
    file = requests.get(each[1]).content
    with open(rf'tables/moscow/{name}.xlsx', "wb") as f:
        f.write(file)
for each in nn_list:
    name = each[0].replace(',', '').replace(' ', '_').replace('"', '')
    file = requests.get(each[1]).content
    with open(rf'tables/nn/{name}.xlsx', "wb") as f:
        f.write(file)
for each in perm_list:
    name = each[0].replace(',', '').replace(' ', '_').replace('"', '')
    file = requests.get(each[1]).content
    with open(rf'tables/perm/{name}.xlsx', "wb") as f:
        f.write(file)
for each in spb_list:
    name = each[0].replace(',', '').replace(' ', '_').replace('"', '')
    file = requests.get(each[1]).content
    with open(rf'tables/spb/{name}.xlsx', "wb") as f:
        f.write(file)
