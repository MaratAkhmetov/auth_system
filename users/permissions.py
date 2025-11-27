"""
DRF Permissions для пользователей.
Проверка авторизации через request.api_user.
"""

from rest_framework import permissions


class IsAuthenticatedAPIUser(permissions.BasePermission):
    """
    Permission для DRF, проверяющий, что пользователь авторизован через API
    и активен (is_active=True).
    """

    def has_permission(self, request, view):
        user = getattr(request, "api_user", None)
        return bool(user and user.is_active)
