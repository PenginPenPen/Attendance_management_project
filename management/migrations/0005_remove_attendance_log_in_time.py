# Generated by Django 4.1.2 on 2023-02-26 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_alter_attendance_date_alter_attendance_in_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance_log',
            name='in_Time',
        ),
    ]
