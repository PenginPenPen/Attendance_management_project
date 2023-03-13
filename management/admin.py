from django.contrib import admin
from . models import  Attendance,Student,News,Attendance_log,schedule

# Register your models here.
admin.site.register(Attendance)
admin.site.register(Student)
admin.site.register(News)
admin.site.register(Attendance_log)
admin.site.register(schedule)