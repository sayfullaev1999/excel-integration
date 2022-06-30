from decimal import Decimal

from django.db import models


class Client(models.Model):
    """
        Модель Клиента
    """
    name = models.CharField(
        verbose_name='Имя', max_length=255, unique=True
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Organization(models.Model):
    """
        Модель организации
    """
    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, related_name='organizations'
    )
    name = models.CharField(
        verbose_name='Имя', max_length=255
    )
    address = models.CharField(
        verbose_name='Адрес', max_length=255,
        null=True, blank=True
    )
    fraud_weight = models.IntegerField(default=0)

    class Meta:
        unique_together = ('client', 'name')
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class Bill(models.Model):
    client = models.ForeignKey(
        verbose_name='Клиент', to=Client, on_delete=models.CASCADE, related_name='bills'
    )
    organization = models.ForeignKey(
        verbose_name='Организация', to=Organization, on_delete=models.CASCADE, related_name='bills'
    )
    number = models.IntegerField(verbose_name='№')
    sum = models.IntegerField(verbose_name='Сумма')
    date = models.DateField(verbose_name='Дата')
    service = models.CharField(verbose_name='Сервис', max_length=255)
    fraud_score = models.DecimalField(
        verbose_name='Детектор мошенничества',
        max_digits=3, decimal_places=2
    )
    service_class = models.IntegerField(verbose_name='Классификатор услуг: Класс')
    service_name = models.CharField(verbose_name='Классификатор услуг: Имя', max_length=255)

    class Meta:
        unique_together = ('organization', 'number')
        verbose_name = 'Счета организации клиента'
        verbose_name_plural = 'Счета организации клиента'

    def save(self, *args, **kwargs):
        if self.pk is None and self.fraud_score >= Decimal('0.9'):
            organization = self.organization
            organization.fraud_weight += 1
            organization.save(update_fields=['fraud_weight'])
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.organization} - {self.number}'
