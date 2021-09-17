import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import (Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)
from .permissions import IsOwnerAuthenticated
from .serializers import (CreateRecipeSerializers, IngredientSerializers,
                          RecipesListSerializers, TagSerializers)


class ListRetrievModel(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


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
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'head', 'delete']

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update' or self.action == 'delete':
            self.permission_classes = [IsOwnerAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwnerAuthenticated]
        elif self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CreateRecipeSerializers
        elif self.action == 'list':
            return RecipesListSerializers
        return self.serializer_class

    @action(
        methods=['get', 'delete'],
        permission_classes=[permissions.IsAuthenticated],
        detail=True)
    def favorite(self, request, id):
        if request.method == 'GET':
            favorite_check = Favorite.objects.filter(
                author=request.user,
                recipe=get_object_or_404(Recipe, id=id))
            if favorite_check.exists() is True:
                return Response(
                    {'error': 'Вы уже добавили этот рецепт в избранное'},
                    status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(
                author=request.user,
                recipe=get_object_or_404(Recipe, id=id))
            recipe = Recipe.objects.get(id=id)
            return Response(
                {
                    'id': str(recipe.id),
                    'name': str(recipe.name),
                    'image': request.build_absolute_uri(recipe.image.url),
                    'cooking_time': str(recipe.cooking_time)
                },
                status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = Favorite.objects.filter(
                author=request.user,
                recipe=get_object_or_404(Recipe, id=id))
            if favorite.exists() is False:
                return Response(
                    {'error':
                        'Вы не можете удалить рецепт не '
                        'добавив его в избранное'},
                    status=status.HTTP_400_BAD_REQUEST)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get', 'delete'],
        permission_classes=[permissions.IsAuthenticated],
        detail=True)
    def shopping_cart(self, request, id):
        if request.method == 'GET':
            shopping_cart_check = ShoppingCart.objects.filter(
                author=request.user,
                recipe=get_object_or_404(Recipe, id=id)
            )
            if shopping_cart_check.exists() is True:
                return Response(
                    {'error': 'Вы уже добавили этот рецепт в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(
                author=request.user,
                recipe=get_object_or_404(Recipe, id=id))
            recipe = Recipe.objects.get(id=id)
            return Response(
                {
                    'id': str(recipe.id),
                    'name': str(recipe.name),
                    'image': request.build_absolute_uri(recipe.image.url),
                    'cooking_time': str(recipe.cooking_time)
                },
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            shopping_cart = ShoppingCart.objects.filter(
                author=request.user,
                recipe=get_object_or_404(Recipe, id=id)
            )
            if shopping_cart.exists() is False:
                return Response(
                    {'error':
                        'Вы не можете удалить рецепт не '
                        'добавив его в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
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
        all_ingredients = dict()
        # Список рецептов юзера с токеном.
        all_shop_list = [recipe for recipe in request.user.shoppings.all()]
        for shop_list in all_shop_list:
            # Словарь ингредиентов для каждого рецепта.
            ingredient_in_recipe = {
                each_ingredient.ingredients.name: [
                    each_ingredient.amount,
                    each_ingredient.ingredients.measurement_unit
                ]
                for each_ingredient in
                shop_list.recipe.ingredientamount_set.all()
            }
            # Добавление ингредиентов в общий словарь.
            for key in ingredient_in_recipe.keys():
                if key in all_ingredients.keys():
                    # Суммирование одинаковых ингредиентов.
                    all_ingredients[key][0] += ingredient_in_recipe[key][0]
                else:
                    all_ingredients[key] = ingredient_in_recipe[key]

        writer = csv.writer(
            response,
            escapechar="'",
            quoting=csv.QUOTE_NONE
        )
        writer.writerow(['Список покупок'])
        writer.writerow([])
        for ingredient in all_ingredients:
            writer.writerow([f'{ingredient} - '
                             f'{all_ingredients[ingredient][0]} '
                             f'{all_ingredients[ingredient][1]}'])
        return response
