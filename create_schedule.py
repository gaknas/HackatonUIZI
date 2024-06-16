import get_doctors_from_db
from doctor_class import doctor
import numpy as np
import openpyxl
import os
import sqlite3
import pandas as pd
import datetime



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

def find_doctors(all_docs, key, week, day):
    mas_of_suitable_doctors = []
    i = 0
    for doc in all_docs:
        #print(doc.get_available_days())
        #print(str(week) + '   '+ str(day) + '   ' + str(doc.get_id()))
        if doc.get_activities_per_day(week, day)>0:
            if key in doc.get_abilities() :
                mas_of_suitable_doctors.append(i)
        i+=1
    return mas_of_suitable_doctors

def find_priority_doctors(all_docs, key, week, day):
    mas_of_doctors_in_priority = [[], []]
    doctors = find_doctors(all_docs,key, week, day)
    for i in doctors:
        if len(all_docs[i].get_abilities()) == 1:
            mas_of_doctors_in_priority[0].append(i)
        else:
            mas_of_doctors_in_priority[1].append(i)

    return mas_of_doctors_in_priority

def update_schetchik(schetchik, all_docs, week,day):
    schetchik_new = {}
    for key in schetchik.keys():
        schetchik_new[key] = 0
    for doc in all_docs:
        if doc.get_activities_per_day(week, day) > 0:
            for key in doc.get_abilities():
                if key in schetchik_new.keys():
                    schetchik_new[key] += 1

    return schetchik_new

def make_schedule_for_month(all_docs, activities, activities_UE, amount_for_weeks,schetchik):
    max = 300
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    book = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL']

    for week in range(0, len(amount_for_weeks)):

        for day in range(0, len(all_docs[0].get_available_week_schedule(week))):
            amount_for_week = dict(amount_for_weeks[week])
            print('start:')
            print(amount_for_week)

            schetchik_for_day = update_schetchik(schetchik, all_docs, week,day)
            print(schetchik_for_day)
            flag = len(schetchik_for_day)

            while flag > 0:

                min_key = find_min_key(schetchik_for_day)

                massive_of_doctors_in_priority_order = find_priority_doctors(all_docs, min_key,week,day)

                for priority_order in massive_of_doctors_in_priority_order:
                    if amount_for_week[min_key] <= 0:
                        break
                    for doc_id in priority_order:

                        if (amount_for_week[min_key] <= 0) | (all_docs[doc_id].get_activities_per_day(week, day) <= 0):
                            break
                        while all_docs[doc_id].get_activities_per_day(week, day) > 0:
                            if amount_for_week[min_key] <= 0:
                                break
                            amount_for_week[min_key] = amount_for_week[min_key] - (all_docs[doc_id].get_day_schedule(week, day) * activities_UE[min_key])

                            #all_docs[doc_id].set_new_day_schedule(week, day, 0)                                                             #UBIRAET DEN
                            new_amount = all_docs[doc_id].get_activities_per_day(week, day) - (all_docs[doc_id].get_day_schedule(week, day) * activities_UE[min_key])
                            #print(str(min_key) + '  '+ str(new_amount) +  '  ' + str(amount_for_week[min_key]))
                            all_docs[doc_id].set_activities_per_day(new_amount, week, day)                                                   #SKOLKO ENERGYY VRACHA OSTALOS

                        all_docs[doc_id].set_new_available_days(all_docs[doc_id].get_available_day_schedule(week, day),week, day)      #RASPISANIE DLA ZAPOLNENIA TABLIZ
                        all_docs[doc_id].set_work_per_day(min_key, week, day)                                                           #KAKOE ISSLEDOVANIE DELAET

                schetchik_for_day.pop(min_key)
                schetchik_for_day = update_schetchik(schetchik_for_day, all_docs, week,day)
                flag-=1
                print('end:')
                print(amount_for_week)
            print(schetchik_for_day)
    doc_id = 0
    schetchik_for_docs = 0
    days_in_month = 0
    for week in range(0, len(amount_for_weeks)):
        for day in range(0, len(all_docs[0].get_available_week_schedule(week))):
            days_in_month+=1
    worksheet['A1'] = 'sys_user'
    worksheet['B1'] = 'day_of_month'
    worksheet['C1'] = 'time_start'
    worksheet['D1'] = 'time_end'
    worksheet['E1'] = 'time_break'
    worksheet['F1'] = 'time_total'
    worksheet['G1'] = 'research_type'
    for doc in all_docs:
        date = 1
        for week in range(0, len(amount_for_weeks)):

            for day in range(0, len(all_docs[0].get_available_week_schedule(week))):
                strin1 = str(book[0]) + str(days_in_month * doc_id + 1 + date)
                strin2 = str(book[1]) + str(days_in_month * doc_id + 1 + date)
                strin3 = str(book[2]) + str(days_in_month * doc_id + 1 + date)
                strin4 = str(book[3]) + str(days_in_month * doc_id + 1 + date)
                strin5 = str(book[4]) + str(days_in_month * doc_id + 1 + date)
                strin6 = str(book[5]) + str(days_in_month * doc_id + 1 + date)
                strin7 = str(book[6]) + str(days_in_month * doc_id + 1 + date)

                worksheet[strin1] = str(all_docs[doc_id].get_id())
                worksheet[strin2] = str(date)



                if doc.get_amount_of_hours_per_day(week,day) == 12:
                    worksheet[strin3] = str('20:00')
                    worksheet[strin4] = str('9:00')
                    worksheet[strin5] = str((all_docs[doc_id].get_pereriv(week)[day] % 1 + int(
                        all_docs[doc_id].get_pereriv(week)[day])) * 60)
                    timee = all_docs[doc_id].get_amount_of_hours_per_day(week,day) + all_docs[doc_id].get_pereriv(week)[day]
                    worksheet[strin6] = str(int(timee)) + ':' + str(int((timee % 1) * 60))
                    worksheet[strin7] = str(doc.get_work_per_day()[week][day])

                elif doc.get_amount_of_hours_per_day(week,day) == 0:
                    worksheet[strin3] = str(0)
                    worksheet[strin4] = str(0)
                else:
                    worksheet[strin3] = str('8:00')
                    timee = all_docs[doc_id].get_amount_of_hours_per_day(week,day) + all_docs[doc_id].get_pereriv(week)[day]
                    worksheet[strin4] = str(8 + int(timee)) + ':' + str(int((timee % 1) * 60))
                    worksheet[strin5] = str((all_docs[doc_id].get_pereriv(week)[day] % 1 + int(
                        all_docs[doc_id].get_pereriv(week)[day])) * 60)
                    worksheet[strin6] = str(int(timee)) + ':' + str(int((timee % 1) * 60))
                    worksheet[strin7] = str(doc.get_work_per_day()[week][day])
                print(date)
                date = date + 1

        doc_id+=1

    workbook.save('test2.xlsx')
    df = pd.read_excel('test2.xlsx', header=0)

    conn = sqlite3.connect('db.sqlite3')
    # Запись данных из Excel файла в базу данных
    df.to_sql('accounts_schedule', conn, if_exists='replace', index=True)
    # Завершение работы с базой данных
    conn.commit()
    conn.close()



        #print(week)
    #os.remove("test2.xlsx")
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





def get_month_of_week(year, week):
    d = datetime.date(year, 1, 1)
    d = d + datetime.timedelta(weeks=week - 1, days=-d.weekday())
    return d.month


def get_stuff(year, week):
    get_month_of_week(year, week)
    month = get_month_of_week(year, week)

    first_day = datetime.date(year, month, 1)
    first_week_number = first_day.isocalendar()[1]
    return first_week_number


def get_amount_for_weeks(schetchik, activities_UE):
    conn = sqlite3.connect('db.sqlite3')  # Укажите название вашей базы данных
    cursor = conn.cursor()
    my_table = 'accounts_excelmodel'
    year = cursor.execute('SELECT * FROM accounts_excelmodel ORDER BY "index" DESC LIMIT 1 OFFSET 1;')
    year = year.fetchone()[1]
    week = cursor.execute('SELECT * FROM accounts_excelmodel ORDER BY "index" DESC LIMIT 1 OFFSET 1;')
    week = week.fetchone()[2]
    week_to_start_from = get_stuff(year,week)
    print(week_to_start_from)
    cursor.execute(f'SELECT * FROM accounts_excelmodel ORDER BY "index" DESC LIMIT {week_to_start_from}')
    last_four_rows = cursor.fetchall()

    # Заполнение массива данными
    data_array = []
    for i in range(0, len(last_four_rows)):
        data_array.append(last_four_rows[-1-i])

    amount_of_weeks = []
    a = 0
    for row in data_array:
        i = 3

        amount_of_weeks.append({})
        for key in schetchik.keys():
            if row[i] % 7 < 3.5:
                amount_of_weeks[a][key] = int(row[i] / 7 * activities_UE[key])
            else:
                amount_of_weeks[a][key] = int((int(row[i] / 7) + 1) * activities_UE[key])

            i+=1
        a+=1

    return amount_of_weeks


#181   300   451

def main():
    all_docs = get_doctors_from_db.get_values()
    schetchik = {'Денситометрия': 0, 'КТ': 0, 'КТ1': 0, 'КТ2': 0, 'ММГ': 0, 'МРТ': 0, 'МРТ1': 0, 'МРТ2': 0, 'РГ': 0, 'ФЛГ': 0}
    activities_max_150 = {'Денситометрия': 210, 'КТ': 39, 'КТ1': 24, 'КТ2': 17, 'ММГ': 123, 'МРТ': 30, 'МРТ1': 23,
                          'МРТ2': 15, 'РГ': 123, 'ФЛГ': 451}  # Словарь со всеми исследованиями и их значениями

    activities = {'Денситометрия': 140, 'КТ': 26, 'КТ1': 16, 'КТ2': 11, 'ММГ': 82, 'МРТ': 20, 'МРТ1': 15, 'МРТ2': 10,
                  'РГ': 82, 'ФЛГ': 300}  # Словарь со всеми исследованиями и их значениями
    activities_UE = {'Денситометрия': 2.4, 'КТ': 11.6, 'КТ1': 18.8, 'КТ2': 26.6, 'ММГ': 3.7, 'МРТ': 15.1, 'МРТ1': 19.7, 'МРТ2': 30.1,
                  'РГ': 3.7, 'ФЛГ': 1}  # Словарь со всеми исследованиями и их значениями in UA

    for key in activities_max_150:
        activities[key] = int(activities_max_150[key] / 1.5)
    print(activities)
    schetchik = make_schetchik(all_docs,schetchik)
    print(schetchik)

    amount_for_week = get_amount_for_weeks(schetchik, activities_UE)       #2022 15 данные для тестов
    print(amount_for_week)
    print(make_schedule_for_month(all_docs, activities,activities_UE, amount_for_week, schetchik))


main()

