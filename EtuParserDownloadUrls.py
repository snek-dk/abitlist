import requests, json, time

Subjects = list()

def GetSubjectUrl():

	print("GetValidUrl-Start")

	url = "https://lists.priem.etu.ru/public/competitions/1/1"
	r = requests.get(url)

	RawJson = r.json()["data"]["competition_groups"]

	for Subject in RawJson:
		Subjects.append({"name":Subject["name"],"code":Subject["code"], "url": list()})
		for SubjectUrls in Subject["lists"]:
			Subjects[-1]["url"].append("https://lists.priem.etu.ru/public/list/" + SubjectUrls["uuid"])
		
	with open("EtuSubjects.json", "w", encoding="utf-8") as OutFile:
		json.dump(Subjects, OutFile, indent=4, ensure_ascii=False)

	print("GetValidUrl-End")

def main():
	try:
		GetSubjectUrl()
	except:
		print("Error to download Subjects Urls")
		time.sleep(0.2)
		try:
			GetSubjectUrl()
		except:
			print("Error")
			return

if __name__ == "__main__":
	main()