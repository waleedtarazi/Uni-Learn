from django.urls import include, path
from rest_framework import routers
from accounts import views
from rest_framework.authtoken import views as rest_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from accounts.views import StudentSingUp, ProfileView

router = routers.DefaultRouter()
router.register(r"accounts", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("student/signup/", StudentSingUp.as_view()),
    path('api-token-auth/', rest_views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name= 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/profile/', ProfileView.as_view(), name='profile_info'),
]


