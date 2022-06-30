from rest_framework import serializers

from apps.core.models import (
    Bill,
    Client,
    Organization,
)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class ClientReadOnlySerializer(serializers.ModelSerializer):
    organizations_count = serializers.IntegerField(help_text='Количество организаций')
    incoming = serializers.IntegerField(help_text='Приход')

    class Meta:
        model = Client
        fields = ('name', 'organizations_count', 'incoming')


class BillReadOnlySerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    organization = OrganizationSerializer()

    class Meta:
        model = Bill
        fields = '__all__'
