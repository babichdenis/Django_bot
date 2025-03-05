from django.db import models
from django.core.exceptions import ValidationError

from apps.orders.models import Order, OrderItem
from apps.core.models import BaseModel
from apps.products.models import Product
from apps.core.models import TelegramUser
from apps.core.validators import validate_positive_integer


class Cart(BaseModel):
    user = models.OneToOneField(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=('Пользователь')
    )

    class Meta(BaseModel.Meta):
        verbose_name = ('Корзина')
        verbose_name_plural = ('Корзины')


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=('Корзина')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=('Товар')
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[validate_positive_integer],
        verbose_name=('Количество')
    )

    class Meta(BaseModel.Meta):
        verbose_name = ('Элемент корзины')
        verbose_name_plural = ('Элементы корзины')
        unique_together = ('cart', 'product')
