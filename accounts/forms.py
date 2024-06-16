from .models import Employee, Notification
from django.forms import ModelForm
from django.contrib.auth.models import User
class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['user_id', 'type_not', 'text_not', 'name_emp']
'''
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        #fields = [User, 'role', 'patronymic']
'''
