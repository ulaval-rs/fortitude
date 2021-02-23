from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .errors import OrthancServerDoesNotExistError
from .services import forward_call_to_server, get_orthanc_servers_names


class OrthancServersAPIView(APIView):

    def get(self, _: Request, *__) -> Response:
        servers_names = get_orthanc_servers_names()

        return Response(servers_names, status.HTTP_200_OK)


class ForwardAPIView(APIView):

    def get(self, _: Request, server_name: str, route: str, *__) -> Response:
        try:
            response = forward_call_to_server('GET', server_name, route)

        except OrthancServerDoesNotExistError:
            return Response(f'Server {server_name} does not exist.', status.HTTP_404_NOT_FOUND)

        return Response(response.content, response.status_code)

    def post(self, request: Request, server_name: str, route: str, *__) -> Response:
        try:
            response = forward_call_to_server('POST', server_name, route, data=request.body)

        except OrthancServerDoesNotExistError:
            return Response(f'Server {server_name} does not exist.', status.HTTP_404_NOT_FOUND)

        return Response(response.content, response.status_code)

    def delete(self, _: Request, server_name: str, route: str, *__) -> Response:
        try:
            response = forward_call_to_server('DELETE', server_name, route)

        except OrthancServerDoesNotExistError:
            return Response(f'Server {server_name} does not exist.', status.HTTP_404_NOT_FOUND)

        return Response(response.content, response.status_code)

    def put(self, request: Request, server_name: str, route: str, *__) -> Response:
        try:
            response = forward_call_to_server('PUT', server_name, route, data=request.body)

        except OrthancServerDoesNotExistError:
            return Response(f'Server {server_name} does not exist.', status.HTTP_404_NOT_FOUND)

        return Response(response.content, response.status_code)
