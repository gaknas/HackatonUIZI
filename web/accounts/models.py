from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    SPOT = [
        {1, 'Доктор'},
        {2, 'Менеджер кадров'},
        {3, 'Руководитель'},
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    patronymic = models.CharField(max_length=40, default='')
    role = models.PositiveSmallIntegerField(choices=SPOT, default=1)
    primary_skill = models.CharField(max_length=10, default='')
    secondary_skills = models.CharField(max_length=30, default='')
    bid = models.DecimalField(max_digits=3, decimal_places=2, default='1.00')

    def __str__(self):
        return self.user.last_name + " " + self.user.first_name + " # " + self.user.username

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        permissions = (
            ("can_manage_dr", "Управление врачами"),
        )

class Shedule(models.Model):
    sys_user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name = 'shedule', null=True)
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


