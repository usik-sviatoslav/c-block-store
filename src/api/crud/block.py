from django.db.models import QuerySet
from pydantic import BaseModel as AnySchema

from api.schemas.block import BlockReadSchema as ReadSchema
from apps.block.models import Block

from .base import CRUDBase

__all__ = ["CRUDBlock"]


class CRUDBlock(CRUDBase[Block, ReadSchema, AnySchema, AnySchema, AnySchema]):
    def __init__(self) -> None:
        super().__init__(Block, ReadSchema)

    def get_queryset(self) -> QuerySet[Block]:
        return super().get_queryset().select_related("currency", "provider")
