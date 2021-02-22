from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .errors import OrthancServerDoesNotExistError
from .services import get_orthanc_servers_names, forward_get_call_to_server


class OrthancServersAPIView(APIView):

    def get(self, _: Request, *__) -> Response:
        servers_names = get_orthanc_servers_names()

        return Response(servers_names, status.HTTP_200_OK)


class ForwardAPIView(APIView):

    def get(self, _: Request, server_name: str, route: str, *__) -> Response:
        try:
            response = forward_get_call_to_server(server_name, route)

        except OrthancServerDoesNotExistError:
            return Response(f'Server {server_name} does not exist.', status.HTTP_404_NOT_FOUND)

        return Response(response.content, response.status_code)
