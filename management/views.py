from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView,DetailView,DeleteView
from .models import News, Student, Attendance,Attendance_log,schedule
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import StreamingHttpResponse
import face_recognition
from os import listdir
import cv2
import numpy as np
from django.shortcuts import render
import datetime
from django.urls import reverse_lazy
from natsort import natsorted
from django.utils import timezone
import datetime

success_img = cv2.imread("management/static/image/認証成功.png")
succces2_img = cv2.imread("management/static/image/認証成功.png")
warning_img = cv2.imread("management/static/image/認証失敗.png")
error_img = cv2.imread("management/static/image/エラー.png")

# str = '2023-02-26 12:30:10'
# dte = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')

# for face_data in student_face_data:
#     # print(face_data['faces_encoding'])
#     data_list=((face_data['faces_encoding']).replace(" ","").replace("\r","").replace("\n",""))
#     Registered_Faces_Encoding.append(numpy.empty(data_list))
# print(Registered_Faces_Encoding)

dt_now = datetime.datetime.now().time() #現在時刻が入る
# dt_now =datetime.datetime.now()
Registered_id = [] #登録済みの生徒の学籍番号が入る
Registered_Faces_Encoding = [] #登録済みの顔の情報格納場所
id_list=[] #生徒のid
st=[] #授業の開始時間
end=[] #授業の終了時間

# in_time = Attendance.objects.values('in_Time')

student_id_datas = Student.objects.values('student_ID_number')
for student_id_data in student_id_datas:
    Registered_id.append(student_id_data['student_ID_number'])
# print(Registered_id)

image_file = [filename for filename in listdir('/Users/tomoya/Desktop/テックソン/出席管理/Attendance_management_project/faces') if not filename.startswith('.')]
images=natsorted(image_file)
# print(images)
for image in images:
    face_image = face_recognition.load_image_file(
        f'/Users/tomoya/Desktop/テックソン/出席管理/Attendance_management_project/faces/{image}')
    face_encoding = face_recognition.face_encodings(face_image)[0]
    Registered_Faces_Encoding.append(face_encoding)

def Home(request):
    return render(request, 'management/index.html')

class index(ListView):
    template_name = "management/index.html"
    model = News

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'management/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attendance = Attendance.objects.all()
        students = Student.objects.all()
        # queryset = students.union(attendance)
        # context['object_list'] = queryset
        # return context
        context['attendances']=attendance
        context['students']=students
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

class StudentDetail(LoginRequiredMixin, DetailView):
    template_name = 'management/student.html'
    model = Student
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attendance_log = Attendance_log.objects.filter(student__name=self.object.name)
        context['logs'] = attendance_log
        return context

# class Attedance_log(LoginRequiredMixin,DeleteView):
#     model = Attendance_log
#     template_name='management/management_detail.html'

class create(LoginRequiredMixin, CreateView):
    model = Student
    fields = ['name','student_ID_number','image',]
    template_name = 'management/create.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)
class Deleteview(LoginRequiredMixin,DeleteView):
    template_name='management/management_delete.html'
    model=Student
    success_url = reverse_lazy('student_list')

class Face_recognition(LoginRequiredMixin, TemplateView):
    def get(self, request,):
        return render(request, 'management/face_recognition.html', {})

def video_feed_view():

    return lambda _: StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

def generate_frame():
    try:
        capture = cv2.VideoCapture(1)  # USBカメラ自動切り替え機能追加予定

        while True:

            ret, frame = capture.read()

            ret, jpeg = cv2.imencode('.jpg', frame)

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = (face_recognition.face_encodings(rgb_frame, face_locations))
            dt_now=datetime.datetime.now()


            for face_encoding in face_encodings:
                matchs = face_recognition.compare_faces(
                    Registered_Faces_Encoding, face_encoding)
                face_distances = face_recognition.face_distance(
                    Registered_Faces_Encoding, face_encoding)
                best_matchs = np.argmin(face_distances)

                today = datetime.date.today()
                week_lsit=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                weekday=(week_lsit[(today.weekday())])
                print(weekday)
                Schedule= schedule.objects.filter(day_of_week=weekday)
                # print(Schedule)
                for i in Schedule:
                    st.append(i.start_time)
                    end.append(i.end_time)
                print(f'===デバッグ===\nスタート:{min(st)}')
                print(f'エンド{max(end)}\n==============')

                time_n= dt_now.time()
                schedule_start_time = min(st)
                schedule_end_time= max(end)

                if matchs[best_matchs]:
                    ID = Registered_id[best_matchs]
                    ret, jpeg = cv2.imencode('.jpg', success_img)
                    attendance = Attendance.objects.get(student__student_ID_number=ID)
                    if attendance.in_Time is None:
                        attendance.in_Time = timezone.now()
                        attendance.in_Time=dt_now
                        attendance.status =  '出席'

                        if time_n > schedule_start_time:
                            attendance.status = '遅刻'
                        attendance.save()

                    elif not attendance.in_Time == None:
                        if not attendance.in_Time.minute == datetime.datetime.now().minute:
                            attendance.out_time = dt_now
                            if time_n < schedule_end_time:
                                attendance.status = '早退'
                            elif time_n < schedule_end_time and attendance.status=='遅刻':
                                attendance.status='遅刻/早退'
                            attendance.save()

                else:
                    ret, jpeg = cv2.imencode('.jpg', warning_img)

            byte_frame = jpeg.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
    except BaseException as error:
        print(error)
        ret, jpeg = cv2.imencode('.jpg', error_img)
        byte_frame = jpeg.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')

class Setting(LoginRequiredMixin,ListView):
    model=schedule
    template_name='management/setting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Monday= schedule.objects.filter(day_of_week='Monday')
        context['Monday']=Monday

        Tuesday= schedule.objects.filter(day_of_week='Tuesday')
        context['Tuesday']=Tuesday

        Wednesday= schedule.objects.filter(day_of_week='Wednesday')
        context['Wednesday']=Wednesday

        Thursday= schedule.objects.filter(day_of_week='Thursday')
        context['Thursday']=Thursday

        Friday= schedule.objects.filter(day_of_week='Friday')
        context['Friday']=Friday

        Saturday= schedule.objects.filter(day_of_week='Saturday')
        context['Saturday']=Saturday

        Sunday= schedule.objects.filter(day_of_week='Sunday')
        context['Sunday']=Sunday
        return context

class Create_setting(LoginRequiredMixin,CreateView):
    model=schedule
    fields = ['day_of_week','lasson_name','start_time','end_time',]
    template_name='management/create_lesson.html'
    success_url = reverse_lazy('setting')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)
