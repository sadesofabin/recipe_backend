from django.urls import path
from recipe_api.views.recipe_views import (
    UpdateUserDetailsAPIView, UserDetailsView
)
from .views.auth_views import LoginAPIView, RegisterAPIView
from .views.ollmareq_views import generate_response


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('update-user-details/', UpdateUserDetailsAPIView.as_view(), name='update-user-details'),
    path('user-details/<int:user_id>/', UserDetailsView.as_view(), name='user-details-detail'),
    path('generate/', generate_response, name='generate_response'),

]

