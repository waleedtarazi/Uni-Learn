from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import CustomUser


class SignupTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_public_signup_cannot_set_admin_role(self):
        resp = self.client.post(
            "/api/auth/register/",
            {
                "username": "u1",
                "first_name": "F",
                "last_name": "L",
                "email": "u1@example.com",
                "password": "pass12345",
                "role": "admin",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201, resp.content)
        user = CustomUser.objects.get(username="u1")
        self.assertEqual(user.role, "student")
