run:
	./manage.py runserver 0.0.0.0:8000 --settings=web.settings
shell:
	./manage.py shell
mm:
	./manage.py makemigrations
mig:
	./manage.py migrate

