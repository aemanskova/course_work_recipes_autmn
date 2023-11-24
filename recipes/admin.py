from django.contrib import admin
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Ingredient, IngredientAmount, Tag
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportMixin,ExportActionModelAdmin
from import_export import resources, fields,widgets

User = get_user_model()

class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1
    raw_id_fields = ('ingredient', )

class RecipeResource(resources.ModelResource):
 
    recipe_tags =  fields.Field(attribute='tags', column_name='Теги',widget=widgets.ManyToManyWidget(Tag, field='name', separator=' '))
    author = fields.Field(
       attribute="author",
       column_name="Автор",
       widget=widgets.ForeignKeyWidget(User, "username")
   )
   

    class Meta:
        model = Recipe
    
        fields =  ("id","name","description","author","tags","cooking_time","pub_date")
        
        
    

    def dehydrate_cooking_time(self, recipe):
        return f'{recipe.cooking_time} минут(ы)' 
    
    def get_export_headers(self):
        headers = []
        for field in self.get_fields():
            model_fields = self.Meta.model._meta.get_fields()
            header = next((x.verbose_name for x in model_fields if x.name == field.column_name), field.column_name)
            headers.append(header)
        return headers


@admin.register(Recipe)
class RecipeAdmin(ImportExportMixin,ExportActionModelAdmin,SimpleHistoryAdmin,admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'cooking_time',
    )
    list_display_links = (
        'id',
        'name',
        'author',
    )

    list_filter = (
        'author__username',
        'cooking_time',
        'tags__name',
    )
    search_fields = (
        'name',
        'author__username',
        'cooking_time',
        'tags__name',
    )
    filter_horizontal = ("tags",)
    inlines = (IngredientAmountInline,)
    date_hierarchy = 'pub_date'
    raw_id_fields = ('author',)

    resource_class = RecipeResource

    
    def get_export_queryset(self, request):
        return Recipe.objects.all().order_by('id')


@admin.register(Ingredient)
class IngredientAdmin(SimpleHistoryAdmin,admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_display_links = (
        'id',
        'name',
        'measurement_unit',
    )

    list_filter = (
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
        'measurement_unit',
    )


@admin.register(IngredientAmount)
class IngredientAmountAdmin(SimpleHistoryAdmin,admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'recipe',
        'amount',
    )
    list_display_links = (
        'id',
        'ingredient',
        'recipe',
        'amount',
    )

    list_filter = (
        'ingredient__name',
        'recipe__name',
    )
    search_fields = (
        'ingredient__name',
        'recipe__name',
    )
    raw_id_fields = ('ingredient',)


@admin.register(Tag)
class TagAdmin(SimpleHistoryAdmin,admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
    )
    list_display_links = (
        'id',
        'name',
        'color'
    )

    list_filter = (
        'name',
        'color'
    )
    search_fields = (
        'name',
        'color',
    )
