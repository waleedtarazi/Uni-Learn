from django.urls import include, path
from rest_framework import routers
from accounts import views
from accounts.views import StaffProfile, StudentProfile

router = routers.DefaultRouter()
router.register(r"accounts", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("staff/me/profile/", StaffProfile.as_view()),
    path("student/me/profile/", StudentProfile.as_view()),

]


