# Generated by Django 5.1.6 on 2025-03-05 23:40

import apps.core.validators
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_active', models.BooleanField(default=True, help_text='Для мягкого удаления', verbose_name='Активен')),
                ('name', models.CharField(max_length=100, validators=[apps.core.validators.validate_no_special_chars], verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('slug', models.SlugField(unique=True, verbose_name='URL-идентификатор')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='Изображение')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='products.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_active', models.BooleanField(default=True, help_text='Для мягкого удаления', verbose_name='Активен')),
                ('name', models.CharField(max_length=255, validators=[apps.core.validators.validate_no_special_chars], verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[apps.core.validators.validate_positive_decimal], verbose_name='Цена')),
                ('stock', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Остаток на складе')),
                ('sku', models.CharField(help_text='Уникальный идентификатор товара', max_length=50, unique=True, verbose_name='Артикул')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('available', models.BooleanField(default=True, verbose_name='Доступен для заказа')),
                ('main_image', models.ImageField(upload_to='products/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='Основное изображение')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[apps.core.validators.validate_positive_decimal], verbose_name='Вес (кг)')),
                ('dimensions', models.CharField(blank=True, max_length=50, null=True, verbose_name='Габариты (Д×Ш×В)')),
                ('categories', models.ManyToManyField(related_name='products', to='products.category', verbose_name='Категории')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['slug'], name='products_ca_slug_da4386_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['parent'], name='products_ca_parent__f3c24e_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['sku'], name='products_pr_sku_ca0cdc_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['available'], name='products_pr_availab_21d9ca_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['price'], name='products_pr_price_9b1a5f_idx'),
        ),
    ]
