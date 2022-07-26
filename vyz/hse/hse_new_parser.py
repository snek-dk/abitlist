import openpyxl


def insert_into_dict(privileges_w_snils, subjects, other_data, main_data):
    abit_id = privileges_w_snils[0]
    entrance_types = ['БВИ', 'ОП', 'ЦП', 'СК', 'ОК']
    if privileges_w_snils[1:].count('Да') > 0:
        entrance = entrance_types[privileges_w_snils.index('Да')]
    else:
        entrance = entrance_types[-1]
    while len(subjects) < 5:
        subjects.append(None)
    city, field_of_study, ed_program = main_data[0], main_data[1], main_data[2]
    try:
        bez_id = str(int(other_data[1]) - int(other_data[0]))
    except:
        bez_id = other_data[1]
    entrant = {
        'ВУЗ': 'ВШЭ' + ' ' + city,
        'Направление': field_of_study,
        'ОП': ed_program,
        'Форма_обучения': "очная",
        'Основа_обучения': other_data[2],
        'СНИЛС_УК': abit_id,
        'Конкурс': entrance,
        'СУММА': other_data[1],
        'СУММА_БЕЗ_ИД': bez_id,
        'ВИ_1': subjects[0],
        'ВИ_2': subjects[1],
        'ВИ_3': subjects[2],
        'ВИ_4': subjects[3],
        'ВИ_5': subjects[4],
        'ИД': other_data[0],
        'Согласие': other_data[-1],
        'Оригинал': other_data[-2]
    }
    return entrant


path = r"C:\Users\dmitr\PycharmProjects\abitlist\vyz\hse\tables\moscow\Информатика_и_вычислительная_техника.xlsx"
book = openpyxl.open(path, read_only=True)
sheet = book.active
needed_columns = set(sheet[15][column].value for column in range(0, sheet.max_column))
print(needed_columns)
to_save = dict()
for row in range(18, sheet.max_row):
    parsed_data = []
    for column in range(0, (len(needed_columns) - 1) * 2, 2):
        parsed_data.append(sheet[row][column].value)
    privileges_w_snils = parsed_data[1:6]
    # print(privileges_w_snils)
    other_data = parsed_data[-8:-3]
    # print(other_data)
    subjects = parsed_data[6:-8]
    # print(subjects)
    main_data = ['Москва', 'ИВТ', 'ИВТ']
    print(insert_into_dict(privileges_w_snils, subjects, other_data, main_data))
