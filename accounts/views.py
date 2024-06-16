from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from .forms import NotificationForm
import subprocess
from .models import Schedule, Employee, Notification
import openpyxl
import pandas as pd
from accounts.models import ExcelModel
import os
from statsmodels.tsa.arima.model import ARIMA
import shutil
import sqlite3

# Create your views here.
def login_redirect(request):
    return redirect('accounts/login/')

def acc_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            employee = Employee.objects.get(user_id=user.pk)
            login(request, user)
            if employee.role == 1:
                return redirect('accounts:dr-cab', user_id = employee.user_id)
            if employee.role == 2:
                return redirect('accounts:hr-cab', user_id = employee.user_id)
            if employee.role == 3:
                return redirect('accounts:mr-cab-month', user_id = employee.user_id)
        else:
            return render(request, 'accounts/login.html', {'error': 'Неверное имя или пароль'})
    return render(request, "accounts/login.html")

@login_required
def acc_view(request):
    return render(request, 'accounts/dr.html')

@login_required
def acc_logout(request):
    logout(request)
    return redirect('accounts:start')

@login_required
def acc_dr_home_view(request, user_id):
    if request.user.is_authenticated:
        if request.user.pk == user_id and Employee.objects.get(user_id=user_id).role == 1:
            return render(request, 'accounts/dr.html')
        else:
            return redirect('/')
    else:
        return redirect('/')

@login_required
def acc_hr_home_view(request, user_id):
    if request.user.pk == user_id and Employee.objects.get(user_id=user_id).role == 2:
        employees = Employee.objects.filter(role=1)
        schedules = Schedule.objects.all()
        return render(request, 'accounts/hr.html', {'employees':employees})
    else:
        return redirect('accounts:logout')

@login_required
def acc_mr_month_view(request, user_id):
    if request.user.pk == user_id and Employee.objects.get(user_id=user_id).role == 3:
        notifications = Notification.objects.all()
        return render(request, 'accounts/mr_month.html', {'uid': user_id, 'notifications':notifications})
    else:
        return redirect('accounts:logout')

@login_required
def acc_mr_hr_view(request, user_id):
    if request.user.pk == user_id and Employee.objects.get(user_id=user_id).role == 3:
        notifications = Notification.objects.all()
        employees = Employee.objects.all()
        return render(request, 'accounts/mr_hr.html', {'uid': user_id, 'notifications':notifications, 'employees':employees})
    else:
        return redirect('accounts:logout')

@login_required
def acc_mr_not_view(request, user_id):
    if request.user.pk == user_id and Employee.objects.get(user_id=user_id).role == 3:
        notifications = Notification.objects.all()
        return render(request, 'accounts/mr_not.html', {'uid': user_id, 'notifications':notifications})
    else:
        return redirect('accounts:logout')

@login_required
def acc_mr_pred_view(request, user_id):
    if request.user.pk == user_id and Employee.objects.get(user_id=user_id).role == 3:
        notifications = Notification.objects.all()
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        raw = cursor.execute('SELECT * FROM accounts_excelmodel ORDER BY "index" DESC LIMIT 4;').fetchall()
        predictions=[{'id':r[0],'year':r[1],'week_num':r[2],'dens':r[3],'kt':r[4],'kt1':r[5],'kt2':r[6],'mmg':r[7],'mrt':r[8],'mrt1':r[9],'mrt2':r[10],'rg':r[11],'flu':r[12]} for r in reversed(raw)]
        return render(request, 'accounts/mr_pred.html', {'uid': user_id, 'notifications':notifications, 'predictions':predictions})
    else:
        return redirect('accounts:logout')

@login_required
def excel_import_count(request):
    if "POST" == request.method and Employee.objects.get(user=User.objects.get(username=request.user)).role == 3:
        uid = Employee.objects.get(user=User.objects.get(username=request.user)).user_id
        ExcelModel.objects.all().delete()
        excel_file = request.FILES["excel_file"]
        file_path = default_storage.save(excel_file.name, excel_file)
        out = subprocess.run(['python', 'PREDICT.py', file_path], stderr = subprocess.DEVNULL)
        os.remove(file_path)
        return redirect('accounts:mr-cab-pred', user_id=uid)
    else:
        return redirect('accounts:login')

@login_required
def excel_import_employee(request):
    if "POST" == request.method and Employee.objects.get(user=User.objects.get(username=request.user)).role == 3:
        uid = Employee.objects.get(user=User.objects.get(username=request.user)).user_id
        excel_file = request.FILES["excel_file_emp"]
        file_path = default_storage.save(excel_file.name, excel_file)
        out = subprocess.run(['python', 'LOAD_EMP.py', file_path, 'login.txt'], stderr = subprocess.DEVNULL)
        os.remove(file_path)
        return redirect('accounts:mr-cab-hr', user_id=uid)
    else:
        return redirect('accounts:login')

@login_required
def add_dr(request):
    uid = Employee.objects.get(user=User.objects.get(username=request.user)).user_id
    if Employee.objects.get(user_id=uid).role != 1:
        return render(request, 'accounts/add_dr.html', {})
    return redirect('accounts:login')

@login_required
def add_dr_submit(request):
    uid = Employee.objects.get(user=User.objects.get(username=request.user)).user_id
    if request.method == 'POST' and Employee.objects.get(user_id=uid).role != 1:
        fio = request.POST.get('FIO')
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/add_dr.html',{'error':'Пользователь с таким именем уже существует'}) 
        password = request.POST.get('password')
        role = request.POST.get('role')
        bid = request.POST.get('bid')
        primary_skill = request.POST.get('primary_skill')
        secondary_skills = request.POST.getlist('secondary_skills')
        if Employee.objects.get(user_id=uid).role == 2:
            if role == '1':
                user = Employee.objects.create(user = User.objects.create_user(username=username, first_name=fio, last_name=1, password=password, is_active=0), role=role, bid=bid,primary_skill=primary_skill, secondary_skills=secondary_skills)
                user.save()
            if role == '2':
                user = Employee.objects.create(user = User.objects.create_user(username=username, first_name=fio, password=password, is_active=0), role=role, bid=bid,primary_skill=primary_skill, secondary_skills=secondary_skills)
                Notification.objects.create(user_id=user.user_id, type_not=False, text_not='Утвердите профиль', name_emp=user.user.first_name)
                user.save()
            if role == '3':
                return render(request, 'accounts/add_dr.html',{'error':'У Вас нет прав на создание этого пользователя'})
            return redirect('accounts:hr-cab', user_id=uid)
        else:
            user = Employee.objects.create(user = User.objects.create_user(username=username, first_name=fio, password=password, is_active=1), role=role, bid=bid,primary_skill=primary_skill, secondary_skills=secondary_skills)
            user.save()
            return redirect('accounts:mr-cab-hr', user_id=uid) 
    return redirect('accounts:login')

@login_required
def del_dr_not(request, notif_id):
    notif = Notification.objects.get(id=notif_id)
    user = User.objects.get(id=notif.user_id)
    emp = Employee.objects.get(user = user)
    emp.delete()
    user.delete()
    notif.delete()
    return redirect('accounts:mr-cab-not', user_id = Employee.objects.get(user=User.objects.get(username=request.user)).user_id)

@login_required
def add_dr_not(request, notif_id):
    notif = Notification.objects.get(id=notif_id)
    user = User.objects.get(id=notif.user_id)
    user.is_active = 1
    user.save()
    notif.delete()
    return redirect('accounts:mr-cab-not', user_id = Employee.objects.get(user=User.objects.get(username=request.user)).user_id)

@login_required
def remove_emp(request, emp_id):
    if Employee.objects.get(user_id=request.user.pk).role == 3:
        emp = Employee.objects.get(user_id=emp_id)
        usr = User.objects.get(id=emp_id)
        emp.delete()
        usr.delete()
        return redirect('accounts:mr-cab-hr', user_id=request.user.pk)
    else:
        return redirect('accounts:login')

@login_required
def add_appeal(request):
    if Employee.objects.get(user_id=request.user.pk).role == 1:
        return render(request, 'accounts/add_appeal.html')
    else:
        return redirect('accounts:login')

@login_required
def add_appeal_submit(request):
    if Employee.objects.get(user_id=request.user.pk).role == 1:
        text = request.POST.get('salutation')
        name = User.objects.get(id=request.user.pk).first_name
        print(name)
        if text:
            notif = Notification.objects.create(user_id=request.user.pk, type_not=1, text_not=text, name_emp=name)
            notif.save()
            return redirect('accounts:dr-cab', user_id=request.user.pk)
        else:
            return render(request, 'accounts/add_appeal.html', {'error':'Введите сообщение'})
    return redirect('accounts:login')

@login_required
def remove_notification(request, notif_id):
    notif = Notification.objects.get(id=notif_id)
    notif.delete()
    return redirect('accounts:mr-cab-not', user_id = Employee.objects.get(user=User.objects.get(username=request.user)).user_id)

@login_required
def download_pred(request):
    if Employee.objects.get(user_id=request.user.pk).role == 3:
        file_path = "doctor.xlsx"
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="Im a doctor.xlsx"'
            return response
    else:
        return redirect('accounts:login')
