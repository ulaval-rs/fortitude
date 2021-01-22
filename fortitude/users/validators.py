import re

from rest_framework import status
from rest_framework.exceptions import ValidationError


def validate_username(value: str) -> None:
    if len(value) < 3:
        raise ValidationError(
            detail='Username should have at least 3 characters.',
            code=status.HTTP_400_BAD_REQUEST
        )
    if not _contains_letters(value):
        raise ValidationError(
            detail='Username should contains letters.',
            code=status.HTTP_400_BAD_REQUEST
        )


def _contains_letters(value: str) -> bool:
    if re.match(r'[a-zA-Z]', value):
        return True

    return False
