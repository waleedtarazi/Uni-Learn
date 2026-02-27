from rest_framework import routers
from django.urls import include, path
from authentication.views import UserSignupView, CustomTokenRefreshView, CustomTokenObtainPairView, DecodeTokenView
from rest_framework_simplejwt.views import (
    TokenVerifyView
)

router = routers.DefaultRouter()

urlpatterns = [
path("auth/register/", UserSignupView.as_view(), name='signup_as_student'),
path('auth/login/', CustomTokenObtainPairView.as_view(), name= 'token_obtain_pair'),
path('auth/refresh-token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
path('auth/verify-token/', TokenVerifyView.as_view(), name='token_verify'),
path('auth/decode-token/', DecodeTokenView.as_view()),
]