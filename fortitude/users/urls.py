from django.urls import path

from .views import UserRegistrationAPIView

users_urlpatterns = [
    path('users/create/', UserRegistrationAPIView.as_view(), name='user-create'),
]
