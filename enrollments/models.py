from django.db import models
from accounts.models import Student
from academics.models import Course
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class EnrollmentStatus(models.TextChoices):
    DROPPED = "DROPPED", "Dropped"
    PASSED = "PASSED", "Passed"
    FAILED = "FAILED", "Failed"
    ONGOING = "ONGOING", "Ongoing"
    REGISTERED = "REGISTERED", "Registered"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    practical_mark = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(30.0)],
    )
    theoretical_mark = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(70.0)],
    )
    status = models.CharField(choices=EnrollmentStatus.choices, default=EnrollmentStatus.REGISTERED, max_length=10)


    @property
    def is_passed(self):
        return self.practical_mark + self.theoretical_mark >= 50
    @property
    def is_failed(self):
        return self.status == EnrollmentStatus.FAILED

    @property
    def is_ongoing(self):
        return self.status == EnrollmentStatus.ONGOING

    @property
    def is_registered(self):
        return self.status == EnrollmentStatus.REGISTERED

    def __str__(self):
        return f"{self.status}-{self.course}"


