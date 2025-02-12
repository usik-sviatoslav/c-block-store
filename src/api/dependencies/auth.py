from fastapi import Depends

from api.utils.jwt import oauth2_scheme, verify_token
from apps.user.models import User
from core.fastapi.exceptions import InvalidTokenException

__all__ = [
    "get_current_user",
]


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Check if the token is valid and get user id
    user_id = verify_token(token, "access").get("sub")

    # Check if the user exists
    if user_id and (user := await User.objects.filter(id=user_id).afirst()):
        return user

    raise InvalidTokenException()
