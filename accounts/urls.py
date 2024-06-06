from django.urls import path
from accounts.views import acc_login_view

urlpatterns = [
        path('', acc_login_view, name = 'login'),
]
