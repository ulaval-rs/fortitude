from typing import List

from .models import OrthancInstance


def get_orthanc_instances_names() -> List[str]:
    orthanc_instances = OrthancInstance.objects.all()
    instances_names = [o.name for o in orthanc_instances]

    return instances_names


def get_orthanc_instance(name: str) -> OrthancInstance:
    return OrthancInstance.objects.get(name=name)
