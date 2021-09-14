from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Ingredient, Tag, Recipe, IngredientAmount, Favorite
from users.serializers import CustomUserSerializer


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
        # fields = '__all__'
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
        depth = 1

    def get_is_favorited(self, obj):
        # import ipdb; ipdb.set_trace() 
        # check_user = self.context['request'].user.username
        favorite = Favorite.objects.filter(
            author=self.context['request'].user,
            recipe=Recipe.objects.get(id=obj.id)
        )
        if favorite.exists() == False:
            return False
        return True
        # if check_user:
        #     if Follow.objects.filter(
        #         user=self.context['request'].user,
        #         author=obj
        #     ).exists() == True:
        #         return True
        # # if follow_check.exists() == True:
        #     # return True
        # # import ipdb; ipdb.set_trace() 
        # return False
        # return False
    
    def get_is_in_shopping_cart(self, obj):
        return False


class CreateRecipeSerializers(serializers.ModelSerializer):
    # tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # image = 
    tags = TagSerializers
    ingredients = IngredientSerializers

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )
    
    def create(self, validated_data):
        import ipdb; ipdb.set_trace()
        
        user = self.context['request'].user
        ingredients_id = validated_data.pop('ingredients')[0]
        tag_id = validated_data.pop('tags')[0]
        ing = Ingredient.objects.get(id=ingredients_id)
        t = Tag.objects.get(id=tag_id)
        new_recipe = Recipe.objects.create(
        author=user,
        ingredients=ingredients_id,
        tags=tag_id,
        **validated_data
        )


        # new_recipe = Recipe()
        # new_recipe.save()
        
        # new_recipe.tags=tag_id
        # new_recipe.ingredients =ingredients_id
        # new_recipe.author = user
        
        new_recipe.save()
        # tag_id = validated_data[0].pop('tags')
        # ingredients_id = validated_data[0].pop('ingredients')
        
        # valid = **validated_data
        # tag_add = Tag.objects.get_or_create(id=tag_id) 
        # new_recipe = Recipe.objects.create(
        #     author=user,
        #     ingredients=ingredients_id,
        #     tags=tag_id,
        #     **validated_data
        # )
        return new_recipe

class FavoriteSerializer(RecipesListSerializers):

    class Meta:
        model = Recipe
        # fields = '__all__'
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )



        