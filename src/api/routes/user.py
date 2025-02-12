from fastapi import APIRouter, Depends

from api.dependencies.auth import get_current_user
from api.schemas.user import UserRetrieve
from apps.user.models import User

router = APIRouter()


@router.get("/me", response_model=UserRetrieve)
async def read_users_me(current_user: User = Depends(get_current_user)) -> UserRetrieve:
    return UserRetrieve.model_validate(current_user)
