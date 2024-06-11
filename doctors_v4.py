import get_doctors
from doctor_class import doctor
import numpy as np
import openpyxl

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
    #будем считать что данные нормы - нормы для 8 часов труда, то есть 10 часов - 1.2 от обычного колва (немного уменьшим), а 12 часов - 1.45 от обычного числа (0.05) уменьшим, ибо иначе упремся в максимум в по рц
    workbook = openpyxl.load_workbook('doc.xlsx')
    worksheet = workbook.active
    print(schetchik)
    for i in all_docs:
        i.vivod()
        # delete_this = {'Денситометрия': 1, 'КТ': 2, 'ММГ': 3, 'МРТ': 4, 'РГ': 5, 'ФЛГ': 6}
    book = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL']



    week = 0
    for amount_for_week in amount_for_weeks:
        #print(week)
        flag = len(schetchik)
        schetchik_for_week = dict(schetchik)
        print(check_for_overload(activities, schetchik_for_week, amount_for_week))
        #print(schetchik_for_week)
        while flag  > 0:

            min_key = find_min_key(schetchik_for_week)
            #print(min_key)
            massive_of_doctors_in_priority_order = find_priority_doctors(all_docs, min_key)
            for priority_order in massive_of_doctors_in_priority_order:
                if amount_for_week[min_key] <= 0:
                    break
                for doc_id in priority_order:

                    #all_docs[doc_id].vivod()
                    if amount_for_week[min_key] <= 0:
                        break
                    for day in range(0,7):
                        if amount_for_week[min_key] <= 0:
                            break
                        if all_docs[doc_id].get_available_day_schedule(week, day) > 0:                     # процентовка за рабочий * сумма в смену * количество отработанного в смену *
                            amount_for_week[min_key] = amount_for_week[min_key] - (all_docs[doc_id].get_week_schedule(week) * activities[min_key] * all_docs[doc_id].get_available_day_schedule(week, day)* all_docs[doc_id].get_working_rate())
                            #print(amount_for_week)
                            strin1 = str(book[day + 7 + week * 7]) + str(4 * (doc_id + 1))
                            strin2 = str(book[day + 7 + week * 7]) + str(4 * (doc_id + 1) + 1)

                            worksheet[strin1] = str(min_key)
                            worksheet[strin2] = str(all_docs[doc_id].get_id())
                            all_docs[doc_id].set_new_day_schedule(week, day, 0)
            schetchik_for_week.pop(min_key)
            schetchik_for_week = update_schetchik(schetchik_for_week, all_docs, week)

            flag-=1
        print(amount_for_week)

        week += 1
    workbook.save('test2.xlsx')
    return 0



















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

    amount_for_week = [{'Денситометрия' : 1436, 'КТ' : 4631 , 'КТ1' : 532 , 'КТ2' : 793 , 'ММГ' : 13190 , 'МРТ' : 2423 , 'МРТ1' : 943 , 'МРТ2' : 7 , 'РГ' : 51049 , 'ФЛГ' : 31419 }, {'Денситометрия' : 1314 , 'КТ' : 4899 , 'КТ1' : 611 , 'КТ2' : 733 , 'ММГ' : 12332 , 'МРТ' : 2384 , 'МРТ1' : 924 , 'МРТ2' : 5 , 'РГ' : 52467 , 'ФЛГ' : 29474 }, {'Денситометрия' : 1436 , 'КТ' : 4631 , 'КТ1' : 532 , 'КТ2' : 793 , 'ММГ' : 13190 , 'МРТ' : 2423 , 'МРТ1' : 943 , 'МРТ2' : 7 , 'РГ' : 51049 , 'ФЛГ' : 31419 }, {'Денситометрия' : 1436 , 'КТ' : 4631 , 'КТ1' : 532 , 'КТ2' : 793 , 'ММГ' : 13190 , 'МРТ' : 2423 , 'МРТ1' : 943 , 'МРТ2' : 7 , 'РГ' : 51049 , 'ФЛГ' : 31419 }]       #2022 15 данные для тестов

    print(make_schedule_for_month(all_docs, activities, amount_for_week, schetchik))

main()