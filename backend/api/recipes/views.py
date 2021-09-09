from django.http import request
from django.shortcuts import get_object_or_404, render
from django.views import generic
from djoser.permissions import CurrentUserOrAdmin 
from rest_framework import mixins, serializers, viewsets, generics
from djoser.views import UserViewSet
from djoser.serializers import SetPasswordSerializer
from .serializers import TagSerializers, IngredientSerializers
from .models import Tag, Ingredient
from rest_framework import permissions, status, pagination
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response


class ListRetrievModel(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    pass

class TagViewSet(ListRetrievModel):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializers
    permission_classes = [permissions.AllowAny,]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['name']
    lookup_field = 'id'
    pagination_class = None


class IngredientViewSet(ListRetrievModel):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializers
    permission_classes = [permissions.AllowAny,]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['name']
    lookup_field = 'id'
    pagination_class = None
