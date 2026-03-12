from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import SemesterSerializer, EnrollmentsRegistrationSerializer
from academics.models import Semester
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsStudent

# Create your views here.
class CurrentSemester(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SemesterSerializer

    def get_object(self):
        return Semester.objects.get(is_open=True)



class EnrollmentRegistrationView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    @extend_schema(
        request=EnrollmentsRegistrationSerializer
    )
    def post(self, request):

        serializer = EnrollmentsRegistrationSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        result = serializer.save()

        return Response({
            "message": "Enrollments created",
            "count": result.created_count
        })