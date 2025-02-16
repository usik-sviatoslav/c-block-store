from pydantic import BaseModel as AnySchema

from api.schemas.user import UserReadSchema as ReadSchema
from apps.user.models import User

from .base import CRUDBase

__all__ = ["CRUDUser"]


class CRUDUser(CRUDBase[User, ReadSchema, AnySchema, AnySchema, AnySchema]):
    def __init__(self) -> None:
        super().__init__(User, ReadSchema)
