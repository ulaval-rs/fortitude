import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import OrthancServer

NAME = 'NAME'
ADDRESS = 'ADDRESS'


class TestGetOrthancServersNames(APITestCase):

    def setUp(self) -> None:
        self.orthanc = OrthancServer.objects.create(name=NAME, address=ADDRESS)
        self.orthanc.save()

    def test_get_servers_names(self):
        response = self.client.get(
            reverse('orthanc-servers-names'),
            format='json'
        )

        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_content, ['NAME'])

