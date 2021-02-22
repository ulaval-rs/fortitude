from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import OrthancServer

NAME = 'NAME'
ADDRESS = 'http://localhost:8042'
USERNAME = 'orthanc'
PASSWORD = 'orthanc'


class TestForwardCall(APITestCase):

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

