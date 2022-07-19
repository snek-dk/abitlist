import openpyxl


def insert_into_dict(state, field_of_study, ed_program, form_of_education, ed_principle, snils, entrance, ege, more,
                     orig, doc):
    vi_1, vi_2, vi_3 = ege[0], ege[1], ege[2]
    if len(ege) == 4:
        vi_4 = ege[3]
    else:
        vi_4 = None
    if len(ege) == 5:
        vi_5 = ege[4]
    else:
        vi_5 = None
    entrant = {
        'ВУЗ': 'ВШЭ' + state,
        'Направление': field_of_study,
        'ОП': ed_program,
        'Форма_обучения': form_of_education,
        'Основа_обучения': ed_principle,
        'СНИЛС_УК': snils,
        'Конкурс': entrance,
        'СУММА': ege,
        'СУММА_БЕЗ_ИД': str(int(ege) - int(more)),
        'ВИ_1': vi_1,
        'ВИ_2': vi_2,
        'ВИ_3': vi_3,
        'ВИ_4': vi_4,
        'ВИ_5': vi_5,
        'ИД': more,
        'Согласие': doc,
        'Оригинал': orig
    }
    return entrant


book = openpyxl.open(r'C:\Users\dmitr\PycharmProjects\abitlist\vyz\hse\tables\moscow\Актер.xlsx', read_only=True)
sheet = book.active
cell_range = ['A15:C15']
print(sheet[15][0].value)
end = False
needed_columns = set(sheet[15][column].value for column in range(0, sheet.max_column))
print(needed_columns)
main_columns = {'Итоговая сумма баллов \nпо индивидуальным достижениям', 'Преимущественное право',
                'Поступление на места в рамках квоты \nдля лиц, имеющих особое право',
                'Оригинал аттестата', 'Поступление на места в рамках специальной квоты',
                'Наличие согласия на зачисление',
                'СНИЛС / Уникальный идентификатор', None, '№ п/п', 'Возврат документов',
                'Сумма конкурсных баллов', 'Поступление на места в рамках квоты\nцелевого приема',
                'Право поступления без вступительных испытаний', 'Вид места',
                'Требуется общежитие на время обучения'}
print(len(main_columns))
print(len(needed_columns))
exams_count = len(needed_columns) - len(main_columns)
to_save = dict()
print(sheet[18][2].value)
for row in range(18, sheet.max_row):
    parsed_data = []
    for column in range(0, (len(needed_columns) - 1) * 2, 2):
        parsed_data.append(sheet[row][column].value)
        print(sheet[row][column].value is not None, sheet[row][column].value)
    print(parsed_data[1:6])
    print(parsed_data)
    print(parsed_data[-8:])
    print(parsed_data[6:-8])
    print(insert_into_dict(*parsed_data[1:6], *parsed_data[6:-8], *parsed_data[-8:-4]))
    break
