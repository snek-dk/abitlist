import requests
import json

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2526 Yowser/2.5 Safari/537.36"
}
page = requests.get(url="https://priem.bmstu.ru/lists/upload/enrollees/first/MGTU-1/meta.json", headers=header).json()

with open('meta.json', 'w', encoding="utf-8") as f:
    json.dump(page, f, ensure_ascii=False, indent=4)
