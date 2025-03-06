from django.db import models
from apps.core.models import BaseModel, TelegramUser
from apps.products.models import Product
from apps.core.validators import validate_positive_integer


class CartItem(BaseModel):
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def __str__(self):
        return f"{self.product.name} x{self.quantity} для {self.user.telegram_id}"

    @property
    def total_cost(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
