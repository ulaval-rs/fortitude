from django.urls import path

from .views import ForwardAPIView, OrthancServersAPIView, OrthancServerInformation

urlpatterns = [
    path('orthanc/servers/', OrthancServersAPIView.as_view(), name='orthanc-servers-names'),
    path('orthanc/servers/<str:server_name>/', OrthancServerInformation.as_view(), name='orthanc-server-info'),
    path('orthanc/servers/<str:server_name>/<path:route>', ForwardAPIView.as_view(), name='orthanc-forward-call'),
]
