from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import UserRegistrationSerializer


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request: Request, *_) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)

        data = serializer.data
        data['token'] = token.key
        headers = self.get_success_headers(data)

        return Response(data, status.HTTP_201_CREATED, headers=headers)
