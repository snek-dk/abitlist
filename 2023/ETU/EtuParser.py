#!python3

import requests, json, time
import EtuParserDownloadUrls

AbitInfo = list()
Subjects = list()

# FlagDebug -> Turn On\Off debug, but idk what...
# FlagDownloadUrls -> If Turn On, It will download fresh url for subjects and onle after will start to pars
#                  -> If Turn Off, It just pars data from old saved urls.


FlagDebug = False
FlagDownloadUrls = False

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': "_ym_uid=1656859781143423161; _ym_d=16871424602; _ga_07ZD6XLVXT=GS1.1.1688727710.1.0.1688728207.0.0.0; _ga=GA1.2.644750581.1687164603; _ga_92ZX4BT4WK=GS1.2.1688733789.11.0.1688733789.0.0.0; __utma=140980720.644750581.1687164603.1687349642.1689181187.5; __utmz=140980720.1689181187.5.5.utmcsr=yandex.ru|utmccn=(referral)|utmcmd=referral|utmcct=/; _ym_isad=1; session-cookie=1772b9df1edce40067bc861427f9396b53509a5f5ec0b44813262127e849cbb248aa1f15f885187250c84e32ff535",
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

level_of_study = {

	"ОМ":"ОК",
	"БВИ":"БВИ",
	"ЦК":"ЦК",
	"ОП":"ОСК",
	"ОК-1":"ОТК",
	"ОК-2":"ОТК",
	"К":"ОК"	
}

def GetDataFromSubject(Name, Code, Url):

	RawJson = requests.get(Url, headers=headers).json()

	Competition = RawJson["data"]["competition"]
	Abits = RawJson["data"]["list"]
	
	for Abit in Abits:
		TempAbitInfo = [{
				"ВУЗ":"СПбГЭТУ ЛЭТИ",
				"ОСНОВА_ОБУЧЕНИЯ":Competition["fin_source"],
				"УРОВЕНЬ_ОБУЧЕНИЯ":"Бакалавриат",
				"НАПРАВЛЕНИЕ":Name,
				"ОП":Code + " " + Name,
				"ФОРМА_ОБУЧЕНИЯ":Competition["edu_form"].split()[0],
				"СНИЛС_УК":Abit["code"],
				"ТИП_КОНКУРСА": level_of_study[Abit["enroll_condition"]],
                "ПРИОРИТЕТ":Abit["priority"],
				"ОРИГИНАЛ": Abit["has_original"],
			    "ПП": Abit["has_preemptive_right"],
			    "ЕГЭ_С_ИД": Abit["total_points"],
			    "ЕГЭ": Abit["subject_total_points"],
			    "ВИ_1": Abit["subject_1_points"],
			    "ВИ_2": Abit["subject_2_points"],
			    "ВИ_3": Abit["subject_3_points"],
			    "ВИ_4": None,
			    "ВИ_5": None,
			    "ВИ_6": None,
			    "ИД": Abit["achievement_points"],
			    "МЕСТА": {
			        "Бюджет": Competition["total_num"] if Competition["fin_source"] == "Бюджет" else None,
			        "Контракт": Competition["total_num"] if Competition["fin_source"] == "Контракт" else None,
			        }
			    }]

		if (Code == "10.05.01") or (Code == "11.05.01"): TempAbitInfo[-1]["УБ(уровень обучения)"] = "Специалитет"

		try:
			TempAbitInfo[-1]["ВИ_4"] = Abit["subject_4_points"]
		except:
			TempAbitInfo[-1]["ВИ_4"] = None

		try:
			TempAbitInfo[-1]["ВИ_5"] = Abit["subject_5_points"]
		except:
			TempAbitInfo[-1]["ВИ_5"] = None

		try:
			TempAbitInfo[-1]["ВИ_6"] = Abit["subject_6_points"]
		except:
			TempAbitInfo[-1]["ВИ_6"] = None

		AbitInfo.extend(TempAbitInfo)


def main():

	print("Parsing-ETU->Start")

	if FlagDownloadUrls: EtuParserDownloadUrls.GetSubjectUrl();

	with open("EtuSubjects.json", "r", encoding="utf-8") as InpFile:
		Subjects = json.load(InpFile)

	for Subject in Subjects:

		print("Etu - " + Subject["name"])
		for SubjectUrl in Subject["url"]:

			try:
				GetDataFromSubject(Subject["name"],Subject["code"], SubjectUrl)
			except:
				print("\tError - " + Subject["name"])
				time.sleep(0.5)
				
	with open("EtuAbitInfo.json", "w", encoding="utf-8") as OutFile:
		json.dump(AbitInfo, OutFile, indent=4, ensure_ascii=False)

	print("Parsing-ETU->End")	



if __name__ == '__main__':
	main()
