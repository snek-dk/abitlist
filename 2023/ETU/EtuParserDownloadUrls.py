#!python3

import requests, json, time

Subjects = list()

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

def GetSubjectUrl():

	print("GetValidUrl-ETU->Start")

	url = "https://lists.priem.etu.ru/public/competitions/1/1"
	r = requests.get(url, headers=headers)
	RawJson = r.json()["data"]["competition_groups"]

	for Subject in RawJson:

		Subjects.append({"name":Subject["name"],"code":Subject["code"], "url": list()})
		for SubjectUrls in Subject["lists"]:
			Subjects[-1]["url"].append("https://lists.priem.etu.ru/public/list/" + SubjectUrls["uuid"])
		
	with open("EtuSubjects.json", "w", encoding="utf-8") as OutFile:
		json.dump(Subjects, OutFile, indent=4, ensure_ascii=False)

	print("GetValidUrl-ETU->End")

def main():
	try:
		GetSubjectUrl()
	except:
		print("Error to download Subjects Urls")
		time.sleep(0.5)
		try:
			GetSubjectUrl()
		except:
			print("Error")
			return

if __name__ == "__main__":
	main()
