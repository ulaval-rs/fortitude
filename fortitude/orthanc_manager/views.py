from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .errors import OrthancServerDoesNotExistError, UnAuthorizedError
from .services import forward_call_to_server, get_orthanc_servers_names


class OrthancServersAPIView(APIView):

    def get(self, _: Request, *__) -> Response:
        servers_names = get_orthanc_servers_names()

        return Response(servers_names, status.HTTP_200_OK)


class ForwardAPIView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request, server_name: str, route: str, *__) -> Response:
        return self._forward_call('GET', request, server_name, route)

    def post(self, request: Request, server_name: str, route: str, *__) -> Response:
        return self._forward_call('POST', request, server_name, route)

    def delete(self, request: Request, server_name: str, route: str, *__) -> Response:
        return self._forward_call('DELETE', request, server_name, route)

    def put(self, request: Request, server_name: str, route: str, *__) -> Response:
        return self._forward_call('PUT', request, server_name, route)

    def _forward_call(self, method: str, request: Request, server_name: str, route: str, *__) -> Response:
        try:
            server_response = forward_call_to_server(request.user, method, server_name, route, data=request.body)

        except OrthancServerDoesNotExistError:
            return Response(f'Server {server_name} does not exist.', status.HTTP_404_NOT_FOUND)

        except UnAuthorizedError:
            return Response(f'Unauthorized access to the DICOM server', status.HTTP_401_UNAUTHORIZED)

        return Response(server_response.content, server_response.status_code)
