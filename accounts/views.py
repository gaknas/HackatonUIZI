from django.shortcuts import render, redirect

# Create your views here.
def acc_login_view(request):
    return render(request, "accounts/login.html")

