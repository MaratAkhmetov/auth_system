"""
Главный URL-маршрутизатор проекта.
Сюда подключаются модули users и business.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/business/", include("business.urls")),
]
