from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import routers
from recipes.views import *
from users.views import UsersViewSet
router = routers.DefaultRouter()

router.register(r'recipes',RecipeViewSet)
router.register(r'ingredientamounts',IngredientAmountViewSet)
router.register(r'ingredients',IngredientViewSet)
router.register(r'users',UsersViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Recipes project API",
        default_version="v1",
        description="Recipes project APO",
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
)

urlpatterns = [

     path('api/v1/',include(router.urls)),



    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include(("users.urls", "users"), namespace="users")),
    path("recipes/", include(("recipes.urls", "recipes"), namespace="recipes")),
    path("news/", include(("news.urls", "news"), namespace="news")),
   
]
