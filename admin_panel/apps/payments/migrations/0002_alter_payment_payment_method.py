# Generated by Django 5.1.7 on 2025-03-07 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('card', 'Банковская карта'), ('tbank', 'Т-Банк'), ('yoomoney', 'ЮMoney'), ('sbp', 'СБП')], max_length=20, verbose_name='Способ оплаты'),
        ),
    ]
