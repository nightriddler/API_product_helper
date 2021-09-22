import csv

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .mixins import ListRetrievModel
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from .permissions import IsOwnerAuthenticated
from .serializers import (CreateRecipeSerializers, IngredientSerializers,
                          RecipesListSerializers, TagSerializers)


class TagViewSet(ListRetrievModel):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializers
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'
    pagination_class = None


class IngredientViewSet(ListRetrievModel):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializers
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, rest_filters.SearchFilter]
    filterset_fields = ['name', 'measurement_unit']
    search_fields = ('^name')
    lookup_field = 'id'
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = RecipesListSerializers
    permission_classes = [IsOwnerAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'head', 'delete']

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CreateRecipeSerializers
        elif self.action == 'list':
            return RecipesListSerializers
        return self.serializer_class

    @action(
        methods=['GET', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated],
        detail=True)
    def favorite(self, request, id):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, id=id)
            favorite_check = Favorite.objects.filter(
                author=request.user,
                recipe=recipe)
            if favorite_check.exists():
                return Response(
                    {'error': 'Вы уже добавили этот рецепт в избранное'},
                    status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(
                author=request.user,
                recipe=recipe)
            return Response(
                {
                    'id': str(recipe.id),
                    'name': str(recipe.name),
                    'image': request.build_absolute_uri(recipe.image.url),
                    'cooking_time': str(recipe.cooking_time)
                },
                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=id)
            favorite = Favorite.objects.filter(
                author=request.user,
                recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error':
                    'Вы не можете удалить рецепт не '
                    'добавив его в избранное'},
                status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated],
        detail=True)
    def shopping_cart(self, request, id):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, id=id)
            shopping_cart_check = ShoppingCart.objects.filter(
                author=request.user,
                recipe=recipe)
            if shopping_cart_check.exists():
                return Response(
                    {'error': 'Вы уже добавили этот рецепт в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(
                author=request.user,
                recipe=recipe)
            return Response(
                {
                    'id': str(recipe.id),
                    'name': str(recipe.name),
                    'image': request.build_absolute_uri(recipe.image.url),
                    'cooking_time': str(recipe.cooking_time)
                },
                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=id)
            shopping_cart = ShoppingCart.objects.filter(
                author=request.user,
                recipe=recipe)
            if shopping_cart.exists():
                shopping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error':
                    'Вы не можете удалить рецепт не '
                    'добавив его в список покупок'},
                status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated],
        detail=False)
    def download_shopping_cart(self, request):
        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition':
                'attachment; filename="Shopping List.csv"'
            },
        )
        all_ingredients_amount = IngredientAmount.objects.filter(
            recipe__shoppings__author=request.user).values_list(
                'ingredients__name', 'amount', 'ingredients__measurement_unit')
        sum_amount_ingredient = all_ingredients_amount.values(
            'ingredients__name', 'ingredients__measurement_unit').annotate(
                total=Sum('amount')).order_by('-total')
        writer = csv.writer(
            response,
            escapechar="'",
            quoting=csv.QUOTE_NONE
        )
        writer.writerow(['Список покупок'])
        writer.writerow([])
        for ingredient in sum_amount_ingredient:
            writer.writerow(
                [f'{ingredient["ingredients__name"]} - '
                 f'{ingredient["total"]} '
                 f'{ingredient["ingredients__measurement_unit"]}']
            )
        return response
