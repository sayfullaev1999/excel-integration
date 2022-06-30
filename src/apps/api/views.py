from django.db.models import Count, Sum
from rest_framework import viewsets

from apps.core.models import (
    Bill,
    Client,
)

from .serializers import (
    BillReadOnlySerializer,
    ClientReadOnlySerializer,
)


class ClientReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientReadOnlySerializer

    def get_queryset(self):
        return super().get_queryset().annotate(
            organizations_count=Count('organizations'),
            incoming=Sum('bills__sum')
        )


class BillReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillReadOnlySerializer
    filterset_fields = ('organization__name', 'client__name')
