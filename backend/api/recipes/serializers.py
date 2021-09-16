from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Ingredient, Tag, Recipe, IngredientAmount, Favorite, ShoppingCart
from users.serializers import CustomUserSerializer
from drf_base64.fields import Base64ImageField


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
    measurement_unit = serializers.ReadOnlyField(source='ingredients.measurement_unit')
    # amount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = IngredientAmount
        # model = Ingredient
        # fields = '__all__'
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class IngredientSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
    

class IngredientRecipeCreateSerializers(serializers.ModelSerializer):
    
    # id = serializers.ReadOnlyField(source='ingredientamount_set.ingredients.id')
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    # name = serializers.ReadOnlyField(source='ingredients.name')
    # measurement_unit = serializers.ReadOnlyField(source='ingredients.measurement_unit')
    # amount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = IngredientAmount
        # model = Ingredient
        # fields = '__all__'
        fields = (
            'id',
            # 'name',
            # 'measurement_unit',
            'amount',
        )
    # def get_amount(self, obj):
    #     import ipdb; ipdb.set_trace() 
    #     return obj.measurement_unit
    
    # def get_measurement_unit(self, obj):
        
        # import ipdb; ipdb.set_trace() 
        # ingredients_id = self.context['request'].data.get('inredients')
        # ingredient = Ingredient.objects.get(id=ingredients_id)
        # return obj.measurement_unit


class RecipesListSerializers(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    ingredients = IngredientRecipeSerializers(many=True, source='ingredientamount_set')
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
        # depth = 1

    def get_is_favorited(self, obj):
        # import ipdb; ipdb.set_trace() 
        if self.context['request'].user.is_authenticated:
            if Favorite.objects.filter(
                author=self.context['request'].user,
                recipe=Recipe.objects.get(id=obj.id)
            ).exists():
                return True
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            if ShoppingCart.objects.filter(
                author=self.context['request'].user,
                recipe=Recipe.objects.get(id=obj.id)
            ).exists():
                return True
        return False


class CreateRecipeSerializers(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
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
        import ipdb; ipdb.set_trace()
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
            ingredient['id']:ingredient['amount'] 
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
        import ipdb; ipdb.set_trace()
        tags = validated_data.pop('tags')
        ingredients_amount = validated_data.pop('ingredients')
        Recipe.objects.filter(id=update_recipe.id).update(**validated_data)
        update_recipe.refresh_from_db()
        update_recipe.tags.clear()

        for tag in tags:
            update_recipe.tags.add(tag)
        update_recipe.ingredients.clear()
        all_ingredients_amount = {
            ingredient['id']:ingredient['amount'] 
            for ingredient in ingredients_amount
        }

        for ingredient in all_ingredients_amount:
            IngredientAmount.objects.create(
                recipe=update_recipe,
                ingredients=ingredient,
                amount=all_ingredients_amount[ingredient]
            )
        return update_recipe
        pass

    def to_representation(self, instance):
            data = RecipesListSerializers(
                instance,
                context={
                    'request': self.context.get('request')
                }
            ).data
            return data

class FavoriteSerializer(RecipesListSerializers):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )



        