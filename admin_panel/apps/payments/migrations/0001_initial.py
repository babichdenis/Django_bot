# Generated by Django 5.1.6 on 2025-03-05 23:40

import apps.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_active', models.BooleanField(default=True, help_text='Для мягкого удаления', verbose_name='Активен')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[apps.core.validators.validate_positive_decimal], verbose_name='Сумма')),
                ('currency', models.CharField(default='RUB', max_length=3, verbose_name='Валюта')),
                ('status', models.CharField(choices=[('pending', 'Ожидает оплаты'), ('completed', 'Успешно'), ('failed', 'Ошибка'), ('refunded', 'Возврат'), ('partially_refunded', 'Частичный возврат')], default='pending', max_length=20, verbose_name='Статус')),
                ('transaction_id', models.CharField(max_length=100, unique=True, verbose_name='ID транзакции')),
                ('payment_method', models.CharField(choices=[('card', 'Банковская карта'), ('qiwi', 'QIWI'), ('yoomoney', 'ЮMoney'), ('sbp', 'СБП')], max_length=20, verbose_name='Способ оплаты')),
                ('gateway_response', models.JSONField(blank=True, null=True, verbose_name='Ответ платежной системы')),
                ('processed_at', models.DateTimeField(blank=True, null=True, verbose_name='Время проведения платежа')),
                ('refund_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[apps.core.validators.validate_positive_decimal], verbose_name='Сумма возврата')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='orders.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
                'ordering': ['-processed_at'],
            },
        ),
        migrations.CreateModel(
            name='PaymentStatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(max_length=20, verbose_name='Предыдущий статус')),
                ('new_status', models.CharField(max_length=20, verbose_name='Новый статус')),
                ('changed_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_logs', to='payments.payment', verbose_name='Платеж')),
            ],
            options={
                'verbose_name': 'Лог статуса платежа',
                'verbose_name_plural': 'Логи статусов платежей',
                'ordering': ['-changed_at'],
            },
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['status', 'processed_at'], name='payments_pa_status_1a23af_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['transaction_id'], name='payments_pa_transac_8e9d99_idx'),
        ),
    ]
