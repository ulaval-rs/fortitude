from unittest import mock

import requests
from django.test import TestCase
from requests.auth import HTTPBasicAuth

from ..errors import OrthancServerDoesNotExistError, UnAuthorizedError
from ..models import OrthancServer
from ..services import _get_orthanc_server, forward_call_to_server, get_orthanc_servers_names
from ...users.models import User

SERVER_NAME = 'NAME'
ADDRESS = 'ADDRESS'
OTHER_NAME = 'OTHER_NAME'
OTHER_ADDRESS = 'OTHER_ADDRESS'
ROUTE = 'patients'
USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'
DATA = b'DATA'


class TestForwardCallToServer(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username=USERNAME, password=PASSWORD)
        self.user.is_active = True
        self.user.save()

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_get_call(self, mock_request):
        self.given_orthanc_server()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server(self.user, 'GET', SERVER_NAME, ROUTE)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('GET', f'{ADDRESS}/{ROUTE}', data=None)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_get_call_with_credentials(self, mock_request):
        self.given_orthanc_server_with_credentials()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server(self.user, 'GET', SERVER_NAME, ROUTE)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('GET', f'{ADDRESS}/{ROUTE}', auth=HTTPBasicAuth(USERNAME, PASSWORD), data=None)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_post_call(self, mock_request):
        self.given_orthanc_server()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server(self.user, 'POST', SERVER_NAME, ROUTE, DATA)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('POST', f'{ADDRESS}/{ROUTE}', data=DATA)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_post_call_with_credentials(self, mock_request):
        self.given_orthanc_server_with_credentials()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server(self.user, 'POST', SERVER_NAME, ROUTE, DATA)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('POST', f'{ADDRESS}/{ROUTE}', auth=HTTPBasicAuth(USERNAME, PASSWORD), data=DATA)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_delete_call(self, mock_request):
        self.given_orthanc_server()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server(self.user, 'DELETE', SERVER_NAME, ROUTE)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('DELETE', f'{ADDRESS}/{ROUTE}', data=None)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_delete_call_with_credentials(self, mock_request):
        self.given_orthanc_server_with_credentials()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server(self.user, 'DELETE', SERVER_NAME, ROUTE)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('DELETE', f'{ADDRESS}/{ROUTE}', auth=HTTPBasicAuth(USERNAME, PASSWORD), data=None)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_put_call(self, mock_request):
        self.given_orthanc_server()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server(self.user, 'PUT', SERVER_NAME, ROUTE, DATA)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('PUT', f'{ADDRESS}/{ROUTE}', data=DATA)

    @mock.patch('fortitude.orthanc_manager.services.requests.request')
    def test_put_call_with_credentials(self, mock_request):
        self.given_orthanc_server_with_credentials()
        response = requests.Response()
        mock_request.return_value = response

        result = forward_call_to_server(self.user, 'PUT', SERVER_NAME, ROUTE, DATA)

        self.assertIsInstance(result, requests.Response)
        mock_request.assert_called_with('PUT', f'{ADDRESS}/{ROUTE}', auth=HTTPBasicAuth(USERNAME, PASSWORD), data=DATA)

    def given_orthanc_server(self):
        OrthancServer.objects.create(name=SERVER_NAME, address=ADDRESS, is_restricted=False)

    def given_orthanc_server_with_credentials(self):
        OrthancServer.objects.create(
            name=SERVER_NAME,
            address=ADDRESS,
            has_credentials=True,
            username=USERNAME,
            password=PASSWORD,
            is_restricted = False
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

    def setUp(self) -> None:
        self.server = OrthancServer.objects.create(name=SERVER_NAME, address=ADDRESS)
        self.user = User.objects.create_user(USERNAME, PASSWORD)

    def test_get_server_with_authorized_user(self):
        self.server.authorized_users.add(self.user)

        result = _get_orthanc_server(self.server.name, self.user)

        self.assertIsInstance(result, OrthancServer)
        self.assertEqual(result.name, SERVER_NAME)
        self.assertEqual(result.address, ADDRESS)

    def test_get_server_with_unauthorized_user_when_server_is_not_restricted(self):
        self.server.is_restricted = False
        self.server.save()

        result = _get_orthanc_server(self.server.name, self.user)

        self.assertIsInstance(result, OrthancServer)
        self.assertEqual(result.name, SERVER_NAME)
        self.assertEqual(result.address, ADDRESS)

    def test_get_server_with_unauthorized_user(self):
        self.assertRaises(
            UnAuthorizedError,
            lambda: _get_orthanc_server(self.server.name, self.user)
        )

    def test_get_non_existing_server(self):
        self.assertRaises(
            OrthancServerDoesNotExistError,
            lambda: _get_orthanc_server(OTHER_NAME, self.user)
        )
