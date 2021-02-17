from typing import List, Optional

from .models import OrthancInstance


def get_orthanc_instances_names() -> List[str]:
    orthanc_instances = OrthancInstance.objects.all()
    instances_names = [o.name for o in orthanc_instances]

    return instances_names


def get_orthanc_instance(name: str) -> Optional[OrthancInstance]:
    if OrthancInstance.objects.filter(name=name).exists():
        return OrthancInstance.objects.get(name=name)

    return None
