from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Ingredient, Tag


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializers(serializers.ModelSerializer):
    # amount = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
    
    # def get_amount(self, obj):
    #     return False
