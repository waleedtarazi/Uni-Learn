from django.urls import include, path
from enrollments.views import CurrentSemester, EnrollmentRegistrationView

urlpatterns = [
    path("semesters/current/", CurrentSemester.as_view()),
    path("semesters/current/register", EnrollmentRegistrationView.as_view()),

]


