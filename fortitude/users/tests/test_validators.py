import unittest

from parameterized import parameterized
from rest_framework.exceptions import ValidationError

from .. import validators


class TestValidateUsername(unittest.TestCase):

    @parameterized.expand(['username', 'user123'])
    def test_validate_username(self, username):
        validators.validate_username(username)

    @parameterized.expand(['', 'aa', '1234', 'user!'])
    def test_validate_username_errors(self, username):
        self.assertRaises(ValidationError, lambda: validators.validate_username(username))
