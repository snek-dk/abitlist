import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

def download():
    with open('out.html','w',encoding='utf-8') as out:
        url = 'https://abit.etu.ru/ru/postupayushhim/bakalavriat-i-specialitet/spiski-podavshih-zayavlenie/'
        r = requests.get(url)
        out.write(r.text)
#download()
def pars():
    with open('out.html','r',encoding='utf-8') as html:        
        soup = BeautifulSoup(html, "html.parser")
        for i in soup.findAll('tr'):
            print(i)
            input()
pars()
