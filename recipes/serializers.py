from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework.validators import ValidationError

from .models import Recipe,Ingredient,IngredientAmount,Tag


User = get_user_model()


class RecipeSerializer(serializers.ModelSerializer):
    
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(),many=True,slug_field='name')
    author = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username')
   

  

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "description",
            "author",
            "tags",
            "cooking_time",
            "pub_date",

        )
    
    def validate_description(self,description):
        if len(description) < 10:
            raise ValidationError('Минимальная длина описания 10 символов')
        return description
    def validate_tags(self,tags):
        if len(tags) < 1:
            raise ValidationError('Для рецепта нужен минимум 1 тег!')
        return tags
    def validate_cooking_time(self, cooking_time):
        if cooking_time < 5:
            raise ValidationError('Минимальное время приготовления 5 минут!')
        return cooking_time

class IngredientAmountSerializer(serializers.ModelSerializer):

    ingredient = serializers.SlugRelatedField(queryset=Ingredient.objects.all(),slug_field='name')

    recipe = serializers.SlugRelatedField(queryset=Recipe.objects.all(),slug_field='name')

    

    class Meta:
        model = IngredientAmount
        fields = (
            "id",
            "ingredient",
            "recipe",
            "amount",
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )

class RecipeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "description",
            "cooking_time",
            "pub_date",
        )


class RecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "description",
            "author",
            "cooking_time",
            "pub_date",

        )
