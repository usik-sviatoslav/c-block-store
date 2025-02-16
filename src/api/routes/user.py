from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from api.crud.user import CRUDUser
from api.dependencies.auth import get_current_user
from api.schemas.user import UserReadSchema as ReadSchema
from apps.user.models import User

router = APIRouter()


@cbv(router)
class UserView(CRUDUser):
    def __init__(self, current_user: User = Depends(get_current_user)) -> None:
        super().__init__()
        self.user = current_user

    @router.get("/me")
    async def read_users_me(self) -> ReadSchema:
        return self.read_schema.model_validate(self.user)
