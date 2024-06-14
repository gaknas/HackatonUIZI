from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    SPOT = [
        {1, 'Доктор'},
        {2, 'Менеджер кадров'},
        {3, 'Руководитель'},
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    role = models.PositiveSmallIntegerField(choices=SPOT, default=1)
    primary_skill = models.CharField(max_length=128, default='')
    secondary_skills = models.CharField(max_length=128, default='')
    bid = models.DecimalField(max_digits=3, decimal_places=2, default='1.00')

    def __str__(self):
        return self.user.last_name + " " + self.user.first_name + " # " + self.user.username

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

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

class ExcelModel(models.Model):
    year = models.IntegerField()
    week_num = models.IntegerField()
    dens = models.IntegerField()
    kt = models.IntegerField()
    kt1 = models.IntegerField()
    kt2 = models.IntegerField()
    mmg = models.IntegerField()
    mrt = models.IntegerField()
    mrt1 = models.IntegerField()
    mrt2 = models.IntegerField()
    rg = models.IntegerField()
    flu = models.IntegerField()

    
