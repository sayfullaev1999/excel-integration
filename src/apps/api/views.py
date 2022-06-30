from decimal import Decimal

from django.db.models import (
    Count,
    Sum,
)
from django.db.models.functions import Coalesce
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework import parsers
from rest_framework.response import Response

from apps.core.models import (
    Bill,
    Client,
)

from .serializers import (
    BillReadOnlySerializer,
    ClientReadOnlySerializer,
    UploadSerializer,
)


class ClientReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientReadOnlySerializer

    def get_queryset(self):
        return super().get_queryset().annotate(
            organizations_count=Count('organizations', distinct=True),
            incoming=Coalesce(Sum('bills__sum', distinct=True), Decimal(0))
        )


class BillReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillReadOnlySerializer
    filterset_fields = ('organization__name', 'client__name')


class UploadFileView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    serializer_class = UploadSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data={'exc': str(e)}, status=status.HTTP_400_BAD_REQUEST)
