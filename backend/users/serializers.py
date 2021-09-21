from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from recipes.models import Recipe
from users.models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta():
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'id',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            return Follow.objects.filter(
                user=self.context['request'].user,
                author=obj
            ).exists()
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)
    email = serializers.EmailField(allow_blank=False)

    class Meta():
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class RecipesSubscribeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta():
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        queryset = obj.recipes.all()
        if self.context['request'].query_params.get('recipes_limit'):
            count_recipe = self.context[
                'request'].query_params['recipes_limit']
            queryset = obj.recipes.all()[:int(count_recipe)]
        serializer = RecipesSubscribeSerializers(queryset, many=True)
        return serializer.data
