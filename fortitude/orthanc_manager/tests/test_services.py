from django.test import TestCase

from ..models import OrthancInstance
from ..services import get_orthanc_instance, get_orthanc_instances_names

NAME = 'NAME'
ADDRESS = 'ADDRESS'
OTHER_NAME = 'OTHER_NAME'
OTHER_ADDRESS = 'OTHER_ADDRESS'


class TestGetOrthancInstancesNames(TestCase):

    def test_get_instance_names(self):
        OrthancInstance.objects.create(name=NAME, address=ADDRESS)
        OrthancInstance.objects.create(name=OTHER_NAME, address=OTHER_ADDRESS)

        result = get_orthanc_instances_names()

        self.assertCountEqual(result, [NAME, OTHER_NAME])

    def test_get_instances_names_when_no_instance(self):
        result = get_orthanc_instances_names()

        self.assertEqual(result, [])


class TestGetOrthancInstance(TestCase):

    def test_getting_instance(self):
        OrthancInstance.objects.create(name=NAME, address=ADDRESS)

        result = get_orthanc_instance(NAME)

        self.assertIsInstance(result, OrthancInstance)
        self.assertEqual(result.name, NAME)
        self.assertEqual(result.address, ADDRESS)

    def test_getting_non_existing_instance(self):
        result = get_orthanc_instance(OTHER_NAME)

        self.assertIsNone(result)
