import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import User

PASSWORD = 'A_PASSword-123!'
USERNAME = 'ValidUser12'
NON_REGISTERED_USERNAME = 'NonRegisteredUser'


class TestUserAuth(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username=USERNAME)
        self.user.set_password(PASSWORD)
        self.user.save()

    def test_active_user_auth(self):
        self.user.is_active = True
        self.user.save()

        response = self.client.post(
            reverse('user-auth'),
            {'username': USERNAME, 'password': PASSWORD},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', json.loads(response.content))

    def test_inactive_user_auth(self):
        response = self.client.post(
            reverse('user-auth'),
            {'username': USERNAME, 'password': PASSWORD},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', json.loads(response.content))

    def test_non_existing_user_auth(self):
        response = self.client.post(
            reverse('user-auth'),
            {'username': NON_REGISTERED_USERNAME, 'password': PASSWORD},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', json.loads(response.content))


