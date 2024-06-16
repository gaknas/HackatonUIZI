import random
from doctor_class import doctor
import sqlite3


def create_doctors(all_doctors):
    all_docs = []

    for doc in all_doctors:
        #print(doc)
        all_docs.append(doctor(doc[0], doc[1], doc[2], doc[3], doc[4], doc[5],True))


    return all_docs




def coun():
    # Подключение к базе данных
    conn = sqlite3.connect('doc_list.db')  # Укажите название вашей базы данных

    # Создание курсора
    cursor = conn.cursor()

    # Запрос на подсчет числа строк в таблице
    table_name = 'users'  # Укажите название вашей таблицы
    cursor.execute(f"SELECT COUNT(*) FROM doc_list")

    # Получение результата
    row_count = cursor.fetchone()[0]

    # Закрытие соединения
    conn.close()
    return row_count


def read_limited_rows():
    try:
        all_mas = []
        sqlite_connection = sqlite3.connect('db.sqlite3')
        cursor = sqlite_connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM accounts_employee")

        # Получение результата
        row_count = cursor.fetchone()[0]
        sqlite_select_query = """SELECT * from accounts_employee"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchmany(row_count)
        j=0
        for i in range(0, len(records)):

            all_mas.append([])
            #print(records[i])
            for a in range(0,len(records[i])):

                if (records[i][1] != 1) | (records[i][2] == '') :
                    all_mas.pop(i-j)
                    j+=1
                    break
                else:

                    if a == 0:
                        all_mas[i-j].append(records[i][a])
                    if a == 2:

                        if records[i-j][a] == 'КТ':
                            all_mas[i-j].append(['КТ'])
                            all_mas[i-j][1].append('КТ1')
                            all_mas[i-j][1].append('КТ2')

                        elif records[i][a] == 'МРТ':
                            all_mas[i-j].append(['МРТ'])
                            all_mas[i-j][1].append('МРТ1')
                            all_mas[i-j][1].append('МРТ2')

                        else:
                            all_mas[i-j].append([str(records[i][a])])

                    if (a == 3) & (records[i][a] != None) & (records[i][a] != '-'):
                        tx = records[i][a].split(',')
                        for mes in tx:
                            if mes.strip() == 'Денс':
                                all_mas[i-j][1].append('Денситометрия')
                            elif mes.strip() == 'Денситометрия':
                                all_mas[i-j][1].append('Денситометрия')
                            elif mes.strip() == 'РГ':
                                all_mas[i-j][1].append('РГ')
                            elif mes.strip() == 'КТ':
                                all_mas[i-j][1].append('КТ')
                                all_mas[i-j][1].append('КТ1')
                                all_mas[i-j][1].append('КТ2')
                            elif mes.strip() == 'ММГ':
                                all_mas[i-j][1].append('ММГ')
                            elif mes.strip() == 'ФЛГ':
                                all_mas[i-j][1].append('ФЛГ')
                            elif mes.strip() == 'МРТ':

                                all_mas[i-j][1].append('МРТ')
                                all_mas[i-j][1].append('МРТ1')
                                all_mas[i-j][1].append('МРТ2')
                    if a == 4:
                        all_mas[i-j].append(records[i][a])

                    if a == 5:
                        all_mas[i-j].append([int(m) for m in records[i][a][1:len(records[i][a])-1].split(', ')])


                    if a == 6:
                        A = records[i][a][2:-2]

                        # Разделяем строку по '], ['
                        list_str = A.split('], [')

                        # Преобразуем каждую строку внутри вложенного списка в список целых чисел
                        array_2d = [[int(num) for num in sublist.split(', ')] for sublist in list_str]


                        all_mas[i-j].append(array_2d)

                    if a == 7:
                        all_mas[i-j].append([int(m) for m in records[i][a][1:len(records[i][a])-1].split(', ')])

        #print(all_mas)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

    return all_mas

print(read_limited_rows())


def get_values():



    doctors = read_limited_rows()
    all_docs = create_doctors(doctors)






    return all_docs

'''aaa = get_values()
for a in aaa:
    a.vivod()'''

