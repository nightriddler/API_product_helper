from django.contrib.auth import get_user_model
from recipes.models import Recipe
import django_filters
from .models import Follow

User = get_user_model()

class RecipeCountInFollowFilter(django_filters.FilterSet):
    recipes_limit = django_filters.NumberFilter(
        label='По подписчикам',
        field_name='recipes_limit',
        method='filter_recipes_limit',
    )
    class Meta:
        model = User
        fields = ('recipes_limit',)

    def filter_recipes_limit(self, queryset, name, value):
        import ipdb; ipdb.set_trace()
        if value:
            return Recipe.objects.all()[:value]
        return Recipe.objects.all()