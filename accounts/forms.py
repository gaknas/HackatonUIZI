from .models import Employee
from django.forms import ModelForm
from django.contrib.auth.models import User

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = [User, "role", "patronymic"]
