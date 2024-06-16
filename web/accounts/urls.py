from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
        path('', views.login_redirect, name = 'start'),
        path('accounts/login/', views.acc_login_view, name = 'login'),
        path('accounts/', views.acc_view, name = 'home'),
        path('accounts/logout/', views.acc_logout, name = 'logout'),
        path('accounts/dr/<int:user_id>', views.acc_dr_home_view, name = 'dr-cab'),
        path('accounts/hr/<int:user_id>', views.acc_hr_home_view, name = 'hr-cab'),
        path('accounts/mr/<int:user_id>', views.acc_mr_home_view, name = 'mr-cab'),
]
