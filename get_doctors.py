import random
from doctor_class import doctor
import sqlite3


def create_doctors(all_doctors, norms, day_availble):
    all_docs = []

    for doc in all_doctors:
        i = random.randint(0,2)
        j = random.randint(0, len(day_availble[i])-1)
        all_docs.append(doctor(doc[0], doc[1], doc[2], norms[i], day_availble[i][j][:], True))


    return all_docs




def coun():
    # Подключение к базе данных
    conn = sqlite3.connect('db.sqlite3')  # Укажите название вашей базы данных

    # Создание курсора
    cursor = conn.cursor()

    # Запрос на подсчет числа строк в таблице
    table_name = 'accounts_employee'  # Укажите название вашей таблицы
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")

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
        sqlite_select_query = """SELECT * FROM accounts_employee"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchmany(row_count)
        for i in range(0, len(records)):

            all_mas.append([])

            for a in range(1,len(records[i])):

                if (records[i][a] == None) & (a == 1):
                    break

                if a == 1:
                    all_mas[i].append(records[i][a])
                if a == 2:
                    if records[i][a] == 'КТ':
                        all_mas[i].append(['КТ'])
                        all_mas[i][1].append('КТ1')
                        all_mas[i][1].append('КТ2')

                    elif records[i][a] == 'МРТ':
                        all_mas[i].append(['МРТ'])
                        all_mas[i][1].append('МРТ1')
                        all_mas[i][1].append('МРТ2')

                    else:
                        all_mas[i].append([records[i][a]])
                if (a == 3) & (records[i][a] != None) & (records[i][a] != '-'):
                    tx = records[i][a].split(',')
                    for mes in tx:
                        if mes.strip() == 'Денс':
                            all_mas[i][1].append('Денситометрия')
                        elif mes.strip() == 'Денситометрия':
                            all_mas[i][1].append('Денситометрия')
                        elif mes.strip() == 'РГ':
                            all_mas[i][1].append('РГ')
                        elif mes.strip() == 'КТ':
                            all_mas[i][1].append('КТ')
                            all_mas[i][1].append('КТ1')
                            all_mas[i][1].append('КТ2')
                        elif mes.strip() == 'ММГ':
                            all_mas[i][1].append('ММГ')
                        elif mes.strip() == 'ФЛГ':
                            all_mas[i][1].append('ФЛГ')
                        elif mes.strip() == 'МРТ':

                            all_mas[i ][1].append('МРТ')
                            all_mas[i ][1].append('МРТ1')
                            all_mas[i ][1].append('МРТ2')
                if a == 4:
                        all_mas[i ].append(records[i][a])


        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

    return all_mas






def get_values():
    activities_max_150 = {'Денситометрия': 210, 'КТ': 39, 'КТ1': 24, 'КТ2': 17, 'ММГ': 123, 'МРТ': 30, 'МРТ1': 23,
                          'МРТ2': 15, 'РГ': 123, 'ФЛГ': 451}  # Словарь со всеми исследованиями и их значениями

    activities = {'Денситометрия': 140, 'КТ': 26, 'КТ1': 16, 'КТ2': 11, 'ММГ': 82, 'МРТ': 20, 'МРТ1': 15, 'МРТ2': 10,
                  'РГ': 82, 'ФЛГ': 300}  # Словарь со всеми исследованиями и их значениями

    for key in activities_max_150:
        activities[key] = int(activities_max_150[key] / 1.5)
    print(activities)






    norma_hour = 40
    norms = [[1, 1], [2, 2], [5, 2]]
    # day_available = [[[1, 0, 1, 0, 1, 0, 0], [0, 1, 0, 1, 0, 1, 0], [0, 0, 1, 0, 1, 0, 1]], [[1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1, 1]], [[1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 0, 0, 1]]]
    day_available = [[[[1, 0, 1, 0, 1, 0, 0], [1, 0, 1, 0, 1, 0, 0], [1, 0, 1, 0, 1, 0, 0], [1, 0, 1, 0, 1, 0, 0]],
                      [[0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0]],
                      [[0, 0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 1, 0, 1]]],
                     [[[1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 0, 0, 1], [1, 0, 0, 1, 1, 0, 0]],
                      [[0, 1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 0, 0, 1], [1, 0, 0, 1, 1, 0, 0], [1, 1, 0, 0, 1, 1, 0]],
                      [[0, 0, 1, 1, 0, 0, 1], [1, 0, 0, 1, 1, 0, 0], [1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 0, 0, 1, 1]],
                      [[1, 0, 0, 1, 1, 0, 0], [1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 0, 0, 1]]],
                     [[[1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 0, 0]],
                      [[0, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 0]],
                      [[0, 0, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1]],
                      [[1, 0, 0, 1, 1, 1, 1], [1, 0, 0, 1, 1, 1, 1], [1, 0, 0, 1, 1, 1, 1], [1, 0, 0, 1, 1, 1, 1]],
                      [[1, 1, 0, 0, 1, 1, 1], [1, 1, 0, 0, 1, 1, 1], [1, 1, 0, 0, 1, 1, 1], [1, 1, 0, 0, 1, 1, 1]],
                      [[1, 1, 1, 0, 0, 1, 1], [1, 1, 1, 0, 0, 1, 1], [1, 1, 1, 0, 0, 1, 1], [1, 1, 1, 0, 0, 1, 1]],
                      [[1, 1, 1, 1, 0, 0, 1], [1, 1, 1, 1, 0, 0, 1], [1, 1, 1, 1, 0, 0, 1], [1, 1, 1, 1, 0, 0, 1]]]]

    doctors = read_limited_rows()
    print(doctors)
    all_docs = create_doctors(doctors, norms, day_available)






    return all_docs

'''aaa = get_values()
for a in aaa:
    a.vivod()'''

