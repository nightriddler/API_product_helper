from django.db.models import Sum, Count
from django.http import request
from django.shortcuts import get_object_or_404, render
from django.views import generic
from djoser.permissions import CurrentUserOrAdmin 
from rest_framework import mixins, serializers, viewsets, generics
from djoser.views import UserViewSet
from djoser.serializers import SetPasswordSerializer
from .serializers import TagSerializers, IngredientSerializers, RecipesListSerializers, CreateRecipeSerializers, FavoriteSerializer
from .models import IngredientAmount, Recipe, Tag, Ingredient, Favorite, ShoppingCart
from rest_framework import permissions, status, pagination
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
import csv
from django.http import HttpResponse


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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('id')
    serializer_class = RecipesListSerializers
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['author', 'tags',]
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'head', 'delete']

    
    def get_permissions(self):
        if self.action == 'create' or self.action == 'update':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CreateRecipeSerializers
        elif self.action == 'list':
            return RecipesListSerializers
        return self.serializer_class


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def favorite(request, recipe_id):
    if request.method == 'GET':
        favorite_check = Favorite.objects.filter(
            author=request.user,
            recipe=get_object_or_404(Recipe, id=recipe_id)
        )
        if favorite_check.exists() == True:
            return Response({'error': 'Вы уже добавили этот рецепт в избранное'}, status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(
            author=request.user,
            recipe=get_object_or_404(Recipe, id=recipe_id)
        )
        recipe = Recipe.objects.get(id=recipe_id)
        return Response(
            {
                'id': str(recipe.id),
                'name': str(recipe.name),
                # Перепроверить путь после правки модели IMAGE.
                'image': request.build_absolute_uri(recipe.image.url),
                'cooking_time': str(recipe.cooking_time)
            },
            status=status.HTTP_201_CREATED
        )
    if request.method == 'DELETE':
        favorite = Favorite.objects.filter(
            author=request.user,
            recipe=get_object_or_404(Recipe, id=recipe_id)
        )
        if favorite.exists() == False:
            return Response({'error': 'Вы не можете удалить рецепт не добавив его в избранное'}, status=status.HTTP_400_BAD_REQUEST)
        
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def shopping_cart(request, recipe_id):
    if request.method == 'GET':
        shopping_cart_check = ShoppingCart.objects.filter(
            author=request.user,
            recipe=get_object_or_404(Recipe, id=recipe_id)
        )
        if shopping_cart_check.exists() == True:
            return Response({'error': 'Вы уже добавили этот рецепт в список покупок'}, status=status.HTTP_400_BAD_REQUEST)
        ShoppingCart.objects.create(
            author=request.user,
            recipe=get_object_or_404(Recipe, id=recipe_id)
        )
        # import ipdb; ipdb.set_trace()
        recipe = Recipe.objects.get(id=recipe_id)
        return Response(
            {
                'id': str(recipe.id),
                'name': str(recipe.name),
                # Перепроверить путь после правки модели IMAGE.
                'image': request.build_absolute_uri(recipe.image.url),
                'cooking_time': str(recipe.cooking_time)
            },
            status=status.HTTP_201_CREATED
        )
    if request.method == 'DELETE':
        shopping_cart = ShoppingCart.objects.filter(
            author=request.user,
            recipe=get_object_or_404(Recipe, id=recipe_id)
        )
        if shopping_cart.exists() == False:
            return Response({'error': 'Вы не можете удалить рецепт не добавив его в список покупок'}, status=status.HTTP_400_BAD_REQUEST)
        
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_shopping_cart(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="Shopping List.csv"'},
    )
    # import ipdb; ipdb.set_trace()
    all_ingredients = dict()
    # Список рецептов юзера с токеном
    all_shop_list = [recipe for recipe in request.user.shoppings.all()]
    for shop_list in all_shop_list:
        # Словарь ингредиентов для каждого рецепта 
        ingredient_in_recipe={
            each_ingredient.ingredients.name: [
                each_ingredient.amount,
                each_ingredient.ingredients.measurement_unit
            ]
            for each_ingredient in shop_list.recipe.ingredientamount_set.all()
        }
        # Добавление ингредиентов в общий словарь.
        for key in ingredient_in_recipe.keys():
            if key in all_ingredients.keys():
                # Суммирование одинаковых ингредиентов
                all_ingredients[key][0] += ingredient_in_recipe[key][0]
            else:
                all_ingredients[key] = ingredient_in_recipe[key]

    # Список ингредиентов для каждого рецепта этого автора
    # all_ingredients_reciepes_user = [shop_cart.recipe.ingredientamount_set.all() for shop_cart in list_shopping_cart]
    # или так (список с кверисетами ингредиентов каждого рецепта автора)
    # all_ingredients_user = [shop_cart.recipe.ingredientamount_set.all() for shop_cart in request.user.shoppings.all()]
    # Объединяем все кверисеты в один список
    # from itertools import chain
    # result_list = list(chain(**all_ingredients_user))
    # Сумма количества ингредиентов без привязки к рецепту
    # IngredientAmount.objects.values('ingredients').annotate(sum=Sum('amount'))
    # Сумма количества ингредиентов с привязкой к рецепту
    # i = IngredientAmount.objects.values('ingredients').annotate(sum=Sum('amount')).filter(recipe=list_shopping_cart[0].recipe)
    # all =  IngredientAmount.objects.values('amount').order_by('-count').annotate(count=Count('amount'))    

    writer = csv.writer(
        response,
        escapechar="'",
        quoting=csv.QUOTE_NONE
    )
    writer.writerow(['Список покупок'])
    writer.writerow([])
    for ingredient in all_ingredients:
        writer.writerow([f'{ingredient} - {all_ingredients[ingredient][0]} {all_ingredients[ingredient][1]}'])
        # writer.writerow([ingredient, all_ingredients[ingredient][0], all_ingredients[ingredient][1]])

    return response
