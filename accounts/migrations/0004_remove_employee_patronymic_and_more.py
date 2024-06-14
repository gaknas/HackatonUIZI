# Generated by Django 5.0.6 on 2024-06-14 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_excelmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='patronymic',
        ),
        migrations.AlterField(
            model_name='employee',
            name='primary_skill',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='employee',
            name='secondary_skills',
            field=models.CharField(default='', max_length=128),
        ),
    ]