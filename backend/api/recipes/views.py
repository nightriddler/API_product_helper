from django.http import request
from django.shortcuts import get_object_or_404, render
from django.views import generic
from djoser.permissions import CurrentUserOrAdmin 
from rest_framework import mixins, serializers, viewsets, generics
from djoser.views import UserViewSet
from djoser.serializers import SetPasswordSerializer
from .serializers import TagSerializers, IngredientSerializers, RecipesListSerializers, CreateRecipeSerializers, FavoriteSerializer
from .models import Recipe, Tag, Ingredient, Favorite
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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('name')
    serializer_class = RecipesListSerializers
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['author', 'tags',]
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'head', 'delete']

    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
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
        favorite = Favorite.objects.filter(
            author=request.user,
            recipe=get_object_or_404(Recipe, id=recipe_id)
        )
        if favorite.exists() == False:
            return Response({'error': 'Вы не можете удалить рецепт не добавив его в избранное'}, status=status.HTTP_400_BAD_REQUEST)
        
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
