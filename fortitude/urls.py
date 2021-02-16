from django.contrib import admin
from django.urls import path

from .users.urls import urlpatterns as users_urlpatterns
from .orthanc_manager.urls import urlpatterns as orthanc_manager_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += users_urlpatterns
urlpatterns += orthanc_manager_urlpatterns
