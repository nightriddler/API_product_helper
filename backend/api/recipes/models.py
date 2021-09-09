from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Название ингредиента',
        help_text='Укажите ингредиент'
    )
    # amount = models.PositiveIntegerField(
    #     verbose_name='Название ингредиента',
    #     help_text='Укажите ингредиент',
    # )
    measurement_unit = models.CharField(
        max_length=250,
        verbose_name='Единица измерения',
        help_text='Укажите единицу измерения'
    )

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название тэга',
        help_text='Укажите тэг',
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='HEX-код цвета',
        help_text='Укажите цвет в формате HEX-кода',
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text='Укажите слаг тэга',
        unique=True
    )

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
