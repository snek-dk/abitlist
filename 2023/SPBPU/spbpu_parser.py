import requests
from bs4 import BeautifulSoup
import json


def get_parameters(education_form, education_basis, url=True):
    education_form_id = {
        "Заочная": 1,
        "Очная": 2,
        "Очно-заочная": 3
    }

    admission_basis = {
        "Бюджет": "BUDGET",
        "Контракт": "CONTRACT",
        # "Иностранцы": "FOREIGN",
        "Особая_квота": "SPECIAL_QUOTA",
        "Отдельная_квота": "EXTRA_QUOTA",
        "Министерская_квота": "QUOTA",
        "Целевая_квота": "GOVERNMENT"
    }

    parameters = {
        "name": '',
        "educationFormId": education_form_id[education_form],
        "admissionBasis": admission_basis[education_basis],
    }
    data = {
        "url": f"name={parameters['name']}&educationFormId={parameters['educationFormId']}&educationLevelId=2%2C5&admissionBasis={parameters['admissionBasis']}&showClosed=true",
        "parameters": parameters
    }

    return data


def get_json_form(main_form, personal_form):
    data_form = {
        "ВУЗ": "СПбПУ",
        "ОСНОВА_ОБУЧЕНИЯ": main_form["ОСНОВА_ОБУЧЕНИЯ"],
        "УРОВЕНЬ_ОБУЧЕНИЯ": main_form["УРОВЕНЬ_ОБУЧЕНИЯ"],
        "НАПРАВЛЕНИЕ": main_form["НАПРАВЛЕНИЕ"],
        "ОП": main_form["ОП"],
        "ФОРМА_ОБУЧЕНИЯ": main_form["ФОРМА_ОБУЧЕНИЯ"],
        "СНИЛС_УК": personal_form["СНИЛС_УК"],
        "ТИП_КОНКУРСА": personal_form["ТИП_КОНКУРСА"],
        "ПРИОРИТЕТ": personal_form["ПРИОРИТЕТ"],
        "СОГЛАСИЕ": personal_form["СОГЛАСИЕ"],
        "ПП": personal_form["ПП"],
        "ЕГЭ_С_ИД": personal_form["ЕГЭ_С_ИД"],
        "ЕГЭ": personal_form["ЕГЭ"],
        "ВИ_1": personal_form["ВИ_1"],
        "ВИ_2": personal_form["ВИ_2"],
        "ВИ_3": personal_form["ВИ_3"],
        "ВИ_4": personal_form["ВИ_4"],
        "ВИ_5": personal_form["ВИ_5"],
        "ВИ_6": personal_form["ВИ_6"],
        "ИД": personal_form["ИД"]
    }

    return data_form


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': "_ym_uid=1656859781143803161; _ym_d=1687164602; _ga_07ZD6XLVXT=GS1.1.1688727710.1.0.1688728207.0.0.0; _ga=GA1.2.644750581.1687164603; _ga_92ZX4BT4WK=GS1.2.1688733789.11.0.1688733789.0.0.0; __utma=140980720.644750581.1687164603.1687349698.1689181187.5; __utmz=140980720.1689181187.5.5.utmcsr=yandex.ru|utmccn=(referral)|utmcmd=referral|utmcct=/; _ym_isad=1; session-cookie=1772b9df1edce40067bc861f80267f9396b53509a5f5ec0b44813262127e849cbb248aa1f15f885187250c84e32ff535",
    'DNT': '1',
    'Host': 'enroll.spbstu.ru',
    'sec-ch-ua': '"Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.674 Yowser/2.5 Safari/537.36'
}

main_url = "https://enroll.spbstu.ru/applications-manager/api/v1/directions/all-pageable"
main_form = {
    "ВУЗ": "СПбПУ",
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
    "СОГЛАСИЕ": None,
    "ПП": None,
    "ЕГЭ_С_ИД": None,
    "ЕГЭ": None,
    "ВИ_1": None,
    "ВИ_2": None,
    "ВИ_3": None,
    "ВИ_4": None,
    "ВИ_5": None,
    "ВИ_6": None,
    "ИД": None
}

to_export = []
for a in ["Заочная", "Очная", "Очно-заочная"]:
    for b in ["Бюджет", "Контракт", "Особая_квота", "Отдельная_квота", "Министерская_квота", "Целевая_квота"]:
        data = get_parameters(a, b)
        url_parameters = data["url"]
        table_url_parameters = data["parameters"]
        page = requests.get(
            url=f"https://enroll.spbstu.ru/applications-manager/api/v1/directions/all-pageable?{url_parameters}",
            headers=headers).json()["result"]
        for result in page:
            main_form["НАПРАВЛЕНИЕ"] = result["title"]
            main_form["ОП"] = result["title"]
            main_form["ФОРМА_ОБУЧЕНИЯ"] = result["educationForm"]["title"]
            main_form["ОСНОВА_ОБУЧЕНИЯ"] = "Бюджет" if (result["paymentForm"]["title"] != "Контракт") else "Контракт"
            main_form["УРОВЕНЬ_ОБУЧЕНИЯ"] = result["educationLevel"]["title"]
            table_url = f"https://enroll.spbstu.ru/applications-manager/api/v1/admission-list/form-rating?applicationEducationLevel=BACHELOR&directionEducationFormId={table_url_parameters['educationFormId']}&directionId={result['id']}"
            table_page = requests.get(url=table_url, headers=headers).json()["list"]
            math_first = result["entranceTestsSets"][0]["title"][0:3] == 'МАТ'
            for row in table_page:
                personal_form["СНИЛС_УК"] = row["userSnils"]
                personal_form["ТИП_КОНКУРСА"] = "БВИ" if row["withoutExam"] else ("ОК" if b == "Бюджет" else b)
                personal_form["ПРИОРИТЕТ"] = row["priority"]
                personal_form["ПП"] = row["hasFeature"]
                personal_form["ЕГЭ_С_ИД"] = row["fullScore"]
                personal_form["ЕГЭ"] = row["subjectScore"]
                personal_form["СОГЛАСИЕ"] = row["hasAgreement"] or row["hasOriginalDocuments"]
                for entrance_test in row["subjects"]:
                    title = entrance_test["title"]
                    score = entrance_test["score"]
                    if title == "Индивидуальное достижение":
                        personal_form["ИД"] = score
                    elif title == "Русский язык":
                        personal_form["ВИ_3"] = score
                    elif title == "Математика":
                        if math_first:
                            personal_form["ВИ_1"] = score
                        else:
                            personal_form["ВИ_2"] = score
                    else:
                        if not math_first:
                            personal_form["ВИ_1"] = score
                        else:
                            personal_form["ВИ_2"] = score
                to_export.append(get_json_form(main_form, personal_form))
with open('output.json', 'w', encoding="utf-8") as f:
    json.dump(to_export, f, ensure_ascii=False, indent=4)
