import json

from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status

from .util import make_bad_dicom_data, make_dicom_data
from ...models import OrthancServer

NAME = 'NAME'
ADDRESS = 'http://localhost:8042'
USERNAME = 'orthanc'
PASSWORD = 'orthanc'


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
        ('instances/', make_dicom_data(), status.HTTP_200_OK),
        ('instances/', make_bad_dicom_data(), status.HTTP_400_BAD_REQUEST),
        ('bad_route/', make_dicom_data(), status.HTTP_404_NOT_FOUND),
    ])
    def test_forward_post_call_with_binary_data(self, route, dicom_data, expected_status):
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
        response = self.client.put(
            reverse('orthanc-forward-call', kwargs={
                'server_name': NAME,
                'route': f'modalities/{modality}'
            }),
            data=modality_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, expected_status)

    def test_forward

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
