from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)


urlpatterns = [
    path('recipes/download_shopping_cart/', views.download_shopping_cart),
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/favorite/', views.favorite),
    path('recipes/<int:recipe_id>/shopping_cart/', views.shopping_cart),
]
