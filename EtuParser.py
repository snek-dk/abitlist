import requests, json
import EtuParserDownloadUrls

AbitInfo = list()
Subjects = list()

FlagDebug = False
FlagDownloadUrls = False

# ВУЗ|ОБ(основа обучения)|УБ(уровень обучения)|Направление|ОП(образовательная программа)
# |ФО(форма обучения)|СНИЛС/УК|Тип_конкурса|Приоритет|ЕГЭ(сумма с ид)|ЕГЭ(сумма без ид)|ВИ1|ВИ2|...|ВИ6|ИД

	
def GetDataFromSubject(Name, Code, Url):

	RawJson = requests.get(Url).json()
	Competition = RawJson["data"]["competition"]
	Abits = RawJson["data"]["list"]

	for Abit in Abits:

		TempAbitInfo = [{
				"ВУЗ":"СПбГЭТУ ЛЭТИ",
				"ОБ(основа обучения)":Competition["fin_source"],
				"УБ(уровень обучения)":"Бакалавриат",
				"Направление":Name,
				"ОП(образовательная программа)":Code,
				"ФО(форма обучения)":Competition["edu_form"],
				"СНИЛС/УК":Abit["code"],
				"Тип_конкурса":Abit["enroll_condition"],
				"Приоритет":Abit["priority"],
				"ЕГЭ(сумма с ид)":Abit["total_points"],
				"ЕГЭ(сумма без ид)":Abit["subject_total_points"],
				"ВИ1":Abit["subject_1_points"],
				"ВИ2":Abit["subject_2_points"],
				"ВИ3":Abit["subject_3_points"],
				"ВИ4":None,
				"ВИ5":None,
				"ВИ6":None,
				"ИД":Abit["achievement_points"]
						}]
		if (Code == "10.05.01") or (Code == "11.05.01"): TempAbitInfo[-1]["УБ(уровень обучения)"] = "Специалитет"

		try:
			TempAbitInfo[-1]["ВИ4"] = Abit["subject_4_points"]
		except:
			TempAbitInfo[-1]["ВИ4"] = None

		try:
			TempAbitInfo[-1]["ВИ5"] = Abit["subject_5_points"]
		except:
			TempAbitInfo[-1]["ВИ5"] = None

		try:
			TempAbitInfo[-1]["ВИ6"] = Abit["subject_6_points"]
		except:
			TempAbitInfo[-1]["ВИ6"] = None

		AbitInfo.extend(TempAbitInfo)


def main():

	if FlagDownloadUrls: EtuParserDownloadUrls.GetSubjectUrl();

	with open("EtuSubjects.json", "r", encoding="utf-8") as InpFile:
		Subjects = json.load(InpFile)

	for Subject in Subjects:
		print("Etu - " + Subject["name"])
		for SubjectUrl in Subject["url"]:

			try:
				GetDataFromSubject(Subject["name"],Subject["code"], SubjectUrl)
			except:
				print("\tError")
				time.sleep(0.5)
				
	with open("EtuAbitInfo.json", "w", encoding="utf-8") as OutFile:
		json.dump(AbitInfo, OutFile, indent=4, ensure_ascii=False)



if __name__ == '__main__':
	main()


