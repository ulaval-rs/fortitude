from django.urls import path

from .views import UserRegistrationAPIView

users_urlpatterns = [
    path('user/create/', UserRegistrationAPIView.as_view(), name='user-create'),
]
