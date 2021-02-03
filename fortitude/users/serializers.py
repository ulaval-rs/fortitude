from django.contrib.auth import password_validation
from rest_framework import serializers

from . import validators
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validators.validate_username])
    password = serializers.CharField(write_only=True, validators=[
        validator.validate for validator in password_validation.get_default_password_validators()
    ])

    class Meta:
        model = User
        fields = ('username', 'password')
