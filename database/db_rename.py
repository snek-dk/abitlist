import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database='testdb'
)

mycursor = mydb.cursor()

# Конкурс/Основа_обучения:
t = '''
Без ВИ/Госбюджетная -> БВИ/Госбюджет
По результатам ВИ/Госбюджетная -> ОК/Госбюджет
По результатам ВИ/Договорная -> ОК/Контракт
По результатам ВИ/Госбюджетная (Особая квота) -> ОП/Госбюджет
По результатам ВИ/Госбюджетная (Специальная квота) -> СК/Госбюджет
По результатам ВИ/Госбюджетная (Целевая квота) -> ЦК/Госбюджет
Без ВИ/Договорная -> БВИ/Контракт
К/контракт -> ОК/Контракт
ОП/госбюджет -> ОП/Госбюджет
ЦК/госбюджет -> ЦК/Госбюджет
СК-2/госбюджет -> СК/Госбюджет
ОК/госбюджет -> ОК/Госбюджет
БВИ/госбюджет -> БВИ/Госбюджет
ЕГЭ/госбюджет ОП -> ОП/Госбюджет
ВИ/госбюджет ОП -> ОП/Госбюджет
ЕГЭ/госбюджет СК -> СК/Госбюджет
ВИ/госбюджет СК -> СК/Госбюджет
ЕГЭ/госбюджет ОК -> ОК/Госбюджет
ВИ/госбюджет ОК -> ОК/Госбюджет
ЕГЭ/контракт -> ОК/Контракт
ВИ/контракт -> ОК/Контракт
ЕГЭ/госбюджет ЦК -> ЦК/Госбюджет'''
t = t.strip().split('\n')
to_change = [t[i] for i in range(len(t))]
for i in range(len(to_change)):
    to_change[i] = to_change[i].replace('->', '/').strip().split('/')
for each in to_change:
    mycursor.execute(f"UPDATE global "
                     f"SET Конкурс = '{each[2].strip()}', Основа_обучения = '{each[3].strip()}' "
                     f"WHERE (id >= 0) AND (Конкурс = '{each[0].strip()}') AND (Основа_обучения = '{each[1].strip()}')")
# NULL/госбюджет БВИ -> БВИ/Госбюджет ОТДЕЛЬНОЕ ВНИМАНИЕ
mycursor.execute(f"UPDATE global "
                 f"SET Конкурс = 'БВИ', Основа_обучения = 'Госбюджет' "
                 f"WHERE (id >= 0) AND (Основа_обучения = 'госбюджет БВИ')")
mycursor.execute(f"UPDATE global "
                 f"SET Согласие = 'Нет' "
                 f"WHERE (id >= 0) AND (Согласие in ('НЕТ','нет'))")
mycursor.execute(f"UPDATE global "
                 f"SET Оригинал = 'Нет' "
                 f"WHERE (id >= 0) AND (Оригинал in ('НЕТ','нет'))")
mycursor.execute(f"UPDATE global "
                 f"SET Согласие = 'Да' "
                 f"WHERE (id >= 0) AND (Согласие in ('ДА','да'))")
mycursor.execute(f"UPDATE global "
                 f"SET Оригинал = 'Да' "
                 f"WHERE (id >= 0) AND (Оригинал in ('ДА','да'))")
mycursor.execute(f"DELETE FROM global WHERE (Конкурс = NULL) AND (id >= 0)")
mycursor.execute("UPDATE global SET СУММА = 310, Основа_обучения = 'Госбюджет', Конкурс = 'ОП' WHERE Основа_обучения = 'Госбюджетная (Особая квота)' AND Конкурс = 'Без ВИ' AND id >= 0")
mydb.commit()