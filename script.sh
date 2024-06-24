#!/bin/bash

python -m venv env #Создаём виртуальное окружение

source env/bin/activate #Запускаем его

pip install -r requirements.txt #Устанавливаем необходимые зависимости

rm -r accounts/migrations/00* #Удаляем ненужные миграции

rm db.sqlite3 #Удаляем БД

python manage.py makemigrations #Выполняем первичный список миграций

python manage.py migrate #Выполняем эти миграции

username="admin"
email="admin@example.com"
password="admin"

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$username', '$email', '$password')" | python manage.py shell #Создаём суперпользователя с данными, указанными тут ранее

python PREDICT.py pred.xlsx #Выполняем предсказание на основе файла pred.xlsx

python LOAD_EMP.py doc.xlsx login.txt #Создаём аккаунты для всех работников из doc.xlsx и временно записываем их данные в login.txt

python create_schedule.py #Создаём расписание для врачей
