const axios = require("axios");
const fs = require("fs");
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const parseDirection = async (direction, directionList, plan) => {
  const { data } = await axios.get(
    `https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=${directionList}`
  );
  const dom = new JSDOM(data);
  const { document } = dom.window;
  const abiturs = document.querySelectorAll("tbody > tr");
  const abitursInfo = Array.from(abiturs)
    .filter((element) =>
      element.querySelector("td").className === "tgtOrgTr" ? false : true
    )
    .map((element) => {
      const entranceExams = element
        .querySelectorAll("td")[5]
        .textContent.split(" ");
      entranceExams.pop();
      entranceExams.forEach((element, index) => {
        if (element == "-") {
          entranceExams[index] = null;
        }
      });
      const snils = element.querySelectorAll("td")[1].textContent;
      return {
        ВУЗ: "МИРЭА",
        Направление: direction.title,
        ОП: direction.title,
        Форма_обучения: "очная",
        Основа_обучения: "Госбюджет",
        СНИЛС_УК:
          snils.length == 14
            ? snils.substring(0, 11) + " " + snils.substring(12)
            : snils,
        Конкурс: plan,
        СУММА:
          element.querySelectorAll("td")[8].textContent == "-"
            ? null
            : element.querySelectorAll("td")[8].textContent,
        СУММА_БЕЗ_ИД:
          element.querySelectorAll("td")[6].textContent == "-"
            ? null
            : element.querySelectorAll("td")[6].textContent,
        ВИ_1: Number(entranceExams[0]) ? Number(entranceExams[0]) : null,
        ВИ_2: Number(entranceExams[1]) ? Number(entranceExams[1]) : null,
        ВИ_3: Number(entranceExams[2]) ? Number(entranceExams[2]) : null,
        ВИ_4: Number(entranceExams[3]) ? Number(entranceExams[3]) : null,
        ВИ_5: Number(entranceExams[4]) ? Number(entranceExams[4]) : null,
        ИД:
          element.querySelectorAll("td")[7].textContent == "-"
            ? null
            : element.querySelectorAll("td")[7].textContent,
        Согласие: element.querySelectorAll("td")[2].textContent,
        Оригинал: element.querySelectorAll("td")[3].textContent,
      };
    });
  return abitursInfo;
};

async function start() {
  const { data } = await axios.get(
    "https://priem.mirea.ru/accepted-entrants-list/getAllCompetitionsRates_p.php"
  );
  data.competitions.forEach(async (direction, index) => {
    let allCompetitions = [];
    if (direction?.common?.listId[0]) {
      const temp = await parseDirection(
        direction,
        direction.common.listId[0],
        "ОК"
      );
      allCompetitions.push(temp);
    }
    if (direction?.no_exams?.listId[0]) {
      const temp = await parseDirection(
        direction,
        direction.no_exams.listId[0],
        "БВИ"
      );
      allCompetitions.push(temp);
    }
    if (direction?.quota?.listId[0]) {
      const temp = await parseDirection(
        direction,
        direction.quota.listId[0],
        "ОП"
      );
      allCompetitions.push(temp);
    }
    if (direction?.special_quota?.listId[0]) {
      const temp = await parseDirection(
        direction,
        direction.special_quota.listId[0],
        "СК"
      );
      allCompetitions.push(temp);
    }
    if (direction?.target?.listId[0]) {
      const temp = await parseDirection(
        direction,
        direction.target.listId[0],
        "ЦК"
      );
      allCompetitions.push(temp);
    }
    if (direction?.target?.listId[1]) {
      const temp = await parseDirection(
        direction,
        direction.target.listId[1],
        "ЦК"
      );
      allCompetitions.push(temp);
    }
    await fs.writeFile(
      `МИРЭА${index}.json`,
      JSON.stringify(allCompetitions.flat()),
      (err) => {
        if (err) throw err;
      }
    );
    allCompetitions = [];
  });
}

start();
