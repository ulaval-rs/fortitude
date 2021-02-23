from unittest import mock

import requests
from django.test import TestCase
from requests.auth import HTTPBasicAuth

from ..errors import OrthancServerDoesNotExistError
from ..models import OrthancServer
from ..services import _get_orthanc_server, forward_call_to_server, get_orthanc_servers_names

SERVER_NAME = 'NAME'
ADDRESS = 'ADDRESS'
OTHER_NAME = 'OTHER_NAME'
OTHER_ADDRESS = 'OTHER_ADDRESS'
ROUTE = 'patients'
USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'
DATA = b'DATA'


class TestForwardCallToServer(TestCase):

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_get_call(self, mock_request):
        OrthancServer.objects.create(name=SERVER_NAME, address=ADDRESS)
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server('GET', SERVER_NAME, ROUTE)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('GET', f'{ADDRESS}/{ROUTE}', data=None)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_get_call_with_credentials(self, mock_request):
        OrthancServer.objects.create(
            name=SERVER_NAME,
            address=ADDRESS,
            has_credentials=True,
            username=USERNAME,
            password=PASSWORD
        )
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server('GET', SERVER_NAME, ROUTE)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('GET', f'{ADDRESS}/{ROUTE}', auth=HTTPBasicAuth(USERNAME, PASSWORD), data=None)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_post_call(self, mock_request):
        self.given_orthanc_server()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server('POST', SERVER_NAME, ROUTE, DATA)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('POST', f'{ADDRESS}/{ROUTE}', data=DATA)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_post_call_with_credentials(self, mock_request):
        self.given_orthanc_server_with_credentials()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server('POST', SERVER_NAME, ROUTE, DATA)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('POST', f'{ADDRESS}/{ROUTE}', auth=HTTPBasicAuth(USERNAME, PASSWORD), data=DATA)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_delete_call(self, mock_request):
        self.given_orthanc_server()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server('DELETE', SERVER_NAME, ROUTE)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('DELETE', f'{ADDRESS}/{ROUTE}', data=None)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_delete_call_with_credentials(self, mock_request):
        self.given_orthanc_server_with_credentials()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server('DELETE', SERVER_NAME, ROUTE)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('DELETE', f'{ADDRESS}/{ROUTE}', auth=HTTPBasicAuth(USERNAME, PASSWORD), data=None)

    def given_orthanc_server(self):
        OrthancServer.objects.create(name=SERVER_NAME, address=ADDRESS)

    def given_orthanc_server_with_credentials(self):
        OrthancServer.objects.create(
            name=SERVER_NAME,
            address=ADDRESS,
            has_credentials=True,
            username=USERNAME,
            password=PASSWORD
        )


class TestGetOrthancServersNames(TestCase):

    def test_get_servers_names(self):
        OrthancServer.objects.create(name=SERVER_NAME, address=ADDRESS)
        OrthancServer.objects.create(name=OTHER_NAME, address=OTHER_ADDRESS)

        result = get_orthanc_servers_names()

        self.assertCountEqual(result, [SERVER_NAME, OTHER_NAME])

    def test_get_servers_names_when_no_server(self):
        result = get_orthanc_servers_names()

        self.assertEqual(result, [])


class TestGetOrthancServer(TestCase):

    def test_get_server(self):
        OrthancServer.objects.create(name=SERVER_NAME, address=ADDRESS)

        result = _get_orthanc_server(SERVER_NAME)

        self.assertIsInstance(result, OrthancServer)
        self.assertEqual(result.name, SERVER_NAME)
        self.assertEqual(result.address, ADDRESS)

    def test_get_non_existing_server(self):
        self.assertRaises(
            OrthancServerDoesNotExistError,
            lambda: _get_orthanc_server(OTHER_NAME)
        )
