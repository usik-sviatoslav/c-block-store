from typing import Any

from api.crud.base import CRUDBase
from api.schemas.user import UserReadSchema as ReadSchema
from apps.user.models import User


class CRUDUser(CRUDBase[User, ReadSchema, Any, Any, Any]):
    def __init__(self) -> None:
        super().__init__(User, ReadSchema)
