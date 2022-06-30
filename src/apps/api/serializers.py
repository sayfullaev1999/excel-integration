from rest_framework import serializers

from apps.core.models import Client


class ClientReadOnlySerializer(serializers.ModelSerializer):
    organizations_count = serializers.IntegerField(help_text='Количество организаций')
    incoming = serializers.IntegerField(help_text='Приход')

    class Meta:
        model = Client
        fields = ('name', 'organizations_count', 'incoming')
