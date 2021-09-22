from django.core.exceptions import ValidationError


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
            'Время приготовления не может быть меньше 1.0')


def validate_amount(value):
    if value <= 0:
        raise ValidationError(
            'Количество ингредиента должно быть больше 0')
