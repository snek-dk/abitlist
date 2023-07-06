import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database='testdb'
)

mycursor = mydb.cursor()
try:
    mycursor.execute('ALTER TABLE global ADD COLUMN УП VARCHAR(255) AFTER ОП')
except:
    pass
try:
    mycursor.execute('ALTER TABLE global ADD COLUMN НОМЕР INT AFTER id')
except:
    pass
mycursor.execute("UPDATE global SET УП = CONCAT(ВУЗ, ' ', ОП)")
mycursor.execute('SELECT DISTINCT УП from global')
t = mycursor.fetchall()
oop_s = [t[i][0] for i in range(len(t))]
for oop in oop_s:
    query = f'''UPDATE
            global, (SELECT id, ВУЗ, УП, Основа_обучения, СНИЛС_УК, Конкурс, СУММА, ВИ_1, ВИ_2, ВИ_3, ROW_NUMBER() OVER () AS НОМЕР
    		        FROM global
    		        WHERE УП = '{oop}'
    		        ORDER BY Основа_обучения = 'Госбюджетная' DESC, Конкурс = 'СК' DESC, Конкурс = 'ОП' DESC, Конкурс = 'ЦК' DESC, Конкурс = 'БВИ' DESC, Основа_обучения = 'Контракт', СУММА DESC
                    ) AS query_in
            SET global.НОМЕР = query_in.НОМЕР
            WHERE (global.id = query_in.id);'''
    mycursor.execute(query)
mydb.commit()
