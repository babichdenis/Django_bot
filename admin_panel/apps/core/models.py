from django.db import models
from .validators import (
    validate_phone,
    validate_postal_code,
)


class BaseModel(models.Model):
    """
    Абстрактная базовая модель с общими полями и методами
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=('Дата создания'),
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=('Дата обновления'),
        editable=False
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=('Активен'),
        help_text=('Для мягкого удаления')
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def clean(self):
        """Общая валидация для всех моделей"""
        super().clean()

    def soft_delete(self):
        """Мягкое удаление записи"""
        self.is_active = False
        self.save(update_fields=['is_active'])

    def __str__(self):
        return f"{self.__class__.__name__} #{self.pk}"


class TelegramUser(BaseModel):
    telegram_id = models.BigIntegerField(
        unique=True,
        verbose_name=('Telegram ID')
    )
    username = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name=('Логин в Telegram')
    )
    first_name = models.CharField(
        max_length=64,
        verbose_name=('Имя')
    )
    last_name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=('Фамилия')
    )

    class Meta(BaseModel.Meta):
        verbose_name = ('Пользователь')
        verbose_name_plural = ('Пользователи')

    @property
    def primary_address(self):
        return self.addresses.filter(is_primary=True).first()


class DeliveryAddress(BaseModel):
    user = models.ForeignKey(
        'TelegramUser',
        on_delete=models.CASCADE,
        verbose_name=('Пользователь'),
        related_name='addresses'
    )
    country = models.CharField(
        max_length=100,
        verbose_name=('Страна')
    )
    region = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=('Регион/Область')
    )
    city = models.CharField(
        max_length=100,
        verbose_name=('Город')
    )
    street = models.CharField(
        max_length=200,
        verbose_name=('Улица')
    )
    building = models.CharField(
        max_length=20,
        verbose_name=('Дом/Строение')
    )
    apartment = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=('Квартира/Офис')
    )
    postal_code = models.CharField(
        max_length=20,
        validators=[validate_postal_code],
        verbose_name=('Почтовый индекс')
    )
    phone = models.CharField(
        max_length=20,
        validators=[validate_phone],
        verbose_name=('Телефон')
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=('Основной адрес')
    )

    class Meta(BaseModel.Meta):
        verbose_name = ('Адрес доставки')
        verbose_name_plural = ('Адреса доставки')
        ordering = ['-is_primary', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_primary']),
            models.Index(fields=['postal_code'])
        ]

    def clean(self):
        super().clean()
        if self.is_primary:
            # Автоматически снимаем флаг основного адреса у других записей
            DeliveryAddress.objects.filter(
                user=self.user,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street} {self.building}"
