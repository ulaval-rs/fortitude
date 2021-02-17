from typing import Dict

from django.db import IntegrityError
from django.test import TestCase
from parameterized import parameterized

from fortitude.orthanc_manager.models import OrthancInstance

NAME = 'NAME'
ADDRESS = 'ADDRESS'
OTHER_NAME = 'OTHER_NAME'
OTHER_ADDRESS = 'OTHER_ADDRESS'


class TestOrthancInstance(TestCase):

    def test_defaults(self):
        orthanc_instance = OrthancInstance.objects.create(name=NAME, address=ADDRESS)

        self.assertEqual(orthanc_instance.name, NAME)
        self.assertEqual(orthanc_instance.address, ADDRESS)
        self.assertFalse(orthanc_instance.has_credentials)
        self.assertEqual(orthanc_instance.username, '')
        self.assertEqual(orthanc_instance.password, '')

    @parameterized.expand([
        (NAME, ADDRESS, NAME, OTHER_ADDRESS),
        (NAME, ADDRESS, OTHER_NAME, ADDRESS),
    ])
    def test_no_duplication(self, name, address, other_name, other_address):
        OrthancInstance.objects.create(name=name, address=address)

        self.assertRaises(
            IntegrityError,
            lambda: OrthancInstance.objects.create(name=other_name, address=other_address)
        )
