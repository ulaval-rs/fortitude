import requests
from requests.auth import HTTPBasicAuth
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ForwardAPIView(APIView):

    def get(self, request: Request, route: str, *_) -> Response:
        orthanc_address = 'http://localhost:8042'
        credentials = HTTPBasicAuth('orthanc', 'orthanc')

        url_to_be_called = '/'.join([orthanc_address, route])
        print(url_to_be_called)
        response = requests.get(url_to_be_called, auth=credentials)

        return Response(response.content, response.status_code)
