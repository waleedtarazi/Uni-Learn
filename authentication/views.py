# Create your views here.
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings

from accounts.models import Student
from accounts.views import StudentProfile
from authentication.serializers import CustomTokenRefreshSerializer, StudentSignUpSerializer, CustomTokenObtainPairSerializer


# Create your views here.
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class StudentSignupView(generics.CreateAPIView):
    serializer_class = StudentSignUpSerializer
    permission_classes = [AllowAny]

