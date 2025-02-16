from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from api.crud.block import CRUDBlock
from api.dependencies.auth import get_current_user
from api.schemas.base import FilterByCurrencyProviderRequestQuery as FilterQuery
from api.schemas.base import PaginationRequestQuery as PaginationQuery
from api.schemas.block import BlockReadSchema as ReadSchema

router = APIRouter(dependencies=[Depends(get_current_user)])


@cbv(router)
class BlockView(CRUDBlock):
    @router.get("/")
    async def get_block_list(
        self, pagination: PaginationQuery = Depends(), filters: FilterQuery = Depends()
    ) -> list[ReadSchema]:
        kwargs = {"currency__symbol": filters.currency, "provider__name": filters.provider}
        return await self.list(skip=pagination.skip, limit=pagination.limit, **kwargs)

    @router.get("/{block_uuid}/")
    async def get_block(self, block_uuid: UUID) -> ReadSchema:
        return await self.get(pk=block_uuid)

    @router.get("/currency/{currency_name}/number/{block_number}/")
    async def get_block_by_currency_and_number(self, currency_name: str, block_number: int) -> ReadSchema:
        return await self.get(currency__symbol=currency_name, block_number=block_number)
