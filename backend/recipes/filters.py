from distutils.util import strtobool

import django_filters

from .models import Recipe, Ingredient


BOOLEAN_CHOICES = (
    ('0', 'False'),
    ('1', 'True'),
    ('False', 'False'),
    ('True', 'True'),
    ('false', 'False'),
    ('true', 'True'),
)


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.TypedChoiceFilter(
        label='По подписчикам',
        field_name='is_favorited',
        method='filter_is_favorited',
        choices=BOOLEAN_CHOICES,
        coerce=strtobool
    )
    is_in_shopping_cart = django_filters.TypedChoiceFilter(
        label='По списку покупок',
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart',
        choices=BOOLEAN_CHOICES,
        coerce=strtobool
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value:
                return Recipe.objects.filter(
                    favorites__author=self.request.user)
        return Recipe.objects.exclude(
                    favorites__author=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value:
                return Recipe.objects.filter(
                    shoppings__author=self.request.user)
        return Recipe.objects.exclude(
                    shoppings__author=self.request.user)


class IngredientsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)
