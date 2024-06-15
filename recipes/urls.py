from django.urls import path

from recipes.views import RecipeDetail, RecipeList

app_name = "recipes"

urlpatterns = [
    path("", RecipeList.as_view(), name="recipe-list"),
    path("<int:pk>/", RecipeDetail.as_view(), name="recipe-detail"),
]
