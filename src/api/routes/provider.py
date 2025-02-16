from fastapi import APIRouter, Depends

from api.crud.provider import crud
from api.dependencies.auth import get_current_user
from api.schemas.base import PaginationRequestQuery
from api.schemas.provider import ProviderRetrieve as ProviderSchema
from core.fastapi.exceptions import ProviderNotFoundException

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[ProviderSchema])
async def get_list(pagination: PaginationRequestQuery = Depends()) -> list[ProviderSchema]:
    if data := await crud.get_list(skip=pagination.skip or 0, limit=pagination.limit or 100):
        return [ProviderSchema.model_validate(block) for block in data]

    raise ProviderNotFoundException()
