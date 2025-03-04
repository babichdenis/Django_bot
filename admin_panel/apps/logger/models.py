from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import BaseModel, TelegramUser


class ActionLog(BaseModel):
    ACTION_TYPES = [
        ('create', 'Создание'),
        ('update', 'Обновление'),
        ('delete', 'Удаление'),
        ('system', 'Системное событие')
    ]

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    action_type = models.CharField(
        max_length=20,
        choices=ACTION_TYPES,
        verbose_name='Тип действия'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Тип объекта'
    )
    object_id = models.PositiveIntegerField(verbose_name='ID объекта')
    content_object = GenericForeignKey('content_type', 'object_id')
    details = models.JSONField(
        verbose_name='Детали',
        default=dict,
        blank=True
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='IP адрес',
        null=True,
        blank=True
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'Лог действия'
        verbose_name_plural = 'Логи действий'
        indexes = [
            models.Index(fields=['action_type', 'created_at']),
            models.Index(fields=['content_type', 'object_id'])
        ]

    def __str__(self):
        return f"{self.get_action_type_display()} #{self.object_id}"
