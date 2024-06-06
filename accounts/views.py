from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.
def acc_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('cabinet/')
        else:
            return render(request, 'accounts/index.html', {'error': 'Неверное имя или пароль'})
    return render(request, "accounts/index.html")

