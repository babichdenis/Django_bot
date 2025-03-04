from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel, TelegramUser


class Notification(BaseModel):
    NOTIFICATION_TYPES = [
        ('order_created', 'Создание заказа'),
        ('payment_received', 'Получение платежа'),
        ('order_shipped', 'Отправка товара'),
        ('advertisement', 'Рекламная рассылка'),
        ('system_alert', 'Системное уведомление')
    ]

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        null=True,
        blank=True,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name='Тип уведомления'
    )
    message = models.TextField(verbose_name='Текст сообщения')
    is_sent = models.BooleanField(
        default=False,
        verbose_name='Отправлено'
    )
    scheduled_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время отправки'
    )
    is_broadcast = models.BooleanField(
        default=False,
        verbose_name='Массовая рассылка'
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        indexes = [
            models.Index(fields=['notification_type', 'is_sent']),
            models.Index(fields=['scheduled_time'])
        ]

    def clean(self):
        super().clean()

        # Валидация для индивидуальных уведомлений
        if not self.is_broadcast and not self.user:
            raise ValidationError(
                {'TelegramUser': 'Обязательно для индивидуальных уведомлений'},
                code='user_required'
            )

        # Проверка telegram_id пользователя
        if self.user and not self.user.telegram_id:
            raise ValidationError(
                {'TelegramUser': 'У пользователя не указан Telegram ID'},
                code='no_telegram_id'
            )

        # Запрет на массовые уведомления для некоторых типов
        if self.is_broadcast and self.notification_type in ['order_created', 'payment_received']:
            raise ValidationError(
                {'notification_type': 'Этот тип не поддерживает массовую рассылку'},
                code='invalid_broadcast_type'
            )

    def get_recipient_id(self):
        """Получить Telegram ID получателя"""
        return self.user.telegram_id if self.user else None

    def mark_as_sent(self):
        """Пометить как отправленное"""
        self.is_sent = True
        self.save(update_fields=['is_sent'])
