from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
        path('', views.login_redirect, name = 'start'),
        path('accounts/login/', views.acc_login_view, name = 'login'),
        path('accounts/', views.acc_view, name = 'home'),
        path('accounts/logout/', views.acc_logout, name = 'logout'),
]
