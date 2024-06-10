from django.db import models
from django.contrib.auth.models import User

class SystemUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=2, default = 'dr')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Employee(models.Model):
    identificator = models.ForeignKey(SystemUser, on_delete=models.CASCADE, related_name = 'employee', null=True)
    last_name = models.CharField(max_length=30, default='Иванов')
    first_name = models.CharField(max_length=30, default='Иван')
    patronymic = models.CharField(max_length=40, default='Иванович')
    primary_skill = models.CharField(max_length=10, default='РГ')
    secondary_skills = models.CharField(max_length=30, default='КТ')
    bid = models.DecimalField(max_digits=3, decimal_places=2, default='1.00')

    def __str__(self):
        return self.last_name + " " + self.first_name + " " + self.primary_skill

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class Shedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name = 'shedule', null=True)
    day_of_month = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    time_break = models.TimeField()
    time_total = models.DecimalField(max_digits=5, decimal_places=3)
    research_type = models.CharField(max_length=13)

    def __str__(self):
        return str(self.day_of_month) + " " + self.research_type

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


