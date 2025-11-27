"""
Views для работы с пользователями.
Регистрация, login, просмотр и редактирование профиля,
деактивация аккаунта.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .utils import generate_jwt
from .permissions import IsAuthenticatedAPIUser


class RegisterView(APIView):
    """Регистрация нового пользователя."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Создает нового пользователя."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """Авторизация пользователя и выдача JWT."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Вход пользователя в систему."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = generate_jwt(user)
        return Response({"token": token}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Выход пользователя из системы (JWT)."""

    permission_classes = [IsAuthenticatedAPIUser]

    def post(self, request):
        """Logout: клиент должен удалить токен."""
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailView(APIView):
    """Просмотр и редактирование текущего пользователя."""

    permission_classes = [IsAuthenticatedAPIUser]

    def get(self, request):
        """Получить данные текущего пользователя."""
        user = request.api_user
        return Response(UserSerializer(user).data)

    def patch(self, request):
        """Обновление данных текущего пользователя."""
        user = request.api_user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        """Мягкое удаление пользователя (деактивация)."""
        user = request.api_user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
