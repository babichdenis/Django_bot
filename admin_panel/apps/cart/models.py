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

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def clear(self):
        self.items.all().delete()

    def convert_to_order(self, delivery_address):
        order = Order.objects.create(
            user=self.user,
            address=delivery_address,
            total=self.total
        )
        for item in self.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        self.clear()
        return order


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

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def clean(self):
        super().clean()
        if self.quantity > self.product.stock:
            raise ValidationError(
                ('Недостаточно товара на складе. Доступно: %(stock)s') % {
                    'stock': self.product.stock}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.cart.save()
