from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from api.crud.provider import CRUDProvider
from api.dependencies.auth import get_current_user
from api.schemas.base import PaginationRequestQuery
from api.schemas.provider import ProviderReadSchema as ReadSchema

router = APIRouter(dependencies=[Depends(get_current_user)])


@cbv(router)
class ProviderView(CRUDProvider):
    @router.get("/")
    async def get_provider_list(self, pagination: PaginationRequestQuery = Depends()) -> list[ReadSchema]:
        return await self.list(skip=pagination.skip, limit=pagination.limit)
