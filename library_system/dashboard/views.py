# dashboard/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser  # Adjust import based on your user model

@login_required
def teacher_dashboard_view(request):
    if not request.user.is_teacher or not request.user.is_approved:
        return render(request, 'dashboard/error.html', {'message': 'You are not authorized to access the teacher dashboard.'})
    return render(request, 'dashboard/teacher.html')

@login_required
def student_dashboard_view(request):
    if not request.user.is_student:
        return render(request, 'dashboard/error.html', {'message': 'You are not authorized to access the student dashboard.'})
    return render(request, 'dashboard/student.html')

@login_required
def schedule_view(request):
    user = request.user
    if not (user.is_teacher or user.is_student):
        return render(request, 'dashboard/error.html', {'message': 'You are not authorized to access the schedule.'})
    
    # Determine school type based on education_level
    education_level = user.education_level
    initial_school_type = 'HighSchool' if education_level == 'high_senior' else 'University'
    
    context = {
        'user': user,
        'is_teacher': user.is_teacher,
        'education_level': education_level,
        'initial_school_type': initial_school_type,
    }
    
    # Use unified template for both teachers and students
    return render(request, 'dashboard/schedule.html', context)

@login_required
def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_teacher and request.user.is_approved:
            return redirect('dashboard:teacher_dashboard')
        elif request.user.is_student:
            return redirect('dashboard:student_dashboard')
    return redirect('login_signup')  # Adjust 'login_signup' to your login URL name