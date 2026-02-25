from django.contrib.auth import user_logged_in
from django.shortcuts import render
from drf_spectacular.utils import extend_schema

# Create your views here.
from rest_framework import status, permissions, viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import serialize

from .models import CustomUser
from .serializers import UserSerializer, StudentSignUpSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]


class StudentSingUp(generics.CreateAPIView):
    serializer_class = StudentSignUpSerializer
    permission_classes = [AllowAny]

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self):
        serializer = UserSerializer(CustomUser.get_username())
        return Response(serializer.data)