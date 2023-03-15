from django.db import models
import numpy as np
CATEGORY=(('出席','出席'),('遅刻','遅刻'),('欠席','欠席'),('早退','早退'))
Day_of_week=(('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday'),('Sunday','Sunday'))

def file_upload_path(instance, filename):
    return f'{instance.id}.jpg'
# Create your models here.
class Student(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image =models.ImageField(upload_to=file_upload_path)
    name= models.CharField(max_length=30)
    student_ID_number = models.CharField(max_length=30)

    in_Time = models.DateTimeField(blank=True, null=True, )
    out_time= models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100,choices=CATEGORY ,blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            uploaded_file = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = uploaded_file
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE,)
    in_Time = models.DateTimeField(blank=True, null=True, )
    out_time= models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100,choices=CATEGORY ,blank=True, null=True)

class Attendance_log(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,choices=CATEGORY)
    in_Time = models.DateTimeField(null=True,blank=True)
    out_time= models.DateTimeField(null=True,blank=True)
    date = models.DateField(auto_now_add=True)

class News(models.Model):
    title  =  models.CharField(max_length=100)
    text=  models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class schedule (models.Model):
    day_of_week=models.CharField(max_length=10,choices=Day_of_week)
    lasson_name=models.CharField(max_length=100,blank=True,null=True)
    start_time= models.TimeField(blank=True,null=True)
    end_time = models.TimeField(blank=True,null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.lasson_name
