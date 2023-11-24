from django.urls import path

from recipes.views import RecipeDetail, RecipeList

app_name = "recipes"

urlpatterns = [
    path("", RecipeList.as_view()),
    path("<int:pk>/", RecipeDetail.as_view()),
]
