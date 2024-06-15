import get_doctors
from doctor_class import doctor
import numpy as np
import openpyxl
import os
import sqlite3
import pandas as pd

def check_for_overload(activities, schetchik, amount_for_month):
    mas = {}
    for key in schetchik.keys():
        mas[key] = amount_for_month[key] - schetchik[key] * activities[key] * 5
    return mas

def make_schetchik(all_docs, schetchik):
    new_schet = {}
    for key in schetchik.keys():
        new_schet[key] = 0

    for key in schetchik.keys():
        for doc in all_docs:
            if key in doc.get_abilities():
                new_schet[key] += 1
    return new_schet


def find_min_key(schetchik):
    min_key = min(schetchik, key=schetchik.get)
    #print(min_key)
    return min(schetchik, key=schetchik.get)

def find_doctors(all_docs, key):
    mas_of_suitable_doctors = []
    i = 0
    for doc in all_docs:
        #print(doc.get_available_days())
        if doc.get_used():
            if key in doc.get_abilities() :
                mas_of_suitable_doctors.append(i)
        i+=1
    return mas_of_suitable_doctors

def find_priority_doctors(all_docs, key):
    mas_of_doctors_in_priority = [[],[]]
    doctors = find_doctors(all_docs,key)
    for i in doctors:
        if len(all_docs[i].get_abilities()) == 1:
            mas_of_doctors_in_priority[0].append(i)
        else:
            mas_of_doctors_in_priority[1].append(i)

    return mas_of_doctors_in_priority

def update_schetchik(schetchik, all_docs, week):
    schetchik_new = {}
    for key in schetchik.keys():
        schetchik_new[key] = 0
    for doc in all_docs:
        if sum(doc.get_available_week_schedule(week)) > 0:
            for key in doc.get_abilities():
                if key in schetchik_new.keys():
                    schetchik_new[key] += 1

    return schetchik_new

def make_schedule_for_month(all_docs, activities, amount_for_weeks,schetchik):

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    book = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL']



    week = 0
    for amount_for_week in amount_for_weeks:

        flag = len(schetchik)
        schetchik_for_week = dict(schetchik)


        while flag  > 0:

            min_key = find_min_key(schetchik_for_week)
            #print(min_key)
            massive_of_doctors_in_priority_order = find_priority_doctors(all_docs, min_key)
            for priority_order in massive_of_doctors_in_priority_order:
                if amount_for_week[min_key] <= 0:
                    break
                for doc_id in priority_order:


                    if amount_for_week[min_key] <= 0:
                        break
                    for day in range(0,7):
                        if amount_for_week[min_key] <= 0:
                            break
                        if all_docs[doc_id].get_available_day_schedule(week, day) > 0:                     # процентовка за рабочий * сумма в смену * количество отработанного в смену *
                            amount_for_week[min_key] = amount_for_week[min_key] - (all_docs[doc_id].get_week_schedule(week) * activities[min_key] * all_docs[doc_id].get_available_day_schedule(week, day)* all_docs[doc_id].get_working_rate())

                            strin1 = str(book[day + week * 7]) + str(5 * (doc_id + 1))
                            strin2 = str(book[day + week * 7]) + str(5 * (doc_id + 1) + 1)
                            strin3 = str(book[day + week * 7]) + str(5 * (doc_id + 1) + 2)
                            strin4 = str(book[day + week * 7]) + str(5 * (doc_id + 1) + 3)
                            strin5 = str(book[day + week * 7]) + str(5 * (doc_id + 1) + 4)
                            worksheet[strin1] = str('8:00')
                            timee = all_docs[doc_id].get_amount_of_hours(week) + all_docs[doc_id].get_pereriv(week)
                            worksheet[strin2] = str(8 + int(timee)) + ':' + str(int((timee % 1) *60))
                            worksheet[strin3] = str((all_docs[doc_id].get_pereriv(week) % 1 + int(all_docs[doc_id].get_pereriv(week)))*60)
                            worksheet[strin4] = str(int(timee)) + ':' + str(int((timee % 1) *60))
                            worksheet[strin5] = str(min_key)

                            all_docs[doc_id].set_new_day_schedule(week, day, 0)
            schetchik_for_week.pop(min_key)
            schetchik_for_week = update_schetchik(schetchik_for_week, all_docs, week)

            flag-=1
        print(amount_for_week)
        print(dop_smena_ravnomerno(all_docs, amount_for_week, activities))

        week += 1
    workbook.save('test2.xlsx')
    df = pd.read_excel('test2.xlsx', header=3)

    conn = sqlite3.connect('db.sqlite3')
    # Запись данных из Excel файла в базу данных
    df.to_sql('accounts_schedule', conn, if_exists='replace', index=True)
    # Завершение работы с базой данных
    conn.commit()
    conn.close()
    os.remove("test2.xlsx")
    return 0

def make_schetchik_for_all(all_docs):
    new_schetchik = {}
    for doc in all_docs:
        for key in doc.get_abilities():
            if key in new_schetchik.keys():
                new_schetchik[key] += 1
            else:
                new_schetchik[key] = 1
    return new_schetchik

def dop_smena_ravnomerno(all_docs, amount_for_week, activities):
    schetchik = make_schetchik_for_all(all_docs)
    amount_of_hours_per_doc = {}
    for key, value in amount_for_week.items():
        if value > 0:
            amount_of_hours_per_doc[key] = (8 * value) / (activities[key] * schetchik[key])

    return amount_of_hours_per_doc



'''ORDER BY rowid DESC LIMIT 4'''

def get_amount_for_weeks(schetchik):
    conn = sqlite3.connect('db.sqlite3')  # Укажите название вашей базы данных
    cursor = conn.cursor()
    my_table = 'accounts_excelmodel'
    cursor.execute('SELECT * FROM accounts_excelmodel ORDER BY rowid DESC LIMIT 4')
    last_four_rows = cursor.fetchall()

    # Заполнение массива данными
    data_array = []
    for i in range(0, len(last_four_rows)):
        data_array.append(last_four_rows[-1-i])

    amount_of_weeks = []
    a = 0
    for row in data_array:
        i=3

        amount_of_weeks.append({})
        for key in schetchik.keys():
            amount_of_weeks[a][key] = row[i]
            i+=1
        a+=1

    return amount_of_weeks









def main():
    all_docs = get_doctors.get_values()
    schetchik = {'Денситометрия': 0, 'КТ': 0, 'КТ1': 0, 'КТ2': 0, 'ММГ': 0, 'МРТ': 0, 'МРТ1': 0, 'МРТ2': 0, 'РГ': 0, 'ФЛГ': 0}
    activities_max_150 = {'Денситометрия': 210, 'КТ': 39, 'КТ1': 24, 'КТ2': 17, 'ММГ': 123, 'МРТ': 30, 'МРТ1': 23,
                          'МРТ2': 15, 'РГ': 123, 'ФЛГ': 451}  # Словарь со всеми исследованиями и их значениями

    activities = {'Денситометрия': 140, 'КТ': 26, 'КТ1': 16, 'КТ2': 11, 'ММГ': 82, 'МРТ': 20, 'МРТ1': 15, 'МРТ2': 10,
                  'РГ': 82, 'ФЛГ': 300}  # Словарь со всеми исследованиями и их значениями

    for key in activities_max_150:
        activities[key] = int(activities_max_150[key] / 1.5)
    print(activities)
    schetchik = make_schetchik(all_docs,schetchik)
    print(schetchik)

    amount_for_week = get_amount_for_weeks(schetchik)       #2022 15 данные для тестов
    print(amount_for_week)
    print(make_schedule_for_month(all_docs, activities, amount_for_week, schetchik))


main()

