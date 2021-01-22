from django.urls import path

from .views import UserRegistrationAPIView

users_urlpatterns = [
    # url(r'', include('djoser.urls')),
    # url(r'', include('djoser.urls.authtoken')),
    path('create/', UserRegistrationAPIView.as_view(), name='user-create'),
]
