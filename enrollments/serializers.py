from rest_framework import serializers

from academics.models import Semester
from enrollments.models import Enrollment
from enrollments.services import register_courses_for_student


class SemesterSerializer(serializers.ModelSerializer):
    courses = serializers.StringRelatedField(many=True)
    # courses = serializers.SlugRelatedField(many=True, read_only=True, slug_field= 'subject')

    class Meta:
        model = Semester
        fields = ['code', 'year', 'is_open', 'start_date', 'end_date', 'courses']


class EnrollmentSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    student = serializers.StringRelatedField()


    class Meta:
        model = Enrollment
        fields = '__all__'



class EnrollmentsRegistrationSerializer(serializers.Serializer):
    courses = serializers.ListField(
        child=serializers.CharField(max_length=10),
        max_length=8,
    )

    def validate(self, attrs):
        # Keep payload shape; service will validate domain rules.
        return attrs

    def create(self, validated_data):
        student = self.context["request"].user.student_profile
        course_ids = validated_data["courses"]
        result = register_courses_for_student(student=student, course_ids=course_ids)
        return result

    class Meta:
        fields = ['courses']