from django.urls import path, re_path

from .views import ForwardAPIView, OrthancInstancesAPIView

urlpatterns = [
    path('orthanc/instances/', OrthancInstancesAPIView.as_view(), name='orthanc-list-instances'),
    path('orthanc/instances/<str:instance_name>/<path:route>', ForwardAPIView.as_view(), name='orthanc-forward-call'),
]
