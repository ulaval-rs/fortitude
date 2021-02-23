import re
import string

from rest_framework import status
from rest_framework.exceptions import ValidationError


def validate_username(username: str) -> None:
    if len(username) < 3:
        raise ValidationError(
            detail='Username should have at least 3 characters.',
            code=status.HTTP_400_BAD_REQUEST
        )
    if not _contains_letters(username):
        raise ValidationError(
            detail='Username should contains letters.',
            code=status.HTTP_400_BAD_REQUEST
        )

    if _contains_special_characters(username):
        raise ValidationError(
            detail=f'Username should not contains a special character.',
            code=status.HTTP_400_BAD_REQUEST
        )


def _contains_letters(username: str) -> bool:
    if re.match(r'[a-zA-Z]', username):
        return True

    return False


def _contains_special_characters(username: str) -> bool:
    for char in username:
        if (char not in string.ascii_letters) and (char not in '0123456789'):
            return True

    return False
