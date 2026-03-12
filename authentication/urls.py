from rest_framework import routers
from django.urls import path
from authentication.views import StudentSignupView, CustomTokenRefreshView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenVerifyView
)

router = routers.DefaultRouter()

urlpatterns = [
path("auth/register/", StudentSignupView.as_view(), name='signup_as_student'),
path('auth/login/', CustomTokenObtainPairView.as_view(), name= 'token_obtain_pair'),
path('auth/refresh-token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
path('auth/verify-token/', TokenVerifyView.as_view(), name='token_verify'),
]