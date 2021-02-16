from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from .views import UserRegistrationAPIView

users_urlpatterns = [
    path('users/create/', UserRegistrationAPIView.as_view(), name='user-create'),
    path('users/login/', ObtainAuthToken.as_view(), name='user-auth'),
]
