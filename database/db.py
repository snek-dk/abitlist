import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database='testdb'
)


# params = '(id INTEGER PRIMARY KEY AUTO_INCREMENT, ВУЗ VARCHAR(20), Направление VARCHAR(105), ОП VARCHAR(105),'
# params += 'Форма_обучения VARCHAR(10), Основа_обучения VARCHAR(20), СНИЛС_УК VARCHAR(20), Конкурс VARCHAR(30),'
# params += 'СУММА INT, СУММА_БЕЗ_ИД INT, ВИ_1 INT, ВИ_2 INT, ВИ_3 INT, ИД INT, СОГЛАСИЕ VARCHAR(5))'
# mycursor.execute(f'CREATE TABLE global {params}')
# mydb.commit()


# form = '(ВУЗ, Направление, ОП, Форма_обучения, Основа_обучения, СНИЛС_УК, Конкурс,'
# form += 'СУММА, СУММА_БЕЗ_ИД, ВИ_1, ВИ_2, ВИ_3, ИД, СОГЛАСИЕ)'
#
# sqlFormula = f"INSERT INTO global {form} VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"


class abitlist:

    def __init__(self, students, name='global', params='', form_for_insert='', commit=False):
        self.mycursor = mydb.cursor()
        self.students = students
        self.name = name
        if len(params) == 0:
            self.params = '(id INTEGER PRIMARY KEY AUTO_INCREMENT, ВУЗ VARCHAR(64), Направление VARCHAR(255), ОП VARCHAR(255),'
            self.params += 'Форма_обучения VARCHAR(128), Основа_обучения VARCHAR(128), СНИЛС_УК VARCHAR(128), Конкурс VARCHAR(128),'
            self.params += 'СУММА INT, СУММА_БЕЗ_ИД INT, ВИ_1 INT, ВИ_2 INT, ВИ_3 INT, ВИ_4 INT, ВИ_5 INT,'
            self.params += 'ИД INT, СОГЛАСИЕ VARCHAR(5), ОРИГИНАЛ VARCHAR(5))'
        else:
            self.params = params
        self.commit = commit
        if len(form_for_insert) == 0:
            self.form_for_insert = '(ВУЗ, Направление, ОП, Форма_обучения, Основа_обучения, СНИЛС_УК, Конкурс,'
            self.form_for_insert += 'СУММА, СУММА_БЕЗ_ИД, ВИ_1, ВИ_2, ВИ_3, ВИ_4, ВИ_5, ИД, СОГЛАСИЕ, ОРИГИНАЛ)'
        else:
            self.form_for_insert = form_for_insert

    def create_table(self):
        # mycursor = mydb.cursor()
        # params = '(id INTEGER PRIMARY KEY AUTO_INCREMENT, ВУЗ VARCHAR(20), Направление VARCHAR(105), ОП VARCHAR(105),'
        # params += 'Форма_обучения VARCHAR(10), Основа_обучения VARCHAR(20), СНИЛС_УК VARCHAR(20), Конкурс VARCHAR(30),'
        # params += 'СУММА INT, СУММА_БЕЗ_ИД INT, ВИ_1 INT, ВИ_2 INT, ВИ_3 INT, ИД INT, СОГЛАСИЕ VARCHAR(5))'
        self.mycursor.execute(f"SHOW TABLES LIKE '{self.name}'")
        if len(self.mycursor.fetchall()) == 0:
            self.mycursor.execute(f'CREATE TABLE {self.name} {self.params}')
            print(f'TABLE {self.name} created!')
            mydb.commit()
        else:
            print(f'Table {self.name} already exists!')

    def to_needed_form(self, student):
        data = (student['ВУЗ'], student['Направление'], student['ОП'],
                student['Форма_обучения'], student['Основа_обучения'],
                student['СНИЛС_УК'], student['Конкурс'], student['СУММА'],
                student['СУММА_БЕЗ_ИД'], student['ВИ_1'], student['ВИ_2'],
                student['ВИ_3'], student['ВИ_4'], student['ВИ_5'],
                student['ИД'], student['Согласие'], student['Оригинал'])
        return data

    def sqlInsert(self, student):
        # form = '(ВУЗ, Направление, ОП, Форма_обучения, Основа_обучения, СНИЛС_УК, Конкурс,'
        # form += 'СУММА, СУММА_БЕЗ_ИД, ВИ_1, ВИ_2, ВИ_3, ИД, СОГЛАСИЕ, ОРИГИНАЛ)'
        query_for_insert = f"INSERT INTO global {self.form_for_insert} VALUES "
        query_for_insert += '(' + '%s,' * (len(self.form_for_insert.split(',')) - 1) + '%s)'
        self.mycursor.execute(query_for_insert, self.to_needed_form(student))

        if self.commit:
            mydb.commit()

    def sqlUpdate(self, student, query_for_update=None):
        query_for_update = f"UPDATE global SET СУММА = {student['СУММА']}, СУММА_БЕЗ_ИД = {student['СУММА_БЕЗ_ИД']}," \
                           f"ВИ_1 = {student['ВИ_1']}, ВИ_2 = {student['ВИ_2']}, ВИ_3 = {student['ВИ_3']}," \
                           f"ИД = {student['ИД']}, СОГЛАСИЕ = '{student['Согласие']}', ОРИГИНАЛ = '{student['Оригинал']}' " \
                           f"WHERE (ОП = '{student['ОП']}') AND (СНИЛС_УК = '{student['СНИЛС_УК']}') AND (ВУЗ = '{student['ВУЗ']}')" \
                           f" AND (id >= 0)"  # в одном вузе каждое ОП уникальное, так что WHERE по ОП жестче, чем по направлению; id >= 0 для SQL safe update
        self.mycursor.execute(query_for_update)

        if self.commit:
            mydb.commit()

    def row_is_in_table(self, student):
        self.mycursor.execute(f"SELECT EXISTS(SELECT id FROM global WHERE (ОП = '{student['ОП']}') "
                              f"AND (СНИЛС_УК = '{student['СНИЛС_УК']}') AND (ВУЗ = '{student['ВУЗ']}')")
        return self.mycursor.fetchone()[0]

    def process_the_data(self):
        for i in range(len(self.students)):
            index = str(i)
            if not (self.row_is_in_table(self.students[index])):
                self.sqlInsert(self.students[index])
            else:
                self.sqlUpdate(self.students[index])
        # if self.commit:
        #     mydb.commit()
