from django.contrib.auth.models import User
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

VALID_PASSWORD = 'A_PASSword-123!'
VALID_USERNAME = 'aValidUsername12'


class TestCreateUser(APITestCase):

    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser('superuser', 'super@user.com', 'superuser_password')
        self.client.login(username='superuser', password='superuser_password')

    @parameterized.expand(['user', 'user12', 'a123'])
    def test_create_user(self, username):
        response = self.client.post(
            reverse('user-create'),
            {'username': username, 'password': VALID_PASSWORD},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestUserCreationErrors(APITestCase):
    @parameterized.expand([
        ('', b'{"username":["This field may not be blank."]}'),
        ('aa', b'{"username":["Username should have at least 3 characters."]}'),
        ('1234', b'{"username":["Username should contains letters."]}'),
        ('user!', b'{"username":["Username should not contains a special character."]}'),
    ])
    def test_create_user_with_bad_username(self, username, expected_content):
        response = self.client.post(
            reverse('user-create'),
            {'username': username, 'password': VALID_PASSWORD},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, expected_content)
