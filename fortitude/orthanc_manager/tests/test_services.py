from unittest import mock

import requests
from django.test import TestCase
from requests.auth import HTTPBasicAuth

from ..models import OrthancInstance
from ..services import _get_orthanc_instance, get_orthanc_instances_names, forward_get_call_to_instance

NAME = 'NAME'
ADDRESS = 'ADDRESS'
OTHER_NAME = 'OTHER_NAME'
OTHER_ADDRESS = 'OTHER_ADDRESS'
ROUTE = 'patients'
USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'


class TestForwardGetCallToInstance(TestCase):

    @mock.patch('fortitude.orthanc_manager.services.requests.get')
    def test_forward_get_call_to_instance(self, mock_get):
        OrthancInstance.objects.create(name=NAME, address=ADDRESS)
        response = requests.Response()
        mock_get.return_value = response

        result = forward_get_call_to_instance(NAME, ROUTE)

        self.assertIsInstance(result, requests.Response)
        mock_get.assert_called_with(f'{ADDRESS}/{ROUTE}')

    @mock.patch('fortitude.orthanc_manager.services.requests.get')
    def test_forward_get_call_to_instance_with_credentials(self, mock_get):
        OrthancInstance.objects.create(
            name=NAME,
            address=ADDRESS,
            has_credentials=True,
            username=USERNAME,
            password=PASSWORD
        )
        response = requests.Response()
        mock_get.return_value = response

        result = forward_get_call_to_instance(NAME, ROUTE)

        self.assertIsInstance(result, requests.Response)
        mock_get.assert_called_with(f'{ADDRESS}/{ROUTE}', auth=HTTPBasicAuth(USERNAME, PASSWORD))


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

    def test_get_instance(self):
        OrthancInstance.objects.create(name=NAME, address=ADDRESS)

        result = _get_orthanc_instance(NAME)

        self.assertIsInstance(result, OrthancInstance)
        self.assertEqual(result.name, NAME)
        self.assertEqual(result.address, ADDRESS)

    def test_get_non_existing_instance(self):
        result = _get_orthanc_instance(OTHER_NAME)

        self.assertIsNone(result)
