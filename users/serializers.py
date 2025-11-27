"""Сериализаторы для регистрации, логина и отображения пользователя."""

from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "password_confirm",
            "role",
        ]

    def validate_email(self, email):
        """Проверка уникальности email."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return email

    def validate(self, data):
        """Проверка совпадения паролей."""
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        """Создание пользователя с хешированным паролем."""
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        return User.objects.create(
            **validated_data,
            password_hash=make_password(password),
        )


class LoginSerializer(serializers.Serializer):
    """Сериализатор логина пользователя."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Проверка email и пароля."""
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверный email или пароль.")

        if not check_password(data["password"], user.password_hash):
            raise serializers.ValidationError("Неверный email или пароль.")

        data["user"] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор текущего пользователя."""

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "role",
        ]
