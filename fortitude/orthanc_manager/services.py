from typing import List, Optional

import requests
from requests.auth import HTTPBasicAuth

from .errors import OrthancInstanceDoesNotExistError
from .models import OrthancInstance


def forward_get_call_to_instance(instance_name: str, route: str) -> requests.Response:
    orthanc_instance = _get_orthanc_instance(instance_name)

    if orthanc_instance is None:
        raise OrthancInstanceDoesNotExistError()

    url_to_be_called = '/'.join([orthanc_instance.address, route])

    if orthanc_instance.has_credentials:
        credentials = HTTPBasicAuth(orthanc_instance.username, orthanc_instance.password)

        return requests.get(url_to_be_called, auth=credentials)

    return requests.get(url_to_be_called)


def get_orthanc_instances_names() -> List[str]:
    orthanc_instances = OrthancInstance.objects.all()
    instances_names = [o.name for o in orthanc_instances]

    return instances_names


def _get_orthanc_instance(name: str) -> Optional[OrthancInstance]:
    if OrthancInstance.objects.filter(name=name).exists():
        return OrthancInstance.objects.get(name=name)

    return None
