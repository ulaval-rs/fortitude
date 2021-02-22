import logging
from typing import Callable

from django.http import HttpRequest, HttpResponse


class LoggingMiddleware:

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response: HttpResponse = self.get_response(request)

        # logger = logging.getLogger('django')
        # logger.info(f'{request.user} - {request.method} {request.path} {response.status_code}')

        return response
