# for accounts app models.py




from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # For teacher approval
    email = models.EmailField(unique=True)  # Ensure email is unique
    school_id = models.CharField(max_length=10, unique=True, blank=True, null=True)  # Unique ID for all users
    full_name = models.CharField(max_length=90, blank=True, null=True)  # Optional full name (e.g., John, Michael, or John Michael Doe)
    education_level = models.CharField(
        max_length=20,
        choices=[
            ('high_school', 'High School'),
            ('senior_high', 'Senior High'),
            ('university_college', 'University/College')
        ],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.full_name or self.username}"