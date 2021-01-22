
import unittest

from parameterized import parameterized
from rest_framework.exceptions import ValidationError

from fortitude.users import validators


class TestValidateUsername(unittest.TestCase):

    @parameterized.expand([
        ('username',),
        ('user123',),
    ])
    def test_validate_username(self, username):
        validators.validate_username(username)

    @parameterized.expand([
        ('', ValidationError),
        ('aa', ValidationError),
        ('1234', ValidationError),
    ])
    def test_validate_username_errors(self, username, expected):
        self.assertRaises(expected, lambda: validators.validate_username(username))