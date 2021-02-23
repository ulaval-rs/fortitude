from typing import List, Optional

import requests
from requests.auth import HTTPBasicAuth

from .errors import OrthancServerDoesNotExistError
from .models import OrthancServer


def forward_call_to_server(
        method: str,
        server_name: str,
        route: str,
        data: Optional[bytes] = None) -> requests.Response:
    if method not in ['GET', 'POST', 'DELETE']:
        raise ValueError(f'Method "{method}" not supported.')

    orthanc_server = _get_orthanc_server(server_name)

    url_to_be_called = f'{orthanc_server.address}/{route}'

    if orthanc_server.has_credentials:
        credentials = HTTPBasicAuth(orthanc_server.username, orthanc_server.password)

        return requests.request(method, url_to_be_called, auth=credentials, data=data)

    return requests.request(method, url_to_be_called, data=data)


def get_orthanc_servers_names() -> List[str]:
    orthanc_servers = OrthancServer.objects.all()
    servers_names = [o.name for o in orthanc_servers]

    return servers_names


def _get_orthanc_server(name: str) -> OrthancServer:
    if OrthancServer.objects.filter(name=name).exists():
        return OrthancServer.objects.get(name=name)

    raise OrthancServerDoesNotExistError()
