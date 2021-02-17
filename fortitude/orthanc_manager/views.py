import requests
from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_orthanc_instances_names, get_orthanc_instance


class OrthancInstancesAPIView(APIView):

    def get(self, _: Request, *__) -> Response:
        instances_names = get_orthanc_instances_names()

        return Response(instances_names, status.HTTP_200_OK)


class ForwardAPIView(APIView):

    def get(self, _: Request, instance_name: str, route: str, *__) -> Response:
        orthanc_instance = get_orthanc_instance(instance_name)

        url_to_be_called = '/'.join([orthanc_instance.address, route])

        if orthanc_instance.has_credentials:
            credentials = HTTPBasicAuth(orthanc_instance.username, orthanc_instance.password)
            response = requests.get(url_to_be_called, auth=credentials)
        else:
            response = requests.get(url_to_be_called)

        return Response(response.content, response.status_code)
