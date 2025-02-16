from typing import Any

from django.db.models import QuerySet

from apps.block.models import Block

from .base import CRUDBase

__all__ = ["crud"]


class CRUDBlock(CRUDBase[Block, Any, Any]):
    def get_queryset(self, **kwargs: Any) -> QuerySet[Block]:
        return super().get_queryset(**kwargs).select_related("currency", "provider")


crud = CRUDBlock(Block)
