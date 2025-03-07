from django.db import models
from django.core.exceptions import ValidationError
from apps.orders.models import Order
from apps.core.models import BaseModel
from apps.core.validators import validate_positive_decimal
import re


class Payment(BaseModel):
    STATUS_CHOICES = [
        ('pending', ('Ожидает оплаты')),
        ('completed', ('Успешно')),
        ('failed', ('Ошибка')),
        ('refunded', ('Возврат')),
        ('partially_refunded', ('Частичный возврат')),
    ]

    PAYMENT_METHODS = [
        ('card', ('Банковская карта')),
        ('tbank', ('Т-Банк')),
        ('yoomoney', ('ЮMoney')),
        ('sbp', ('СБП')),
    ]
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name='Заказ'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[validate_positive_decimal],
        verbose_name=('Сумма')
    )
    currency = models.CharField(
        max_length=3,
        default='RUB',
        verbose_name=('Валюта')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=('Статус')
    )
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=('ID транзакции')
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name=('Способ оплаты')
    )
    gateway_response = models.JSONField(
        verbose_name=('Ответ платежной системы'),
        null=True,
        blank=True
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=('Время проведения платежа')
    )
    refund_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[validate_positive_decimal],
        verbose_name=('Сумма возврата')
    )

    class Meta:
        verbose_name = ('Платеж')
        verbose_name_plural = ('Платежи')
        indexes = [
            models.Index(fields=['status', 'processed_at']),
            models.Index(fields=['transaction_id']),
        ]
        ordering = ['-processed_at']

    def clean(self):
        super().clean()


class PaymentStatusLog(models.Model):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='status_logs',
        verbose_name='Платеж'
    )
    old_status = models.CharField(
        max_length=20,
        verbose_name='Предыдущий статус'
    )
    new_status = models.CharField(
        max_length=20,
        verbose_name='Новый статус'
    )
    changed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата изменения'
    )

    class Meta:
        verbose_name = 'Лог статуса платежа'
        verbose_name_plural = 'Логи статусов платежей'
        ordering = ['-changed_at']
