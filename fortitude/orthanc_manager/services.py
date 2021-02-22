from typing import List, Optional

import requests
from requests.auth import HTTPBasicAuth

from .errors import OrthancServerDoesNotExistError
from .models import OrthancServer


def forward_get_call_to_server(server_name: str, route: str) -> requests.Response:
    orthanc_server = _get_orthanc_server(server_name)

    if orthanc_server is None:
        raise OrthancServerDoesNotExistError()

    url_to_be_called = f'{orthanc_server.address}/{route}'

    if orthanc_server.has_credentials:
        credentials = HTTPBasicAuth(orthanc_server.username, orthanc_server.password)

        return requests.get(url_to_be_called, auth=credentials)

    return requests.get(url_to_be_called)


def get_orthanc_servers_names() -> List[str]:
    orthanc_servers = OrthancServer.objects.all()
    servers_names = [o.name for o in orthanc_servers]

    return servers_names


def _get_orthanc_server(name: str) -> Optional[OrthancServer]:
    if OrthancServer.objects.filter(name=name).exists():
        return OrthancServer.objects.get(name=name)

    return None
