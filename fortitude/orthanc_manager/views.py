from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .errors import OrthancInstanceDoesNotExistError
from .services import get_orthanc_instances_names, forward_get_call_to_instance


class OrthancInstancesAPIView(APIView):

    def get(self, _: Request, *__) -> Response:
        instances_names = get_orthanc_instances_names()

        return Response(instances_names, status.HTTP_200_OK)


class ForwardAPIView(APIView):

    def get(self, _: Request, instance_name: str, route: str, *__) -> Response:
        try:
            response = forward_get_call_to_instance(instance_name, route)

        except OrthancInstanceDoesNotExistError:
            return Response(f'Instance {instance_name} does not exist.', status.HTTP_404_NOT_FOUND)

        return Response(response.content, response.status_code)
