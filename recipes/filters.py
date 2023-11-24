from django_filters import rest_framework as filters
from .models import * 

from  django.db.models import Q

class RecipeFilter(filters.FilterSet):
    min_time = filters.NumberFilter(field_name="cooking_time", lookup_expr='gte',label='Минимальное время готовки')
    max_time = filters.NumberFilter(field_name="cooking_time", lookup_expr='lte',label='Максимальное время готовки')
    
    author = filters.CharFilter(method='filter_author',label='Автор')
    
    class Meta:
        model = Recipe
        fields = ['author','min_time','max_time']

    def filter_author(self, queryset, name, value):
      
        return queryset.filter(Q(author__username=value))