from django.db import models

from fortitude.users.models import User


class OrthancServer(models.Model):
    name = models.CharField(max_length=64, unique=True)

    address = models.CharField(max_length=255, unique=True)

    has_credentials = models.BooleanField(default=False)
    username = models.CharField(max_length=64, default='')
    password = models.CharField(max_length=64, default='')

    is_restricted = models.BooleanField(default=True)
    authorized_users = models.ManyToManyField(User)

    objects = models.Manager()
