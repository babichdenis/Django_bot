from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel, DeliveryAddress, TelegramUser
from apps.products.models import Product
from apps.core.validators import validate_positive_decimal, validate_positive_integer


class Order(BaseModel):
    STATUS_CHOICES = [
        ('new', ('Новый')),
        ('processing', ('В обработке')),
        ('shipped', ('Отправлен')),
        ('delivered', ('Доставлен')),
        ('canceled', ('Отменен'))
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('partially_paid', 'Частично оплачено'),
        ('refunded', 'Возвращено'),
        ('failed', 'Ошибка оплаты'),
    ]
    DELIVERY_METHODS = [
        ('standard', ('Стандартная')),
        ('express', ('Экспресс')),
    ]
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=('Пользователь')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name=('Статус')
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name=('Статус оплаты')
    )
    address = models.ForeignKey(
        DeliveryAddress,
        on_delete=models.PROTECT,
        verbose_name=('Адрес доставки'),
        null=True, 
        blank=True,
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[validate_positive_decimal],
        verbose_name=('Сумма заказа')
    )
    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_METHODS,
        default='standard',
        verbose_name=('Способ доставки')
    )
    delivery_cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        validators=[validate_positive_decimal],
        verbose_name=('Стоимость доставки')
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[validate_positive_decimal],
        verbose_name=('Скидка (%)')
    )
    promo_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=('Промокод')
    )
    expected_delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=('Ожидаемая дата доставки')
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name=('Комментарий')
    )

    class Meta(BaseModel.Meta):
        verbose_name = ('Заказ')
        verbose_name_plural = ('Заказы')
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at', 'status']),
            models.Index(fields=['expected_delivery_date']),
        ]

class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=('Заказ')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=('Товар')
    )
    quantity = models.PositiveIntegerField(
        validators=[validate_positive_integer],
        verbose_name=('Количество')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_positive_decimal],
        verbose_name=('Цена за единицу')
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[validate_positive_decimal],
        verbose_name=('Скидка на товар (%)')
    )

    class Meta(BaseModel.Meta):
        verbose_name = ('Элемент заказа')
        verbose_name_plural = ('Элементы заказа')
        unique_together = ('order', 'product')

    @property
    def subtotal(self):
        return self.quantity * self.price * (1 - self.discount / 100)


class OrderStatusHistory(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history',
        verbose_name=('Заказ')
    )
    status = models.CharField(
        max_length=20,
        choices=Order.STATUS_CHOICES,
        verbose_name=('Статус'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = ('История статуса заказа')
        verbose_name_plural = ('Истории статусов заказов')
