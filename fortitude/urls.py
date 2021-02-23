from django.contrib import admin
from django.urls import path

from fortitude.users.urls import users_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += users_urlpatterns
