# Create your views here.
from rest_framework import status, permissions, viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .models import CustomUser, Student
from .permissions import IsStudent
from .serializers import UserSerializer, StudentProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class StaffProfile(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user



class StudentProfile(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = StudentProfileSerializer

    def get_object(self):
        return (
            Student.objects.select_related("user")
            .get(user=self.request.user)
        )