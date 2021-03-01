import json

from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import OrthancServer

NAME = 'NAME'
ADDRESS = 'ADDRESS'

SERVER_EXISTS = True
SERVER_DOES_NOT_EXIST = not SERVER_EXISTS

IS_RESTRICTED = True
IS_NOT_RESTRICTED = not IS_RESTRICTED


class TestGetOrthancServerInformation(APITestCase):

    @parameterized.expand([
        (IS_NOT_RESTRICTED, SERVER_EXISTS, bytes(f'{{"name":"{NAME}","address":"{ADDRESS}"}}', 'utf8'), status.HTTP_200_OK),
        (IS_RESTRICTED, SERVER_EXISTS, bytes(f'"Unauthorized access to the DICOM server"', 'utf8'), status.HTTP_401_UNAUTHORIZED),
        (IS_NOT_RESTRICTED, SERVER_DOES_NOT_EXIST, bytes(f'"Server {NAME} does not exist."', 'utf8'), status.HTTP_404_NOT_FOUND)
    ])
    def test_get_server_information(self, with_restricted_server, with_existing_server, expected_content, expected_status):
        if with_existing_server:
            self.given_server(with_restricted_server)

        response = self.client.get(
            reverse('orthanc-server-info', kwargs={'server_name': NAME}),
            format='json'
        )

        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(response.content, expected_content)

    def given_server(self, with_restricted_server: bool) -> None:
        server = OrthancServer(name=NAME, address=ADDRESS, is_restricted=with_restricted_server)
        server.save()
