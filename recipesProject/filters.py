import django_filters
from recipes.models import Recipe

class RecipeFilter(django_filters.FilterSet):
    class Meta:
        model = Recipe
        fields = {
            'author__username': ['exact'],  # предполагается, что 'author' - это внешний ключ к модели User
        }