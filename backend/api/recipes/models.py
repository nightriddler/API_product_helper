from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields.related import ManyToManyField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
        ('Время приготовления не может быть меньше 1.0'),
        params={'value': value},
    )

class Ingredient(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Название ингредиента',
        help_text='Укажите ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=250,
        verbose_name='Единица измерения',
        help_text='Укажите единицу измерения'
    )

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        blank=False,
        # related_name='ingredientsamount',
        verbose_name='Рецепт',
        help_text='Укажите рецепт',
        # default='0'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        blank=False,
        # related_name='ingredientsamount',
        verbose_name='Ингредиенты',
        help_text='Укажите ингредиенты',
        # default='0'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        help_text='Укажите количество',
        default='0'
    )
    
    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'ingredients'], name='recipe and ingredients in IngredientAmount restraint')]
    
    def __str__(self):
        return f'{self.ingredients} - {self.amount}'



class Tag(models.Model):
    name = models.CharField(
        max_length=200,
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


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes',
        verbose_name='Тэг',
        help_text='Укажите тэг',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Выберите автора'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        # related_name='recipes',
        verbose_name='Ингредиенты',
        help_text='Укажите ингредиенты',
        through='IngredientAmount'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Укажите название рецепта'
    )
    text = models.TextField(
        verbose_name='Рецепт',
        help_text='Напишите рецепт'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True,
        null=True,
        verbose_name='Изображение рецепта',
        help_text='Загрузите изображение рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления',
        validators=[validate_cooking_time]
    )

    def __str__(self):
        return self.name


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Подписчик на рецепт',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'author'], name='recipe and author in Favorite restraint')]

    def __str__(self):
        return f'{self.author}->{self.recipe}'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppings',
        verbose_name='Рецепт для списка покупок',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppings',
        verbose_name='Автор рецепта',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe',], name='recipe and author in ShoppingCart restraint')]

    def __str__(self):
        return f'{self.author}->{self.recipe}'
