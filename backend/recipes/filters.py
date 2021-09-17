from distutils.util import strtobool

import django_filters

from .models import Recipe

BOOLEAN_CHOICES = (('0', 'False'), ('1', 'True'),)


class RecipeFilter(django_filters.FilterSet):
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
        return Recipe.objects.all()

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value:
                return Recipe.objects.filter(
                    shoppings__author=self.request.user)
        return Recipe.objects.all()
