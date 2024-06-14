from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
import subprocess
from .models import Shedule, Employee
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
                return redirect('accounts:mr-cab', user_id = employee.user_id)
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
        return render(request, 'accounts/hr.html')
    else:
        return redirect('/')

@login_required
def acc_mr_home_view(request, user_id):
    if request.user.pk == user_id and Employee.objects.get(user_id=user_id).role == 3:
        return render(request, 'accounts/mr.html')
    else:
        return redirect('/')

@login_required
def excel_import_count(request):
    if "POST" == request.method and Employee.objects.get(user=User.objects.get(username=request.user)).role == 3:
        uid = Employee.objects.get(user=User.objects.get(username=request.user)).user_id
        ExcelModel.objects.all().delete()
        excel_file = request.FILES["excel_file"]
        file_path = default_storage.save(excel_file.name, excel_file)
        out = subprocess.run(['python', 'PREDICT.py', file_path], stderr = subprocess.DEVNULL)
        os.remove(file_path)
        return redirect('accounts:mr-cab', user_id=uid)
    else:
        return redirect('accounts:login')