import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import OrthancInstance

NAME = 'NAME'
ADDRESS = 'ADDRESS'


class TestGetOrthancInstancesNames(APITestCase):

    def setUp(self) -> None:
        self.orthanc_instance = OrthancInstance.objects.create(name=NAME, address=ADDRESS)
        self.orthanc_instance.save()

    def test_get_instance_names(self):
        response = self.client.get(
            reverse('orthanc-instances-names'),
            format='json'
        )

        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content, ['NAME'])

