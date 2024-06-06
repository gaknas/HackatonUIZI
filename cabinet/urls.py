from django.urls import path
from . import views

app_name = "cabinet"
urlpatterns = [
        path('cabinet/', views.cabinet_view, name = "cabinet"),
]
