from django.urls import path
from recipe_api.views.recipe_views import (
    UpdateUserDetailsAPIView, UserProfileView
)
from .views.auth_views import LoginAPIView, RegisterAPIView
from .views.ollmareq_views import generate_response
from .views.saved_recipe_views import SavedRecipeView

SavedRecipeView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('update-user-details/', UpdateUserDetailsAPIView.as_view(), name='update-user-details'),
    path('user/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('generate/', generate_response, name='generate_response'),
    path('saved_recipes/', SavedRecipeView.as_view(), name='saved_recipe_list'), 
    path('saved_recipes/<int:pk>/', SavedRecipeView.as_view(), name='saved_recipe_detail'),
    path('api/saved_recipes/<int:user_id>/', SavedRecipeView.as_view(), name='saved_recipe_list_by_user'),

]

