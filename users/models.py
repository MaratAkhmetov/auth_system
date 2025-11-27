"""Модели пользователей, ролей и правил доступа."""

from django.db import models


class Role(models.Model):
    """Роль пользователя (admin, manager и т.п.)."""

    name = models.CharField(
        "Название роли",
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(models.Model):
    """Пользователь системы."""

    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    email = models.EmailField("Email", unique=True)
    password_hash = models.CharField("Хеш пароля", max_length=255)

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Роль",
    )

    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email


class BusinessElement(models.Model):
    """Бизнес-объект (например: Клиенты, Заказы, Товары)."""

    name = models.CharField(
        "Название элемента",
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = "Бизнес-элемент"
        verbose_name_plural = "Бизнес-элементы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AccessRolesRules(models.Model):
    """
    Правила доступа ролей к бизнес-элементам.
    Например: admin может create/update/delete, а manager — только read.
    """

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name="Роль",
    )
    element = models.ForeignKey(
        BusinessElement,
        on_delete=models.CASCADE,
        verbose_name="Элемент",
    )

    read_permission = models.BooleanField("Чтение", default=False)
    read_all_permission = models.BooleanField("Чтение всех", default=False)
    create_permission = models.BooleanField("Создание", default=False)
    update_permission = models.BooleanField("Обновление", default=False)
    update_all_permission = models.BooleanField(
        "Обновление всех",
        default=False
    )
    delete_permission = models.BooleanField("Удаление", default=False)
    delete_all_permission = models.BooleanField("Удаление всех", default=False)

    class Meta:
        verbose_name = "Право доступа"
        verbose_name_plural = "Права доступа"
        unique_together = ("role", "element")

    def __str__(self):
        return f"{self.role} — {self.element}"
