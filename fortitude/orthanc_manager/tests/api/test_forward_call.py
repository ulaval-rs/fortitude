import json

from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status

from ...models import OrthancServer

NAME = 'NAME'
ADDRESS = 'http://localhost:8042'
USERNAME = 'orthanc'
PASSWORD = 'orthanc'

DICOM_FILE_PATH = './fortitude/orthanc_manager/tests/data/CT_small.dcm'


class TestForwardCall(TestCase):

    def setUp(self) -> None:
        self.orthanc = OrthancServer.objects.create(
            name=NAME,
            address=ADDRESS,
            has_credentials=True,
            username=USERNAME,
            password=PASSWORD
        )
        self.orthanc.save()

    @parameterized.expand([
        ('patients/', status.HTTP_200_OK),
        ('studies/', status.HTTP_200_OK),
        ('series/', status.HTTP_200_OK),
        ('instances/', status.HTTP_200_OK),
        ('modalities/', status.HTTP_200_OK),
        ('bad_route/', status.HTTP_404_NOT_FOUND),
    ])
    def test_forward_get_call(self, route, expected_status):
        response = self.client.get(
            reverse('orthanc-forward-call', kwargs={'server_name': NAME, 'route': route}),
            format='json'
        )

        self.assertEqual(response.status_code, expected_status)

    @parameterized.expand([
        ('instances/', status.HTTP_200_OK),
    ])
    def test_forward_post_call_with_binary_data(self, route, expected_status):
        dicom_data = self.given_dicom_data()

        # The standard self.client.post force data serialization as json or a multipart message
        response = self.client.generic(
            method='POST',
            path=reverse('orthanc-forward-call', kwargs={'server_name': NAME, 'route': route}),
            data=dicom_data,
            content_type='application/dicom'
        )

        self.assertEqual(response.status_code, expected_status)

    def given_dicom_data(self) -> bytes:
        with open(DICOM_FILE_PATH, 'rb') as file:
            return file.read()

    def upload_dicom_instance(self) -> str:
        """Returns the DICOM objects id path in Orthanc"""
        dicom_data = self.given_dicom_data()

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

        return json.loads(response.data)['Path'][1:]
