from django.db import models


class OrthancServer(models.Model):
    name = models.CharField(max_length=64, unique=True)

    address = models.CharField(max_length=255, unique=True)

    has_credentials = models.BooleanField(default=False)
    username = models.CharField(max_length=64, default='')
    password = models.CharField(max_length=64, default='')
