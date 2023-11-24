from django.contrib.auth import get_user_model
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from recipes.serializers import RecipeListSerializer, RecipeDetailSerializer
from rest_framework.pagination import PageNumberPagination

from .pagination import BasePagination,IngredientAmountPagination
from rest_framework import viewsets
from .serializers import *
from .filters import *
from .models import *
from rest_framework.decorators import action
from rest_framework.response import Response
User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.prefetch_related("tags").select_related("author").all()
    serializer_class = RecipeSerializer
    pagination_class = BasePagination
    filterset_class = RecipeFilter

    

class IngredientAmountViewSet(viewsets.ModelViewSet):

    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientAmountSerializer
    pagination_class = IngredientAmountPagination
    
    filterset_fields = ['recipe']

   

class IngredientViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = IngredientAmountPagination

    @action(methods=['GET'], detail=False)
    def get_measurement_unit_gr_kg(self, request, **kwargs):
        queryset = self.get_queryset().filter(~Q(measurement_unit='веточка') & ~Q(measurement_unit='щепотка') & ~Q(measurement_unit='зубчик') & (Q(measurement_unit='кг') | Q(measurement_unit='г')))
        serializer = IngredientSerializer(queryset, many=True)
        data = dict()
        data['data'] = serializer.data
        return Response(data)
    
    @action(methods=['GET'], detail=False)
    def get_measurement_unit_abstract(self, request, **kwargs):
        queryset = self.get_queryset().filter(Q(measurement_unit='веточка') | Q(measurement_unit='щепотка') | Q(measurement_unit='зубчик') & (~Q(measurement_unit='кг') | ~Q(measurement_unit='г')))
        serializer = IngredientSerializer(queryset, many=True)
        data = dict()
        data['data'] = serializer.data
        return Response(data)

class FourRecipePagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10 

class RecipeList(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    pagination_class = FourRecipePagination


class RecipeDetail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
