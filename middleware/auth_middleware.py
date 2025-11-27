"""
Кастомный middleware для API-аутентификации пользователей.
Определяет request.api_user по JWT-токену из заголовка Authorization.
Пропускает админку и не трогает стандартный request.user.
"""

from django.utils.deprecation import MiddlewareMixin
from users.utils import get_user_from_token


class AuthMiddleware(MiddlewareMixin):
    """Middleware для определения пользователя API."""

    def process_request(self, request):
        """
        Извлекает JWT из Authorization: Bearer <jwt>
        и присваивает request.api_user.
        """
        if request.path.startswith('/admin/'):
            return None

        auth_header = request.headers.get("Authorization")
        request.api_user = None

        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        token = parts[1]
        user = get_user_from_token(token)
        if user:
            request.api_user = user

        return None
