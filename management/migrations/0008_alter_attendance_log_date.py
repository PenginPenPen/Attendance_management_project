# Generated by Django 4.1.2 on 2023-02-26 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_remove_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance_log',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
