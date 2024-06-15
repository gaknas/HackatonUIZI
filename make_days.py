import random
import sqlite3
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from accounts.models import Employee
import calendar
import datetime

def colt_nedel(year, week, schedule, masso):
    # Получаем первый день года
    first_day = datetime.date(year, 1, 1)
    # Находим первый понедельник в году
    first_monday = first_day + datetime.timedelta(days=(0 - first_day.weekday()))
    # Находим начало недели
    start_of_week = first_monday + datetime.timedelta(weeks=(week - 1))
    # Находим конец недели
    end_of_week = start_of_week + datetime.timedelta(days=6)
    # print("Неделя", week, "в", year, "году:")
    # print(start_of_week.strftime("%d %B %Y"), "-", end_of_week.strftime("%d %B %Y"))
    # print(start_of_week.strftime("%d %B %Y"))

    date = start_of_week.strftime("%d %B %Y")
    day, month, year = date.split()
    # print(f"day = {int(day)}")
    # print(f"month = {list(calendar.month_name).index(month.capitalize())}")
    # print(f"year = {int(year)}")
    month = list(calendar.month_name).index(month.capitalize())
    year = int(year)
    day = int(day)
    cal = calendar.monthcalendar(year, month)
    for week in cal:
        if day in week:
            week_index = cal.index(week)
            break
    # print(calendar.month_name[month])
    # print('Mo Tu We Th Fr Sa Su')
    b_arr1 = []
    if schedule == 1:
        tik = 1
    if schedule == 2:
        tik = 0
    if schedule == 3:
        tik = 0
    tiks = 1
    for week in cal:
        a = []
        for i, d in enumerate(week):
            if d == 0:
                print('  ', end='')
            else:
                print('{:2}'.format(d), end=' ')
                a.append(masso[d-1])
                #masso


        b_arr1.append(a)
    print()
    print("b_arr1 = ", b_arr1)
    print(len(b_arr1))
    nomer_con_mas = 0
    nomer_nah_mas = 0
    nomer_obsh_mas = []
    array_obh = []
    for i in range(0, len(b_arr1)):
        # print(i)
        # print(a[i][ii]) # вывод 14 массивов
        if len(b_arr1[i]) == 7:
            nomer_obsh_mas.append(i)
            print(len(b_arr1[i]))
        teta1 = 0
        teta2 = 1
        b_arr = 12
        for ii in range(0, len(b_arr1[i])):
            teta1 += b_arr1[i][ii]
        b_arr = int(40 / teta1)
        if b_arr > 12:
            array_obh.append(12)
        else:
            array_obh.append(b_arr)
            # print(iii)
            # b = 0
            # for iii in range(0, len(b[i][ii])):
    print(array_obh)
    print(len(array_obh))
    print(nomer_obsh_mas)
    print(len(nomer_obsh_mas))

    print(nomer_obsh_mas[len(nomer_obsh_mas) - 1])

    if len(b_arr1[0]) < 7:
        i = array_obh[nomer_obsh_mas[len(nomer_obsh_mas) - 1]]
        array_obh[0] = i
    if len(b_arr1[len(b_arr1) - 1]) < 7:
        i = array_obh[nomer_obsh_mas[0]]
        array_obh[len(array_obh) - 1] = i
    print(array_obh)
    return array_obh, b_arr1


#schedule = 3
#masso = [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0]
#colt_nedel(year, week, schedule, masso)

def creating():

    norms = [[1, 1], [2, 2], [5, 2]]

    day_available = [[[1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
                      [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
                      [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1]],
                     [[1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
                      [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                      [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
                      [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]],
                     [[1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
                      [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                      [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
                      [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                      [1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
                      [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]]]

    i = random.randint(0, len(norms) - 1)
    j = random.randint(0, len(day_available[i]) - 1)

    return i, norms[i], day_available[i][j][:]



conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
employees = Employee.objects.filter(role='1')
for employee in employees:
    i, norms, day_available = creating()
    employee.add_list_to_shed(norms, 0)
    year = cursor.execute('SELECT * FROM accounts_excelmodel ORDER BY "index" DESC LIMIT 1 OFFSET 1;')
    year = year.fetchone()[1]
    week = cursor.execute('SELECT * FROM accounts_excelmodel ORDER BY "index" DESC LIMIT 1 OFFSET 1;')
    week = week.fetchone()[2]
    arr,barr = colt_nedel(year, week, i+1, day_available)
    employee.add_list_to_shed(barr, 1)
    employee.add_list_to_shed(arr, 2)
    employee.save()
    
print("success")
