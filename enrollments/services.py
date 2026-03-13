from __future__ import annotations

from dataclasses import dataclass

from django.db import transaction, connection
from django.db.models import Q
from rest_framework import serializers

from academics.models import Course, Semester
from enrollments.models import Enrollment, EnrollmentStatus


@dataclass(frozen=True)
class EnrollmentResult:
    created_count: int


def register_courses_for_student(*, student, course_ids: list[str]) -> EnrollmentResult:
    """
    Domain service for student course registration.
    Keeps business rules out of serializers/views.
    """
    if len(course_ids) != len(set(course_ids)):
        raise serializers.ValidationError("Duplicated courses are not allowed")

    try:
        current_semester = Semester.objects.get(is_open=True)
    except Semester.DoesNotExist:
        raise serializers.ValidationError("No open semester to register for")

    courses = []
    student_enrollments = student.enrollments.exclude(Q(status=EnrollmentStatus.FAILED) | Q(status=EnrollmentStatus.DROPPED))

    for course_id in course_ids:
        try:
            course = Course.objects.select_related("semester").get(pk=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError(f"course_{course_id} is not found")

        if course.semester_id != current_semester.id:
            raise serializers.ValidationError(f"course_{course_id} is not in the current semester")

        if student_enrollments.filter(course__subject=course.subject).exists():
            raise serializers.ValidationError(f"already enrolled in course_{course_id}")
        #
        course_pre_reqs = course.subject.subjects_pre_requisites.all()
        student_enrollments = student_enrollments.exclude(status=EnrollmentStatus.REGISTERED)
        student_subjects = student_enrollments.values_list('course__subject')
        missing = course_pre_reqs.exclude(id__in=student_subjects)
        if missing:
            raise serializers.ValidationError(f" you have to take course pre-prerequisites")

        courses.append(course)

    enrollments = [
        Enrollment(student=student, course=course, status=EnrollmentStatus.REGISTERED)
        for course in courses
    ]

    with transaction.atomic():
        Enrollment.objects.bulk_create(enrollments)

    return EnrollmentResult(created_count=len(enrollments))

