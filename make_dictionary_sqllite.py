import pandas as pd
import sqlite3


def transform_modalities(modalities):
    if modalities:
        return [mod.strip() for mod in modalities.split(',')]
    return []


file_path = 'table_template_doc_list.xlsx'
df = pd.read_excel(file_path, header=1)
df = df.dropna(how='all')
df.columns = ['ФИО', 'модальность', 'дополнительные модальности', 'ставка']
df = df.fillna({'ФИО': '', 'модальность': '', 'дополнительные модальности': '', 'ставка': 0})
df['дополнительные модальности'] = df['дополнительные модальности'].apply(transform_modalities)

conn = sqlite3.connect('doc_list.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS doc_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ФИО TEXT,
    модальность TEXT,
    дополнительные_модальности TEXT,
    ставка REAL
)
''')

c.execute('DELETE FROM doc_list')

for _, row in df.iterrows():
    c.execute('''
    INSERT INTO doc_list (ФИО, модальность, дополнительные_модальности, ставка)
    VALUES (?, ?, ?, ?)
    ''', (row['ФИО'], row['модальность'], ','.join(row['дополнительные модальности']), row['ставка']))

conn.commit()
conn.close()

print("Данные успешно записаны в базу данных SQLite")

