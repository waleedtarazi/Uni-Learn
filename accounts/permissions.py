from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    """
    Global permission check if user is a student
    """
    def has_permission(self, request, view):
        return request.user.is_student
