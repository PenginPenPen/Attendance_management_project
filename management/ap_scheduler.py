from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Attendance,Student,Attendance_log
import time

students = []

def log_save():
    try:
        Attendance_data=Attendance.objects.all()
        print('以下の生徒の出席データをログに保存します。')
        for attendance in Attendance_data:
            print(f'・{attendance.student}')
        time.sleep(5)
        for attendance in Attendance_data:
            # print('いいからデバックだ!')
            if attendance.in_Time==None or attendance.out_time==None:
                Attendance_log.objects.create(student=attendance.student,in_Time=None,out_time=None,status='欠席')
            else:
                Attendance_log.objects.create(student=attendance.student,in_Time=attendance.in_Time,out_time=attendance.out_time,status=attendance.status,)
        print('ログに保存しました。')
        print('処理中')
        for attendance in Attendance_data:
            attendance.in_Time=None
            attendance.out_time=None
            attendance.status='----'
            attendance.save()
        print('完了しました。')
    except BaseException as e:
        print('エラーが発生しました。')

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(log_save, 'cron', hour=23,minute=30)
    # scheduler.add_job(log_save, 'interval', seconds=5)
    scheduler.start()