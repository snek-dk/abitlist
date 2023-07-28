import requests
import subprocess
from bs4 import BeautifulSoup as soup
import os
import json


def get_the_page(cookie):
    curl_command = f'''curl "https://abit.miet.ru/bak-submitted/index.php" -H "authority: abit.miet.ru" -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" -H "accept-language: ru,en;q=0.9" -H "cache-control: max-age=0"  -H "cookie: {cookie}" -H "dnt: 1" -H "referer: https://abit.miet.ru/main_pages/list.php?access_mode=public&edu_type=bak&campaign_type=basic&list_type=submitted&cg=000002168" -H "sec-fetch-dest: document" -H "sec-fetch-mode: navigate" -H "sec-fetch-site: same-origin" -H "sec-fetch-user: ?1"  -H "upgrade-insecure-requests: 1" -H "user-agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1" --output miet.html'''
    resp = subprocess.run(curl_command, stdout=subprocess.PIPE)
    return 0


def get_json_form(main_form, personal_form, amount_of_places):
    data_form = {
        "ВУЗ": "МИЭТ",
        "ОСНОВА_ОБУЧЕНИЯ": main_form["ОСНОВА_ОБУЧЕНИЯ"],
        "УРОВЕНЬ_ОБУЧЕНИЯ": main_form["УРОВЕНЬ_ОБУЧЕНИЯ"],
        "НАПРАВЛЕНИЕ": main_form["НАПРАВЛЕНИЕ"],
        "ОП": main_form["ОП"],
        "ФОРМА_ОБУЧЕНИЯ": main_form["ФОРМА_ОБУЧЕНИЯ"],
        "СНИЛС_УК": personal_form["СНИЛС_УК"],
        "ТИП_КОНКУРСА": personal_form["ТИП_КОНКУРСА"],
        "ПРИОРИТЕТ": personal_form["ПРИОРИТЕТ"],
        "ОРИГИНАЛ": personal_form["ОРИГИНАЛ"],
        "ПП": personal_form["ПП"],
        "ЕГЭ_С_ИД": personal_form["ЕГЭ_С_ИД"],
        "ЕГЭ": personal_form["ЕГЭ"],
        "ВИ_1": personal_form["ВИ_1"],
        "ВИ_2": personal_form["ВИ_2"],
        "ВИ_3": personal_form["ВИ_3"],
        "ВИ_4": personal_form["ВИ_4"],
        "ВИ_5": personal_form["ВИ_5"],
        "ВИ_6": personal_form["ВИ_6"],
        "ИД": personal_form["ИД"],
        "МЕСТА": {
            "Бюджет": amount_of_places["Бюджет"],
            "Контракт": amount_of_places["Контракт"]
        }
    }

    return data_form


miet_cookie = requests.get("https://abit.miet.ru/bak-submitted/index.php").content.decode("utf-8")
miet_cookie = miet_cookie[miet_cookie.index('wl'):miet_cookie.index(';')]
get_the_page(miet_cookie)

with open(os.getcwd() + r'/miet.html', 'r', encoding="utf-8") as f:
    main_page = soup(f.read(), "lxml")

links_of_all_programs = main_page.find("h3").find_all_next("a")
main_form = {
    "ВУЗ": "МИЭТ",
    "ОСНОВА_ОБУЧЕНИЯ": None,
    "УРОВЕНЬ_ОБУЧЕНИЯ": None,
    "НАПРАВЛЕНИЕ": None,
    "ОП": None,
    "ФОРМА_ОБУЧЕНИЯ": None
}
personal_form = {
    "СНИЛС_УК": None,
    "ТИП_КОНКУРСА": None,
    "ПРИОРИТЕТ": None,
    "ОРИГИНАЛ": None,
    "ПП": None,
    "ЕГЭ_С_ИД": None,
    "ЕГЭ": None,
    "ВИ_1": 0,
    "ВИ_2": 0,
    "ВИ_3": 0,
    "ВИ_4": None,
    "ВИ_5": None,
    "ВИ_6": None,
    "ИД": 0
}
amount_of_places = {
    "Бюджет": None,
    "Контракт": None
}

to_export = []
for program_link in links_of_all_programs:
    current_program_id = program_link["href"]
    current_program_id = current_program_id[current_program_id.index("cg=") + 3::]
    current_json = requests.get(f"https://abit.miet.ru/data/public/bak/basic/submitted/{current_program_id}.json",
                                cookies={"wl": miet_cookie[3::]}).json()
    title_data = current_json["parametrs"]["title"]
    title_data = title_data[title_data.index('>') + 1::].split(', ')
    print(title_data)
    main_form["НАПРАВЛЕНИЕ"] = title_data[0]
    main_form["ОП"] = main_form["НАПРАВЛЕНИЕ"]
    if "очно-заочная" in title_data[-1]:
        main_form["ФОРМА_ОБУЧЕНИЯ"] = "Очно-заочная"
    elif "заочная" in title_data[-1]:
        main_form["ФОРМА_ОБУЧЕНИЯ"] = "Заочная"
    else:
        main_form["ФОРМА_ОБУЧЕНИЯ"] = "Очная"
    main_form["УРОВЕНЬ_ОБУЧЕНИЯ"] = "Бакалавриат"

    applications = current_json["applications"]
    current_program_is_design = 1 if "Дизайн" in title_data[0] else 0
    if title_data[1] == "бюджет":
        main_form["ОСНОВА_ОБУЧЕНИЯ"] = "Бюджет"
        amount_of_places["Бюджет"] = current_json["parametrs"]["head_columns"][0][1]
        for application in applications:
            personal_form["СНИЛС_УК"] = application[4]
            personal_form["ОРИГИНАЛ"] = True if application[5] == '+' else False
            personal_form["ЕГЭ_С_ИД"] = application[8] if application[8] is not None else 0
            personal_form["ВИ_1"] = application[10] if application[10] is not None else 0
            personal_form["ВИ_2"] = application[11] if application[11] is not None else 0
            personal_form["ВИ_3"] = application[12] if application[12] is not None else 0
            if current_program_is_design:
                personal_form["ВИ_4"] = application[13] if application[13] is not None else 0
            personal_form["ИД"] = application[13 + current_program_is_design] if application[
                                                                                     13 + current_program_is_design] is not None else 0
            personal_form["ПП"] = True if application[17] == '+' else False
            personal_form["ПРИОРИТЕТ"] = application[18]
            contest_type = application[16]
            if contest_type is None:
                contest_type = "ОК"
            elif "БВИ" in contest_type:
                pass
            elif "ЦП" in contest_type:
                contest_type = "ЦК"
            elif "ОП" in contest_type:
                contest_type = "ОТК"
            else:
                contest_type = "ОСК"
            personal_form["ТИП_КОНКУРСА"] = contest_type
            personal_form["ЕГЭ"] = max(int(personal_form["ЕГЭ_С_ИД"]) - int(personal_form["ИД"]), 0)
            to_export.append(get_json_form(main_form, personal_form, amount_of_places))
    else:
        main_form["ОСНОВА_ОБУЧЕНИЯ"] = "Контракт"
        personal_form["ТИП_КОНКУРСА"] = "ОК"
        for application in applications:
            personal_form["СНИЛС_УК"] = application[4]
            personal_form["ОРИГИНАЛ"] = True if application[6] == '+' else False
            personal_form["ЕГЭ_С_ИД"] = application[9] if application[9] is not None else 0
            personal_form["ВИ_1"] = application[11] if application[11] is not None else 0
            personal_form["ВИ_2"] = application[12] if application[12] is not None else 0
            personal_form["ВИ_3"] = application[13] if application[13] is not None else 0
            if current_program_is_design:
                personal_form["ВИ_4"] = application[14] if application[14] is not None else 0
            personal_form["ИД"] = application[14 + current_program_is_design] if application[
                                                                                     14 + current_program_is_design] is not None else 0
            personal_form["ПП"] = True if application[16] == '+' else False
            personal_form["ПРИОРИТЕТ"] = application[17]

            to_export.append(get_json_form(main_form, personal_form, amount_of_places))

with open(os.getcwd() + "\output.json", 'w', encoding='utf-8') as fp:
    json.dump(to_export, fp, indent=4, ensure_ascii=False)
