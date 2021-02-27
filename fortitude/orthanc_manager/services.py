from typing import List, Optional

import requests
from requests.auth import HTTPBasicAuth

from fortitude.users.models import User
from .errors import OrthancServerDoesNotExistError, UnAuthorizedError
from .models import OrthancServer


def forward_call_to_server(
        user: User,
        method: str,
        server_name: str,
        route: str,
        data: Optional[bytes] = None) -> requests.Response:
    orthanc_server = _get_orthanc_server(server_name, user)

    url_to_be_called = f'{orthanc_server.address}/{route}'

    if orthanc_server.has_credentials:
        credentials = HTTPBasicAuth(orthanc_server.username, orthanc_server.password)

        return requests.request(method, url_to_be_called, auth=credentials, data=data)

    return requests.request(method, url_to_be_called, data=data)


def get_orthanc_servers_names() -> List[str]:
    orthanc_servers = OrthancServer.objects.all()
    servers_names = [o.name for o in orthanc_servers]

    return servers_names


def _get_orthanc_server(name: str, user: User) -> OrthancServer:
    if OrthancServer.objects.filter(name=name).exists():
        server = OrthancServer.objects.get(name=name)

        if not server.is_restricted:
            return server

        if _does_user_is_authorized_to_server(user, server):
            return server

        raise UnAuthorizedError()

    raise OrthancServerDoesNotExistError()


def _does_user_is_authorized_to_server(user: User, server: OrthancServer) -> bool:
    return user in server.authorized_users.all()
