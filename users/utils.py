"""
Утилиты для работы с JWT-токенами:
- генерация токена
- декодирование токена
- получение пользователя по токену
"""

import jwt
from datetime import timedelta
from django.conf import settings
from django.utils.timezone import now

from users.models import User

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_LIFETIME_MINUTES = settings.JWT_LIFETIME_MINUTES


def generate_jwt(user):
    """Генерация JWT-токена для пользователя."""
    payload = {
        "user_id": user.id,
        "email": user.email,
        "iat": int(now().timestamp()),
        "exp": int(
            (now() + timedelta(minutes=JWT_LIFETIME_MINUTES)).timestamp()
            ),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt(token):
    """Декодирование JWT-токена. Возвращает payload или None при ошибке."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_user_from_token(token):
    """Получение пользователя по JWT-токену. Возвращает User или None."""
    payload = decode_jwt(token)
    if not payload:
        return None

    user_id = payload.get("user_id")
    if not user_id:
        return None

    try:
        return User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        return None
