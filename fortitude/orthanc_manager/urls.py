from django.urls import path

from .views import ForwardAPIView

urlpatterns = [
    path('orthanc/<str:route>', ForwardAPIView.as_view(), name='user-create'),
]
