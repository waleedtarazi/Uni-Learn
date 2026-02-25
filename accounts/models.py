from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.transaction import rollback
from django.utils.translation import gettext_lazy as _

class ROLES(models.TextChoices):
    ADMIN = "admin", "Admin"
    TEACHER = "teacher","Teacher"
    TEACHER_ASSISTANT = "teacher_assistant", "Teacher Assistant"
    EMPLOYEE = "employee", "Employee"
    STUDENT = "student", "Student"



class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20, choices=ROLES.choices, default=ROLES.EMPLOYEE
    )
    @property
    def is_admin(self):
        return self.role == ROLES.ADMIN

    @property
    def is_teacher(self):
        return self.role == ROLES.TEACHER

    @property
    def is_teacher_assistant(self):
        return self.role == ROLES.TEACHER_ASSISTANT

    @property
    def is_employee(self):
        return self.role == ROLES.EMPLOYEE

    @property
    def is_student(self):
        return self.role == ROLES.STUDENT

    def __str__(self):
        return self.username + "_" +self.role

class Student(models.Model):
    YEARS = {
        "1st": "First Year",
        "2ed": "Second Year",
        "3ed": "Third Year",
        "4th" : "Fourth Year",
        "5th" : "Fifth Year",
        "6th" : "Sixth Year"
    }
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    MAJORS = {
        "CS":"Computer Science",
        "AI":"Artificial Intelligence",
        "SE":"Software Engineering",
        "NE": "Networking Engineering",
    }

    university_number = models.CharField(max_length=20, unique=True, blank=False)
    gpa = models.FloatField(default=0.0)
    year = models.CharField(max_length=14, blank=False, choices=YEARS, default="1st")
    major = models.CharField(max_length=20, blank=False, choices=MAJORS, default="CS")

    def __str__(self):
        return self.user.username + "_" + self.university_number