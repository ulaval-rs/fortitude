from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import User

VALID_PASSWORD = 'A_PASSword-123!'
VALID_USERNAME = 'ValidUser12'


class TestUserCreation(APITestCase):

    @parameterized.expand(['user', 'user12', 'a123'])
    def test_create_user(self, username):
        response = self.client.post(
            reverse('user-create'),
            {'username': username, 'password': VALID_PASSWORD},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(User.objects.get(username=username).is_active)


class TestUserCreationErrors(APITestCase):

    @parameterized.expand([
        ('', VALID_PASSWORD, b'{"username":["This field may not be blank."]}'),
        ('aa', VALID_PASSWORD, b'{"username":["Username should have at least 3 characters."]}'),
        ('1234', VALID_PASSWORD, b'{"username":["Username should contains letters."]}'),
        ('user!', VALID_PASSWORD, b'{"username":["Username should not contains a special character."]}'),
        (VALID_USERNAME, '', b'{"password":["This field may not be blank."]}'),
        (VALID_USERNAME, 'a!2', b'{"password":["This password is too short. It must contain at least 8 characters."]}'),
        (VALID_USERNAME, 'password123', b'{"password":["This password is too common."]}'),
    ])
    def test_create_user_with_bad_username_or_password(self, username, password, expected_content):
        response = self.client.post(
            reverse('user-create'),
            {'username': username, 'password': password},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, expected_content)
