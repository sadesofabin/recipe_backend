from django.urls import path
from recipe_api.views.recipe_views import (
    RecipeCreateAPIView,
    RecipeListAPIView,
    RecipeDetailAPIView,
    RecipeUpdateAPIView,
    RecipeDeleteAPIView,
)
from .views.auth_views import LoginAPIView, RegisterAPIView
from .views.ollmareq_views import generate_response


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('recipes/', RecipeListAPIView.as_view(), name='recipe-list'),
    path('recipes/create/', RecipeCreateAPIView.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/', RecipeDetailAPIView.as_view(), name='recipe-detail'),
    path('recipes/update/<int:pk>/', RecipeUpdateAPIView.as_view(), name='recipe-update'),
    path('recipes/delete/<int:pk>/', RecipeDeleteAPIView.as_view(), name='recipe-delete'),
    path('generate/', generate_response, name='generate_response'),

]

