"""
Permission-классы для проверки прав доступа к бизнес-объектам.
"""

from rest_framework import permissions
from users.models import AccessRolesRules


class CanReadPermission(permissions.BasePermission):
    """DRF Permission-класс для проверки права чтения бизнес-объектов."""

    def has_permission(self, request, view):
        """Проверяет, есть у юзера право чтения хотя бы одного элемента."""
        user = getattr(request, "api_user", None)
        if not user:
            return False

        return AccessRolesRules.objects.filter(
            role=user.role,
            read_permission=True
        ).exists()
