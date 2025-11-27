"""Регистрация моделей в Django Admin."""

from django.contrib import admin

from .models import (
    Role,
    User,
    BusinessElement,
    AccessRolesRules,
)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Админ-панель для ролей."""
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админ-панель для пользователей."""
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
    )
    list_filter = ("role", "is_active")
    search_fields = ("email", "first_name", "last_name")


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    """Админ-панель бизнес-элементов."""
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(AccessRolesRules)
class AccessRolesRulesAdmin(admin.ModelAdmin):
    """Админ-панель правил доступа."""
    list_display = (
        "id",
        "role",
        "element",
        "read_permission",
        "create_permission",
        "update_permission",
        "delete_permission",
    )
    list_filter = ("role", "element")
