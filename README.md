# ИНСТРУКЦИЯ

1. **Запуск тестовой версии приложения**

Тестовая версия веб-приложения размещена на хосте [http://176.123.162.87:8000/](http://176.123.162.87:8000/),
соответственно, для тестирования возможно перейти по данной ссылке в любом браузере

2. **Установка и запуск локальной версии приложения**
- Запустить терминал в папке, где будет находиться проект
- Установите python, pip, venv:
```bash
sudo apt update -y
sudo apt install python3 -y
sudo apt-get install python3-pip python3-dev -y
sudo apt install python3-venv -y

```
  
- Склонировать репозиторий:
  ```bash
  git clone https://github.com/gaknas/HackatonUIZI
  ```
- Перейти в директорию проекта:
  ```bash
  cd HackatonUIZI
  ```
- Выдать необходимые права для запуски скрипта установки: 
  ```bash
  chmod +x script.sh
  ```
- Запустить установочный скрипт:
  ```bash
  source script.sh
  ```
- Запустить локальный сервер:
  ```bash
  make run
  ```
- Перейти по адресу [http://localhost:8000/](http://localhost:8000/) в любом браузере
- Чтобы остановить сервер, введите в консоли `Ctrl+C`

3. **Создание пользователей**
- Чтобы создать пользователей:


3.1 **Рекомендуемый способ:**
- Выполнить набор команд в терминале:
```bash
make shell
from django.contrib.auth.models import User
from accounts.models import Employee
emp = Employee.objects.create(user_id=User.objects.create_user('mr1', password='mr1').pk, role=3)
emp.save()
exit()
```

- Зайти из-под пользователя mr1/mr1.


3.2 **Другой способ:**
- На этапе выполнения скрипта был создан суперпользователь с установленными в скрипте данными.
- Перейдите по адресу [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Войдите от имени суперпользователя.
- Во вкладке "Сотрудники" добавьте необходимых пользователей. Необходимо заполнение большей части полей.

4. Вы можете более подробно ознакомиться с проектом, если откроете документацию, а также скрипт установки, как текст!
  
5. **Если у вас возникли вопросы или проблемы, не стесняйтесь обращаться к участникам проекта. Вместе мы сможем сделать это приложение лучше!**
