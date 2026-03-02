from django.contrib.auth.models import AbstractUser
from django.db import models

class ROLES(models.TextChoices):
    ADMIN = "admin", "Admin"
    TEACHER = "teacher","Teacher"
    TEACHER_ASSISTANT = "teacher_assistant", "Teacher Assistant"
    EMPLOYEE = "employee", "Employee"
    STUDENT = "student", "Student"


class Year(models.TextChoices):
    FIRST = "1st", "First Year"
    SECOND = "2nd", "Second Year"
    THIRD = "3rd", "Third Year"
    FOURTH = "4th", "Fourth Year"
    FIFTH = "5th", "Fifth Year"

class Major(models.TextChoices):
    CS = "CS","Computer Science"
    AI = "AI","Artificial Intelligence"
    SE = "SE","Software Engineering"
    NE = "NE", "Networking Engineering"


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

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")


    university_number = models.CharField(max_length=20, unique=True, blank=False)
    gpa = models.FloatField(default=0.0)
    year = models.CharField(max_length=14, blank=False, choices=Year.choices, default="1st")
    major = models.CharField(max_length=20, blank=False, choices=Major.choices, default="CS")

    def __str__(self):
        return self.user.username + "_" + self.university_number


