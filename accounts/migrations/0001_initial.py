# Generated by Django 5.0.6 on 2024-06-16 19:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_id', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Доктор'), (2, 'Менеджер кадров'), (3, 'Руководитель')], default=1)),
                ('primary_skill', models.CharField(default='', max_length=128)),
                ('secondary_skills', models.CharField(default='', max_length=128)),
                ('bid', models.DecimalField(decimal_places=2, default='1.00', max_digits=3)),
                ('shed', models.TextField(default='', null=True)),
                ('month_shed', models.TextField(default='', null=True)),
                ('time_per_week', models.TextField(default='', null=True)),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='ExcelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('week_num', models.IntegerField()),
                ('dens', models.IntegerField()),
                ('kt', models.IntegerField()),
                ('kt1', models.IntegerField()),
                ('kt2', models.IntegerField()),
                ('mmg', models.IntegerField()),
                ('mrt', models.IntegerField()),
                ('mrt1', models.IntegerField()),
                ('mrt2', models.IntegerField()),
                ('rg', models.IntegerField()),
                ('flu', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('type_not', models.BooleanField()),
                ('text_not', models.TextField(default='')),
                ('name_emp', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_month', models.DateField()),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('time_break', models.TimeField()),
                ('time_total', models.DecimalField(decimal_places=3, max_digits=5)),
                ('research_type', models.CharField(max_length=13)),
                ('sys_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.employee')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписания',
            },
        ),
    ]
