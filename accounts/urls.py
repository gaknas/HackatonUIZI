from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
        path('', views.acc_login_view, name = 'login'),
]
