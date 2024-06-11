from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Shedule, Employee
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
    if request.user.pk == user_id:
        return render(request, 'accounts/dr.html')
    elif request.user is not None:
        messages.error(request, 'Извините, у Вас нет доступа к запрашиваемой странице')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('/')

@login_required
def acc_hr_home_view(request, user_id):
    return render(request, 'accounts/hr.html')
