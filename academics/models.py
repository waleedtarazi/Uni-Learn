from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q, UniqueConstraint

class SubjectCategory(models.TextChoices):
    UNIVERSITY_MANDATORY = 'UNI_MAND', 'University Mandatory'
    UNIVERSITY_ELECTIVE = 'UNI_ELEC', 'University Elective'
    COLLEGE_MANDATORY = 'COL_MAND', 'College Mandatory'
    COLLEGE_ELECTIVE = 'COL_ELEC', 'College Elective'
    DEPARTMENT_MANDATORY = 'DEP_MAND', 'Department Mandatory',
    DEPARTMENT_ELECTIVE = 'DEP_ELEC', 'Department Elective'

class Department(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name + f"_{self.code}"


# Create your models here.
class Subject(models.Model):
    code = models.CharField(max_length=10, blank=False, unique=True)
    name = models.CharField(max_length=30, blank=False)
    category = models.CharField(max_length=50, choices= SubjectCategory.choices, default=SubjectCategory.COLLEGE_MANDATORY)
    departments = models.ManyToManyField(Department, related_name='subjects')
    credit_hours = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        default= 2
    )
    description = models.CharField(max_length=200, blank=True)
    level = models.IntegerField(
        validators = [MinValueValidator(0),MaxValueValidator(10)],
        default=1
    )
    dep_approval_pre_requisite = models.BooleanField(default=False)
    hours_pre_requisites = models.IntegerField(
        validators= [MinValueValidator(0), MaxValueValidator(165)],
        default= 0,
    )
    subjects_pre_requisites = models.ManyToManyField('Subject', related_name='opens', blank=True)


    def __str__(self):
        return f"{self.pk}-{self.name}_{self.code}"


class SemesterType(models.TextChoices):
    FIRST = "FIRST", "First"
    SECOND = "SECOND", "Second"
    SUMMER = "SUMMER", "Summer"

class Semester(models.Model):
    code = models.CharField(choices=SemesterType.choices, default= SemesterType.FIRST, max_length=10)
    year = models.CharField(max_length=4)
    is_open = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    # official_vacancies =

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["is_open"],
                condition=Q(is_open=True),
                name="unique_open_semester",
            )
        ]

    def clean(self):
        super().clean()
        if self.end_date <= self.start_date:
            raise ValidationError({
                'end_date': "End date must be after start date."
            })
        if self.is_open:
            others_open = Semester.objects.filter(is_open=True).exclude(pk=self.pk)
            if others_open.exists():
                raise ValidationError({
                    "is_open": "Can not open two semesters at the same time"
                })

    def __str__(self):
        return f"{self.code}-{self.year[2:]}"


class Course(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    is_full = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.subject}"

