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
        path('accounts/mr/<int:user_id>/month', views.acc_mr_month_view, name = 'mr-cab-month'),
        path('accounts/mr/<int:user_id>/hr', views.acc_mr_hr_view, name = 'mr-cab-hr'),
        path('accounts/mr/<int:user_id>/not', views.acc_mr_not_view, name = 'mr-cab-not'),
        path('accounts/mr/<int:user_id>/pred', views.acc_mr_pred_view, name = 'mr-cab-pred'),
        path('accounts/excel_count', views.excel_import_count, name='excel_import_count'),
        path('accounts/excel_emp', views.excel_import_employee, name = 'excel_import_employee'),
]
