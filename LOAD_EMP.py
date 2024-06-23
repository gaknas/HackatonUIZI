from django.contrib.auth.hashers import make_password
import datetime
import pandas as pd
import sqlite3
import sys 
import os
import random
import string
import django
import calendar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from accounts.models import Employee

def colt_nedel(year, week, schedule, masso):
    # Получаем первый день года
    first_day = datetime.date(year, 1, 1)
    # Находим первый понедельник в году
    first_monday = first_day + datetime.timedelta(days=(0 - first_day.weekday()))
    # Находим начало недели
    start_of_week = first_monday + datetime.timedelta(weeks=(week - 1))
    # Находим конец недели
    end_of_week = start_of_week + datetime.timedelta(days=6)
    date = start_of_week.strftime("%d %B %Y")
    day, month, year = date.split()
    month = list(calendar.month_name).index(month.capitalize())
    year = int(year)
    day = int(day)
    cal = calendar.monthcalendar(year, month)
    for week in cal:
        if day in week:
            week_index = cal.index(week)
            break
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
    nomer_con_mas = 0
    nomer_nah_mas = 0
    nomer_obsh_mas = []
    array_obh = []
    for i in range(0, len(b_arr1)):
        if len(b_arr1[i]) == 7:
            nomer_obsh_mas.append(i)
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
            # b = 0
            # for iii in range(0, len(b[i][ii])):

    if len(b_arr1[0]) < 7:
        i = array_obh[nomer_obsh_mas[len(nomer_obsh_mas) - 1]]
        array_obh[0] = i
    if len(b_arr1[len(b_arr1) - 1]) < 7:
        i = array_obh[nomer_obsh_mas[0]]
        array_obh[len(array_obh) - 1] = i
    return array_obh, b_arr1

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

def transform_modalities(modalities):
    if modalities:
        return [mod.strip() for mod in modalities.split(',')]
    return []

def generate_sequence(length):
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))

def gen_seq_total(file_path, length, status):
    sequence = generate_sequence(length)
    with open(file_path, 'a') as file:
        if status:
            file.write(f"Login: {sequence}\t")
        else:
            file.write(f"Pass: {sequence}\n")
    return sequence
file_path = sys.argv[1]
login_db_path = sys.argv[2]
df = pd.read_excel(file_path, usecols=[0, 1, 2, 3], header=1)
df = df.dropna(how='all')
df.columns = ['ФИО', 'Модальность', 'Дополнительные модальности', 'Ставка']
df = df.fillna({'ФИО': '', 'Модальность': '', 'Дополнительные модальности': '', 'Ставка': 0})
df['Дополнительные модальности'] = df['Дополнительные модальности'].apply(transform_modalities)

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute('DELETE FROM auth_user WHERE last_name=1')
c.execute('DELETE FROM accounts_employee WHERE NOT EXISTS (SELECT 1 FROM auth_user WHERE auth_user.id=accounts_employee.user_id );')
os.remove('login.txt')
open("login.txt", "w")

for _, row in df.iterrows():
    c.execute('''
    INSERT INTO auth_user (username, password, first_name, last_name, is_superuser, email, is_staff, is_active, date_joined)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (gen_seq_total(login_db_path, 12, 1), make_password(gen_seq_total(login_db_path, 16, 0)), row['ФИО'], 1, 0, '', 0, 1, datetime.datetime.now()))
    uid = c.execute('''
    SELECT * FROM auth_user ORDER BY date_joined DESC LIMIT 1
    ''')
    c.execute('''
    INSERT INTO accounts_employee (primary_skill, secondary_skills, bid, role, user_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (row['Модальность'], ','.join(row['Дополнительные модальности']), row['Ставка'], 1, uid.fetchone()[0] ))
conn.commit()
conn.close()


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
    
print("Данные успешно записаны в базу данных SQLite")
