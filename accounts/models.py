from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    SPOT = [
        {1, 'Доктор'},
        {2, 'Менеджер кадров'},
        {3, 'Руководитель'},
    ]
    user = models.OneToOneField(User, primary_key=True, related_name='user_id', on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=SPOT, default=1)
    primary_skill = models.CharField(max_length=128, default='')
    secondary_skills = models.CharField(max_length=128, default='')
    bid = models.DecimalField(max_digits=3, decimal_places=2, default='1.00')
    shed = models.TextField(default='', null=True)
    month_shed = models.TextField(default='', null=True)
    time_per_week = models.TextField(default='', null=True)
    def get_shed_as_list(self, shed_id):
        if not shed_id:
            if len(self.shed) != 0:
                return [int(num) for num in self.shed.split(',')]
            else:
                return []
        else:
            if len(self.month_shed) != 0:
                return [int(num) for num in self.month_shed.split(',')]
            else:
                return []

    def set_time(self, field):
        self.time_per_week = []


    def add_list_to_shed(self, field, shed_id):
        if not shed_id:
            print(self.get_shed_as_list(0))
            field_list = self.get_shed_as_list(0)
        else:
            field_list = self.get_shed_as_list(1)
        field_list.append(field)
        if not shed_id:
            self.shed = ','.join(str(num) for num in field_list)
        else:
            self.month_shed = ','.join(str(num) for num in field_list)
        
    def set_num_at_index(self, index, value, shed_id):
        field_list = self.get_shed_at_list(shed_id)
        if index >= 0 and index <= len(field_list):
            field_list[index] = value
        if not shed_id:
            self.shed = ','.join(str(num) for num in field_list)
        else:
            self.month_shed = ','.join(str(num) for num in field_list)


    def __str__(self):
        return self.user.last_name + " " + self.user.first_name + " # " + self.user.username

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class Schedule(models.Model):
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

class Notification(models.Model):
    user_id = models.IntegerField()
    type_not = models.BooleanField()
    text_not = models.TextField(default='')
    name_emp = models.TextField(default='')
    
