from django.contrib import admin
from .models import Ingredient, Tag, Recipe, IngredientAmount, Favorite, ShoppingCart


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredients',
        'recipe', 
        'amount'
    )
    search_fields = ('recipe', )
    list_filter = ('amount',)
    empty_value_display = '-пусто-'
    # filter_horizontal = ('ingredient',)
    


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', )
    list_filter = ('name', 'color')
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        # 'tags',
        'author',
        # 'ingredients',
        'name',
        'text',
        'image',
        'cooking_time'
    )
    search_fields = ('name', )
    list_filter = ('name', 'author')
    empty_value_display = '-пусто-'
    # filter_horizontal = ('ingredients', 'tags')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'author')
    search_fields = ('author',)
    list_filter = ('author', 'recipe',)
    empty_value_display = '-пусто-'



class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'author')
    search_fields = ('author',)
    list_filter = ('author', 'recipe',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)