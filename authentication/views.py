# Create your views here.
from rest_framework import status, permissions, viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView


from authentication.serializers import CustomTokenRefreshSerializer, UserSignUpSerializer, CustomTokenObtainPairSerializer


# Create your views here.
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]

from rest_framework_simplejwt.tokens import UntypedToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class DecodeTokenView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token = request.data.get("token")
        try:
            decoded = AccessToken(token)  # Validates signature & expiry
            return Response({"decoded_payload": decoded})
        except (InvalidToken, TokenError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
