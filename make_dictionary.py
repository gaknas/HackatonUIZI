import pandas as pd
import json


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
records = df.to_dict('records')

output_file_path = 'doc_list.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(records, file, ensure_ascii=False, indent=4)

print(f"Данные успешно записаны в {output_file_path}")

