import logging
from enum import unique
from typing import Any

from django.conf import settings
from rest_framework import serializers
from accounts.models import CustomUser, Student, ROLES


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["url", "username", "email", "role"]


class StudentSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email', 'password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validation_data: object):

        print("before creating user")
        user = CustomUser.objects.create_user(
               role=ROLES.STUDENT, **validation_data
        )

        return user
