# accounts/admin.py
from django.contrib import admin
from .models import CustomUser
from django.urls import reverse
from django.utils.html import format_html
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponseRedirect
import logging

logger = logging.getLogger(__name__)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'email', 'is_teacher', 'is_student', 'is_approved', 'education_level', 'approve_link']
    list_editable = ['is_approved']  # Allow editing is_approved directly in the list view
    actions = ['approve_teachers']

    def approve_link(self, obj):
        if obj.is_teacher and not obj.is_approved:
            return format_html('<a href="{}">Approve</a>', reverse('approve_teacher', args=[obj.id]))
        return "-"
    approve_link.short_description = "Approve Teacher"

    def approve_teachers(self, request, queryset):
        for user in queryset.filter(is_teacher=True, is_approved=False):
            user.is_approved = True
            user.save()
            try:
                html_message = None
                try:
                    html_message = render_to_string('accounts/email/teacher_approval.html', {
                        'username': user.username,
                        'login_url': request.build_absolute_uri('/')
                    })
                    logger.debug(f"Rendered teacher approval HTML for {user.email}: {html_message[:100]}...")
                except Exception as template_error:
                    logger.error(f"Failed to render teacher approval template for {user.email}: {str(template_error)}")
                
                send_mail(
                    'Teacher Account Approved',
                    f'Dear {user.full_name or user.username},\n\nYour teacher account has been approved by the school admin. You can now log in at {request.build_absolute_uri("/")}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                    html_message=html_message,
                )
                logger.info(f"Teacher approved and email sent to: {user.email}")
                self.message_user(request, f'Approved {user.full_name or user.username} and sent email.')
            except Exception as e:
                logger.error(f"Failed to send teacher approval email to {user.email}: {str(e)}")
                self.message_user(request, f'Approved {user.full_name or user.username}, but failed to send email: {str(e)}', level='warning')
    approve_teachers.short_description = "Approve selected teachers"

    def save_model(self, request, obj, form, change):
        old_approved = CustomUser.objects.get(id=obj.id).is_approved if change else False
        if change and 'is_approved' in form.changed_data and obj.is_teacher and not old_approved and obj.is_approved:
            try:
                html_message = None
                try:
                    html_message = render_to_string('accounts/email/teacher_approval.html', {
                        'username': obj.username,
                        'login_url': request.build_absolute_uri('/')
                    })
                    logger.debug(f"Rendered teacher approval HTML for {obj.email}: {html_message[:100]}...")
                except Exception as template_error:
                    logger.error(f"Failed to render teacher approval template for {obj.email}: {str(template_error)}")
                
                send_mail(
                    'Teacher Account Approved',
                    f'Dear {obj.full_name or obj.username},\n\nYour teacher account has been approved by the school admin. You can now log in at {request.build_absolute_uri("/")}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [obj.email],
                    fail_silently=False,
                    html_message=html_message,
                )
                logger.info(f"Teacher approved and email sent to: {obj.email}")
                self.message_user(request, f'Approved {obj.full_name or obj.username} and sent email notification.')
            except Exception as e:
                logger.error(f"Failed to send teacher approval email to {obj.email}: {str(e)}")
                self.message_user(request, f'Approved {obj.full_name or obj.username}, but failed to send email: {str(e)}', level='warning')
        super().save_model(request, obj, form, change)

    def response_change(self, request, obj):
        if obj.is_teacher and 'is_approved' in request.POST and obj.is_approved:
            self.message_user(request, f'Teacher {obj.full_name or obj.username} has been approved. An email notification has been sent.')
            return HttpResponseRedirect(reverse('admin:accounts_customuser_changelist'))
        return super().response_change(request, obj)