from django.db import models
from django.core.validators import (
    MinValueValidator,
    FileExtensionValidator
)
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel
from apps.core.validators import (
    validate_no_special_chars,
    validate_positive_decimal
)


class Category(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name=('Название'),
        validators=[validate_no_special_chars]
    )
    description = models.TextField(
        verbose_name=('Описание'),
        blank=True
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=('Родительская категория'),
        related_name='children'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name=('URL-идентификатор')
    )
    image = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True,
        verbose_name=('Изображение'),
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png']
            )
        ]
    )

    class Meta(BaseModel.Meta):
        verbose_name = ('Категория')
        verbose_name_plural = ('Категории')
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent']),
        ]
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.parent and self.parent == self:
            raise ValidationError(
                ('Категория не может быть своим собственным родителем')
            )


class Product(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=('Название'),
        validators=[validate_no_special_chars]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=('Цена'),
        validators=[validate_positive_decimal]
    )
    stock = models.PositiveIntegerField(
        verbose_name=('Остаток на складе'),
        validators=[MinValueValidator(0)],
        default=0
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=('Артикул'),
        help_text=('Уникальный идентификатор товара')
    )
    description = models.TextField(
        verbose_name=('Описание'),
        blank=True
    )
    available = models.BooleanField(
        default=True,
        verbose_name=('Доступен для заказа')
    )
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        verbose_name=('Категории')
    )
    main_image = models.ImageField(
        upload_to='products/',
        verbose_name=('Основное изображение'),
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png']
            )
        ]
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=('Вес (кг)'),
        validators=[validate_positive_decimal]
    )
    dimensions = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=('Габариты (Д×Ш×В)')
    )

    class Meta(BaseModel.Meta):
        verbose_name = ('Товар')
        verbose_name_plural = ('Товары')
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['available']),
            models.Index(fields=['price']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def stock_status(self):
        if self.stock is None:  # Проверка на None
            return 'Не указано'
        if self.stock == 0:
            return 'Нет в наличии'
        elif self.stock < 10:
            return 'Мало осталось'
        return 'В наличии'

    def clean(self):
        super().clean()
        if self.price <= 0:
            raise ValidationError(
                ('Цена должна быть положительным числом')
            )
