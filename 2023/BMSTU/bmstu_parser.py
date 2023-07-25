import requests
from PyPDF2 import PdfReader
import io

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.0.2526 Yowser/2.5 Safari/537.36"
}

contest_queue = {
    "Особая_квота": {
        "БВИ": False,
        "ОК": False
    },
    "Отдельная_квота": {
        "БВИ": False,
        "ОК": False
    },
    "Целевая_квота": {
        "БВИ": False,
        "ОК": False
    },
    "БВИ": False,
    "ОК": False
}
page = io.BytesIO(requests.get(url="https://priem.bmstu.ru/lists/upload/enrollees/first/MGTU-1/02.03.01.pdf",
                               headers=header).content)
pdf_reader = PdfReader(page)
pdf_text = pdf_reader.pages[1].extract_text()
print(pdf_text)