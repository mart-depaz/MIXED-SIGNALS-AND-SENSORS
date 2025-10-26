# for accounts app urls.py


from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_signup_view, name='login_signup'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('approve_teacher/<int:user_id>/', views.approve_teacher, name='approve_teacher'),
]