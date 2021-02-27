from django.db import IntegrityError
from django.test import TestCase
from parameterized import parameterized

from ..models import OrthancServer

NAME = 'NAME'
ADDRESS = 'ADDRESS'
OTHER_NAME = 'OTHER_NAME'
OTHER_ADDRESS = 'OTHER_ADDRESS'


class TestOrthancServer(TestCase):

    def test_defaults(self):
        server = OrthancServer.objects.create(name=NAME, address=ADDRESS)

        self.assertEqual(server.name, NAME)
        self.assertEqual(server.address, ADDRESS)
        self.assertFalse(server.has_credentials)
        self.assertEqual(server.username, '')
        self.assertEqual(server.password, '')
        self.assertTrue(server.is_restricted)

    @parameterized.expand([
        (NAME, ADDRESS, NAME, OTHER_ADDRESS),
        (NAME, ADDRESS, OTHER_NAME, ADDRESS),
    ])
    def test_no_duplication(self, name, address, other_name, other_address):
        OrthancServer.objects.create(name=name, address=address)

        self.assertRaises(
            IntegrityError,
            lambda: OrthancServer.objects.create(name=other_name, address=other_address)
        )
