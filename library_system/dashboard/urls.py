# for dashboard app urls.py


# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Teacher dashboards
    path('teacher-dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('high-school-teacher-dashboard/', views.teacher_dashboard_view, name='high_school_teacher_dashboard'),
    path('senior-high-teacher-dashboard/', views.teacher_dashboard_view, name='senior_high_teacher_dashboard'),
    path('university-college-teacher-dashboard/', views.teacher_dashboard_view, name='university_college_teacher_dashboard'),
    
    # Student dashboards  
    path('student-dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('high-school-dashboard/', views.student_dashboard_view, name='high_school_dashboard'),
    path('senior-high-dashboard/', views.student_dashboard_view, name='senior_high_dashboard'),
    path('university-college-dashboard/', views.student_dashboard_view, name='university_college_dashboard'),
    
    path('schedule/', views.schedule_view, name='schedule'),
    path('', views.home_view, name='home'),
]