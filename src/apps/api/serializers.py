import pandas as pd
from django.db import transaction

from rest_framework import serializers

from apps.core.models import (
    Bill,
    Client,
    Organization,
)
from apps.core.services import (
    fraud_detector,
    service_classifier,
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


class UploadSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=(('bills', 'bills'), ('client_org', 'client_org')))
    file = serializers.FileField()

    class Meta:
        fields = ['file']

    def create(self, validated_data):
        with transaction.atomic():
            try:
                file = validated_data['file'].file
                if validated_data['type'] == 'client_org':
                    df = pd.read_excel(io=file, sheet_name=['client', 'organization'])
                    Client.objects.bulk_create(
                        [
                            Client(name=client['name'])
                            for _, client in df['client'].iterrows()
                            if not Client.objects.filter(name=client['name']).exists()
                        ]
                    )
                    for _, organization in df['organization'].iterrows():
                        name = organization['name']
                        client = Client.objects.get(name=organization['client_name'])
                        if not Organization.objects.filter(name=name, client=client).exists():
                            address = organization['address']
                            if address:
                                address = f'Адрес: {address}'
                                Organization.objects.create(
                                    client=client,
                                    name=name,
                                    address=address,
                                )
                else:
                    df = pd.read_excel(io=file)
                    for _, bill in df.iterrows():
                        client = Client.objects.get(name=bill['client_name'])
                        organization = Organization.objects.get(name=bill['client_org'])
                        if client and organization:
                            Bill.objects.create(
                                client=client,
                                organization=organization,
                                number=bill['№'],
                                sum=bill['sum'],
                                date=bill['date'],
                                service=bill['service'],
                                fraud_score=fraud_detector(bill['service']),
                                **service_classifier(bill['service'])
                            )
            finally:
                file.close()
        return 1
