import json

from django.contrib.auth.models import User
from django.urls import reverse, path, include
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase


def make_data(username='username', password='lasdju2312!'):
    return {'username': username, 'password': password}


class TestCreateUser(APITestCase):

    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser('superuser', 'super@user.com', 'superuser_password')
        self.client.login(username='superuser', password='superuser_password')

    @parameterized.expand([
        (reverse('user-create'), make_data(), status.HTTP_201_CREATED),
    ])
    def test_create_user(self, url, data, expected_status):
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, expected_status)


class TestUserCreationErrors(APITestCase):
    @parameterized.expand([
        (
                reverse('user-create'),
                make_data(username=''),
                status.HTTP_400_BAD_REQUEST,
                b'{"username":["This field may not be blank."]}'
        ),
        (
                reverse('user-create'),
                make_data(username='aa'),
                status.HTTP_400_BAD_REQUEST,
                b'{"username":["Username should have at least 3 characters."]}'
        ),
        (
                reverse('user-create'),
                make_data(username='1234'),
                status.HTTP_400_BAD_REQUEST,
                b'{"username":["Username should contains letters."]}'
        )
    ])
    def test_create_user(self, url, data, expected_status, expected_content):
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(response.content, expected_content)
