from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.Home ,name='home'),
    path('top/',views.index.as_view(),name='index'),
    path('student_list/',views.StudentListView.as_view(),name='student_list'),
    path('create/',views.create.as_view(),name='create'),
    path('Attendance/',views.Face_recognition.as_view(),name='Attendance'),
    path('video_feed', views.video_feed_view(), name="video_feed"),
    path('student/<int:pk>',views.StudentDetail.as_view(),name='student'),
    path('setting/',views.Setting.as_view(),name='setting'),
    path('create_lesson/',views.Create_setting.as_view(),name='create_lesson'),
    # path('Attendance_log/<int:pk>',views.Attedance_log.as_view(),name='log'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)