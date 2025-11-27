"""Mock-views бизнес-объектов."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import BusinessElement
from .permissions import CanReadPermission


class BusinessElementListView(APIView):
    """Список бизнес-объектов с проверкой прав доступа."""

    permission_classes = [CanReadPermission]

    def get(self, request):
        """
        Возвращает список элементов.
        Доступ только если CanReadPermission разрешил.
        """
        user = getattr(request, "api_user", None)
        if not user:
            return Response(
                {"detail": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        elements = BusinessElement.objects.all()
        data = [{"id": el.id, "name": el.name} for el in elements]

        return Response(data, status=status.HTTP_200_OK)
