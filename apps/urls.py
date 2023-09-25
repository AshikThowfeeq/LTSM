from django.urls import path
from apps.views import *

urlpatterns = [
    path('', datelist, name='date_list'),
    path('attendance-dashboard/<str:date>/', attendance_dashboard, name='attendance_dashboard'),
    path('batch-attendance/<str:batch>/<str:date>/', batch_attendance, name='batch_attendance'),
    path('student-detail/<str:student_email>/', student_detail, name='student_detail'),
]
