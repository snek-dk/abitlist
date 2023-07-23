import requests
from bs4 import BeautifulSoup as soup

spbsu_links_page = soup(
    requests.get("https://cabinet.spbu.ru/Lists/1k_EntryLists/index_comp_groups.html").content.decode("utf-8"), "lxml")

main_link = "https://cabinet.spbu.ru/Lists/1k_EntryLists/"
links = [main_link + link["href"] for link in spbsu_links_page.find_all('a')[1:]]

with open("spbsu_links.txt", "w") as file:
    for link in links:
        file.write("%s\n" % link)