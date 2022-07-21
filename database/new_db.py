import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database='testdb'
)


def sqlInsert(to_insert, name='global'):
    args = to_insert
    query = f'''
        INSERT INTO {name} (ВУЗ, Направление,ОП,Форма_обучения,Основа_обучения,СНИЛС_УК,Конкурс,СУММА,СУММА_БЕЗ_ИД,ВИ_1,ВИ_2,ВИ_3,ВИ_4,ВИ_5,ИД,Согласие,Оригинал)
        SELECT *
        FROM JSON_TABLE('[
        '''
    query += str(to_insert)
    query += '''
        ]', '$[*]' COLUMNS (
        ВУЗ VARCHAR(100) PATH '$."ВУЗ"',
        Направление VARCHAR(100) PATH '$."Направление"',
        ОП VARCHAR(100) PATH '$."ОП"',
        Форма_обучения VARCHAR(100) PATH '$."Форма_обучения"',
        Основа_обучения VARCHAR(100) PATH '$."Основа_обучения"',
        СНИЛС_УК varchar(128) PATH '$."СНИЛС_УК"',
        Конкурс varchar(128) PATH '$."Конкурс"',
        СУММА varchar(128) PATH '$."СУММА"',
        СУММА_БЕЗ_ИД varchar(128) PATH '$."СУММА_БЕЗ_ИД"',
        ВИ_1 varchar(128) PATH '$."ВИ_1"',
        ВИ_2 varchar(128) PATH '$."ВИ_2"',
        ВИ_3 varchar(128) PATH '$."ВИ_3"',
        ВИ_4 varchar(128) PATH '$."ВИ_4"',
        ВИ_5 varchar(128) PATH '$."ВИ_5"',
        ИД varchar(128) PATH '$."ИД"',
        Согласие varchar(128) PATH '$."Согласие"',
        Оригинал varchar(128) PATH '$."Оригинал"'
        )
        ) AS example_json;'''
    return query


# with open('../out_json/spbsu_new.json', encoding='utf-8') as fp:
#     to_insert = json.load(fp)
for i in range(51):
    if str(i) not in('41', '42', '44'):
        with open(f"C:\\Users\\dmitr\\Desktop\\mirea\\МИРЭА{i}.json", encoding='utf-8') as fp:
            to_insert = json.load(fp)
        mycursor = mydb.cursor()
        s = str(to_insert[0]).replace("'", '"').replace('None', 'null')
        data = []
        for j in range(len(to_insert)):
            data.append(str(to_insert[j]).replace("'", '"').replace('None', 'null'))
        t = str(data).replace('[', '').replace(']', '').replace("'", '')
        mycursor.execute(sqlInsert(t))
        mydb.commit()