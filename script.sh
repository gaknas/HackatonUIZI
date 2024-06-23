#!/bin/bash

python -m venv env

source env/bin/activate

pip install -r requirements.txt

rm -r accounts/migrations/00*

rm db.sqlite3

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'admin')" | python manage.py shell

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000
