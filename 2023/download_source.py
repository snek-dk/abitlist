from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time, json


def download_source():
    '''Download id in json to create url'''

    url = 'https://abit.itmo.ru/ratings/bachelor'
    driver = Chrome()
    driver.get(url)
    time.sleep(2)
    table = driver.find_elements(By.TAG_NAME, 'a')
    json_dict = {'id_fak': set()}

    for i in table:

        micro_url = str(i.get_attribute("href"))
        time.sleep(0.01)
        num = micro_url[-4::]

        if all(i.isdigit() for i in num):
            print('DONE', num)
            json_dict['id_fak'].add(num)

    json_dict['id_fak'] = list(json_dict['id_fak'])
    driver.quit()
    with open('url_id.json', 'w', encoding='utf-8') as out_file:
        json.dump(json_dict, out_file, indent=4, ensure_ascii=False)
    print('Data saved')


download_source()