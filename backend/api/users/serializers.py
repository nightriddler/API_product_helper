from re import S
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from djoser.conf import settings
from .models import Follow


User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    class Meta():
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',  'id', 'is_subscribed')
    
    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            if Follow.objects.filter(
                user=self.context['request'].user,
                author=obj
            ).exists():
                return True
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)
    email = serializers.EmailField(allow_blank=False)

    class Meta():
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password') 


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.CharField(allow_blank=True, default='default')
    recipes_count = serializers.IntegerField(default='0')

    class Meta():
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',  'id', 'recipes', 'is_subscribed', 'recipes_count') 
