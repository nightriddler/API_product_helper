from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class TagSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializers(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializers(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


# class IngredientSerializers(serializers.ModelSerializer):

#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeCreateSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientAmount
        fields = (
            'id',
            'amount',
        )


class RecipesListSerializers(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    ingredients = IngredientRecipeSerializers(
        many=True, source='ingredientamount_set')
    tags = TagSerializers(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            return Favorite.objects.filter(
                author=self.context['request'].user,
                recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            return ShoppingCart.objects.filter(
                author=self.context['request'].user,
                recipe=obj).exists()
        return False


class CreateRecipeSerializers(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    ingredients = IngredientRecipeCreateSerializers(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients_amount = validated_data.pop('ingredients')
        new_recipe = Recipe.objects.create(
            author=user,
            **validated_data
            )

        for tag in tags:
            new_recipe.tags.add(tag)

        all_ingredients_amount = {
            ingredient['id']: ingredient['amount']
            for ingredient in ingredients_amount
        }

        for ingredient in all_ingredients_amount:
            IngredientAmount.objects.create(
                recipe=new_recipe,
                ingredients=ingredient,
                amount=all_ingredients_amount[ingredient]
            )
        return new_recipe

    def update(self, update_recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients_amount = validated_data.pop('ingredients')
        Recipe.objects.filter(id=update_recipe.id).update(**validated_data)
        update_recipe.refresh_from_db()
        update_recipe.tags.clear()

        for tag in tags:
            update_recipe.tags.add(tag)
        update_recipe.ingredients.clear()
        all_ingredients_amount = {
            ingredient['id']: ingredient['amount']
            for ingredient in ingredients_amount
        }

        for ingredient in all_ingredients_amount:
            IngredientAmount.objects.create(
                recipe=update_recipe,
                ingredients=ingredient,
                amount=all_ingredients_amount[ingredient]
            )
        return update_recipe

    def to_representation(self, instance):
        return RecipesListSerializers(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data


class FavoriteSerializer(RecipesListSerializers):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
