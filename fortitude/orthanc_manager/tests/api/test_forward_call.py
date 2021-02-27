import json

from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from fortitude.users.models import User
from .util import make_bad_dicom_data, make_dicom_data
from ...models import OrthancServer

NAME = 'NAME'
ADDRESS = 'http://localhost:8042'
USERNAME = 'orthanc'
PASSWORD = 'orthanc'

IS_AUTHENTICATED = True
IS_NOT_AUTHENTICATED = not IS_AUTHENTICATED

IS_IN_AUTHORIZED_USERS = True
IS_NOT_IN_AUTHORIZED_USERS = not IS_IN_AUTHORIZED_USERS

IS_RESTRICTED_SERVER = True
IS_NOT_RESTRICTED_SERVER = not IS_RESTRICTED_SERVER


class TestForwardCall(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('USERNAME', 'PASSWORD')

    @parameterized.expand([
        ('patients/', IS_AUTHENTICATED, IS_IN_AUTHORIZED_USERS, IS_RESTRICTED_SERVER, status.HTTP_200_OK),
        ('studies/', IS_AUTHENTICATED, IS_IN_AUTHORIZED_USERS, IS_RESTRICTED_SERVER, status.HTTP_200_OK),
        ('series/', IS_AUTHENTICATED, IS_IN_AUTHORIZED_USERS, IS_RESTRICTED_SERVER, status.HTTP_200_OK),
        ('instances/', IS_AUTHENTICATED, IS_IN_AUTHORIZED_USERS, IS_RESTRICTED_SERVER, status.HTTP_200_OK),
        ('modalities/', IS_AUTHENTICATED, IS_IN_AUTHORIZED_USERS, IS_RESTRICTED_SERVER, status.HTTP_200_OK),

        ('patients/', IS_NOT_AUTHENTICATED, IS_IN_AUTHORIZED_USERS, IS_RESTRICTED_SERVER, status.HTTP_401_UNAUTHORIZED),
        ('patients/', IS_AUTHENTICATED, IS_NOT_IN_AUTHORIZED_USERS, IS_RESTRICTED_SERVER, status.HTTP_401_UNAUTHORIZED),
        ('patients/', IS_AUTHENTICATED, IS_NOT_IN_AUTHORIZED_USERS, IS_NOT_RESTRICTED_SERVER, status.HTTP_200_OK),
        ('bad_route/', IS_AUTHENTICATED, IS_IN_AUTHORIZED_USERS, IS_RESTRICTED_SERVER, status.HTTP_404_NOT_FOUND),
    ])
    def test_forward_get_call(self, route, with_authenticated_user, with_authorized_user, with_restricted_server, expected_status):
        self.setup_server_and_user(with_authenticated_user, with_authorized_user, with_restricted_server,)

        response = self.client.get(
            reverse('orthanc-forward-call', kwargs={'server_name': NAME, 'route': route}),
            format='json'
        )

        self.assertEqual(response.status_code, expected_status)

    @parameterized.expand([
        ('instances/', make_dicom_data(), status.HTTP_200_OK),
        ('instances/', make_bad_dicom_data(), status.HTTP_400_BAD_REQUEST),
        ('bad_route/', make_dicom_data(), status.HTTP_404_NOT_FOUND),
    ])
    def test_forward_post_call_with_binary_data(self, route, dicom_data, expected_status):
        self.setup_server_and_user(with_authenticated_user=True, with_authorized_user=True, with_restricted_server=True)

        # The standard self.client.post force data serialization as json or a multipart message
        response = self.client.generic(
            method='POST',
            path=reverse('orthanc-forward-call', kwargs={'server_name': NAME, 'route': route}),
            data=dicom_data,
            content_type='application/dicom'
        )

        self.assertEqual(response.status_code, expected_status)

    @parameterized.expand([
        ('instances/', status.HTTP_200_OK),
        ('bad_route/', status.HTTP_404_NOT_FOUND),
    ])
    def test_forward_delete_call(self, route, expected_status):
        self.setup_server_and_user(with_authenticated_user=True, with_authorized_user=True, with_restricted_server=True)
        instance_id = self.given_dicom_instance_in_orthanc()

        response = self.client.delete(
            reverse('orthanc-forward-call', kwargs={'server_name': NAME, 'route': f'{route}/{instance_id}'}),
        )

        self.assertEqual(response.status_code, expected_status)

    @parameterized.expand([
        ('A_MODALITY', {'AET': 'AN_AET', 'Host': '127.0.0.1', 'Port': 2002}, status.HTTP_200_OK),
        ('A_MODALITY', {'BAD_FIELD': 'AN_AET', 'Host': '127.0.0.1', 'Port': 2002}, status.HTTP_400_BAD_REQUEST),
    ])
    def test_forward_put_call(self, modality, modality_data, expected_status):
        """Put /modalities/{modality_name} is used as test"""
        self.setup_server_and_user(with_authenticated_user=True, with_authorized_user=True, with_restricted_server=True)

        response = self.client.put(
            reverse('orthanc-forward-call', kwargs={
                'server_name': NAME,
                'route': f'modalities/{modality}'
            }),
            data=json.dumps(modality_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, expected_status)

    def given_dicom_instance_in_orthanc(self) -> str:
        """Returns the DICOM objects ID in Orthanc"""
        dicom_data = make_dicom_data()

        # The standard self.client.post force data serialization as json or a multipart message
        response = self.client.generic(
            method='POST',
            path=reverse('orthanc-forward-call', kwargs={'server_name': NAME, 'route': 'instances/'}),
            data=dicom_data,
            content_type='application/dicom'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Failed to upload DICOM file (required for the test).'
        )

        return json.loads(response.data)['ID']

    def setup_server_and_user(
            self,
            with_authenticated_user: bool,
            with_authorized_user: bool,
            with_restricted_server: bool):
        self.server = OrthancServer.objects.create(
            name=NAME,
            address=ADDRESS,
            has_credentials=True,
            username=USERNAME,
            password=PASSWORD,
        )
        self.server.save()

        if with_authenticated_user:
            self.client.force_authenticate(self.user)

        if with_authorized_user:
            self.server.authorized_users.add(self.user)

        self.server.is_restricted = with_restricted_server
        self.server.save()
