from django.core.exceptions import ValidationError
import re


def validate_positive_integer(value):
    """
    Проверяет, что значение является положительным целым числом.
    """
    if not isinstance(value, int):
        raise ValidationError(
            ("Значение должно быть целым числом. Передано: %(value)s"),
            params={"value": value},
        )

    if value <= 0:
        raise ValidationError(
            ("Значение должно быть больше нуля. Передано: %(value)s"),
            params={"value": value},
        )


def validate_no_special_chars(value):
    """Проверка на отсутствие специальных символов"""
    if re.search(r'[!@#$%^&*()+=}{[\]|\\:;"\'<>?/~`]', value):
        raise ValidationError(
            ('Запрещено использовать специальные символы'),
            code='invalid_chars'
        )


def validate_positive_decimal(value):
    """Проверка положительного Decimal значения"""
    if value < 0:
        raise ValidationError(
            ('Значение не может быть отрицательным'),
            code='negative_value'
        )


def validate_telegram_id(value):
    """Проверка формата Telegram ID"""
    if not isinstance(value, int) or value <= 0:
        raise ValidationError(
            'Некорректный формат Telegram ID',
            code='invalid_telegram_id'
        )


def validate_phone(value):
    """Валидация номера телефона"""
    pattern = r'^\+7\d{10}$|^8\d{10}$'
    if not re.fullmatch(pattern, value):
        raise ValidationError(
            ('Номер должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX'),
            code='invalid_phone'
        )


def validate_postal_code(value):
    """Валидация почтового индекса"""
    if not re.fullmatch(r'^\d{6}$', value):
        raise ValidationError(
            ('Почтовый индекс должен содержать 6 цифр'),
            code='invalid_postal_code'
        )
