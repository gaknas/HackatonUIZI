#!/bin/bash

python3 -m venv env #Создаём виртуальное окружение

source env/bin/activate #Запускаем его

pip3 install -r requirements.txt #Устанавливаем необходимые зависимости

rm -r accounts/migrations/00* #Удаляем ненужные миграции

rm db.sqlite3 #Удаляем БД

python3 manage.py makemigrations #Выполняем первичный список миграций

python3 manage.py migrate #Выполняем эти миграции

username="admin"
email="admin@example.com"
password="admin"

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$username', '$email', '$password')" | python3 manage.py shell #Создаём суперпользователя с данными, указанными тут ранее

python3 PREDICT.py pred.xlsx #Выполняем предсказание на основе файла pred.xlsx

python3 LOAD_EMP.py doc.xlsx login.txt #Создаём аккаунты для всех работников из doc.xlsx и временно записываем их данные в login.txt

python3 create_schedule.py #Создаём расписание для врачей
