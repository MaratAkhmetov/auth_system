"""
URL конфигурация для бизнес-объектов.
Используется Mock-View с проверкой прав через permissions.
"""

from django.urls import path
from .views import BusinessElementListView

urlpatterns = [
    path("elements/",
         BusinessElementListView.as_view(),
         name="business-elements"),
]
