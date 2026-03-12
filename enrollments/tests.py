from django.test import TestCase

from rest_framework.test import APIClient


class EnrollmentRegistrationPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration_requires_auth(self):
        resp = self.client.post(
            "/api/semesters/current/register",
            {"courses": ["1"]},
            format="json",
        )
        self.assertIn(resp.status_code, (401, 403), resp.content)
