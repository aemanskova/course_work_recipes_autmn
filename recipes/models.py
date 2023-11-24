from django.contrib.auth import get_user_model
from django.db import models
from simple_history.models import HistoricalRecords 


User = get_user_model()


class Recipe(models.Model):
    name = models.CharField(max_length=512,
                            verbose_name='Название',
                            help_text='Максимум 512 символов')
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    ingredients = models.ManyToManyField('Ingredient',
                                         through='IngredientAmount',
                                         related_name='recipes',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField('Tag', related_name='recipes',

                                  verbose_name='Теги')
    cooking_time = models.PositiveIntegerField(verbose_name='Время приготовления',
                                               help_text='В минутах')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    null=True,
                                    verbose_name='Дата публикации',
                                    help_text='Дата публикации формируется автоматически'
                                    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единица измерения')

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredient_amounts',
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredient_amounts',
                               verbose_name='Рецепт')
    amount = models.PositiveIntegerField(verbose_name='Количество')

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'


class Tag(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название')
    color = models.CharField(max_length=200,
                             verbose_name='Цвет')

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
