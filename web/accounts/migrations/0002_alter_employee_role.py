# Generated by Django 5.0.6 on 2024-06-10 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Доктор'), (2, 'Менеджер кадров'), ('Руководитель', 3)], default=1),
        ),
    ]
