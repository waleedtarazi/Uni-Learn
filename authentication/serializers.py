from typing import Any
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import Token

from accounts.models import CustomUser
from accounts.serializers import UserSerializer


class StudentSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Public signup is always a student account.
        return CustomUser.objects.create_user(
            role="student",
            **validated_data
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        token["username"] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        extra_date = {"data": UserSerializer(user).data}
        data.update(extra_date)
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super(CustomTokenRefreshSerializer,self).validate(attrs)
        decode_payload = token_backend.decode(data['access'], verify=True)
        user_id = decode_payload['user_id']
        user_object = UserSerializer(CustomUser.objects.get(pk=user_id))
        data.update(user_object.data)
        return data

