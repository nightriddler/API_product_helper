from re import S
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from djoser.conf import settings



User = get_user_model()


class CustomUserSerializer(UserSerializer):
    # pass
    # first_name = serializers.CharField(required=True)
    class Meta():
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',  'id') 


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)
    email = serializers.EmailField(allow_blank=False)

    class Meta():
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password') 


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.CharField(allow_blank=True, default='default')
    is_subscribed = serializers.BooleanField(default=True)
    recipes_count = serializers.IntegerField(default='0')

    class Meta():
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',  'id', 'recipes', 'is_subscribed', 'recipes_count') 

