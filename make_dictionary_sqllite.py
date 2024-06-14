import pandas as pd
import sqlite3
import sys 
import random
import string

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
            file.write("\n")
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

#c.execute('''
#CREATE TABLE IF NOT EXISTS doc_list (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    ФИО TEXT,
#    модальность TEXT,
#    дополнительные_модальности TEXT,
#    ставка REAL
#)
#''')


c.execute('DELETE FROM accounts_employee WHERE role=1')
c.execute('DELETE FROM auth_user WHERE last_name=1')

for _, row in df.iterrows():
    c.execute('''
    INSERT INTO auth_user (username, password, first_name, last_name, is_superuser, email)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (gen_seq_total(login_db_path, 12, 1), gen_seq_total(login_db_path, 16, 0), row['ФИО'], 1, 0, ''))

for _, row in df.iterrows():
    c.execute('''
    INSERT INTO accounts_employee (primary_skill, secondary_skills, bid)
    VALUES (?, ?, ?)
    ''', (row['Модальность'], ','.join(row['Дополнительные модальности']), row['Ставка']))

conn.commit()
conn.close()

print("Данные успешно записаны в базу данных SQLite")

