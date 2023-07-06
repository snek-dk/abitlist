import mysql.connector
import json
import os

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


mycursor = mydb.cursor()
name = 'global'
params = '(id INTEGER PRIMARY KEY AUTO_INCREMENT, ВУЗ VARCHAR(64), Направление VARCHAR(255), ОП VARCHAR(255),'
params += 'Форма_обучения VARCHAR(128), Основа_обучения VARCHAR(128), СНИЛС_УК VARCHAR(128), Конкурс VARCHAR(128),'
params += 'СУММА INT, СУММА_БЕЗ_ИД INT, ВИ_1 INT, ВИ_2 INT, ВИ_3 INT, ВИ_4 INT, ВИ_5 INT,'
params += 'ИД INT, СОГЛАСИЕ VARCHAR(5), ОРИГИНАЛ VARCHAR(5))'
mycursor.execute(f"SHOW TABLES LIKE '{name}'")
if len(mycursor.fetchall()) != 0:
    print(f'TABLE {name} already exists!')
    mycursor.execute(f'DROP TABLE {name}')
    print(f'TABLE {name} deleted!')
    mycursor.execute(f'CREATE TABLE {name} {params}')
    print(f'TABLE {name} created!')
    mydb.commit()
else:
    mycursor.execute(f'CREATE TABLE {name} {params}')
    print(f'TABLE {name} created!')
    mydb.commit()

abit_dir = os.getcwd().replace('\\database', '')
out_json_path = abit_dir + '\\out_json'
for file in os.listdir(out_json_path):
    path = out_json_path + '\\' + file
    if '.json' in path:
        with open(path, encoding='utf-8') as fp:
            to_insert = json.load(fp)
        data = []
        for j in range(len(to_insert)):
            to_insert[j]['Направление'] = to_insert[j]['Направление'][0:100]
            to_insert[j]['ОП'] = to_insert[j]['ОП']
            data.append(str(to_insert[j]).replace("'", '"').replace('None', 'null'))
        t = str(data).replace('[', '').replace(']', '').replace('//', '').replace('xa0', '').replace('\\', '').replace(
            "'", '')
        mycursor.execute(sqlInsert(t))
mydb.commit()
