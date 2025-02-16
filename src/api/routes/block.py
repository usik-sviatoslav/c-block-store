from uuid import UUID

from fastapi import APIRouter, Depends

from api.crud.block import crud
from api.dependencies.auth import get_current_user
from api.schemas.base import FilterByCurrencyProviderRequestQuery as FilterQuery
from api.schemas.base import PaginationRequestQuery as PaginationQuery
from api.schemas.block import Block as BlockSchema
from core.fastapi.exceptions import BlockNotFoundException

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[BlockSchema])
async def get_list(pagination: PaginationQuery = Depends(), filters: FilterQuery = Depends()) -> list[BlockSchema]:
    kwargs = {"currency__symbol": filters.currency, "provider__name": filters.provider}

    if data := await crud.get_list(skip=pagination.skip or 0, limit=pagination.limit or 100, **kwargs):
        return [BlockSchema.model_validate(block) for block in data]

    raise BlockNotFoundException()


@router.get("/{block_uuid}/", response_model=BlockSchema)
async def get(block_uuid: UUID) -> BlockSchema:
    if data := await crud.get(pk=block_uuid):
        return BlockSchema.model_validate(data)

    raise BlockNotFoundException()


@router.get("/currency/{currency_name}/number/{block_number}/", response_model=BlockSchema)
async def get_by_currency_and_block_number(currency_name: str, block_number: int) -> BlockSchema:
    if data := await crud.get_by_kwargs(currency__symbol=currency_name, block_number=block_number):
        return BlockSchema.model_validate(data)

    raise BlockNotFoundException()
