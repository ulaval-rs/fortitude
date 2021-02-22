from django.urls import path

from .views import ForwardAPIView, OrthancServersAPIView

urlpatterns = [
    path('orthanc/servers/', OrthancServersAPIView.as_view(), name='orthanc-servers-names'),
    path('orthanc/servers/<str:server_name>/<path:route>', ForwardAPIView.as_view(), name='orthanc-forward-call'),
]
