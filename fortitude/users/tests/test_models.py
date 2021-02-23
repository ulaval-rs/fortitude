from django.test import TestCase

from ..models import User

USERNAME = 'ValidUser12'
PASSWORD = 'A_PASSword-123!'


class TestUser(TestCase):

    def test_user(self):
        user = User.objects.create_user(USERNAME, PASSWORD)

        self.assertEqual(user.username, USERNAME)
        self.assertEqual(str(user), USERNAME)
        self.assertNotEqual(user.password, PASSWORD)  # Assert that the password is hashed

        self.assertFalse(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_superuser)

    def test_superuser(self):
        user = User.objects.create_superuser(USERNAME, PASSWORD)

        self.assertEqual(user.username, USERNAME)
        self.assertEqual(str(user), USERNAME)
        self.assertNotEqual(user.password, PASSWORD)  # Assert that the password is hashed

        self.assertTrue(user.is_active)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_superuser)
