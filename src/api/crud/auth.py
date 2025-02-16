from pydantic import BaseModel as AnySchema
from pydantic import EmailStr

from api.crud.base import CRUDBase
from api.schemas.auth import TokenPair
from api.utils.jwt import create_token_pair
from apps.user.models import User
from core.fastapi.exceptions import (
    InvalidCredentialsException,
    InvalidEmailOrPasswordException,
    ObjectAlreadyExistsException,
)

__all__ = ["CRUDAuth"]


class CRUDAuth(CRUDBase[User, AnySchema, AnySchema, AnySchema, AnySchema]):

    def __init__(self) -> None:
        super().__init__(User, AnySchema)

    async def obtain(
        self,
        *,
        email: EmailStr | str | None = None,
        username: str | None = None,
        password: str,
    ) -> TokenPair:
        """Validate a user by credentials and obtain a token pair."""
        user = await self.validate_user(email=email, username=username, password=password)
        return create_token_pair(data={"sub": str(user.id)})

    async def validate_user(
        self,
        *,
        email: EmailStr | str | None = None,
        username: str | None = None,
        password: str,
        raise_if_exists: bool = False,
    ) -> User:
        """Validate a user by credentials and return the Django model instances."""
        kwargs = {"email": email, "username": username}
        kwargs = {k: v for k, v in kwargs.items() if v is not None and v != ""}

        if not kwargs:
            raise ValueError("email or username must be provided")

        if (user := await self.get_first(**kwargs)) and raise_if_exists:
            raise ObjectAlreadyExistsException(self.model.__name__)

        if not user or not await user.acheck_password(password):
            raise InvalidEmailOrPasswordException() if email else InvalidCredentialsException()

        return user
