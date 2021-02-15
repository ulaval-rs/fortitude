from audioop import reverse

from rest_framework.test import APITestCase

VALID_PASSWORD = 'A_PASSword-123!'
VALID_USERNAME = 'ValidUser12'


class TestUserAuth(APITestCase):

    def test_user_auth(self, username):
        response = self.client.post(
            reverse('user-auth'),
            {'username': username, 'password': VALID_PASSWORD},
            format='json'
        )

        raise NotImplementedError

